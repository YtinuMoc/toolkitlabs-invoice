# Quarterly tax set-aside guide

Buyer-channel shape: [wilsonhoe/4lhd Tax Season Cash Crunch](https://dev.to/wilsonhoe/the-tax-season-cash-crunch-why-solopreneurs-lose-33-workdays-a-year-and-the-quarterly-system-that-4lhd).

## The problem

Xero's 2026 report: small business owners lose **33 workdays/year** to tax chaos — not paying tax, but reconstructing records and scrambling in April. At $75/hr effective rate, that's ~$19,800 in lost earning capacity.

Only **26%** of freelancers feel completely confident about their taxes (FreshBooks 2025).

## The fix (Rosidssoy clone shape)

[Rosidssoy's Finance Tracker](https://rosidssoy.gumroad.com/l/financetracker) ($5+ · 190 ratings) centralizes income, expenses, and goals in one Notion dashboard. Our clone ships the same modules as CSV + CLI — no Notion account required.

### Weekly (5 minutes)

1. Log new income and expenses to your CSV files.
2. Glance at category totals — catch subscription creep early.

### Quarterly (15 minutes)

```bash
python3 notion_finance_tracker.py --quarterly-tax income-sample.csv expenses-sample.csv
```

Transfer the per-quarter set-aside to a dedicated tax reserve account. When April arrives, the money is already there.

### What the CLI calculates

- Quarterly income vs expenses
- Estimated income tax (default 25%)
- Self-employment tax (~15.3%)
- Per-quarter reserve target

Adjust `DEFAULT_TAX_PCT` in the script for your bracket.

Not tax advice. Work with a CPA for your jurisdiction.
