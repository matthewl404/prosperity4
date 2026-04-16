# Round 1 — Manual Trading Notes

## Dryland Flax

**Setup:**
- Guaranteed exit price: 30 XIRECs (no fees)
- Order book (stale):

| Side | Price | Volume |
|------|-------|--------|
| Bid | 30 | 30k |
| Bid | 29 | 5k |
| Bid | 28 | 12k |
| Bid | 27 | 28k |
| Ask | 28 | 40k |
| Ask | 31 | 20k |
| Ask | 32 | 20k |
| Ask | 33 | 30k |

**Analysis:**
- Best ask is 28, guaranteed sell at 30 → +2/unit
- Asks at 31+ lose money (above guaranteed price)
- No fees, so full spread captured

**Order placed:**
- Buy | Price: 30 | Volume: 40,000
- Expected profit: **+80,000 XIRECs**

---

## Ember Mushroom

**Setup:**
- Guaranteed exit price: 20 XIRECs
- Fees: 0.05 buy + 0.05 sell = 0.10/unit
- Net value: **19.90/unit**

**Order book (stale):**

| Side | Price | Volume | Profit/unit | Total |
|------|-------|--------|-------------|-------|
| Ask | 12 | 20k | 7.90 | 158,000 |
| Ask | 13 | 25k | 6.90 | 172,500 |
| Ask | 14 | 35k | 5.90 | 206,500 |
| Ask | 15 | 6k | 4.90 | 29,400 |
| Ask | 16 | 5k | 3.90 | 19,500 |
| Ask | 18 | 10k | 1.90 | 19,000 |
| Ask | 19 | 12k | 0.90 | 10,800 |

*Ask at 17 had 0 volume — skipped*

**Order placed:**
- Buy | Price: 19 | Volume: 113,000 (sweeps all profitable asks)
- Expected profit: **~615,200 XIRECs**

---

## What I'd change
> Fill in after results drop
