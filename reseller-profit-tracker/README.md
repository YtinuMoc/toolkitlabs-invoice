# Reseller Profit Tracker 2025

Clone of [Hustlin Hooks Reseller Spreadsheet 2025](https://hustlinhooks.gumroad.com/l/hustlinhooks2025) ($50, **7 Gumroad ratings**, 4.3 stars).

CSV logs + Python CLI for multi-platform resellers (eBay, Poshmark, Amazon, Mercari).

## Quick start

1. Copy `*-template.csv` files and rename (drop `-template`).
2. Log sales in `sales-log.csv` — leave `net_profit` blank for auto-calc.
3. Track inventory in `inventory.csv` — aging days auto-computed from `acquired_date`.
4. Log expenses (supplies, mileage, rental) in `expenses.csv`.
5. Run:

```bash
python3 reseller_dashboard.py sales-log-sample.csv inventory-sample.csv expenses-sample.csv
```

## Modules (clone of Hustlin Hooks)

- **Sales log** — platform fees, shipping, COGS → net profit per order
- **Platform summary** — side-by-side eBay vs Poshmark vs Mercari vs Amazon
- **Monthly summary** — gross and net by month
- **Aging inventory** — master sheet with days listed; flags 90+ day stale stock
- **Worst order** — single order that lost the most money
- **Expense breakdown** — supplies, mileage, rental categories

## Checkout

EUR 9 one-time via Stripe — instant zip download.

Landing: https://ytinumoc.github.io/toolkitlabs-invoice/reseller-profit-tracker/
