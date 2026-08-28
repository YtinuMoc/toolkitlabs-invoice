# SMC FVG Lite → back-testing workflow

Buyer-channel shape: [orion_operator/4219970](https://dev.to/orion_operator/3-pine-script-smc-indicators-i-built-grab-the-fvg-lite-free-full-co-3k8h) — free Pine Script code → log every signal → prove win rate.

Clone of [aheadofthetrade ojdzA](https://aheadofthetrade.gumroad.com/l/ojdzA) ($1.99 · 35 ratings).

## 1. Copy FVG Lite into TradingView

Free Pine Script: [smc_fvg_lite.pine](https://github.com/YtinuMoc/toolkitlabs-invoice/blob/main/pine-smc/smc_fvg_lite.pine)

## 2. Log every back-test trade

When FVG Lite fires a signal, record it in `trades-template.csv`:

| Column | Example |
|--------|---------|
| `date` | 2026-06-02 |
| `strategy` | smc-fvg-bull |
| `symbol` | ES1! |
| `direction` | long |
| `entry_price` | 5420 |
| `exit_price` | 5448 |
| `position_size` | 1 |
| `risk_pct` | 1.0 |

## 3. Run the dashboard

```bash
python3 backtesting_profit_tracker.py my-fvg-trades.csv --capital 10000
```

## 4. Decide before going live

Check win rate, profit factor, and max drawdown — the same metrics [aheadofthetrade's Excel tracker](https://aheadofthetrade.gumroad.com/l/ojdzA) plots automatically.
