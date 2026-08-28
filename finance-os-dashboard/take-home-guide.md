# Take-home estimator — freelancer tax reserve guide

Clone of [MarginMap's Freelancer Tax Guide 2026](https://dev.to/marginmap/the-freelancer-tax-guide-2026-what-you-actually-take-home-14ag) buyer channel + [chrisnotion Finance OS Dashboard (30,427 sales · 506 ratings · 4.9★)](https://chrisnotion.gumroad.com/l/fcufra).

**Not tax advice.** Planning numbers only — confirm with a CPA.

## Reserve rates by state type (single filer, standard deduction)

| State type | Examples | Reserve % of **net** profit |
|------------|----------|----------------------------|
| No state income tax | TX, FL, WA, NV | 22–28% |
| Low state tax | CO, IL, UT | 25–30% |
| Medium state tax | GA, NC, AZ | 28–33% |
| High state tax | CA, NY, NJ | 32–38% |

Default in `finance_os_dashboard.py`: **28%** (middle of low-state band).

## Worked example ($80k gross, $8k expenses, Colorado 4.4%)

| Item | Amount |
|------|--------|
| Gross revenue | $80,000 |
| Business expenses | −$8,000 |
| Net self-employment income | $72,000 |
| SE tax (15.3% × net) | −$11,016 |
| Federal + state (simplified) | −$8,144 |
| **Take-home** | **~$52,840** |

Effective rate ≈ 29% on gross — not the flat "30% of gross" shortcut.

## Run it

```bash
python3 finance_os_dashboard.py --take-home income-sample.csv expenses-sample.csv
```

## How to use with Finance OS Dashboard

1. Log income and expenses in the CSV templates.
2. Run `--take-home` after each big deposit or monthly close.
3. Transfer the reserve amount to a tax-only savings account same day.
4. Use the full dashboard for subscriptions, accounts, and monthly overview:

```bash
python3 finance_os_dashboard.py income-sample.csv expenses-sample.csv accounts-sample.csv goals-sample.csv debts-sample.csv subscriptions-sample.csv
```

Full kit: [Finance OS Dashboard clone (EUR 9)](https://ytinumoc.github.io/toolkitlabs-invoice/finance-os-dashboard/)
