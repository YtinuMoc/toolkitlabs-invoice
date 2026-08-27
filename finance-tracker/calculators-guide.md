# Finance Calculators Hub Guide

Clone of [profiterole/1pnb](https://dev.to/profiterole/5-free-finance-calculators-every-developer-should-bookmark-1pnb) listicle buyer channel — five calculators developers bookmark: compound interest, FIRE, freelance rate, DCA, and savings goal.

## Calculators

| # | Calculator | What it answers |
|---|------------|-----------------|
| 1 | Compound interest | What does $X/month become in Y years at R%? |
| 2 | FIRE | When can you stop needing a salary (4% rule)? |
| 3 | Freelance rate | What hourly rate covers taxes, benefits, and admin time? |
| 4 | DCA | Total invested vs portfolio value with dollar-cost averaging |
| 5 | Savings goal | Months until a named target (see [savings calculator guide](savings-calculator-guide.md)) |

## Free CLI

```bash
python3 monthly_dashboard.py sample-transactions.csv "" "" "" "" calculators-sample.csv
```

Or pass calculators as the 7th argument:

```bash
python3 monthly_dashboard.py sample-transactions.csv invoices-sample.csv bills-sample.csv debt-sample.csv savings-sample.csv "" calculators-sample.csv
```

Free sample: [calculators-sample.csv](calculators-sample.csv)

Pairs with Quillenhart qaduu finance tracker tabs (bills, debt, invoices, savings, tax set-aside) in the full EUR 9 kit.
