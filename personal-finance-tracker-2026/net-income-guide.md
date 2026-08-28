# Net income visibility — what's actually safe to spend

Clone of [faisalmq/5797](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-5797) buyer channel + [ohmygoshna's 2026 Personal Finance Tracker ($13)](https://ohmygoshna.gumroad.com/l/2026).

## The financial fog

You finish a side gig, watch the deposit land. For a brief moment you feel flush.

Then the fog:

- How much of this is actually mine?
- Did everyday expenses already eat the margin?
- Can I spend on goals or is that money spoken for?

faisalmq/5797 frames the fix as **net income visibility** — see safe-to-spend after obligations, not gross deposits.

ohmygoshna's **2026 Personal Finance Tracker** rolls income, expenses, debt snowball, savings goals, and net worth into one Google Sheets file — the safe-to-spend number belongs in the same workbook.

## Free CLI preview

```bash
python3 personal_finance_tracker_2026.py --net-income income-sample.csv expenses-sample.csv
```

Read the **NET INCOME VISIBILITY** block:

```plaintext
=== NET INCOME VISIBILITY (faisalmq/5797 shape) ===
  Gross collected:     $10,335.00
  Expenses (deductible): $3,202.84
  Net profit:            $7,132.16
  Tax set-aside (25%): $1,783.04
  Safe to spend:         $5,349.12
  Take-home rate:        51.8% of gross deposits
```

**Safe to spend** is your net-income visibility number — collected income minus expenses minus tax buffer. Not the gross deposit.

## Why gross deposits lie

| What your paycheck says | What your bank shows | What you can spend |
|-------------------------|----------------------|--------------------|
| Side gig paid $450 | Deposit $450 | Less after rent, SaaS, tax reserve |

Spending from gross deposits is how people overspend in Q3 and panic in April.

## Pair with

- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run288)
- [debt-snowball-guide.md](debt-snowball-guide.md) — aissam_baidi/37m7 buyer channel (run287)
- [start-here.md](start-here.md) — full income, expense, debt, savings setup

Full bundle: [2026 Personal Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/personal-finance-tracker-2026/) — income + expense + debt + savings + account CSVs, snowball CLI, tax buffer, and net-income module.
