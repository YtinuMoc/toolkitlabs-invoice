# Amazon FBA fees — multichannel seller math

Clone of [ambrosetheshield's multi-platform tracker](https://ambrosetheshield.gumroad.com/l/xdjzq) (£14.85 Gumroad).

ambrosetheshield's promise: log every order with real fees, postage, packaging, and COGS — see net profit per channel. Amazon FBA stacks referral + fulfillment; most handmade sellers track Etsy/Vinted and **guess** Amazon.

## Amazon FBA fee stack (simplified)

```plaintext
Total platform cost = Referral fee + FBA fulfillment

Referral fee  = sale price × category rate (often 15% on accessories)
FBA fee       = weight/dimension tier (small standard ≈ $3.22 / ~£2.50)
```

Log `platform_fee` as referral + FBA combined. Leave blank only if you use `amazon_handmade` auto-calc (15% referral, no FBA).

## Worked example: £18 phone case on Amazon FBA

| Line | Amount |
|------|--------|
| Sale price | £18.00 |
| Referral (15%) | £2.70 |
| FBA fulfillment | £2.50 |
| Postage (inbound to warehouse) | £1.20 |
| Packaging | £0.50 |
| COGS | £4.00 |
| **Net profit** | **£7.10** |

Same SKU on Etsy at £22 might net more after handmade fees — **the channel matters more than list price.**

## Log Amazon rows in your order CSV

```csv
date,order_id,item,platform,sale_price,platform_fee,postage,packaging,cogs,time_minutes
2026-08-01,AM-441,Phone case,amazon,18.00,5.20,1.20,0.50,4.00,25
2026-08-05,AM-442,Cable,amazon,12.00,4.05,0.80,0.30,2.50,15
```

`platform_fee` = £5.20 = £2.70 referral + £2.50 FBA.

```bash
python3 multi_platform_seller_tracker.py orders-sample.csv
```

```plaintext
=== PROFIT BY PLATFORM ===
  amazon            2 orders · gross £30.00 · net £11.55
  etsy              3 orders · gross £82.00 · net £38.72
```

## Pricing calculator for Amazon Handmade (no FBA)

For Handmade listings without FBA, use `amazon_handmade` in the pricing CLI:

```bash
python3 multi_platform_seller_tracker.py --price-profit 8 5 2 1 amazon_handmade
```

Full workbook: [EUR 9 checkout](https://buy.stripe.com/8x24gA3CK6PO7Fcc4d5Ne0I) · [start here](start-here.md)
