from datamodel import OrderDepth, TradingState, Order
from typing import List
import jsonpickle


class Trader:
    """
    Round 2 trader v5 — robust across both observed market conditions.

    PROBLEM WITH V4:
    - Pepper: MAX_OVERPAY=8 with anchor-based expected failed when round anchor
      was 12998.5 (v4) instead of 13000 (v1). Entry delayed 1500 ticks.
    - Osmium: tight edge=3 + asymmetric quoting sold too cheap early when
      true market fair was 10008 but hardcoded fair=10000 dragged ask to 10003.

    V5 FIX (empirically tested on both v1 and v4 market data):
    - Pepper: threshold = best_bid + 14 (captures L1 asks; spread-invariant).
      Simulates 7,383 on v1 data and 7,340 on v4 data. Robust across rounds.
    - Osmium: exactly v1 parameters. 888 PnL proven reliable. No "improvements".
    """

    PEPPER = "INTARIAN_PEPPER_ROOT"
    OSMIUM = "ASH_COATED_OSMIUM"
    PEPPER_LIMIT = 80
    OSMIUM_LIMIT = 80

    # Pepper
    PEPPER_TARGET = 80
    PEPPER_DRIFT = 0.001
    PEPPER_CIRCUIT_BREAKER = 50
    PEPPER_MAX_ASK_OVER_BID = 14  # typical spread is 14-16, this catches L1 reliably

    # Osmium - v1 EXACT
    OSMIUM_FAIR = 10000
    OSMIUM_EDGE = 5
    OSMIUM_QUOTE_SIZE = 15
    OSMIUM_SKEW = 0.25
    OSMIUM_FAIR_TOLERANCE = 30

    def bid(self) -> int:
        return 2500

    def run(self, state: TradingState):
        result = {}
        td = {}
        if state.traderData:
            try:
                td = jsonpickle.decode(state.traderData)
                if not isinstance(td, dict):
                    td = {}
            except Exception:
                td = {}

        if self.PEPPER in state.order_depths:
            pos = state.position.get(self.PEPPER, 0)
            result[self.PEPPER] = self.trade_pepper(
                state.order_depths[self.PEPPER], pos, state.timestamp, td
            )

        if self.OSMIUM in state.order_depths:
            pos = state.position.get(self.OSMIUM, 0)
            result[self.OSMIUM] = self.trade_osmium(
                state.order_depths[self.OSMIUM], pos, td
            )

        return result, 0, jsonpickle.encode(td)

    def trade_pepper(self, order_depth, position, timestamp, td):
        orders = []
        if not order_depth.buy_orders or not order_depth.sell_orders:
            return orders

        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())
        mid = (best_bid + best_ask) / 2

        # Circuit breaker anchor
        last_ts = td.get("pepper_last_ts")
        if last_ts is None or timestamp < last_ts:
            td["pepper_anchor_price"] = mid
            td["pepper_anchor_ts"] = timestamp
        td["pepper_last_ts"] = timestamp

        ticks = timestamp - td["pepper_anchor_ts"]
        expected = td["pepper_anchor_price"] + self.PEPPER_DRIFT * ticks
        if mid - expected < -self.PEPPER_CIRCUIT_BREAKER:
            return orders

        to_buy = self.PEPPER_TARGET - position
        if to_buy <= 0:
            return orders

        # SPREAD-INVARIANT THRESHOLD: take any ask within bid+14 of current best_bid
        threshold = best_bid + self.PEPPER_MAX_ASK_OVER_BID

        for ask_price in sorted(order_depth.sell_orders.keys()):
            if to_buy <= 0:
                break
            if ask_price <= threshold:
                ask_vol = -order_depth.sell_orders[ask_price]
                take = min(to_buy, ask_vol)
                if take > 0:
                    orders.append(Order(self.PEPPER, int(ask_price), take))
                    to_buy -= take

        if to_buy > 0:
            orders.append(Order(self.PEPPER, int(best_bid) + 1, to_buy))

        return orders

    def trade_osmium(self, order_depth, position, td):
        """v1 EXACT."""
        orders = []
        if not order_depth.buy_orders or not order_depth.sell_orders:
            return orders

        best_bid = max(order_depth.buy_orders.keys())
        best_ask = min(order_depth.sell_orders.keys())
        mid = (best_bid + best_ask) / 2

        if abs(mid - self.OSMIUM_FAIR) <= self.OSMIUM_FAIR_TOLERANCE:
            fair = self.OSMIUM_FAIR
        else:
            fair = mid

        fair_adj = fair - position * self.OSMIUM_SKEW
        working_pos = position

        for ask_price in sorted(order_depth.sell_orders.keys()):
            if ask_price < fair_adj:
                ask_vol = -order_depth.sell_orders[ask_price]
                capacity = self.OSMIUM_LIMIT - working_pos
                take = min(ask_vol, capacity)
                if take > 0:
                    orders.append(Order(self.OSMIUM, int(ask_price), take))
                    working_pos += take

        for bid_price in sorted(order_depth.buy_orders.keys(), reverse=True):
            if bid_price > fair_adj:
                bid_vol = order_depth.buy_orders[bid_price]
                capacity = self.OSMIUM_LIMIT + working_pos
                take = min(bid_vol, capacity)
                if take > 0:
                    orders.append(Order(self.OSMIUM, int(bid_price), -take))
                    working_pos -= take

        quote_bid = int(round(fair_adj - self.OSMIUM_EDGE))
        quote_ask = int(round(fair_adj + self.OSMIUM_EDGE))

        if quote_bid >= best_ask:
            quote_bid = best_ask - 1
        if quote_ask <= best_bid:
            quote_ask = best_bid + 1

        buy_qty = min(self.OSMIUM_QUOTE_SIZE, self.OSMIUM_LIMIT - working_pos)
        sell_qty = min(self.OSMIUM_QUOTE_SIZE, self.OSMIUM_LIMIT + working_pos)

        if buy_qty > 0:
            orders.append(Order(self.OSMIUM, quote_bid, buy_qty))
        if sell_qty > 0:
            orders.append(Order(self.OSMIUM, quote_ask, -sell_qty))

        return orders