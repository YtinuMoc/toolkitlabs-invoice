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

- [Savings goals tracker](savings-tracker.md)
- [Annual summary template](annual-summary.md)
- [Take-home estimator guide](take-home-guide.md)
- [1099-K reconciliation guide](1099k-guide.md)
- [1099k sample CSV](1099k-sample.csv)
- [Invoices receivable guide](invoices-guide.md)
- [Invoices sample CSV](invoices-sample.csv)
- [Bills calendar guide](bills-guide.md)
- [Debt minimums guide](debt-guide.md)
- [Bills sample CSV](bills-sample.csv)
- [Debt sample CSV](debt-sample.csv)
- [Savings goals guide](savings-goals-guide.md)
- [Savings sample CSV](savings-sample.csv)
- [Savings calculator guide](savings-calculator-guide.md)
- [Savings calculator sample CSV](savings-calculator-sample.csv)
- [Finance calculators hub guide](calculators-guide.md)
- [Calculators sample CSV](calculators-sample.csv)
- [Self-assessment tax tracker guide](self-assessment-guide.md)
- [Freelance monthly dashboard guide](dashboard-guide.md)
- [Spreadsheet system guide](spreadsheet-system-guide.md)
