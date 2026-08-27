# Freelancer Tax Stack — Tools Without Losing Your Mind

Clone of [tatelyman/3427384](https://dev.to/tatelyman/the-freelancer-tax-stack-tools-i-use-to-not-get-destroyed-by-the-irs-2) buyer channel + Quillenhart qaduu deduction tracking.

Nobody withholds taxes for freelancers. Self-employment tax alone is 15.3% on top of income tax. This guide maps the five-layer stack to files in the finance tracker kit.

## 1. Quarterly tax estimates

Run `python3 monthly_dashboard.py my-transactions.csv` and read the **QUARTERLY TAX SET-ASIDE** block. Plug your real net profit — not gross deposits — into the estimate.

Pair with [take-home-guide.md](take-home-guide.md) for marginmap-style reserve math.

## 2. Invoice tracking

Log sent invoices in `invoices-sample.csv` format. Run with invoices path:

```bash
python3 monthly_dashboard.py my-transactions.csv invoices-sample.csv
```

Read **ACCOUNTS RECEIVABLE** for overdue flags (agentchip/2b11 shape).

## 3. Rate calculation

Your hourly rate only makes sense after taxes, insurance, and non-billable hours. Use [dashboard-guide.md](dashboard-guide.md) monthly P&L + [take-home-guide.md](take-home-guide.md) to price from net, not gut feel.

## 4. Deduction categories to log

Use these `category` values in your transaction CSV:

| Category key | What it covers |
|--------------|----------------|
| `home_office` | Home office (simplified $5/sq ft up to $1,500) |
| `software` | Software subscriptions |
| `internet_phone` | Internet/phone business % |
| `health_insurance` | Health insurance premiums (100% deductible) |
| `professional_dev` | Courses, books, conferences |
| `mileage` | Business mileage |
| `equipment` | Equipment under $2,500 (Section 179) |

The dashboard prints a **FREELANCER TAX STACK** block summarizing logged deductions.

## 5. SEP-IRA (planning only)

You can contribute up to 25% of net SE income to a SEP-IRA. Contributions reduce taxable income. Confirm limits with a CPA — this kit does not track retirement accounts.

## April 15 move (US planning)

1. Estimate what you owe → run dashboard on full-year CSV
2. File Form 4868 extension if needed
3. Pay estimated amount by deadline
4. Organize deductions from category breakdown → file by extension date

Not tax advice. Clone of [Quillenhart qaduu ($15)](https://quillenhart.gumroad.com/l/qaduu).
