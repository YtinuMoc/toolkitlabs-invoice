# 5-minute daily money check

Clone of [wilsonhoe/4413368 2kdc](https://dev.to/wilsonhoe/the-5-minute-daily-money-check-why-solopreneurs-who-look-at-their-numbers-every-day-catch-problems-2kdc) buyer channel + [Anna Hickman's Freelance Dashboard ($97 · 1,251 sales · 69 ratings)](https://cedabranding.gumroad.com/l/pro-dashboard).

[wilsonhoe's daily money check post](https://dev.to/wilsonhoe/the-5-minute-daily-money-check-why-solopreneurs-who-look-at-their-numbers-every-day-catch-problems-2kdc) frames the problem: monthly P&L is a tax record, not a steering wheel. Solopreneurs who log numbers daily catch problems **3 weeks earlier** than monthly reviewers.

## The 4-level cadence (wilsonhoe/2kdc)

| How often | What you check | Time |
|-----------|---------------|------|
| **Daily** | Today's revenue, variable spend, one-line note | ~90 seconds |
| **Weekly** | 7-day rolling trend — flat, rising, or drifting? | ~5 minutes |
| **Monthly** | Structural ratios: COGS %, margin, owner-pay status | ~20 minutes |
| **Quarterly** | Pricing, hiring, dropping product lines | ~1 hour |

The daily layer is a **log**, not an analysis. Record what came in, what went out, and anything that felt off.

## Free CLI: daily-check mode

```bash
python3 freelance_dashboard_tracker.py --daily-check revenue-sample.csv expenses-sample.csv
```

## 90-second daily protocol

1. Log today's deposits and expenses (30 sec)
2. Glance at 7-day rolling net — up, flat, or down? (30 sec)
3. Flag one anomaly: late client, unusual charge, subscription creep (30 sec)

That's 30 minutes/week — and it replaces hours of month-end reconstruction.
