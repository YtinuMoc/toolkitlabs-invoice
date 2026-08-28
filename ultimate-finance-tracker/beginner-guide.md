# Beginner-friendly finance — no spreadsheet formulas (simonotion clone)

Clone of [simonotion Ultimate Finance Tracker ($47 · 109 ratings · 5.0★)](https://simonotion.gumroad.com/l/finance-tracker). Buyer-channel shape: [faisalmq/2fj6](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-2fj6): end-of-month dread → clarity without an accounting degree → paid kit upsell.

## The faisalmq/2fj6 promise

[faisalmq/2fj6](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-2fj6) names three outcomes freelancers actually want:

1. **Track income and expenses in one place** — no hunting email for invoice history
2. **Visualize take-home pay** — net after business costs, not gross deposits
3. **Prepare for tax season** — organized data so filing isn't a month-long headache

Simo's Gumroad tracker adds subscriptions, investments, debts, and savings goals behind the same rule: **you only type into the log cells**. Everything else calculates itself.

## Shaded cells in this kit

| You type (shaded) | Auto-calculated |
|-------------------|-----------------|
| `income-template.csv` rows | Monthly income totals |
| `expenses-template.csv` rows | Category totals, net profit |
| date, source, amount columns | Tax set-aside estimate |
| category, description | Savings rate, cash flow |
| | Full dashboard via CLI |

No `SUMIFS`. No pivot tables. Run the CLI after you log.

## Free preview

```bash
python3 ultimate_finance_tracker.py --beginner income-sample.csv expenses-sample.csv
```

Look for `BEGINNER-FRIENDLY` in stdout:

```plaintext
=== BEGINNER-FRIENDLY (faisalmq/2fj6 — no formulas required) ===
  You only type into shaded cells. In this kit that's your CSV rows.
  Type here:     income + expense CSV columns (see templates)
  Auto-calculated: monthly P&L, tax set-aside, net worth preview
  Income log: 8 rows · Expense log: 12 rows (expandable — duplicate templates)
```

## Who it's for

- Freelancers who've never touched a spreadsheet formula
- Creators who want bookkeeping to get out of the way
- Anyone replacing "hope my bank balance looks healthy" with a five-minute weekly log

## Pair with

- [guesswork-guide.md](guesswork-guide.md) — faisalmq/54h7 guesswork → clarity
- [start-here.md](start-here.md) — kit setup
- [faq.md](faq.md) — common questions

Full kit: [Ultimate Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/ultimate-finance-tracker/) — EUR 9 one-time · same delivery shape as [simonotion on Gumroad ($47)](https://simonotion.gumroad.com/l/finance-tracker).
