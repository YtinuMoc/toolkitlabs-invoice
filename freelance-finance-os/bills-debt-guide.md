# Recurring Bills + Debt Minimums Guide

Clone of [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os) + [crazychief/jg5](https://dev.to/crazychief/the-spreadsheet-that-eliminated-debt-in-five-months-and-what-it-taught-me-about-system-design-jg5) buyer channel: label, balance, minimum — habit first, payoff optimizer later.

## Why freelancers need this inside the finance OS

Client income is irregular. Fixed bills (hosting, software, insurance) and debt minimums hit every month whether you invoiced or not. The expense tab tracks what you spent; the bills/debt tab tracks what you **must** pay.

## Bills: one row per subscription, forever

| Bill | Amount | Frequency | Due day | Status |
|------|--------|-----------|---------|--------|
| Hosting | $20 | monthly | 1 | paid |
| Adobe CC | $54.99 | monthly | 15 | paid |
| Business insurance | $120 | quarterly | 1 | pending |

Mark `paid` when the charge clears. The CLI estimates your **monthly fixed load** (quarterly ÷ 3, yearly ÷ 12).

## Debt: minimums before avalanche vs snowball

| Creditor | Current balance | Min payment | Due day |
|----------|-----------------|-------------|---------|
| Business credit card | $1,850 | $75 | 15 |
| Equipment loan | $3,200 | $210 | 1 |

Update balances after payments. First question: **does this month's net profit cover all minimums?**

## Free CLI workflow

```bash
python3 freelance_finance_os.py --bills-debt bills-sample.csv debt-sample.csv
```

Or run the full OS with bills/debt wired into cash runway:

```bash
python3 freelance_finance_os.py invoice-log-sample.csv expense-log-sample.csv subscriptions-sample.csv bills-sample.csv debt-sample.csv
```

Free files: [bills-sample.csv](bills-sample.csv) · [debt-sample.csv](debt-sample.csv)

Full four-tool bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) · EUR 9 one-time · same delivery shape as [By the Loop on Gumroad ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).
