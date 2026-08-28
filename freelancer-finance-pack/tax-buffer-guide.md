# Tax buffer calculator — the day a client pays

Clone of [faisalmq/4gao](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-4gao) buyer channel + [saksham82's Freelancer Finance Pack ($9)](https://saksham82.gumroad.com/l/cueko).

## The five-minute panic

You finish a project, send the invoice, watch the deposit land. For five minutes it feels great. Then:

- How much is actually yours?
- How much goes to taxes?
- Did you profit after subscriptions?

faisalmq/4gao calls this "mental accounting" — treating your business account like personal checking. saksham82's fix: invoice tracker + expense log → net profit → per-payment buffer → safe-to-spend number.

## Per-payment withholding (faisalmq/4gao shape)

Default reserve: **25% of net profit** (adjust `TAX_BUFFER_PCT` in `freelancer_finance_pack.py`).

For each paid invoice in your log:

| Client | Collected | Est. buffer (25%) | Safe to spend |
|--------|-----------|-------------------|---------------|
| Acme Corp | $2,500 | $625 | $1,875 |
| Beta LLC | $4,000 | $1,000 | $3,000 |

Run:

```bash
python3 freelancer_finance_pack.py --tax-buffer invoices-sample.csv expenses-sample.csv
```

Read **EXPENSE + TAX BUFFER** — net profit, 25% earmark, safe-to-spend number.

## Tax-only savings account

faisalmq/4gao users set up a separate account and transfer the buffer amount **when the payment lands**, not in April. saksham82's US quarterly tax sheet rolls up the same numbers for 1040-ES deadlines.

## Pair with

- [self-assessment-guide.md](self-assessment-guide.md) — landolio/5hae monthly tax pot
- [merge-ledger-guide.md](merge-ledger-guide.md) — goldenalien/206o Gumroad/Stripe/PayPal merge
- [start-here.md](start-here.md) — full seven-sheet pack setup

Full bundle: [Freelancer Finance Pack landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelancer-finance-pack/) — invoice tracker + expense log + US/India tax + profit dashboard + ledger merge.
