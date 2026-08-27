# Quarterly estimated taxes — newly self-employed, no accountant

Clone of tool #4 in [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os). Buyer-channel shape: [olubunminelson/3n45](https://dev.to/olubunminelson/how-to-calculate-quarterly-estimated-taxes-when-youre-newly-self-employed-without-an-accountant-3n45).

## You got your first 1099

Congratulations — and welcome to quarterly estimated taxes.

You do not need a $300/hour accountant in year one to stay out of trouble. You need:

1. One invoice + expense log
2. Net profit after expenses (not gross deposits)
3. A set-aside % you transfer before each 1040-ES deadline

By the Loop's **Quarterly Tax Estimator** tab prefills the four IRS due dates. Our CLI mirrors the same block from the same CSV logs.

## When payments are due

Estimated taxes are due four times a year — roughly **April 15, June 15, September 15, and January 15**. They are not evenly spaced calendar quarters.

| Quarter | Due date | Income period |
|---------|----------|---------------|
| Q1 | Apr 15 | Jan–Mar |
| Q2 | Jun 15 | Apr–May |
| Q3 | Sep 15 | Jun–Aug |
| Q4 | Jan 15 (next year) | Sep–Dec |

Miss a date and penalties apply even if you "catch up" at filing time.

## What you actually owe (simplified)

As a 1099 worker you owe:

1. **Income tax** — on net profit after expenses
2. **Self-employment tax** — roughly 15.3% on net profit

A practical first-year shortcut: **set aside 25–30% of net profit** each month. Adjust `ESTIMATED_TAX_PCT` in `freelance_finance_os.py` to match what your tax professional recommends.

## Free CLI preview

```bash
python3 freelance_finance_os.py invoice-log-sample.csv expense-log-sample.csv
```

Read **QUARTERLY TAX ESTIMATOR (1040-ES shape)**:

```
=== QUARTERLY TAX ESTIMATOR (1040-ES shape) ===
  Estimated annual tax (28% planning rate): $934.08
  Suggested per deadline: $233.52
    Q1 due Apr 15           (Jan–Mar income)
    Q2 due Jun 15           (Apr–May income)
    Q3 due Sep 15           (Jun–Aug income)
    Q4 due Jan 15 next year (Sep–Dec income)
```

## The habit that prevents April panic

1. **Log weekly** — invoice status + expense categories in one place
2. **Transfer set-aside on the 1st** — treat quarterly payments like a bill
3. **Use net profit** — if you collected $5k but spent $1.2k on tools, set-aside is on $3.8k net
4. **Pair with per-payment buffer** — [tax-buffer-guide.md](tax-buffer-guide.md) (faisalmq/4gao shape) for deposit-day transfers

## Pair with

- [invoice-panic-guide.md](invoice-panic-guide.md) — faisalmq/43dl invoice clarity
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao per-payment withhold
- [start-here.md](start-here.md) — four-tool bundle setup

Full bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) — invoice tracker + tax buffer + rate calculator + quarterly estimator.
