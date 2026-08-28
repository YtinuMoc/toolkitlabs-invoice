# Solopreneur revenue tracking without QuickBooks

Clone of [wilsonhoe/3d34](https://dev.to/wilsonhoe/how-solopreneurs-track-business-finances-without-quickbooks-and-why-72-are-leaving-money-on-the-3d34) buyer channel + [Amy Ragland's 2026 Solo Business Revenue & Expense Tracker ($10)](https://amyragland.gumroad.com/l/tckuq).

[wilsonhoe's post](https://dev.to/wilsonhoe/how-solopreneurs-track-business-finances-without-quickbooks-and-why-72-are-leaving-money-on-the-3d34) nails the solopreneur gap: you don't need QuickBooks at $200–$660/year. You need four things in one view:

1. Income tracking — what came in, from whom, when
2. Expense categorization — where the money went
3. Cash flow visibility — monthly snapshot, not quarterly panic
4. Tax preparation — organized records your accountant can use

[Amy Ragland on Gumroad](https://amyragland.gumroad.com/l/tckuq) sells a **$10 tracker** (1 verified 5-star rating) for freelancers, coaches, and consultants running a business of one:

- Revenue & expense worksheets
- Annual and monthly P&L at a glance
- Month, quarter, and YTD tracking
- Client revenue % — see concentration risk

Our shameless clone ships the same promise as CSV + Python CLI at EUR 9.

## Free CLI

```bash
python3 solo_business_revenue_tracker.py revenue-sample.csv expenses-sample.csv
```

Sample output:

```plaintext
=== SOLO BUSINESS REVENUE TRACKER (amyragland tckuq clone) ===
  Total revenue:       $12,150.00
  Total expenses:      $380.49
  Net profit:          $11,769.51
  Tax set-aside (25%): $2,942.38

--- Monthly P&L ---
  2026-01  revenue    $5,000.00  expense      $295.00  net    $4,705.00  margin  94.1%
  2026-02  revenue    $4,150.00  expense       $56.99  net    $4,093.01  margin  98.6%
  2026-03  revenue    $3,000.00  expense       $28.50  net    $2,971.50  margin  99.1%

--- Revenue by client (% of total) ---
  Acme Coaching              $6,400.00  ( 52.7%)
  Beta Consulting            $2,400.00  ( 19.8%)
  ...
```

Free files: [start here](start-here.md) · [revenue sample](revenue-sample.csv) · [expenses sample](expenses-sample.csv)

## Why solopreneurs pay $10 instead of winging it

wilsonhoe/3d34: poor financial tracking is the root cause of scope overload and inconsistent income pressure. If you can't answer "how much did I make last month, and where did it go?" without opening five apps, you make bad pricing decisions.

amyragland buyers want one honest P&L — monthly, quarterly, and by client — without learning spreadsheet formulas.

## Checkout

[Amy Ragland's complete workbook is $10 on Gumroad](https://amyragland.gumroad.com/l/tckuq) (1 rating · verified buyer).

Our clone: revenue + expense CSVs, P&L CLI, setup guide — **EUR 9 one-time** (instant zip after Stripe).
