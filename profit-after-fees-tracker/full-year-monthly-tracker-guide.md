# Full-year monthly tracker — 12 months of Etsy profit in one view (sundayscope clone)

Clone of [sundayscope Profit After Fees ($27 on Gumroad)](https://sundayscope.gumroad.com/l/jmqyil) **Full-Year Monthly Tracker** tab.

Buyer-channel shape: [orion/40gi](https://dev.to/orion_operator/the-solo-gumroad-sellers-guide-to-tracking-income-expenses-quarterly-taxes-with-a-google-sheet-40gi) — month-level gross, fees, expenses, and profit rolled up for quarterly tax planning.

## The problem

January looked strong on Etsy's shop stats. February ad spend spiked. Without a **month-by-month rollup**, you only see YTD gross — not which months actually cleared profit after fees and expenses.

Sunday Current's tab shows all 12 months: gross, Etsy fees, expenses, and take-home profit per calendar month.

## Free CLI preview

```bash
python3 profit_after_fees_tracker.py sales-sample.csv expense-sample.csv
```

Look for `=== FULL-YEAR MONTHLY TRACKER (sundayscope tab) ===`:

```plaintext
  2026-01  gross $  130.48  fees $  25.35  exp $ 85.49  profit $   19.64
  2026-02  gross $   82.49  fees $  18.44  exp $ 75.50  profit $  -11.44
```

February lost money after ads — January's win would hide that in a single YTD number.

## Pair with tax set-aside

Use monthly profit (not gross deposits) as the input for quarterly set-aside. See [tax set-aside guide](tax-set-aside-guide.md) (l_d/5284 shape — run238).

Full workbook: [EUR 9 checkout](https://buy.stripe.com/cNicN68X45LK8Jgd8h5Ne0H?client_reference_id=monthly-tracker-guide-run240).
