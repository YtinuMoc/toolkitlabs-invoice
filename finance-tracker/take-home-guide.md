# Take-home estimator — freelancer tax reserve guide

Clone of [MarginMap's Freelancer Tax Guide 2026](https://dev.to/marginmap/the-freelancer-tax-guide-2026-what-you-actually-take-home-14ag) shape + Quillenhart qaduu quarterly set-aside tab.

**Not tax advice.** Planning numbers only — confirm with a CPA.

## Reserve rates by state type (single filer, standard deduction)

| State type | Examples | Reserve % of **net** profit |
|------------|----------|----------------------------|
| No state income tax | TX, FL, WA, NV | 22–28% |
| Low state tax | CO, IL, UT | 25–30% |
| Medium state tax | GA, NC, AZ | 28–33% |
| High state tax | CA, NY, NJ | 32–38% |

Default in `monthly_dashboard.py`: **28%** (middle of low-state band).

## Worked example ($80k gross, $8k expenses, Colorado 4.4%)

| Item | Amount |
|------|--------|
| Gross revenue | $80,000 |
| Business expenses | −$8,000 |
| Net self-employment income | $72,000 |
| SE tax (15.3% × net) | −$11,016 |
| SE tax deduction (50%) | +$5,508 |
| AGI (simplified) | $66,492 |
| Standard deduction | −$15,000 |
| Taxable income | $51,492 |
| Federal income tax (approx) | −$5,820 |
| Colorado state (4.4%) | −$2,266 |
| **Total taxes** | **$23,160** |
| **Take-home** | **$56,840** |

Effective rate ≈ 29% on gross — not the flat "30% of gross" shortcut.

## How to use with this kit

1. Log transactions in `transaction-log-template.csv`
2. Run `python3 monthly_dashboard.py your-log.csv`
3. Read **TAKE-HOME ESTIMATE** — uses your YTD net + chosen reserve %
4. Transfer set-aside monthly; adjust reserve % in `setup-guide.md`

Full kit: [Quillenhart qaduu clone ($15 → EUR 9)](https://ytinumoc.github.io/toolkitlabs-invoice/finance-tracker/)
