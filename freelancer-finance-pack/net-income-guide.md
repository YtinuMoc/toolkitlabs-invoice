# Net income visibility — what's actually yours

Clone of [faisalmq/5797](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-5797) buyer channel + [saksham82's Freelancer Finance Pack ($9)](https://saksham82.gumroad.com/l/cueko).

## The financial fog

You finish a project, send the invoice, watch the payment land. For a brief moment you feel flush.

Then the realization hits: you aren't sure how much of that money is actually yours to spend.

Is that cash meant for your quarterly tax bill? Does it cover subscription renewals due next month? Or is it profit you can finally pull for personal use?

faisalmq/5797 frames the fix as four clarity layers:

1. **Separate personal and business** — one invoice + expense log
2. **Tax readiness** — set-aside calculated from net profit in real time
3. **Subscription management** — categorize recurring software in your expense log
4. **Net income visibility** — see safe-to-spend after obligations, not gross deposits

saksham82's **Profit dashboard** tab does the math from the same logs. Our CLI mirrors it from CSV.

## Free CLI preview

```bash
python3 freelancer_finance_pack.py --net-income invoices-sample.csv expenses-sample.csv
```

Read the **NET INCOME VISIBILITY** block:

```plaintext
=== NET INCOME VISIBILITY (faisalmq/5797 shape) ===
  Gross collected:     $6,500.00
  Expenses (deductible): $559.00
    subscriptions/SaaS:  $69.99
  Net profit:            $5,941.00
  Tax set-aside (25%): $1,485.25
  Safe to spend:         $4,455.75
  Take-home rate:        68.5% of gross deposits
```

**Safe to spend** is your net-income visibility number — collected revenue minus expenses minus tax buffer. Not the gross deposit.

## Why gross deposits lie

A $6,500 collected month with $559 in categorized expenses and a 25% tax buffer leaves **$4,455.75** actually spendable — not $6,500.

Without that number you overcommit to subscriptions, under-price projects, and scramble at quarterly deadlines.

## Pair with

- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers
- [self-assessment-guide.md](self-assessment-guide.md) — landolio/5hae monthly tax pot
- [merge-ledger-guide.md](merge-ledger-guide.md) — goldenalien/206o Gumroad/Stripe/PayPal merge
- [start-here.md](start-here.md) — full seven-sheet pack setup

Full bundle: [Freelancer Finance Pack landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelancer-finance-pack/) — invoice tracker + expense log + US/India tax + profit dashboard + ledger merge.
