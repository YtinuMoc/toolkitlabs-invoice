# Freelance self-assessment tax tracker

Clone of [landolio/5hae](https://dev.to/landolio/the-freelance-tax-tracker-setup-that-makes-january-self-assessment-painless-5hae) buyer channel + [saksham82's Freelancer Finance Pack ($9)](https://saksham82.gumroad.com/l/cueko).

Monthly tracking beats January panic. Five transaction columns → automatic tax-pot arithmetic.

## The five columns

| Column | Rule |
|--------|------|
| `date` | When the money moved, not when the invoice was raised |
| `category` | Income, Equipment, Software, Travel, Professional Services, Home Office, Other |
| `amount` | Positive income, negative expense |
| `description` | Receipt reference or client name — enough for an audit trail |
| `type` | `income` or `expense` |

## Automatic calculations

- **Profit** = Income − Allowable Expenses
- **Income tax estimate** = profit above personal allowance × relevant rate (planning only)
- **Class 4 NI** = profit between allowance band × 9% (UK sole trader planning shape)
- **Tax pot** = running total to set aside (25–30% rule)

## Free CLI

```bash
python3 freelancer_finance_pack.py --self-assessment self-assessment-sample.csv
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

Pairs with the [merge ledger guide](merge-ledger-guide.md) and US/India tax blocks in the full EUR 9 kit.

## Paid kit

[Freelancer Finance Pack — EUR 9](https://buy.stripe.com/00w7sMgpwdecf7Efgp5Ne0M) — invoice tracker + expense log + US quarterly tax + India advance tax + profit dashboard. Same architecture as [saksham82 on Gumroad ($9)](https://saksham82.gumroad.com/l/cueko).
