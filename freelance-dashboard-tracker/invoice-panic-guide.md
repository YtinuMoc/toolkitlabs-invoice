# Invoice tracker without end-of-month panic

Clone of [faisalmq/43dl](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-43dl) buyer channel + [Anna Hickman's Freelance Dashboard ($97 · 1,251 sales · 69 ratings)](https://cedabranding.gumroad.com/l/pro-dashboard).

## The panic

You finish a freelance project, send the invoice, and see the deposit hit. For five minutes you feel successful. Then:

- Did that other client ever pay?
- Which invoices are overdue?
- How much is actually collected vs still outstanding?

Checking your bank balance is reactive. The Freelance Dashboard needs a **status log** — paid / unpaid / overdue — with per-client totals.

## Five-minute habit

1. Log every invoice when you send it (status = `unpaid`, due date set).
2. Mark `paid` when the deposit lands.
3. Run the dashboard weekly — overdue rows flag automatically.

```csv
invoice_id,client,amount,due_date,status
INV-2026-001,Gamma Studio,1900.00,2026-02-15,paid
INV-2026-002,Delta Inc,1200.00,2026-02-20,overdue
INV-2026-003,Acme Corp,1800.00,2026-03-15,unpaid
```

```bash
python3 freelance_dashboard_tracker.py --invoice-panic invoices-sample.csv
```

Read the **INVOICE TRACKER WITHOUT END-OF-MONTH PANIC** block:

```plaintext
=== INVOICE TRACKER WITHOUT END-OF-MONTH PANIC (faisalmq/43dl shape) ===
  Invoices logged:     4
  Collected (paid):    $1,900.00
  Awaiting payment:    $2,750.00
  Overdue (late):      1 invoices · $1,200.00
```

## Why bank balance fails

"Money in the bank" is not "money owed to you." Without an invoice log you chase clients twice, miss overdue payments, and confuse collected revenue with outstanding AR.

## Pair with

- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers
- [freelance-finance-tracker-guide.md](freelance-finance-tracker-guide.md) — faisalmq/5598 income vs expenses
- [daily-check-guide.md](daily-check-guide.md) — wilsonhoe/2kdc 5-minute daily protocol
- [spreadsheet-trap-guide.md](spreadsheet-trap-guide.md) — wilsonhoe/4khk planning layer
- [start-here.md](start-here.md) — full revenue + expense setup

Full bundle: [Freelance Dashboard landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-dashboard-tracker/) — revenue + expense CSVs, dashboard CLI, and all buyer-channel guides.
