# Take-home estimator — what you actually keep after tax

Clone of [MarginMap's Freelancer Tax Guide 2026](https://dev.to/marginmap/the-freelancer-tax-guide-2026-what-you-actually-take-home-14ag) shape + [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os) rate calculator + tax buffer modules.

**Not tax advice.** Planning numbers only — confirm with a CPA.

## Why gross deposits lie

You land an $80,000 client year. Your brain says you banked $80,000. marginmap/14ag walks the real math:

1. **Business expenses** reduce your SE tax base first
2. **Self-employment tax** (15.3% of net, not gross) hits before income tax
3. **Federal brackets** apply to taxable income after deductions
4. **State tax** varies from 0% (TX, FL) to 13%+ (CA)

The "30% of gross" shortcut is wrong in both directions — it underestimates in high-tax states and overestimates when you have real deductions.

## Reserve rates by state type (single filer, planning)

| State type | Examples | Reserve % of **net** profit |
|------------|----------|----------------------------|
| No state income tax | TX, FL, WA, NV | 22–28% |
| Low state tax | CO, IL, UT | 25–30% |
| Medium state tax | GA, NC, AZ | 28–33% |
| High state tax | CA, NY, NJ | 32–38% |

Default in the CLI: **28%** (middle of low-state band).

## Worked example ($80k gross, $8k expenses, Colorado 4.4%)

| Item | Amount |
|------|--------|
| Gross revenue | $80,000 |
| Business expenses | −$8,000 |
| Net self-employment income | $72,000 |
| SE tax (15.3% × net) | −$11,016 |
| Federal + state (simplified) | −$8,086 |
| **Take-home** | **~$56,840** |

Effective rate ≈ 29% on gross — not a flat 30% haircut.

## Free CLI preview

```bash
python3 freelance_finance_os.py --take-home invoice-log-sample.csv expense-log-sample.csv
```

Sample output:

```plaintext
=== TAKE-HOME ESTIMATE (marginmap/14ag shape) ===
  Collected (gross paid): $3,100.00
  Business expenses:      $313.99
  Net self-employment:    $2,786.01
  Est. SE tax (15.3% net): $426.26
  Planned reserve (28% of net): $780.08
  Est. take-home after reserve: $2,005.93
  Effective reserve on gross: 25.2%
```

## Pair with By the Loop's four tools

- [rate-calculator.html](rate-calculator.html) — work backwards from take-home target to hourly floor
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers
- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend visibility
- [quarterly-tax-guide.md](quarterly-tax-guide.md) — olubunminelson/3n45 1040-ES deadlines

Full bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) — invoice tracker + expense/tax buffer + rate calculator + quarterly estimator.
