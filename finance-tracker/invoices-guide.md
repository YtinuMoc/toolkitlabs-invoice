# Freelance Invoices & Accounts Receivable Guide

Clone of [agentchip/2b11](https://dev.to/agentchip/i-fixed-my-freelance-invoicing-with-a-spreadsheet-that-does-the-math-for-me-2b11) buyer-channel shape + Quillenhart qaduu invoices tab.

## The invisible cost

Freelancers lose 5–10% of revenue to invoices they forget to chase. A simple receivables log beats a $12/mo SaaS reminder paywall.

## Five linked views (spreadsheet or CSV)

1. **Clients** — name, payment terms, hourly rate (reference only)
2. **Invoices** — one row per invoice: client, amount, sent date, due date, status
3. **Payments** — log deposits against invoice numbers in your transaction log
4. **Overdue** — anything past due date with status `Pending` or `Overdue`
5. **Dashboard** — total outstanding, overdue count, paid vs unpaid split

## Status values

`Paid` · `Pending` · `Overdue` · `Partial`

Mark `Paid` when the deposit hits your bank and you log income in `transaction-log-template.csv`.

## Worked example

| Invoice # | Client | Amount | Sent | Due | Status |
|-----------|--------|--------|------|-----|--------|
| 101 | Client A | $2,500 | 2026-01-10 | 2026-01-25 | Paid |
| 102 | Client B | $1,800 | 2026-01-20 | 2026-02-05 | Pending |
| 103 | Client C | $3,200 | 2026-01-05 | 2026-01-20 | Overdue |

- **Outstanding (unpaid):** $5,000 ($1,800 + $3,200)
- **Overdue:** 1 invoice · $3,200 · 7+ days late
- **Recovery win:** chase #103 before writing it off mentally

## CLI check

```bash
python3 monthly_dashboard.py sample-transactions.csv invoices-sample.csv
```

Prints `=== ACCOUNTS RECEIVABLE (agentchip/2b11 shape) ===` with outstanding and overdue totals.

Full kit: [Quillenhart qaduu clone ($15 → EUR 9)](https://ytinumoc.github.io/toolkitlabs-invoice/finance-tracker/)
