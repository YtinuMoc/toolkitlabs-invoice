# Hidden pricing math — Etsy, Gumroad & Amazon bookkeeping

Clone of [vivre05's E-Commerce Bookkeeping Dashboard](https://vivre05.gumroad.com/l/xytjqh) ($29+ Gumroad).

Buyer-channel shape: [sellermind/4307601 — The Hidden Math Behind Etsy Pricing](https://dev.to/sellermind/the-hidden-math-behind-etsy-pricing-why-most-sellers-lose-money-without-knowing-it-2ga8).

## The list-price illusion

| What you think | What actually happens |
|----------------|----------------------|
| $25 sale = $25 revenue | Payout is sale minus platform fees, postage, and COGS |
| Fees are "about 10%" | Etsy 6.5% + 3% + $0.20 listing; Gumroad 10% + $0.30; Amazon ~15% |
| Postage is neutral | "Free shipping" means you eat the label — often $3–6 |
| One sale = profit | Relist fees, software subs, and offsite ads flip winners to losers |

## Break-even before you publish

```bash
python3 ecommerce_bookkeeping_dashboard.py --price-profit 10 8 3 1 etsy
# Charge at least: $25.12

python3 ecommerce_bookkeeping_dashboard.py --price-margin 40 6 0 0 gumroad
# Charge at least: $11.00
```

## Log every hidden line in your transaction CSV

```csv
date,platform,type,description,amount,category
2026-03-01,etsy,sale,Handmade candle,25.00,revenue
2026-03-01,etsy,expense,Etsy fees (listing + 6.5% + 3%),-2.15,fees
2026-03-01,etsy,expense,Postage label,-3.50,shipping
2026-03-01,other,expense,Packaging,-0.80,supplies
2026-03-01,other,expense,COGS wax + jar,-6.00,cogs
```

```bash
python3 ecommerce_bookkeeping_dashboard.py transactions-sample.csv
```

See [start-here.md](start-here.md) · [transactions-sample.csv](transactions-sample.csv) · [fee-calculator-guide.md](fee-calculator-guide.md).
