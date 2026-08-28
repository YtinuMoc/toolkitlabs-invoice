# Etsy pay-yourself math — safe to spend after fees and tax reserve

Clone of [sundayscope Profit After Fees ($27 on Gumroad)](https://sundayscope.gumroad.com/l/jmqyil) **Pay Yourself Calculator** tab.

Buyer-channel shape: [faisalmq/5797 net income visibility](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-5797) — deposit lands → financial fog → tax reserve → **safe-to-spend** number, not gross deposits.

## The Etsy fog

Etsy deposits hit your bank. You treat the full amount as spendable. Then materials, Etsy Ads, and quarterly taxes arrive — and you overspent from gross.

**Safe to spend** = net profit after Etsy fees and expenses − tax set-aside. That is the sundayscope Pay Yourself tab.

## Worked example

| Step | Amount |
|------|--------|
| Gross sales | $4,200 |
| Etsy fees | −$682 |
| Materials + ads | −$1,240 |
| **Net profit** | **$2,678** |
| Tax set-aside (28%) | −$750 |
| **Safe to spend** | **$1,928** |

Spending $2,678 from the bank account ignores $750 you still owe the tax authority.

## CLI workflow

```bash
python3 profit_after_fees_tracker.py sales-sample.csv expense-sample.csv
```

Look for the `PAY YOURSELF CALCULATOR` block in stdout.

## Pair with

- [tax-set-aside-guide.md](tax-set-aside-guide.md) — l_d/5284 quarterly set-aside from net
- [start-here.md](start-here.md) — full 7-module workbook
