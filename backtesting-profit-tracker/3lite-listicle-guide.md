# 3 SMC Lite indicators → back-testing workflow

Buyer-channel shape: [orion_operator/4218626](https://dev.to/orion_operator/3-smc-pine-script-indicators-every-tradingview-trader-needs-free-code-inside-2ncg) — three free Pine Script indicators + confluence rules → log every trade → prove win rate.

Clone of [aheadofthetrade ojdzA](https://aheadofthetrade.gumroad.com/l/ojdzA) ($1.99 · 35 ratings).

## 1. Install all three Lite indicators

Free Pine Script files in our [pine-smc folder](https://github.com/YtinuMoc/toolkitlabs-invoice/tree/main/pine-smc):

- [smc_fvg_lite.pine](https://github.com/YtinuMoc/toolkitlabs-invoice/blob/main/pine-smc/smc_fvg_lite.pine)
- [smc_liquidity_zones_lite.pine](https://github.com/YtinuMoc/toolkitlabs-invoice/blob/main/pine-smc/smc_liquidity_zones_lite.pine)
- [smc_order_blocks_lite.pine](https://github.com/YtinuMoc/toolkitlabs-invoice/blob/main/pine-smc/smc_order_blocks_lite.pine)

TradingView Pine Editor (Alt+P) → paste each file → Add to chart.

## 2. Use the 3-confluence rule

| Signal combo | Bias | Notes |
|---|---|---|
| SSL Swept + Bullish FVG in same zone | Long | High probability reversal |
| BSL Swept + Bearish OB above | Short | Smart money distributed above |
| Bullish OB inside Bullish FVG | Long | Institutional confluence zone |

Only log trades where at least two signals agree.

## 3. Log every back-test trade

When confluence fires, record it in `trades-template.csv`:

| Column | Example |
|--------|---------|
| `date` | 2026-06-02 |
| `strategy` | smc-confluence-bull |
| `symbol` | ES1! |
| `direction` | long |
| `entry_price` | 5420 |
| `exit_price` | 5448 |
| `position_size` | 1 |
| `risk_pct` | 1.0 |

## 4. Run the dashboard

```bash
python3 backtesting_profit_tracker.py my-smc-trades.csv --capital 10000
```

## 5. Decide before going live

Check win rate, profit factor, and max drawdown — the same metrics [aheadofthetrade's Excel tracker](https://aheadofthetrade.gumroad.com/l/ojdzA) plots automatically.
