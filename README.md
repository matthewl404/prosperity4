# IMC Prosperity 4 — Matthew's Writeup

A round-by-round log of my experience in the IMC Prosperity 4 algorithmic trading competition. Covers both the algorithmic and manual trading components.

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
│   │   └── trader.py         # Algorithm submitted for round 1
│   ├── manual/
│   │   └── notes.md          # Manual trading decisions + reasoning
│   └── writeup.md            # Round 1 reflection
├── round2/
│   └── ...
└── utils/
    └── helpers.py            # Shared utilities (e.g. order book parsing)
```

---

## Round 1

### Products
- **Rainforest Resin** — stable, close to fair value
- **Kelp** — momentum-driven
- **Squid Ink** — high volatility

### Algo Strategy
> TBD — fill in after submission

### Manual Trading

**Dryland Flax**
- Guaranteed sell price: 30 XIRECs, no fees
- Best ask in the book: 28 (40k volume)
- Strategy: Buy at price 30, volume 40,000 → guaranteed +2/unit = **+80k XIRECs**

**Ember Mushroom**
- Guaranteed sell price: 20 XIRECs, fees 0.05 buy + 0.05 sell = 0.10/unit
- Net value per unit: 19.90
- All asks from 12–19 are profitable
- Strategy: Buy at price 19, sweep ~113k units → expected **+615k XIRECs**

| Good | Side | Price | Volume |
|------|------|-------|--------|
| Dryland Flax | Buy | 30 | 40,000 |
| Ember Mushroom | Buy | 19 | 113,000 |

### Reflection
> TBD — what worked, what didn't, what I'd change

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

## Key Takeaways
> To be filled in after the competition ends

---

## About

First time doing Prosperity. Going in with a background in competitive programming and quant prep (Jane Street AMP, combinatorics, expected value). Main focus is building solid mean-reversion and market-making strategies on the algo side while staying sharp on the manual rounds.
