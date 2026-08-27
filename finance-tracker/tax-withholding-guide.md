# Tax withholding calculator — when the deposit lands

Clone of Quillenhart qaduu **quarterly tax set-aside** promise — *"Estimated quarterly tax set-aside, calculated from your actual profit"* — plus [faisalmq/4gao](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-4gao) buyer channel: **see how much of every payment to earmark for taxes the moment it hits**.

## The five-minute panic

You finish a project, send the invoice, watch the deposit land. For five minutes it feels great. Then:

- How much is actually yours?
- How much goes to taxes?
- Did you profit after subscriptions?

faisalmq/4gao calls this "mental accounting" — treating your business account like personal checking. Quillenhart's fix: log once on Transactions, tax set-aside calculates from real profit.

## Per-payment withholding (faisalmq/4gao shape)

Default reserve: **25% of net profit** (adjust in `setup-guide.md` via `TAX_SET_ASIDE_PCT`).

For each income deposit in your log:

| Deposit | Gross | Est. withhold (25%) | Not for spending |
|---------|-------|---------------------|------------------|
| Client A | $2,500 | $625 | Park in tax-only account |
| Client B | $1,200 | $300 | Same day as deposit |

Run:

```bash
python3 monthly_dashboard.py sample-transactions.csv
```

Read **TAX WITHHOLDING CALCULATOR** — per-payment earmark + quarterly rollup.

## Tax-only savings account

faisalmq/4gao users set up a separate account and transfer the withhold amount **when the payment lands**, not in April. Quillenhart's Dashboard tab shows quarterly set-aside from the same transaction log.

## Pair with

- [take-home-guide.md](take-home-guide.md) — marginmap reserve math
- [net-income-visibility-guide.md](net-income-visibility-guide.md) — faisalmq/5797 spendable-after-obligations
- [quarterly tax article](https://dev.to/toolkitlabs/quarterly-estimated-taxes-for-newly-self-employed-without-an-accountant-quillenhart-qaduu-clone-4nf) — olubunminelson/3n45 clone
