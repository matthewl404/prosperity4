from datamodel import OrderDepth, TradingState, Order
from typing import Dict, List, Optional
import jsonpickle

# ==============================================================
# trader_v5.py
#
# Changes from v4, and why a quant would make each one:
#
# OSMIUM
#   1. Microprice fair value (volume-weighted by opposite side).
#      Top-of-book imbalance is the strongest 1-tick price predictor
#      in any LOB. Naive mid ignores it entirely.
#   2. Dynamic take edge: scales with realized vol. Taking at edge=1
#      in a high-vol regime is free alpha to informed flow.
#   3. Inventory shift applied to FAIR itself (not just quotes).
#      v4 would aggressively buy dips even at pos=+70 because the
#      take-threshold ignored inventory. v5 tightens both sides.
#   4. Profitability guards: never bid above eff_fair, never ask
#      below it. Prevents pathological quotes on skewed books.
#   5. Layer collision guards: L2 only posts if strictly wider than
#      L1, same for L3 vs L2.
#   6. Vol-adaptive quote sizing.
#
# PEPPER
#   7. Max-pay cap: don't cross at any ask > mid + PEPPER_MAX_PREMIUM.
#      Each unit of premium paid = 10 ticks of drift given back.
#   8. Two-tier passive bids (75% at top, 25% one tick lower) to
#      catch dips at better average price.
# ==============================================================

LIMITS = {
    "INTARIAN_PEPPER_ROOT": 80,
    "ASH_COATED_OSMIUM": 80,
}

POSITION_BUFFER = 2         # Osmium safe_limit = 78

# --- Osmium model ---
ANCHOR = 10000.0
EMA_ALPHA = 0.20            # slightly faster than v4's 0.15
ANCHOR_WEIGHT = 0.08        # stronger pull to known anchor
VOL_WINDOW = 40
MIN_EDGE = 1
VOL_EDGE_COEF = 0.5         # take_edge = max(MIN_EDGE, vol * coef)

# --- Pepper model ---
# Drift ~ +0.1/tick. Paying +5 = giving back 50 ticks of drift.
PEPPER_MAX_PREMIUM = 5


class Trader:

    # -------- helpers --------
    @staticmethod
    def _init_state():
        return {"osmium_ema": ANCHOR, "osmium_mids": []}

    @staticmethod
    def _microprice(depth: OrderDepth) -> Optional[float]:
        """Volume-weighted fair that corrects for book imbalance.

        Intuition: if bid size >> ask size, pressure is on the buy
        side, true price sits closer to ask. Formula weights each
        side's price by the OPPOSITE side's volume.
        """
        if not depth.buy_orders or not depth.sell_orders:
            return None
        bb = max(depth.buy_orders.keys())
        ba = min(depth.sell_orders.keys())
        bv = depth.buy_orders[bb]
        av = -depth.sell_orders[ba]
        if bv + av <= 0:
            return (bb + ba) / 2.0
        return (bv * ba + av * bb) / (bv + av)

    @staticmethod
    def _realized_vol(mids: List[float]) -> float:
        if len(mids) < 3:
            return 1.0
        diffs = [mids[i] - mids[i - 1] for i in range(1, len(mids))]
        m = sum(diffs) / len(diffs)
        var = sum((d - m) ** 2 for d in diffs) / len(diffs)
        return max(1.0, var ** 0.5)

    # -------- main --------
    def run(self, state: TradingState):
        result: Dict[str, List[Order]] = {}
        conversions = 0

        data = {}
        if state.traderData:
            try:
                data = jsonpickle.decode(state.traderData)
            except Exception:
                data = {}
        for k, v in self._init_state().items():
            data.setdefault(k, v)

        for product in state.order_depths:
            depth: OrderDepth = state.order_depths[product]
            pos = state.position.get(product, 0)
            limit = LIMITS.get(product, 80)

            bb = max(depth.buy_orders.keys()) if depth.buy_orders else None
            ba = min(depth.sell_orders.keys()) if depth.sell_orders else None
            if bb is None and ba is None:
                result[product] = []
                continue

            if bb is not None and ba is not None:
                mid = (bb + ba) / 2.0
            else:
                mid = bb if bb is not None else ba

            if product == "INTARIAN_PEPPER_ROOT":
                result[product] = self._trade_pepper(product, depth, pos, limit, bb, ba, mid)
            elif product == "ASH_COATED_OSMIUM":
                result[product] = self._trade_osmium(product, depth, pos, limit, bb, ba, mid, data)
            else:
                result[product] = []

        return result, conversions, jsonpickle.encode(data)

    # -------- pepper --------
    def _trade_pepper(self, product, depth, pos, limit, bb, ba, mid):
        """
        Deterministic upward drift. Get to +80, never sell.
        Key discipline: don't pay above mid + PEPPER_MAX_PREMIUM.
        """
        orders: List[Order] = []
        if mid is None:
            return orders
        max_pay = mid + PEPPER_MAX_PREMIUM

        # (1) Aggressive sweep, capped by max_pay
        if depth.sell_orders and pos < limit:
            for ask in sorted(depth.sell_orders.keys()):
                if pos >= limit:
                    break
                if ask > max_pay:
                    break
                vol = -depth.sell_orders[ask]
                qty = min(vol, limit - pos)
                if qty > 0:
                    orders.append(Order(product, ask, qty))
                    pos += qty

        # (2) Two-tier passive bids: front of queue + one tick deeper
        if pos < limit and bb is not None:
            remaining = limit - pos
            if ba is not None and (ba - bb) > 1:
                top_bid = bb + 1        # penny-jump
            else:
                top_bid = bb            # join best bid

            top_qty = min(remaining, max(1, (3 * remaining) // 4))
            orders.append(Order(product, top_bid, top_qty))

            rem = remaining - top_qty
            if rem > 0:
                orders.append(Order(product, top_bid - 1, rem))

        return orders

    # -------- osmium --------
    def _trade_osmium(self, product, depth, pos, limit, bb, ba, mid, data):
        """
        Market-make around a mean-reverting asset near 10000.
        eff_fair = fair shifted by inventory penalty.
        All decisions (take AND quote) use the same eff_fair for consistency.
        """
        orders: List[Order] = []
        safe_limit = limit - POSITION_BUFFER

        micro = self._microprice(depth)
        if micro is None:
            micro = mid

        # Fair value update: EMA of microprice, anchored
        data["osmium_ema"] = EMA_ALPHA * micro + (1 - EMA_ALPHA) * data["osmium_ema"]
        mids = data.get("osmium_mids", [])
        mids.append(micro)
        if len(mids) > VOL_WINDOW:
            mids = mids[-VOL_WINDOW:]
        data["osmium_mids"] = mids

        fair = (1 - ANCHOR_WEIGHT) * data["osmium_ema"] + ANCHOR_WEIGHT * ANCHOR

        # Dynamic edge = f(realized vol). Quiet regime = tight, noisy = wide.
        vol = self._realized_vol(mids)
        take_edge = max(MIN_EDGE, int(round(vol * VOL_EDGE_COEF)))

        # Inventory shift: linear up to ±40, steeper beyond.
        # At pos=+40 shift = 2.4, at pos=+70 shift = 7.8.
        abs_pos = abs(pos)
        sign = 1 if pos >= 0 else -1
        if abs_pos <= 40:
            inv_shift = pos * 0.06
        else:
            inv_shift = sign * (40 * 0.06 + (abs_pos - 40) * 0.18)
        eff_fair = fair - inv_shift

        # -------- (1) Aggressive taking, edge-filtered --------
        if depth.sell_orders:
            for ask in sorted(depth.sell_orders.keys()):
                if ask >= eff_fair - take_edge:
                    break
                if pos >= safe_limit:
                    break
                vol_avail = -depth.sell_orders[ask]
                qty = min(vol_avail, safe_limit - pos)
                if qty > 0:
                    orders.append(Order(product, ask, qty))
                    pos += qty

        if depth.buy_orders:
            for bid in sorted(depth.buy_orders.keys(), reverse=True):
                if bid <= eff_fair + take_edge:
                    break
                if pos <= -safe_limit:
                    break
                vol_avail = depth.buy_orders[bid]
                qty = min(vol_avail, safe_limit + pos)
                if qty > 0:
                    orders.append(Order(product, bid, -qty))
                    pos -= qty

        # -------- (2) Passive layered quoting --------
        if bb is None or ba is None:
            return orders

        spread = ba - bb

        # Layer 1: inside the spread when wide, else anchored to eff_fair
        if spread > 2:
            l1_bid = bb + 1
            l1_ask = ba - 1
        else:
            l1_bid = int(round(eff_fair - max(1, take_edge)))
            l1_ask = int(round(eff_fair + max(1, take_edge)))

        # Profitability guard: never bid above fair, never ask below it.
        if l1_bid >= eff_fair:
            l1_bid = int(eff_fair) - 1
        if l1_ask <= eff_fair:
            l1_ask = int(eff_fair) + 1
        if l1_bid >= l1_ask:
            l1_bid = l1_ask - 1

        max_buy = max(0, safe_limit - pos)
        max_sell = max(0, safe_limit + pos)

        # Sizing: shrink in high vol (adverse selection protection)
        if vol < 3:
            base_size = 30
        elif vol < 6:
            base_size = 22
        else:
            base_size = 15

        l1_buy = min(base_size, max_buy)
        l1_sell = min(base_size, max_sell)
        if l1_buy > 0:
            orders.append(Order(product, l1_bid, l1_buy))
        if l1_sell > 0:
            orders.append(Order(product, l1_ask, -l1_sell))

        # Layer 2: wider, catch swings (5 ticks from fair)
        l2_bid = int(round(eff_fair - 5))
        l2_ask = int(round(eff_fair + 5))
        l2_buy_want = min(20, max(0, max_buy - l1_buy))
        l2_sell_want = min(20, max(0, max_sell - l1_sell))
        l2_buy_posted = 0
        l2_sell_posted = 0
        if l2_buy_want > 0 and l2_bid < l1_bid:
            orders.append(Order(product, l2_bid, l2_buy_want))
            l2_buy_posted = l2_buy_want
        if l2_sell_want > 0 and l2_ask > l1_ask:
            orders.append(Order(product, l2_ask, -l2_sell_want))
            l2_sell_posted = l2_sell_want

        # Layer 3: deep stink bids for extreme mean-reversion swings
        l3_bid = int(round(eff_fair - 11))
        l3_ask = int(round(eff_fair + 11))
        l3_buy_want = min(15, max(0, max_buy - l1_buy - l2_buy_posted))
        l3_sell_want = min(15, max(0, max_sell - l1_sell - l2_sell_posted))
        ref_bid = l2_bid if l2_buy_posted > 0 else l1_bid
        ref_ask = l2_ask if l2_sell_posted > 0 else l1_ask
        if l3_buy_want > 0 and l3_bid < ref_bid:
            orders.append(Order(product, l3_bid, l3_buy_want))
        if l3_sell_want > 0 and l3_ask > ref_ask:
            orders.append(Order(product, l3_ask, -l3_sell_want))

        return orders
