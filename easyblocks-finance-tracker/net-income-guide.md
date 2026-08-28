# Net income visibility — what's actually safe to spend

Clone of [faisalmq/5797](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-5797) buyer channel + [EasyBlocks Notion Finance Tracker (11 ratings · 5★ · $39)](https://easyblocks.gumroad.com/l/notion-finance-tracker).

## The financial fog

You finish a freelance project, send the invoice, watch the payment land. For a brief moment you feel flush.

Then the fog:

- How much of this is actually mine?
- Did I already owe quarterly taxes on the gross?
- Can I upgrade software or is that money already spoken for?

faisalmq/5797 frames the fix as **net income visibility** — see safe-to-spend after obligations, not gross deposits.

EasyBlocks' **Notion Finance Tracker** rolls income, expenses, accounts, budgets, and goals into one workspace — the safe-spend number belongs in the same file.

## Free CLI preview

```bash
python3 easyblocks_finance_tracker.py --net-income income-sample.csv expenses-sample.csv
```

Read the **NET INCOME VISIBILITY** block — gross collected, deductible expenses, tax set-aside, and safe-to-spend.

## Why gross deposits lie

| What your invoice says | What your bank shows | What you can spend |
|------------------------|----------------------|--------------------|
| Client paid $4,500 | Deposit $4,500 | Less after expenses, SaaS, tax reserve |

Spending from gross deposits is how freelancers overspend in Q3 and panic in April.

## Pair with

- [merge-ledger-guide.md](merge-ledger-guide.md) — goldenalien/206o platform CSV merge (run403)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run401)
- [take-home-guide.md](take-home-guide.md) — marginmap/14ag buyer channel (run400)
- [start-here.md](start-here.md) — full income + expense setup

Full bundle: [Notion Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/easyblocks-finance-tracker/) — CSV templates, dashboard CLI, and all buyer-channel guides.
