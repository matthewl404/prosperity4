# Round 2 — Manual Trading Notes

## Result

**Manual PnL: +163,492 XIRECs — Round Rank: 244th**

---

## Setup

Formula: `RESEARCH(X) * SCALE(Y) * HIT_RATE(RANK(Z)) - BUDGET = PNL`

Budget: 50,000 XIRECs

| Allocation | % Invested | Output |
| --- | --- | --- |
| Research | 21% | 133,953 XIRECs (logarithmic) |
| Scale | 54% | x3.8 multiplier (linear) |
| Speed | 25% | 0.42 hit rate (rank #2574) |

Total gross: 213,492 — Budget: 50,000 — **Net PnL: 163,492**

---

## Analysis

- Heavy allocation to Scale (54%) paid off — the x3.8 multiplier dominated the formula.
- Research at 21% gave diminishing returns (logarithmic curve); would allocate less here next time.
- Speed at 25% gave hit rate 0.42 at rank #2574 — marginal but contributed.
- Net rank 244 globally is a strong result.

## What I'd Change

- Reduce Research allocation (logarithmic returns plateau early), shift more to Scale.
- Speed allocation seems right around 20–25% given the hit rate curve.
