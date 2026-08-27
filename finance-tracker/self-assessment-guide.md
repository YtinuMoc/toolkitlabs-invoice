# Freelance Self-Assessment Tax Tracker Guide

Clone of [landolio/5hae](https://dev.to/landolio/the-freelance-tax-tracker-setup-that-makes-january-self-assessment-painless-5hae) buyer channel — monthly tracking beats annual panic; five transaction columns; automatic tax-pot arithmetic.

## The five columns that matter

Every income or expense row in `transaction-log-template.csv`:

| Column | Rule |
|--------|------|
| `date` | When the money moved, not when the invoice was raised |
| `category` | Income, Equipment, Software, Travel, Professional Services, Home Office, Other |
| `amount` | Positive income, negative expense |
| `description` | Receipt reference or client name — enough for an audit trail |
| `type` | `income` or `expense` |

## Automatic calculations

Once income and allowable expenses are logged:

- **Profit** = Income − Allowable Expenses
- **Income tax estimate** = profit above personal allowance × relevant rate (planning only)
- **Class 4 NI** = profit between allowance band × 9% (UK sole trader planning shape)
- **Tax pot** = running total to set aside (25–30% rule works for most freelancers)

## Free CLI

```bash
python3 monthly_dashboard.py sample-transactions.csv
```

Look for the `SELF-ASSESSMENT TAX POT (landolio/5hae shape)` block in stdout.

## Allowable expenses most people miss

- Home office (flat rate or proportional utilities)
- Professional development (courses, books, subscriptions)
- Accountant and bookkeeping fees
- Business bank account fees
- Equipment depreciation
- Phone (business proportion only)
- Software (100% if business-only)

Pairs with Quillenhart qaduu quarterly tax set-aside + annual summary tabs in the full EUR 9 kit.
