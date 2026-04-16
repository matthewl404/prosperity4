# IMC Prosperity 4 — matthewl404

Round-by-round writeup of my experience in IMC Prosperity 4, an algorithmic + manual trading competition by IMC Trading.

---

## Competition Overview

You play as a trader establishing an outpost on the planet Intara, earning profit across 5 rounds of algorithmic and manual trading. Goal for round 1: **200,000 XIRECs net profit** before the third trading day.

---

## Results

| Round | Algo PnL | Manual PnL | Total PnL | Rank |
|-------|----------|------------|-----------|------|
| 1 | TBD | TBD | TBD | TBD |
| 2 | TBD | TBD | TBD | TBD |
| 3 | TBD | TBD | TBD | TBD |
| 4 | TBD | TBD | TBD | TBD |
| 5 | TBD | TBD | TBD | TBD |

---

## Repo Structure

```
prosperity4/
├── README.md
├── round1/
│   ├── algo/
│   │   ├── trader_v3.py       # Submitted algorithm
│   │   └── notes.md           # Strategy breakdown
│   └── manual/
│       └── notes.md           # Manual trading decisions
├── round2/
│   └── ...
```

---

## Round 1 — First Intarian Goods

### Products
| Product | Position Limit |
|---------|---------------|
| `INTARIAN_PEPPER_ROOT` | 80 |
| `ASH_COATED_OSMIUM` | 80 |

### Algo Strategy
- **INTARIAN_PEPPER_ROOT** — price drifts +1 every ~10 ticks. Strategy: buy and hold at max position (80), never sell.
- **ASH_COATED_OSMIUM** — mean-reverts around ~10,000. Strategy: market making with penny-jump quoting, aggressive taking at fair value, and inventory skew to stay flat.

See [`round1/algo/notes.md`](round1/algo/notes.md) for full breakdown and code.

### Manual Trading — An Intarian Welcome
Two sealed-bid auctions for `DRYLAND_FLAX` and `EMBER_MUSHROOM`. Both have guaranteed buyback prices after the auction closes, so the edge is purely buying below the buyback price.

| Product | Buyback | Fee | Net Value | Order |
|---------|---------|-----|-----------|-------|
| `DRYLAND_FLAX` | 30 | 0 | 30.00 | Buy @ 30, vol 40,000 |
| `EMBER_MUSHROOM` | 20 | 0.10/unit | 19.90 | Buy @ 19, vol 113,000 |

Expected manual profit: **~695,000 XIRECs**

See [`round1/manual/notes.md`](round1/manual/notes.md) for order book analysis.

---

## Round 2
> Coming soon

---

## Round 3
> Coming soon

---

## Round 4
> Coming soon

---

## Round 5
> Coming soon

---

## About

First time doing Prosperity.
