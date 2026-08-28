# Hidden pricing math — Etsy, eBay & Vinted

Clone of [ambrosetheshield's multi-platform tracker](https://ambrosetheshield.gumroad.com/l/xdjzq) (£14.85 Gumroad).

Buyer-channel shape: [sellermind/4307601 — The Hidden Math Behind Etsy Pricing](https://dev.to/sellermind/the-hidden-math-behind-etsy-pricing-why-most-sellers-lose-money-without-knowing-it-2ga8).

## The list-price illusion

| What you think | What actually happens |
|----------------|----------------------|
| £25 list = £25 revenue | Buyer may pay £25 + shipping; you receive sale minus fees |
| Fees are "about 10%" | Etsy 6.5% + 3% + £0.20 listing; eBay ~12.9% + £0.30; Vinted 5% + £0.70 |
| Postage is neutral | "Free shipping" means you eat the label — often £3–6 on a small parcel |
| One sale = profit | Relist fees, returns, and offsite ads can flip a winner to a loser |

## Break-even before you publish

```bash
python3 multi_platform_seller_tracker.py --price-profit 8 6 3 1 etsy
# Charge at least: £19.47

python3 multi_platform_seller_tracker.py --price-margin 40 6 3 1 vinted
# Charge at least: £18.33
```

## Log every hidden line in one CSV

```csv
date,order_id,item,platform,sale_price,platform_fee,postage,packaging,cogs,time_minutes
2026-08-01,ET-101,Handmade mug,etsy,25.00,2.15,3.50,0.80,6.00,45
2026-08-03,VI-202,Vintage jacket,vinted,35.00,2.45,0.00,0.50,8.00,20
```

```bash
python3 multi_platform_seller_tracker.py orders-sample.csv
```

See [start-here.md](start-here.md) · [orders-sample.csv](orders-sample.csv) · [pricing-calculator-guide.md](pricing-calculator-guide.md).
