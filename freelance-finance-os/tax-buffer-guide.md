# Tax buffer calculator — the day a client pays

Clone of tool #2 in [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os). Buyer-channel shape: [faisalmq/4gao](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-4gao).

## The five-minute panic

You finish a project, send the invoice, watch the deposit land. For five minutes it feels great. Then:

- How much is actually yours?
- How much goes to taxes?
- Did you profit after subscriptions?

faisalmq/4gao calls this "mental accounting" — treating your business account like personal checking. By the Loop's fix: log income and expenses once, tax buffer calculates from real net profit.

## Per-payment withholding (faisalmq/4gao shape)

Default reserve: **25% of net profit** (adjust `TAX_BUFFER_PCT` in `freelance_finance_os.py`).

For each paid invoice in your log:

| Client | Collected | Est. buffer (25%) | Safe to spend |
|--------|-----------|-------------------|---------------|
| Acme Corp | $2,500 | $625 | $1,875 |
| Beta LLC | $1,200 | $300 | $900 |

Run:

```bash
python3 freelance_finance_os.py invoice-log-sample.csv expense-log-sample.csv
```

Read **EXPENSE + TAX BUFFER** — net profit, 25% earmark, safe-to-spend number.

## Tax-only savings account

faisalmq/4gao users set up a separate account and transfer the buffer amount **when the payment lands**, not in April. By the Loop's quarterly estimator tab rolls up the same numbers for 1040-ES deadlines.

## Pair with

- [invoice-panic-guide.md](invoice-panic-guide.md) — faisalmq/43dl invoice clarity
- [start-here.md](start-here.md) — four-tool bundle setup
- [rate-calculator.html](rate-calculator.html) — take-home target → hourly floor

Full bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) — invoice tracker + tax buffer + rate calculator + quarterly estimator.
