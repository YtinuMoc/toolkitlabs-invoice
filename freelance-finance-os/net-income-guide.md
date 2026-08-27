# Net income visibility — what's actually yours after tax

Clone of the expense + tax buffer module in [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os). Buyer-channel shape: [faisalmq/5797](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-5797).

## The financial fog

You finish a project, send the invoice, watch the payment land. For a brief moment you feel flush.

Then the realization hits: you aren't sure how much of that money is actually yours to spend.

Is that cash meant for your quarterly tax bill? Does it cover subscription renewals due next month? Or is it profit you can finally pull for personal use?

faisalmq/5797 frames the fix as four clarity layers:

1. **Separate personal and business** — one invoice + expense log
2. **Tax readiness** — set-aside calculated from net profit in real time
3. **Subscription management** — categorize recurring software in your expense log
4. **Net income visibility** — see safe-to-spend after obligations, not gross deposits

By the Loop's **Expense + Tax Buffer** tab does the math from the same logs. Our CLI mirrors it from CSV.

## Free CLI preview

```bash
python3 freelance_finance_os.py invoice-log-sample.csv expense-log-sample.csv
```

Read the **EXPENSE + TAX BUFFER** block:

```plaintext
=== EXPENSE + TAX BUFFER ===
  Expenses YTD:        $313.99
    marketing    $120.00
    education    $89.00
    software     $69.99
    office       $35.00
  Net profit (paid):   $2,786.01
  Tax buffer (25%):   $696.50
  Safe to spend:       $2,089.51
```

**Safe to spend** is your net-income visibility number — collected revenue minus expenses minus tax buffer. Not the gross deposit.

## Why gross deposits lie

A $3,100 deposit month with $314 in categorized expenses and a 25% tax buffer leaves **$2,089.51** actually spendable — not $3,100.

Without that number you overcommit to subscriptions, under-price projects, and scramble at quarterly deadlines.

## Pair with

- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers
- [invoice-panic-guide.md](invoice-panic-guide.md) — faisalmq/43dl invoice clarity
- [quarterly-tax-guide.md](quarterly-tax-guide.md) — olubunminelson/3n45 quarterly math
- [start-here.md](start-here.md) — four-tool bundle setup

Full bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) — invoice tracker + expense/tax buffer + rate calculator + quarterly estimator.
