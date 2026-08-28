# Net income visibility — what's actually safe to spend from digital sales

Clone of [faisalmq/5797](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-5797) buyer channel + [alannotion Automated Sales OS ($15 · creator 5★/20 reviews)](https://alannotion.gumroad.com/l/automatedsalesos).

## The financial fog

A Gumroad sale notification hits. Stripe deposits land. For a brief moment you feel flush.

Then the fog:

- How much of this revenue is actually mine to spend?
- Did I already owe quarterly taxes on the gross?
- Can I run ads or is that money already spoken for?

faisalmq/5797 frames the fix as **net income visibility** — see safe-to-spend after obligations, not gross deposits.

Alan Graf's **Automated Sales OS** merges Gumroad + Stripe sales into daily, weekly, and monthly dashboards — the safe-spend number belongs in the same morning routine.

## Free CLI preview

```bash
python3 automated_sales_os.py --net-income gumroad-sample.csv stripe-sample.csv
```

Read the **NET INCOME VISIBILITY** block — gross collected, platform fees, tax set-aside, and safe-to-spend.

## Why gross deposits lie

| What Gumroad shows | What your bank shows | What you can spend |
|--------------------|----------------------|--------------------|
| Sale $29.00 | Deposit $26.10 | Less after fees + tax reserve |

Spending from gross deposits is how digital product sellers overspend in Q3 and panic in April.

## Pair with

- [sales-dashboard-guide.md](sales-dashboard-guide.md) — goldenalien/206o merge-ledger buyer channel (run405)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run406)
- [start-here.md](start-here.md) — full sales merge setup

Full bundle: [Automated Sales OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/alannotion-automated-sales-os/) — sales CSV merge, dashboard CLI, and all buyer-channel guides.
