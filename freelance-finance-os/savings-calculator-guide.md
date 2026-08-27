# Freelance savings goal calculator

Clone of [tatelyman/4kcj](https://dev.to/tatelyman/savings-goal-calculator-how-long-until-you-hit-your-target-4kcj) buyer channel + [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).

Goal amount + monthly savings + starting balance + APR → months until target, total contributed, interest earned, final balance.

Distinct from the [12-week sprint guide](savings-goals-guide.md) (stephane/5629): this answers **how long** at a fixed monthly rate, not weekly ladder pacing.

## Inputs

| Field | Meaning |
|-------|---------|
| `goal` | Named target (emergency fund, equipment, sabbatical) |
| `target` | Goal amount ($) |
| `initial_balance` | Already saved ($) |
| `monthly_contribution` | Planned monthly deposit from freelance surplus ($) |
| `annual_interest_rate` | APR on the balance (%, e.g. 4.5) |

## Freelancer use cases

| Goal | Why it matters |
|------|----------------|
| Emergency fund | 3–6 months of expenses after tax buffer is set aside |
| Equipment upgrade | Camera, laptop, software — plan the purchase date |
| Sabbatical fund | Voluntary income gap between contracts |
| Tax overpayment buffer | Extra set-aside beyond quarterly estimates |

Run the calculator **after** your tax buffer CLI shows safe-to-spend — savings come from surplus, not the tax pot.

## Free CLI

```bash
python3 freelance_finance_os.py --savings-calculator savings-calculator-sample.csv
```

Look for the `SAVINGS GOAL CALCULATOR (tatelyman/4kcj shape)` block in stdout.

## Paid kit

[Freelance Finance OS — EUR 9](https://buy.stripe.com/4gM3cw0qy8XWgbI2tD5Ne0E) — four tools in one bundle. Same architecture as [By the Loop on Gumroad ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).
