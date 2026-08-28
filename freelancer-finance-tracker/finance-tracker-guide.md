# Freelance finance tracker — stop guessing what you owe

Clone of [faisalmq/gc](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-gc) buyer channel + [moonlight573's Freelancer Finance Tracker ($10)](https://moonlight573.gumroad.com/l/unsjlk).

## The deposit-day anxiety

You land a client, finish the work, send the invoice. When the payment hits your bank account, relief lasts five minutes — then:

- How much of this money is actually yours?
- How much must you set aside for taxes?
- After subscriptions and coffee-shop visits, did you profit this month?

faisalmq/gc calls winging it with a mental tally a fast track to burnout. moonlight573's fix: a live dashboard — income, expenses, net profit, outstanding invoices, tax set-aside — updated the moment you log a row.

## What moonlight573's tracker includes

From the [Gumroad listing](https://moonlight573.gumroad.com/l/unsjlk):

- **Live dashboard** — total income, expenses, net profit, outstanding invoices, tax set-aside
- **Income tracker** — log payments by client and project; mark paid or unpaid
- **Expense tracker** — categorized spending with tax-deductible flags
- **Invoice tracker** — who owes you and when it's due
- **Tax set-aside calculator** — enter your rate once; every dollar earned shows what to move to savings
- **$10 live checkout** — instant download, Excel + Google Sheets

## Free CLI: live dashboard preview

```bash
python3 freelancer_finance_tracker.py income-sample.csv expenses-sample.csv invoices-sample.csv
```

Sample output:

```plaintext
=== FREELANCER FINANCE TRACKER (moonlight573 unsjlk clone) ===
  Total income:        $11,400.00
  Total expenses:      $882.40
  Deductible expenses: $882.40
  Net profit:          $10,517.60
  Outstanding invoices:$2,750.00
  Overdue invoices:    $1,200.00
  Tax set-aside (25%): $2,629.40
  Safe to spend:       $7,908.20
```

Free files: [start here](start-here.md) · [sample income](income-sample.csv) · [sample expenses](expenses-sample.csv) · [sample invoices](invoices-sample.csv)

## Why freelancers pay $10 instead of a bank app

Bank apps show what happened. This shows what it means — how much is really yours after taxes, who still owes you, and whether you're making money this month or just moving it around.

## Pair with

- [Freelancer Finance Pack mesh hub](https://dev.to/toolkitlabs/freelancer-finance-pack-complete-guide-index-5-saksham82-clones-1n9l) — saksham82 cueko clone (EXHAUSTED run267)
