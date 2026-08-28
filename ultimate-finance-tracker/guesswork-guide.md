# Guesswork → clarity (faisalmq/54h7 shape)

Clone of [faisalmq/54h7 freelance finance tracker](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-54h7) buyer channel + [simonotion Ultimate Finance Tracker ($47 · 109 ratings)](https://simonotion.gumroad.com/l/finance-tracker).

## The problem

Deposit hits your bank. Feels great for five minutes. Then:

- How much is actually yours after tax?
- Are subscriptions eating more than you think?
- Which categories are out of control?

Mental math and scattered bank statements = flying blind.

## The fix — one file

[faisalmq/54h7](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-54h7) sells three outcomes:

1. Categorize income and expenses at a glance
2. Automate tax savings so quarterly bills don't surprise you
3. Monitor profit margins and subscription drag

Simo's [Ultimate Finance Tracker](https://simonotion.gumroad.com/l/finance-tracker) ($47 · 109 ratings · 5.0★) adds subscriptions, investments, debts, and goals in one Notion workspace.

## Free CLI

```bash
python3 ultimate_finance_tracker.py --guesswork income-sample.csv expenses-sample.csv subscriptions-sample.csv
```

Sample output:

```plaintext
=== GUESSWORK → CLARITY (faisalmq/54h7 shape) ===
  Gross income YTD:    $10,975.00
  Expenses YTD:        $3,522.84
  Net profit:          $7,502.16
  Tax set-aside (25%): $1,875.54
  Safe to spend:       $5,622.62

--- Subscription drag (often invisible) ---
  Adobe CC               $54.99/mo
  Spotify                $11.99/mo
  ...
  Total:                 $126.97/mo  ($1,523.64/yr)
```

## Full dashboard

```bash
python3 ultimate_finance_tracker.py income-sample.csv expenses-sample.csv debts-sample.csv savings-sample.csv accounts-sample.csv subscriptions-sample.csv investments-sample.csv
```

Includes monthly overview, investment portfolio, debt avalanche, savings goals, and net worth — matching simonotion's automated reports promise.
