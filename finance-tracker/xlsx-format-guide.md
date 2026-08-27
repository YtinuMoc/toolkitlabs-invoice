# XLSX format — Excel & Google Sheets (Quillenhart qaduu clone)

Clone of Quillenhart Gumroad **Format: xlsx (works in Excel & Google Sheets)** + **Capacity: 150 transaction rows, expandable** + [guillermo_llopis/3h7l](https://dev.to/guillermo_llopis_8e2a58a6/best-free-invoice-tracking-templates-for-google-sheets-2026-3h7l) buyer channel: compare formats → pick portable spreadsheet → paid kit upsell ($15 Gumroad, 7 ratings).

## Why xlsx beats a SaaS subscription

Quillenhart ships one `.xlsx` file. You own it. No monthly fee, no vendor lock-in, no "export roulette" when you cancel.

[guillermo_llopis/3h7l](https://dev.to/guillermo_llopis_8e2a58a6/best-free-invoice-tracking-templates-for-google-sheets-2026-3h7l) compares spreadsheet templates on what actually matters. For a **finance tracker**, the same filters apply:

| Option | Offline | Excel | Google Sheets | Full P&L + tax | One-time cost |
|--------|:-------:|:-----:|:-------------:|:--------------:|:-------------:|
| QuickBooks / Xero | No | No | No | Yes | Monthly |
| Notion template | No | No | Partial | Maybe | Free–$10 |
| Blank Google Sheet | Yes* | Import | Yes | DIY formulas | Free |
| Quillenhart xlsx | Yes | Yes | Yes | Yes (9 tabs) | $15 once |
| This kit (CSV + CLI) | Yes | Import CSV | Import CSV | Yes | EUR 9 once |

\*Google Sheets needs sync for cloud access; the file still opens offline in the mobile app once cached.

## 150 rows, expandable

Quillenhart's Transactions tab ships **150 rows**. When you outgrow it:

1. Select the last data row in Excel/Sheets
2. Insert rows below (same column layout)
3. Formulas in Dashboard and Annual Summary pull from the expanded range

In this kit: duplicate rows in `transaction-log-template.csv` or append to your log file. The CLI reports `N/150 rows used`.

## Import this kit into Excel

1. Extract the zip
2. Open Excel → **Data → Get Data → From File → From Text/CSV**
3. Select `sample-transactions.csv` (or your log)
4. Load to a worksheet named `Transactions`
5. Run `monthly_dashboard.py` locally for P&L, or build SUMIFS in Excel mirroring the CLI output

## Import into Google Sheets

1. **File → Import → Upload** → select `sample-transactions.csv`
2. Import location: **Replace current sheet** or insert new sheet `Transactions`
3. Share view-only with your accountant (Quillenhart buyers do this at tax time)
4. Run the Python dashboard on the same CSV for tax set-aside and annual chart

## Free preview

```bash
python3 monthly_dashboard.py sample-transactions.csv
```

Look for `XLSX FORMAT` in stdout:

```
=== XLSX FORMAT (Quillenhart qaduu — Excel & Google Sheets) ===
  Native format: .xlsx (Quillenhart Gumroad) · this kit: CSV import → same 9-tab logic
  Compatibility: Microsoft Excel | Google Sheets | LibreOffice Calc
  Transaction capacity: 8/150 rows (expandable — insert rows or duplicate template)
```

## Paid kit

Full finance tracker: [landing](https://ytinumoc.github.io/toolkitlabs-invoice/finance-tracker/) · EUR 9 one-time · [Stripe checkout](https://buy.stripe.com/6oUeVe5KS6PO7Fc5FP5Ne0t?client_reference_id=xlsx-format-guide)
