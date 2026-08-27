# Freelance self-assessment tax tracker

Clone of [landolio/5hae](https://dev.to/landolio/the-freelance-tax-tracker-setup-that-makes-january-self-assessment-painless-5hae) buyer channel + [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).

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
python3 freelance_finance_os.py --self-assessment self-assessment-sample.csv
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

Pairs with the [quarterly tax estimator](quarterly-tax-guide.md) and [tax buffer](tax-buffer-guide.md) in the full EUR 9 kit.

## Paid kit

[Freelance Finance OS — EUR 9](https://buy.stripe.com/4gM3cw0qy8XWgbI2tD5Ne0E) — four tools in one bundle. Same architecture as [By the Loop on Gumroad ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).
