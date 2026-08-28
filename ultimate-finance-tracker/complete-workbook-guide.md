# Complete finance workbook — CSV + CLI, no Notion (simonotion clone)

Clone of [simonotion Ultimate Finance Tracker ($47 · 109 ratings · 5.0★)](https://simonotion.gumroad.com/l/finance-tracker). Buyer-channel shape: [hemantdev/1iae](https://dev.to/hemantdev/i-built-a-freepaid-finance-gst-tracker-for-indian-freelancers-excel-no-notion-needed-1iae).

## Why a file, not Notion

Notion templates need an account, sync, and block syntax. [hemantdev/1iae](https://dev.to/hemantdev/i-built-a-freepaid-finance-gst-tracker-for-indian-freelancers-excel-no-notion-needed-1iae) sells a **single workbook** that opens offline in Excel or Google Sheets — shaded cells only, everything else calculates. Simo's Gumroad tracker ships the same offline shape: income, expenses, subscriptions, investments, debts, and savings goals in one connected system.

## Six connected views (hemantdev → simonotion)

| hemantdev sheet | simonotion module | Our clone |
|-----------------|-------------------|-----------|
| Dashboard | Monthly & quarterly reports | CLI stdout — income, expenses, net, net worth |
| Income | Income tracking | `income-template.csv` |
| Expenses | Expense tracking | `expenses-template.csv` |
| Subscriptions | Subscriptions manager | `subscriptions-template.csv` |
| Investments | Investment tracker | `investments-template.csv` |
| Debts | Debt & loan tracker | `debts-template.csv` |
| Savings goals | Savings goals | `savings-template.csv` |
| Accounts | Net worth | `accounts-template.csv` |

## Free CLI preview

```bash
python3 ultimate_finance_tracker.py --complete-workbook income-sample.csv expenses-sample.csv
```

Look for `COMPLETE WORKBOOK` in stdout — seven CSV templates, one CLI, zero Notion account.

## Who it's for

- Freelancers who want offline files, not SaaS dashboards
- Creators with irregular income juggling subscriptions and investments
- Anyone replacing a $20/mo Notion finance template with one owned file

## Pair with

- [beginner-guide.md](beginner-guide.md) — faisalmq/2fj6 no-formulas shape
- [guesswork-guide.md](guesswork-guide.md) — faisalmq/54h7 guesswork → clarity
- [start-here.md](start-here.md) — kit setup

Full kit: [Ultimate Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/ultimate-finance-tracker/) — EUR 9 one-time · same delivery shape as [simonotion on Gumroad ($47)](https://simonotion.gumroad.com/l/finance-tracker).
