# Net income visibility — what's actually yours

Clone of [faisalmq/5797](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-5797) buyer channel + [moonlight573's Freelancer Finance Tracker ($10)](https://moonlight573.gumroad.com/l/unsjlk).

## The financial fog

You finish a project, send the invoice, watch the payment land. For a brief moment you feel flush.

Then the realization hits: you aren't sure how much of that money is actually yours to spend.

Is that cash meant for your quarterly tax bill? Does it cover subscription renewals due next month? Or is it profit you can finally pull for personal use?

faisalmq/5797 frames the fix as four clarity layers:

1. **Separate personal and business** — one income + expense log
2. **Tax readiness** — set-aside calculated from net profit in real time
3. **Subscription management** — categorize recurring software in your expense log
4. **Net income visibility** — see safe-to-spend after obligations, not gross deposits

moonlight573's **live dashboard** does the math from the same logs. Our CLI mirrors it from CSV.

## Free CLI preview

```bash
python3 freelancer_finance_tracker.py --net-income income-sample.csv expenses-sample.csv
```

Read the **NET INCOME VISIBILITY** block:

```plaintext
=== NET INCOME VISIBILITY (faisalmq/5797 shape) ===
  Gross collected:     $11,400.00
  Expenses (deductible): $882.40
    subscriptions/SaaS:  $69.99
  Net profit:            $10,517.60
  Tax set-aside (25%): $2,629.40
  Safe to spend:         $7,908.20
  Take-home rate:        69.4% of gross deposits
```

**Safe to spend** is your net-income visibility number — collected revenue minus expenses minus tax buffer. Not the gross deposit.

## Why gross deposits lie

A $11,400 collected month with $882 in categorized expenses and a 25% tax buffer leaves **$7,908.20** actually spendable — not $11,400.

Without that number you overcommit to subscriptions, under-price projects, and scramble at quarterly deadlines.

## Pair with

- [tax-set-aside-guide.md](tax-set-aside-guide.md) — faisalmq/4gao deposit-day transfers
- [finance-tracker-guide.md](finance-tracker-guide.md) — faisalmq/gc live dashboard
- [start-here.md](start-here.md) — full tracker setup

Full bundle: [Freelancer Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelancer-finance-tracker/) — income + expense + invoice CSVs, live dashboard CLI, tax set-aside module.
