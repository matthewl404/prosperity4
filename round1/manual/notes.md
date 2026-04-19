# Round 1 — Manual Trading Notes

## Dryland Flax

**Setup:**

* Guaranteed exit price: 30 XIRECs (no fees)
* Order book (stale):

| Side | Price | Volume |
| --- | --- | --- |
| Bid | 30 | 30k |
| Bid | 29 | 5k |
| Bid | 28 | 12k |
| Bid | 27 | 28k |
| Ask | 28 | 40k |
| Ask | 31 | 20k |
| Ask | 32 | 20k |
| Ask | 33 | 30k |

**Analysis:**

* Best ask is 28, guaranteed sell at 30 → +2/unit
* Asks at 31+ lose money (above guaranteed price)
* No fees, so full spread captured

**Order placed:**

* Buy | Price: 30 | Volume: 40,000
* Expected profit: **+80,000 XIRECs**

---

## Ember Mushroom

**Setup:**

* Guaranteed exit price: 20 XIRECs
* Fees: 0.05 buy + 0.05 sell = 0.10/unit
* Net value: **19.90/unit**

**Order book (stale):**

| Side | Price | Volume | Profit/unit | Total |
| --- | --- | --- | --- | --- |
| Ask | 12 | 20k | 7.90 | 158,000 |
| Ask | 13 | 25k | 6.90 | 172,500 |
| Ask | 14 | 35k | 5.90 | 206,500 |
| Ask | 15 | 6k | 4.90 | 29,400 |
| Ask | 16 | 5k | 3.90 | 19,500 |
| Ask | 18 | 10k | 1.90 | 19,000 |
| Ask | 19 | 12k | 0.90 | 10,800 |


**Order placed:**

* Buy | Price: 19 | Volume: 113,000 (sweeps all profitable asks)

---

## Actual Results

**Total manual PnL: +71,500 XIRECs — Round Rank: 72nd**

71,500. The stale order book did not reflect the actual auction state.
The sealed-bid format means everyone is competing for the same volume simultaneously — by the time the auction cleared, profitable ask levels were likely swept clean by other bidders before my orders filled at those prices.

Despite the gap from projection, **rank 72 globally** validates that the bid placement strategy was correct relative to the field. Most teams either bid too low (no fill) or too high (negative edge). Hitting top-100 manual on the first round with no prior Prosperity experience is a strong signal.

## What I'd Change

- **Don't anchor to stale order book depth.** Treat the displayed volumes as upper bounds, not guaranteed fill. In a sealed-bid auction with thousands of competing teams, real fill is a fraction of what's shown.
- **Model competition explicitly.** If 2,000 teams all see the same book and sweep the same asks, fill at the lowest-ask levels gets split. Expected fill per team ≈ displayed volume / estimated # of aggressive bidders.
- **Bid more aggressively on low-ask levels.** The deeper asks (12–15 for mushroom) have the highest profit/unit. Even partial fill at those prices beats full fill at 18–19. Consider sending larger volume at the best levels rather than sweeping the whole book.
- **Size based on edge, not total availability.** For mushroom, a 113k order sweeping all the way to ask=19 at 0.90/unit edge dilutes average PnL/unit. Better to go heavy on 12–15 and light (or skip) on 18–19.
