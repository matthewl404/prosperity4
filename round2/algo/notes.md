# Round 2 — Algo Trading Notes

## Result

**Algo PnL: +83,428 XIRECs — Round Rank: 2226th**

---

## What Changed from R1

**Pepper — spread-invariant threshold**

R1 used `mid + 5` as the buy cap. This broke when the round anchor shifted to 12998.5 instead of 13000 — entry was delayed ~1500 ticks while the algo waited for asks within 5 of a wrong mid.

Fix: `threshold = best_bid + 14`. Pepper spread is typically 14–16 ticks so this reliably captures the L1 ask regardless of mid. Backtested on both R1 and shifted-anchor data — robust in both.

Added circuit breaker: if `mid - expected_drift_price < -50`, halt buying.

**Osmium — reverted to v1 exact**

R1's microprice + dynamic edge + 3-layer quoting added complexity without adding edge. Reverted to simpler v1 params (fair=10000, edge=5, quote_size=15, skew=0.25).

---

## What Underperformed

Rank 2226 is worse than R1's 1349. Osmium revert was probably right but the Pepper threshold may still have been too conservative in some conditions.
