# Net income visibility — what's actually yours to spend?

Clone of [faisalmq's Freelance Finance Tracker (Google Sheets)](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-5797) buyer channel + Quillenhart qaduu net-profit dashboard tab.

**Not tax advice.** Planning numbers only.

## The problem (financial fog)

You finish a project, send the invoice, and watch payment land. For a moment you feel flush.

Then the questions hit:

- How much is for quarterly taxes?
- Does it cover subscription renewals due next month?
- Is any of it profit you can actually pull for personal use?

Treating your freelance business like a personal checking account puts long-term stability at risk.

## The four clarity layers

| Layer | What it answers | Kit module |
|-------|-----------------|------------|
| Gross vs net | Deposits vs real profit after expenses | `monthly_dashboard.py` P&L |
| Tax readiness | Set-aside from **net**, not gross | Quarterly tax block |
| Subscription load | Monthly break-even from recurring bills | `bills-sample.csv` |
| Net income visibility | Spendable after tax + bills + debt mins | NET INCOME VISIBILITY stdout |

## 10-minute weekly habit

1. Log every transaction in `transaction-log-template.csv` (one row per money event).
2. Mark recurring bills in `bills-tracker.md` or `bills-sample.csv`.
3. Run:

```bash
python3 monthly_dashboard.py sample-transactions.csv invoices-sample.csv bills-sample.csv debt-sample.csv
```

4. Read the **NET INCOME VISIBILITY** block — that is your spendable number, not the deposit alert.

## Worked example

| Item | Amount |
|------|--------|
| January gross deposits | $5,000 |
| Business expenses | −$545 |
| Net profit | $4,455 |
| Tax reserve (25%) | −$1,114 |
| Monthly subscriptions | −$180/mo |
| Debt minimums | −$250/mo |
| **Est. spendable (monthly avg)** | **~$2,911** |

The bank showed $5,000. Only ~$2,900 was actually yours to spend or save.

## Who it's for

Freelancers, indie hackers, and solopreneurs who want clarity without bloated accounting software — the same audience [Quillenhart's $15 Gumroad tracker](https://quillenhart.gumroad.com/l/qaduu) (7 ratings) serves.
