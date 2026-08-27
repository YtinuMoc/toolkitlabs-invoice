# Free preview — transaction log + one month P&L

## Sample transactions (copy into your CSV)

```csv
date,type,category,description,amount
2026-01-15,income,client_work,Invoice #101,2500.00
2026-01-18,expense,software,Adobe subscription,-54.99
2026-01-22,expense,marketing,Google Ads,-120.00
```

## Run the dashboard

```bash
python3 monthly_dashboard.py sample-transactions.csv
```

Expected output shape:

```
=== MONTHLY P&L ===
2026-01  income $2,500.00  expense $174.99  net $2,325.01
...
=== QUARTERLY TAX SET-ASIDE (25% of net) ===
```

Full kit adds bills/debt/invoices trackers + 150-row template. Clone of [Quillenhart qaduu ($15)](https://quillenhart.gumroad.com/l/qaduu).
