# Net income visibility — what's actually safe to spend

Clone of [faisalmq/5797](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-5797) buyer channel + [Anna Hickman's Freelance Dashboard ($97 · 1,251 sales · 69 ratings)](https://cedabranding.gumroad.com/l/pro-dashboard).

## The financial fog

You finish a freelance project, send the invoice, watch the payment land. For a brief moment you feel flush.

Then the fog:

- How much of this is actually mine?
- Did I already owe quarterly taxes on the gross?
- Can I upgrade software or is that money already spoken for?

faisalmq/5797 frames the fix as **net income visibility** — see safe-to-spend after obligations, not gross deposits.

cedabranding's **Freelance Dashboard** rolls revenue, client mix, tax set-aside, and cash runway into one planning view — the safe-spend number belongs in the same workbook.

## Free CLI preview

```bash
python3 freelance_dashboard_tracker.py --net-income revenue-sample.csv expenses-sample.csv
```

Read the **NET INCOME VISIBILITY** block:

```plaintext
=== NET INCOME VISIBILITY (faisalmq/5797 shape) ===
  Gross collected:     $12,150.00
  Expenses (deductible): $380.49
    subscriptions/SaaS:  $160.00
  Net profit:            $11,769.51
  Tax set-aside (25%): $2,942.38
  Safe to spend:         $8,827.13
  Take-home rate:        72.7% of gross deposits
```

**Safe to spend** is your net-income visibility number — collected revenue minus expenses minus tax buffer. Not the gross deposit.

## Why gross deposits lie

| What your invoice says | What your bank shows | What you can spend |
|------------------------|----------------------|--------------------|
| Client paid $4,500 | Deposit $4,500 | Less after expenses, SaaS, tax reserve |

Spending from gross deposits is how freelancers overspend in Q3 and panic in April.

## Pair with

- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers
- [freelance-finance-tracker-guide.md](freelance-finance-tracker-guide.md) — faisalmq/5598 income vs expenses
- [daily-check-guide.md](daily-check-guide.md) — wilsonhoe/2kdc 5-minute daily protocol
- [spreadsheet-trap-guide.md](spreadsheet-trap-guide.md) — wilsonhoe/4khk planning layer
- [start-here.md](start-here.md) — full revenue + expense setup

Full bundle: [Freelance Dashboard landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-dashboard-tracker/) — revenue + expense CSVs, dashboard CLI, and all buyer-channel guides.
