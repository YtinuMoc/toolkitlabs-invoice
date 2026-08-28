# Take-home estimator — freelancer tax reserve guide

Clone of [MarginMap's Freelancer Tax Guide 2026](https://dev.to/marginmap/the-freelancer-tax-guide-2026-what-you-actually-take-home-14ag) buyer channel + [BodegaLabs Emotional Finance Tracker (1,253 sales · 39 ratings · 5★)](https://bodegalaabs.gumroad.com/l/emotional-finance-tracker).

**Not tax advice.** Planning numbers only — confirm with a CPA.

## Reserve rates by state type (single filer, standard deduction)

| State type | Examples | Reserve % of **net** profit |
|------------|----------|----------------------------|
| No state income tax | TX, FL, WA, NV | 22–28% |
| Low state tax | CO, IL, UT | 25–30% |
| Medium state tax | GA, NC, AZ | 28–33% |
| High state tax | CA, NY, NJ | 32–38% |

Default in `emotional_finance_tracker.py`: **28%** (middle of low-state band).

## Run it

```bash
python3 emotional_finance_tracker.py --take-home income-sample.csv expenses-sample.csv
```

## How to use with Emotional Finance Tracker

1. Log income and expenses in the CSV templates.
2. Run `--take-home` after each big deposit or monthly close.
3. Transfer the reserve amount to a tax-only savings account same day.

Full bundle: [Emotional Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/emotional-finance-tracker/) — CSV templates, wishlist CLI, dashboard CLI, and take-home guide.
