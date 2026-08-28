# Business self-assessment tax tracker

Buyer-channel shape: [landolio/5hae](https://dev.to/landolio/the-freelance-tax-tracker-setup-that-makes-january-self-assessment-painless-5hae).

Clone target: [heyismail Finance OS Pro ($29+ · 15,254 sales)](https://heyismail.gumroad.com/l/TheUltimateFinanceTracker).

Monthly tracking beats January panic. Five transaction columns → automatic tax-pot arithmetic.

## The five columns

| Column | Rule |
|--------|------|
| `date` | When the money moved, not when the invoice was raised |
| `category` | Income, Equipment, Software, Travel, Professional Services, Home Office, Other |
| `amount` | Positive income, negative expense |
| `description` | Receipt reference or client name — enough for an audit trail |
| `type` | `income` or `expense` |

## Free CLI

```bash
python3 finance_os_tracker.py --self-assessment self-assessment-sample.csv
```

Look for the `SELF-ASSESSMENT TAX POT (landolio/5hae shape)` block in stdout.

## Pair with

- [finance-os-guide.md](finance-os-guide.md) — full command center setup
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day buffer
- [merge-ledger-guide.md](merge-ledger-guide.md) — goldenalien/206o platform CSV merge
- [start-here.md](start-here.md) — income, expense, budget, subscription modules
