# IMC Prosperity 4 — matthewl404

Round-by-round writeup of my experience in IMC Prosperity 4, an algorithmic + manual trading competition by IMC Trading.

---

## Results

| Round | Algo PnL | Algo Rank | Manual PnL | Manual Rank | Round Total | Overall Rank |
| --- | --- | --- | --- | --- | --- | --- |
| 1 | +96,469 | 1349 | +71,500 | **72** | 167,969 | 2139 |
| 2 | +83,428 | 2226 | +163,492 | **244** | 246,920 | 1517 |
| 3 | +3,079 | 2263 | +65,240 | 621 | 68,319 | 2502 |
| 4 | +7,388 | 1810 | -60,781 | 1213 | -53,393 | 2934 |
| 5 | +41,108 | **439** | -12,339 | 1889 | 28,769 | 2652 |

**Final XIREC: 43,696 — Final Position: 2652**

---

## Repo Structure

```
prosperity4/
├── README.md
├── round1/
│   ├── algo/
│   │   ├── trader_v5.py       # Submitted algorithm
│   │   └── notes.md
│   └── manual/
│       └── notes.md
├── round2/
│   ├── algo/
│   │   ├── trader_v5.py
│   │   └── notes.md
│   └── manual/
│       └── notes.md
├── round3/
│   ├── algo/
│   │   └── notes.md
│   └── manual/
│       └── notes.md
├── round4/
│   ├── algo/
│   │   └── notes.md
│   └── manual/
│       └── notes.md
└── round5/
    ├── algo/
    │   └── notes.md
    └── manual/
        └── notes.md
```

---

## Round 1 — First Intarian Goods

**Products:** `INTARIAN_PEPPER_ROOT` (drift +1/tick), `ASH_COATED_OSMIUM` (mean-reverts ~10,000)

**Algo:** Market making on Osmium with microprice fair value, EMA anchor, 3-layer passive quoting, dynamic spread based on realized vol, and inventory skew on `eff_fair`. Pepper: buy-and-hold to +80 with two-tier passive bids.

**Manual:** Sealed-bid auctions for `DRYLAND_FLAX` and `EMBER_MUSHROOM` with guaranteed buybacks.

See [round1/algo/notes.md](round1/algo/notes.md) and [round1/manual/notes.md](round1/manual/notes.md).

---

## Round 2 — Return to Intaria

**Products:** `INTARIAN_PEPPER_ROOT`, `ASH_COATED_OSMIUM`

**Algo:** v5 fix — switched Pepper threshold to `best_bid + 14` (spread-invariant, robust across anchor shifts). Osmium reverted to v1 exact params after v5 improvements backfired in R1.

**Manual:** Resource allocation problem — `RESEARCH(X) * SCALE(Y) * HIT_RATE(RANK(Z)) - BUDGET = PNL`. Invested 21% research, 54% scale, 25% speed. Hit rate 0.42 at rank #2574. PnL: +163,492.

See [round2/algo/notes.md](round2/algo/notes.md) and [round2/manual/notes.md](round2/manual/notes.md).

---

## Round 3

**Algo:** +3,079 (rank 2263) — algo nearly flat, market conditions not favorable.

**Manual:** Two-item sealed bid auction. Bid 751 → 320 accepted, bid 836 → 348 accepted. Buy 531,248, Sell 614,560. PnL: +65,240.

See [round3/algo/notes.md](round3/algo/notes.md) and [round3/manual/notes.md](round3/manual/notes.md).

---

## Round 4

**Algo:** +7,388 (rank 1810)

**Manual:** Options/derivatives trading on `AC` products. Mixed results — profitable on AC, AC_50_P, AC_50_C, AC_35_P, AC_40_P, AC_45_P. Heavy losses on AC_50_CO (-69k), AC_40_BP (-30k), AC_45_KO (-29k). PnL: -60,781.

See [round4/algo/notes.md](round4/algo/notes.md) and [round4/manual/notes.md](round4/manual/notes.md).

---

## Round 5

**Algo:** +41,108 (rank **439**) — best algo round.

**Manual:** Portfolio allocation with 1,000,000 budget across 6 goods. Only Lava cake (+53k) was profitable. Heavy fees across all positions. PnL: -12,339.

See [round5/algo/notes.md](round5/algo/notes.md) and [round5/manual/notes.md](round5/manual/notes.md).

---

## About

First time doing Prosperity. Team: **JSAMP**
