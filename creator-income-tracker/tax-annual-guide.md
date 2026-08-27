# Tax & Annual Summary (PattyBun rauxja tab 6 clone)

Clone of [PattyBun's Digital Product Creator Income Tracker](https://pattybun.gumroad.com/l/rauxja) ($14.99) — tab 6: quarterly net revenue, SE tax estimate, income tax reserve, suggested quarterly payment.

## Run the tax block

```bash
python3 creator_dashboard.py sample-revenue.csv
```

Look for `=== TAX & ANNUAL SUMMARY (PattyBun tab 6) ===` in stdout.

## What it prints

| Field | Default |
|-------|---------|
| Quarterly net revenue | Sum of net after platform fees per calendar quarter |
| SE tax estimate | 15.3% × 92.35% of quarterly net (US self-employment default) |
| Income tax reserve | 12% of quarterly net (adjust `INCOME_TAX_RESERVE_PCT` in CLI) |
| Suggested quarterly payment | SE tax + income reserve for that quarter |

PattyBun's Gumroad page uses US self-employment tax as the default. Edit `SE_TAX_RATE`, `SE_TAXABLE_RATIO`, and `INCOME_TAX_RESERVE_PCT` at the top of `creator_dashboard.py` for your jurisdiction.

## Habit (faisalmq/4gao buyer-channel shape)

When a sale lands on Gumroad, Etsy, or Payhip:

1. Log gross in `revenue-log-template.csv`
2. Run the CLI — fee math + tax block update together
3. Transfer the suggested quarterly payment slice to a tax-only account

One revenue log feeds dashboard, platform summary, product performance, launch tracker, and tax summary — same as PattyBun's six-tab Google Sheet.

## Not tax advice

Planning defaults only. Talk to a CPA before filing.
