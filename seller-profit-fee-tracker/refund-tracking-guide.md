# Refund tracking — margin impact (smadsby ejxcg shape)

[SimpleBizDash](https://smadsby.gumroad.com/l/ejxcg) logs refunds in the **Expense Log** alongside ads and software — because a $19 Gumroad refund you forgot still shrinks real profit.

Buyer-channel shape: [orion_operator/40gi](https://dev.to/orion_operator/the-solo-gumroad-sellers-guide-to-tracking-income-expenses-quarterly-taxes-with-a-google-sheet-40gi) — payout chaos → net after fees **and refunds** → quarterly set-aside from real numbers.

## Run it

```bash
python3 seller_profit_fee_tracker.py sales-sample.csv expense-sample.csv
```

Look for the `REFUND IMPACT` block:

- Refund count and total dollars
- Refunds as % of gross sales
- Profit margin with vs without refunds

## Log refunds in expenses

Use `expense-log-template.csv` with category `refunds`:

```csv
date,category,amount,vendor
2026-01-18,refunds,19.00,Gumroad buyer
2026-02-08,refunds,12.99,Etsy return
```

Negative sale rows in Gumroad CSV exports are easy to miss. Logging refunds explicitly keeps margin honest.

## Why gross revenue lies after refunds

A $500 Gumroad month with two forgotten refunds is not $500 profit. SimpleBizDash's rule: **log once, profit recalculates** — same promise as Orion's Transactions tab (sale, fee, refund on one ledger).

Pair with [profit margins](profit-margin-guide.md) and [monthly summary](monthly-summary-guide.md).
