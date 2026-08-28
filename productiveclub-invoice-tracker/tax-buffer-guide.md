# Tax buffer calculator — the day client payment lands

Clone of [faisalmq/4gao](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-4gao) buyer channel + [Productive Club AI-Powered Invoice Tracker ($19+ · creator 4.9★/134 reviews)](https://productiveclub.gumroad.com/l/gnohas).

## The five-minute panic

A client payment hits your bank. It feels great for five minutes. Then:

- How much of this invoice is actually yours to spend?
- How much goes to quarterly taxes?
- Did you already spend it on tools?

faisalmq/4gao calls this "mental accounting" — treating your business account like a slush fund. Productive Club's Invoice Tracker links clients → invoices → payments in one workspace — the tax buffer habit belongs in the same morning routine.

## Per-payment withholding (faisalmq/4gao shape)

Default reserve: **25% of payments received** (adjust fourth argument or `TAX_BUFFER_PCT` in `productiveclub_invoice_tracker.py`).

| Client | Received | Est. buffer (25%) | Safe to spend |
|--------|----------|-------------------|---------------|
| Acme Corp | $2,500.00 | $625.00 | $1,875.00 |

Run:

```bash
python3 productiveclub_invoice_tracker.py --tax-buffer payments-sample.csv invoices-sample.csv
```

Read **INVOICE PAYMENTS + TAX BUFFER** — total received, 25% earmark, safe-to-spend number.

## Tax-only savings account

faisalmq/4gao users set up a separate account and transfer the buffer amount **when the payment lands**, not in April. Productive Club pairs this habit with invoice + payment tracking in one dashboard.

## Pair with

- [payment-follow-up-guide.md](payment-follow-up-guide.md) — agentchip/11n6 follow-up cadence (run410)
- [start-here.md](start-here.md) — full invoice tracker setup
