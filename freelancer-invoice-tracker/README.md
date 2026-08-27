# Freelancer Invoice & Client Tracker

Shameless clone of [AgentChip's Freelancer Invoice & Client Tracker](https://qiliang.gumroad.com/l/ahefab) ($15 on Gumroad).

Five linked sheets as CSV + Python CLI:

1. **Clients** — registry with hourly rates and payment terms
2. **Invoices** — ledger with auto-total and status
3. **Payments** — every payment logged against an invoice
4. **Overdue flags** — computed from due dates vs today
5. **Dashboard** — outstanding, overdue, and per-client totals

## Quick start

```bash
python3 freelancer_invoice_tracker.py clients-sample.csv invoices-sample.csv payments-sample.csv
```

Copy `*-template.csv` files, fill with your data, re-run.

## Files

| File | Purpose |
|------|---------|
| `clients-template.csv` | Client registry |
| `invoices-template.csv` | Invoice ledger |
| `payments-template.csv` | Payment log |
| `freelancer_invoice_tracker.py` | CLI dashboard + overdue flags |

EUR 9 one-time via Stripe — instant zip after checkout.
