# Net income visibility — what's actually safe to spend

Clone of [faisalmq/5797](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-5797) buyer channel + [heyismail's Finance OS Pro ($29+ · 15,254 sales)](https://heyismail.gumroad.com/l/TheUltimateFinanceTracker).

## The financial fog

You finish a project, send the invoice, watch the payment land. For a brief moment you feel flush.

Then the fog:

- How much of this is actually mine?
- Did I already owe quarterly taxes on the gross?
- Can I upgrade software or is that money already spoken for?

faisalmq/5797 frames the fix as **net income visibility** — see safe-to-spend after obligations, not gross deposits.

heyismail's **Finance OS Pro** rolls the same numbers into monthly and quarterly reporting views — budgets, subscriptions, net worth, and goals on top.

## Free CLI preview

```bash
python3 finance_os_tracker.py --net-income income-sample.csv expenses-sample.csv
```

Read the **NET INCOME VISIBILITY** block:

```plaintext
=== NET INCOME VISIBILITY (faisalmq/5797 shape) ===
  Gross collected:     $15,950.00
  Expenses (deductible): $1,410.00
    subscriptions/SaaS:  $160.00
  Net profit:            $14,540.00
  Tax set-aside (25%): $3,635.00
  Safe to spend:         $10,905.00
  Take-home rate:        68.4% of gross deposits
```

**Safe to spend** is your net-income visibility number — collected revenue minus expenses minus tax buffer. Not the gross deposit.

## Why gross deposits lie

| What your invoice says | What your bank shows | What you can spend |
|------------------------|----------------------|--------------------|
| Client paid $4,500 | Deposit $4,500 | Less after expenses, SaaS, tax reserve |

Spending from gross deposits is how solopreneurs overspend in Q3 and panic in April.

## Pair with

- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers
- [self-assessment-guide.md](self-assessment-guide.md) — landolio/5hae monthly tax pot
- [merge-ledger-guide.md](merge-ledger-guide.md) — goldenalien/206o unified payment ledger
- [start-here.md](start-here.md) — full Finance OS setup

Full bundle: [Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/finance-os-tracker/) — income + expense + budget + subscription + account + goal CSVs, ledger merge, tax buffer, and self-assessment module.
