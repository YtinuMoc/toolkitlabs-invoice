# Beginner-friendly solo business finance — no spreadsheet formulas (amyragland clone)

Clone of [amyragland's 2026 Solo Business Revenue & Expense Tracker ($10)](https://amyragland.gumroad.com/l/tckuq). Buyer-channel shape: [faisalmq/2fj6](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-2fj6): end-of-month dread → clarity without an accounting degree → paid kit upsell.

## The faisalmq/2fj6 promise

[faisalmq/2fj6](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-2fj6) names three outcomes freelancers actually want:

1. **Track income and expenses in one place** — no hunting email for invoice history
2. **Visualize take-home pay** — net after business costs, not gross deposits
3. **Prepare for tax season** — organized data so filing isn't a month-long headache

amyragland's Gumroad kit adds monthly P&L, client revenue %, and expense categories behind the same rule: **you only type into the log cells**. Everything else calculates itself.

## Shaded cells in this kit

| You type (shaded) | Auto-calculated |
|-------------------|-----------------|
| `revenue-template.csv` rows | Monthly P&L per month |
| `expenses-template.csv` rows | Category totals, net profit |
| date, client, amount columns | Client revenue % |
| category, deductible flag | Tax set-aside estimate |
| | Quarterly rollups, YTD totals |

No `SUMIFS`. No pivot tables. Run the CLI after you log.

## Free preview

```bash
python3 solo_business_revenue_tracker.py --beginner revenue-sample.csv expenses-sample.csv
```

Look for `BEGINNER-FRIENDLY` in stdout:

```plaintext
=== BEGINNER-FRIENDLY (faisalmq/2fj6 — no formulas required) ===
  You only type into shaded cells. In this kit that's your CSV rows.
  Type here:     revenue + expense CSV columns (see templates)
  Auto-calculated: monthly P&L, client %, tax set-aside, margins
  Revenue log: 6 rows · Expense log: 8 rows (expandable — duplicate templates)
```

## Who it's for

- Solopreneurs who've never touched a spreadsheet formula
- Freelancers who want bookkeeping to get out of the way
- Anyone replacing "hope my bank balance looks healthy" with a five-minute weekly log

## Pair with

- [revenue-tracker-guide.md](revenue-tracker-guide.md) — wilsonhoe/3d34 solopreneur finance
- [portable-tracker-guide.md](portable-tracker-guide.md) — faisalmq/3gcp portable CSV
- [dashboard-setup-guide.md](dashboard-setup-guide.md) — datanestdigital/4l0h five-minute dashboard
- [start-here.md](start-here.md) — kit setup

Full kit: [Solo Business Revenue Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/solo-business-revenue-tracker/) — EUR 9 one-time · same delivery shape as [amyragland on Gumroad ($10)](https://amyragland.gumroad.com/l/tckuq).
