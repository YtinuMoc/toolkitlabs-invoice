# Tax buffer calculator — the day side income lands

Clone of [faisalmq/4gao](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-4gao) buyer channel + [ohmygoshna's 2026 Personal Finance Tracker ($13)](https://ohmygoshna.gumroad.com/l/2026).

## The five-minute panic

You finish a side gig, watch the deposit land in your personal account. It feels great for five minutes. Then:

- How much is actually yours?
- How much goes to quarterly taxes?
- Did everyday expenses eat the margin?

faisalmq/4gao calls this "mental accounting" — treating your checking account like a slush fund. ohmygoshna's 2026 tracker rolls income, expenses, debt snowball, and savings goals into one Google Sheets file — the tax buffer habit belongs in the same workbook.

## Per-payment withholding (faisalmq/4gao shape)

Default reserve: **25% of net cash flow** (adjust `DEFAULT_TAX_PCT` in `personal_finance_tracker_2026.py`).

| Source | Collected | Est. buffer (25%) | Safe to spend |
|--------|-----------|-------------------|---------------|
| Salary | $3,200 | $800 | $2,400 |
| Side gig | $450 | $113 | $337 |

Run:

```bash
python3 personal_finance_tracker_2026.py --tax-buffer income-sample.csv expenses-sample.csv
```

Read **EXPENSE + TAX BUFFER** — net cash flow, 25% earmark, safe-to-spend number.

## Tax-only savings account

faisalmq/4gao users set up a separate account and transfer the buffer amount **when the payment lands**, not in April. ohmygoshna's tracker pairs this habit with debt snowball and savings goals in one view.

## Pair with

- [debt-snowball-guide.md](debt-snowball-guide.md) — aissam_baidi/37m7 buyer channel (run287)
- [start-here.md](start-here.md) — full income, expense, debt, savings setup
- [dev.to debt snowball article](https://dev.to/toolkitlabs/free-debt-snowball-tracker-that-actually-gets-finished-2026-ohmygoshna-clone-2mk6) — ohmygoshna clone buyer channel
