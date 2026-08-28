# Start here — Trading Journal Tracker

Clone of [jordisquare tradingjournal](https://jordisquare.gumroad.com/l/tradingjournal) ($48 Gumroad · 6 sales · creator 4.9/35 reviews).

## 1. Run the free sample

```bash
python3 trading_journal_tracker.py trades-sample.csv
```

Shows win rate, profit factor, calendar daily P&L, monthly summary, and journal reflections — the same promise as the Google Sheets journal on Gumroad.

## 2. Log your trades

Copy `trades-template.csv` and add one row per trade:

| Column | Example |
|--------|---------|
| `date` | 2026-07-01 |
| `market` | EURUSD |
| `setup` | breakout |
| `direction` | long or short |
| `entry_price` | 1.0850 |
| `exit_price` | 1.0892 |
| `position_size` | 1.0 |
| `pnl` | optional — auto-calculated |
| `reflection` | optional journal note |

## 3. Custom starting capital

```bash
python3 trading_journal_tracker.py my-trades.csv --capital 25000
```

## 4. Data asymmetry

See [mesh-hub.md](mesh-hub.md) for the full guide index · [data-asymmetry-guide.md](data-asymmetry-guide.md) — gfil86/4502459 buyer channel shape.

## 5. Full zip

EUR 9 one-time checkout on the landing page — same delivery shape as the Gumroad original.
