# Round 1 — Algo Trading Notes

## Products

| Product | Position Limit | Behavior |
| --- | --- | --- |
| `INTARIAN_PEPPER_ROOT` | 80 | Deterministic upward drift ~+1/tick |
| `ASH_COATED_OSMIUM` | 80 | Mean-reverts around 10,000 |

---

## Actual Results

**Total algo PnL: +96,469 XIRECs — Round Rank: 1349th**

---

## Submitted Algorithm: `trader_v5.py`

### INTARIAN_PEPPER_ROOT

Price drifts up deterministically. The only edge is getting to position +80 as fast and cheaply as possible.

**Strategy:**
- Aggressive sweep of all sell orders up to `mid + PEPPER_MAX_PREMIUM` (= 5). Paying more than 5 above mid means giving back too many future drift ticks.
- Two-tier passive bids: 75% of remaining capacity at top of book (penny-jump if spread > 1, else join), 25% one tick lower to catch dips.
- Never sell. Position target is max (+80) and held there.

**Key param:** `PEPPER_MAX_PREMIUM = 5`

---

### ASH_COATED_OSMIUM

Mean-reverting asset anchored near 10,000. Classic market-making setup with inventory skew.

**Fair Value**

Used **microprice** instead of naive mid:

```
microprice = (bid_vol * ask_price + ask_vol * bid_price) / (bid_vol + ask_vol)
```

This corrects for book imbalance — if bid volume >> ask volume, true price sits closer to the ask. Naive mid ignores this.

EMA of microprice, anchored to 10,000:

```
ema = 0.20 * microprice + 0.80 * ema_prev
fair = 0.92 * ema + 0.08 * 10000
```

**Inventory Skew**

Shift fair value down when long, up when short, to discourage building extreme positions:

```
if |pos| <= 40: shift = pos * 0.06
else:           shift = sign * (2.4 + (|pos| - 40) * 0.18)

eff_fair = fair - shift
```

At pos = +40: shift = 2.4. At pos = +70: shift = 7.8. This makes it less attractive to keep buying as position grows.

**Dynamic Edge**

```
take_edge = max(1, round(realized_vol * 0.5))
```

In low-vol regimes, take aggressively (tight edge). In high-vol, widen to avoid adverse selection.

**Aggressive Taking**

- Buy any ask below `eff_fair - take_edge`
- Sell any bid above `eff_fair + take_edge`
- Both capped at `safe_limit = 78` (leaves 2-unit buffer)

**Layered Passive Quoting**

3 layers per side, all relative to `eff_fair`:

| Layer | Bid | Ask | Max Size |
| --- | --- | --- | --- |
| L1 | inside spread or `eff_fair - edge` | inside spread or `eff_fair + edge` | 30 / 22 / 15 (by vol regime) |
| L2 | `eff_fair - 5` | `eff_fair + 5` | 20 |
| L3 | `eff_fair - 11` | `eff_fair + 11` | 15 |

Collision guards prevent L2 from posting at or inside L1, L3 from posting at or inside L2.

Profitability guards: L1 bid is capped below `eff_fair`, L1 ask is floored above it.

---

## What Worked

- Microprice gave a more stable fair value estimate than naive mid, especially during imbalanced book conditions.
- Inventory skew prevented runaway long positions — v4 would aggressively buy even at pos = +70 because the take threshold ignored inventory.
- Layer collision guards kept the book clean.

## What Underperformed

- **Rank 1349 on algo is weak.** The spread capture was real but left a lot of PnL on the table.
- The `take_edge` threshold was too conservative in practice. With `VOL_EDGE_COEF = 0.5`, the bot rarely took unless the price was clearly mispriced. More aggressive taking on high-confidence signals would have helped.
- L3 stink bids at `eff_fair - 11` rarely filled. The asset doesn't swing 11 ticks from fair often enough for those to contribute meaningfully. Tightening L3 to ~7–8 ticks might capture more fills.
- The EMA alpha (0.20) may have been too fast — fair value sometimes chased microprice into a momentum trap, causing the bot to quote unfavorably during short bursts.

## What I'd Change for Round 2

- Increase `VOL_EDGE_COEF` to be more aggressive on takes: `max(1, int(round(vol * 0.35)))` — tighter edge = more fills at favorable prices.
- Tighten L3 from 11 to 7 ticks to increase fill frequency.
- Slow EMA: `EMA_ALPHA = 0.12` to reduce fair value noise from short bursts.
- Add a momentum filter: if microprice moved >3 ticks in the same direction for 3 consecutive timestamps, widen quotes on that side by 1 tick.
