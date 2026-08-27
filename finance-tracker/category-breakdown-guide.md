# Category breakdown — where your money went every month

Clone of Quillenhart qaduu **Dashboard + Annual Summary** promise — *"A category-by-category breakdown of where your money went, every month"* — plus [raxxostudios/5a8i](https://dev.to/raxxostudios/solo-studio-bookkeeping-in-90-minutes-a-month-my-stack-and-routine-5a8i) categorization shape: **12 categories is the sweet spot**.

## The 12 starter categories

| Category | What goes here |
|----------|----------------|
| `client_work` | Invoice payments (income — excluded from expense breakdown) |
| `product_sales` | Gumroad/Stripe product revenue |
| `software` | SaaS, hosting, domains |
| `marketing` | Ads, SEO tools, business cards |
| `contractor` | Outsourced work, VA |
| `platform_fee` | Gumroad/Stripe/PayPal fees |
| `home_office` | Coworking, utilities (business %) |
| `equipment` | Computer, monitor, peripherals |
| `education` | Courses, books, conferences |
| `travel` | Client trips, mileage |
| `meals` | Client meals (track separately for tax) |
| `fees` | Bank charges, wire fees |

Fewer than ~8 and your P&L is useless. More than ~15 and you spend 20 minutes deciding whether Notion is "software" or "office."

## Workflow

1. Log every row in [transaction-log-template.csv](transaction-log-template.csv) with a consistent `category` tag
2. Run: `python3 monthly_dashboard.py sample-transactions.csv`
3. Read **CATEGORY BREAKDOWN BY MONTH** — expenses per category, per month, with % of month total
4. At year-end, the YTD category rollup is what you hand to your tax advisor (raxxostudios/5a8i yearly handoff shape)

## Quillenhart promise

> Log everything once on the Transactions tab, and the rest handles itself — including switching between months with a single dropdown.

Our CLI mirrors month switching via `FINANCE_MONTH=2026-01 python3 monthly_dashboard.py ...` or the 8th argument.

## Pair with

- [transactions-log-guide.md](transactions-log-guide.md) — single source of truth
- [dashboard-guide.md](dashboard-guide.md) — pick-a-month net profit view
- [annual-chart-guide.md](annual-chart-guide.md) — 12-month income vs expenses chart
