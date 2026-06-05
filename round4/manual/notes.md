# Round 4 — Manual Trading Notes

## Result

**Manual PnL: -60,781 XIRECs — Round Rank: 1213th**

---

## Setup

Options/derivatives trading on `AC` (Ash-Coated Osmium derivatives).

| Product | Side | Volume | P&L |
| --- | --- | --- | --- |
| AC (underlying) | BUY | 200 | +36,642 |
| AC_50_P (put, K=50) | BUY | 50 | +18,505 |
| AC_50_C (call, K=50) | BUY | 50 | +31,416 |
| AC_35_P (put, K=35) | BUY | 50 | +9,243 |
| AC_40_P (put, K=40) | BUY | 50 | +17,254 |
| AC_45_P (put, K=45) | BUY | 50 | +20,280 |
| AC_60_C (call, K=60) | BUY | 50 | -28,240 |
| AC_50_P_2 | BUY | 50 | -14,120 |
| AC_50_C_2 | BUY | 50 | -23,442 |
| AC_50_CO | BUY | 50 | **-69,354** |
| AC_40_BP (barrier put, K=40) | BUY | 50 | -30,000 |
| AC_45_KO (knock-out, K=45) | BUY | 500 | -28,966 |

---

## Analysis

The core directional bet (AC underlying + ATM puts + calls) was profitable. All standard options near the money worked.

The losses came entirely from exotic derivatives:
- `AC_50_CO` — likely a capped/corridor option. Lost -69k, the single largest loss.
- `AC_40_BP` — barrier put. Hit the barrier and expired worthless (-30k).
- `AC_45_KO` — knock-out option. Got knocked out (-29k).
- `AC_50_P_2`, `AC_50_C_2` — second-series contracts, likely different expiry or vol surface.

## What I'd Change

- Avoid exotic derivatives without fully understanding the payoff structure. The knock-out and corridor products wiped out all gains from the vanilla positions.
- Stick to vanilla puts/calls and the underlying. The simple directional trades all worked.
- Never size exotic positions at 500 volume (AC_45_KO) — that was 10x the standard lot.
