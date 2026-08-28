# AI-Powered Invoice Tracker

Shameless clone of [Productive Club's AI-Powered Invoice Tracker](https://productiveclub.gumroad.com/l/gnohas) ($19+ on Gumroad · creator 4.9★/134 reviews).

Connected workspace as CSV + Python CLI:

1. **Clients** — registry with payment terms
2. **Invoices** — ledger with due dates and status
3. **Payments** — every payment logged against an invoice
4. **Overdue flags** — computed from due dates vs today
5. **Follow-up cadence** — 1/3/7/14/30-day preview (you send, no SMTP)
6. **Dashboard** — outstanding, overdue, revenue overview

## Quick start

```bash
python3 productiveclub_invoice_tracker.py clients-sample.csv invoices-sample.csv payments-sample.csv
```

Copy `*-template.csv` files, fill with your data, re-run.

EUR 9 one-time via Stripe — instant zip after checkout.
