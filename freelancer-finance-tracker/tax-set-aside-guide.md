# Tax set-aside calculator — stop guessing what you owe

Clone of [faisalmq/4gao](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-4gao) buyer channel + [moonlight573's Freelancer Finance Tracker ($10)](https://moonlight573.gumroad.com/l/unsjlk).

## The deposit-day panic

You finish a project, send the invoice, watch the deposit land. For five minutes it feels great. Then:

- How much is actually yours?
- How much goes to taxes?
- Did you profit after subscriptions?

moonlight573's listing opens with **"Stop guessing what you owe the IRS."** faisalmq/4gao calls the alternative "mental accounting" — treating your business account like personal checking. The fix: per-payment buffer → tax-only savings account → paid tracker upsell.

## Per-payment tax set-aside (faisalmq/4gao shape)

Default reserve: **25% of net profit** (pass fourth argument to CLI or edit `DEFAULT_TAX_PCT`).

For each paid income row:

| Client | Collected | Est. set-aside (25%) | Safe to spend |
|--------|-----------|----------------------|---------------|
| Acme Corp | $2,500 | $625 | $1,875 |
| Beta LLC | $4,000 | $1,000 | $3,000 |

Run:

```bash
python3 freelancer_finance_tracker.py --tax-buffer income-sample.csv expenses-sample.csv invoices-sample.csv
```

Read **EXPENSE + TAX SET-ASIDE** — net profit, 25% earmark, safe-to-spend number.

## Tax-only savings account

faisalmq/4gao users set up a separate account and transfer the set-aside **when the payment lands**, not in April. moonlight573's Tax Set-Aside Calculator tab does the same math inside the spreadsheet — enter your rate once, every dollar shows what to move to savings.

## Pair with

- [finance-tracker-guide.md](finance-tracker-guide.md) — faisalmq/gc live dashboard buyer channel
- [start-here.md](start-here.md) — full tracker setup

Full bundle: [Freelancer Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelancer-finance-tracker/) — income + expense + invoice CSVs, live dashboard CLI, tax set-aside module.
