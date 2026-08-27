# Read Me — Small Business Finance Tracker

Clone of Quillenhart qaduu **Read Me** tab + [datanestdigital/4l0h](https://dev.to/datanestdigital/freelance-financial-dashboard-4l0h) dashboard-setup-guide buyer channel.

## What this kit is

A complete finance system without monthly bookkeeping software. Log income and expenses once, pick any month, and see profit, bills, savings, debt, invoices, and tax set-aside — the same 9-tab promise Quillenhart ships on Gumroad ($15, **7 ratings**).

**Nothing left out. Nothing extra to buy.** One file replaces a bookkeeping app, budget planner, invoice tracker, and P&L report.

## 9 tabs (Quillenhart shape)

| Tab | Purpose |
|-----|---------|
| **Read Me** | This guide — plain English, no formulas required |
| **Setup** | Business name, tax year, tax set-aside % |
| **Transactions** | Master income & expense log (150+ rows) |
| **Bills** | Recurring bills with Jan–Dec payment grid |
| **Savings** | Goals with progress toward target |
| **Debt** | Running balance + minimum payments |
| **Invoices** | Accounts receivable — what clients owe you |
| **Dashboard** | Pick a month, see everything |
| **Annual Summary** | Whole year at a glance + income vs expenses chart |

Our clone uses CSV + `monthly_dashboard.py` instead of Excel tabs. Same workflow.

## Shaded cells = you type

In Quillenhart's spreadsheet, only shaded cells get typed into. In our kit:

- **You type:** rows in `transaction-log-template.csv`, fields in `setup-guide.md`
- **Script calculates:** net profit, YTD totals, quarterly set-aside, category breakdown, annual chart

## 5-minute setup (datanestdigital/4l0h quick start)

1. Extract the zip
2. Open `setup-guide.md` — enter business name, tax year, set-aside %
3. Copy `transaction-log-template.csv` → `my-transactions.csv`
4. Log this month's income and expenses (date, type, category, amount)
5. Run: `python3 monthly_dashboard.py my-transactions.csv`
6. Open `bills-tracker.md` and mark recurring bills for the month

## Usage tips (from datanestdigital/4l0h)

- Log expenses weekly — Friday afternoon works well
- Reconcile monthly — compare dashboard totals against bank statements
- Tag everything — consistent categories make tax time painless
- Use 25–30% set-aside until you know your actual rate (planning only, not filing advice)
- Back up monthly — save a copy of your CSV at month-end

## Who it's for

Freelancers, solopreneurs, and small business owners who want the complete financial picture without a subscription.

## Next steps

- [Start here](start-here.md) — condensed 5-minute walkthrough
- [Setup tab](setup-guide.md) — business name, tax year, set-aside %
- [Dashboard guide](dashboard-guide.md) — monthly P&L from real numbers
- [Free preview](free-preview.md) — sample CSV + CLI output
