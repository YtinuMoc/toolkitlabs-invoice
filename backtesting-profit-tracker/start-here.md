# Start here — Back-testing Profit Tracker

Clone of [aheadofthetrade ojdzA](https://aheadofthetrade.gumroad.com/l/ojdzA) ($1.99 Gumroad · 35 ratings).

## 1. Run the free sample

```bash
python3 backtesting_profit_tracker.py trades-sample.csv
```

Shows win rate, profit factor, max drawdown, and equity curve — the same promise as the Excel tracker on Gumroad.

## 2. Log your back-test trades

Copy `trades-template.csv` and add one row per simulated trade:

| Column | Example |
|--------|---------|
| `date` | 2026-06-02 |
| `strategy` | breakout |
| `symbol` | BTCUSDT |
| `direction` | long or short |
| `entry_price` | 62000 |
| `exit_price` | 63450 |
| `position_size` | 0.5 |
| `risk_pct` | 1.0 |
| `pnl` | optional — auto-calculated from prices |

## 3. Custom starting capital

```bash
python3 backtesting_profit_tracker.py my-trades.csv --capital 25000
```

## 4. SMC FVG back-testing

See [smc-fvg-listicle-guide.md](smc-fvg-listicle-guide.md) — orion_operator/4219970 buyer channel shape.

## 5. Technical breakdown

See [technical-breakdown-guide.md](technical-breakdown-guide.md) — orion_operator/4219902 buyer channel shape.

## 6. Full zip

EUR 9 one-time checkout on the landing page — same delivery shape as the Gumroad original.
