# Savings Goal Calculator Guide

Clone of [TateLyman's savings goal calculator buyer channel](https://dev.to/tatelyman/savings-goal-calculator-how-long-until-you-hit-your-target-4kcj) — enter goal amount, monthly savings, starting balance, and interest rate; see months until you hit the target.

## Inputs

| Field | Meaning |
|-------|---------|
| `target` | Goal amount ($) |
| `initial_balance` | Already saved ($) |
| `monthly_contribution` | Planned monthly deposit ($) |
| `annual_interest_rate` | APR on the balance (%, e.g. 4.5) |

## Outputs

- **Time to goal** — months (and years) until balance ≥ target
- **Total contributed** — sum of monthly deposits
- **Interest earned** — final balance minus starting balance minus contributions
- **Final balance** — ending amount at goal date

## Free CLI

```bash
python3 monthly_dashboard.py sample-transactions.csv "" "" "" savings-calculator-sample.csv
```

The dashboard detects `monthly_contribution` in the CSV header and runs the calculator module.

Full stack (goals + calculator):

```bash
python3 monthly_dashboard.py sample-transactions.csv invoices-sample.csv bills-sample.csv debt-sample.csv savings-sample.csv savings-calculator-sample.csv
```

Free sample: [savings-calculator-sample.csv](savings-calculator-sample.csv)

Pairs with the [12-week sprint guide](savings-goals-guide.md) (stephane/5629) and Quillenhart savings tab in the full kit.
