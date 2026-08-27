# Savings Goals Guide

Clone of [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os) + [stephane/5629](https://dev.to/stephane_guertin_98bb6736/how-to-save-1000-in-12-weeks-using-a-spreadsheet-a-system-that-actually-works-5629) buyer channel: weekly ladder → running total → flex when you miss a week.

## Why freelancers need named savings goals

Income and expense logs tell you what happened. Savings goals tell you **where the surplus is going** — emergency fund, equipment, tax buffer — before it disappears into lifestyle creep.

## The weekly ladder (12-week sprint)

$1,000 in 12 weeks without saving the same amount every week:

| Weeks | Target/week | Subtotal |
|-------|-------------|----------|
| 1–4 | $60 | $240 |
| 5–8 | $85 | $340 |
| 9–12 | $105 | $420 |

**Total: $1,000.** Low start builds momentum; the spreadsheet recalculates remaining weeks if you miss one.

## Multi-goal tracker

| Goal | Target | Saved | % complete |
|------|--------|-------|------------|
| Emergency fund | $10,000 | $3,200 | 32% |
| Equipment upgrade | $2,000 | $800 | 40% |
| Tax buffer | $5,000 | $1,250 | 25% |

Log transfers as positive amounts on the expense log with category `savings_transfer`.

## Free CLI workflow

```bash
python3 freelance_finance_os.py --savings-goals savings-sample.csv
```

Full OS with bills/debt + savings wired in:

```bash
python3 freelance_finance_os.py invoice-log-sample.csv expense-log-sample.csv subscriptions-sample.csv bills-sample.csv debt-sample.csv savings-sample.csv
```

Free files: [savings-sample.csv](savings-sample.csv)

Full four-tool bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) · EUR 9 one-time · same delivery shape as [By the Loop on Gumroad ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).
