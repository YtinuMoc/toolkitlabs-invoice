# Etsy vs Gumroad fee shapes (smadsby ejxcg shape)

[SimpleBizDash](https://smadsby.gumroad.com/l/ejxcg) targets Etsy sellers **and** Gumroad creators in one workbook. The fee stacks are different — comparing dashboard gross misleads.

## Gumroad (digital products)

- **10%** platform fee on sale price
- **$0.30** flat per transaction
- Low-ticket SKUs ($5–$15) often see **15–18% effective** fee rate because of the flat

## Etsy (physical + digital)

- **$0.20** listing fee per listing (renewed every 4 months or on sale)
- **6.5%** transaction fee on order total
- **3% + $0.25** payment processing on order total
- Small orders ($8–$12) often see **18–22% effective** fee rate

## Head-to-head CLI

```bash
python3 seller_profit_fee_tracker.py sales-sample.csv expense-sample.csv --etsy-gumroad
```

Shows net per platform, effective fee %, and which storefront wins on the same gross basket.

## When to sell where

- **Gumroad** — higher net on $20+ digital SKUs, no listing fee churn
- **Etsy** — discovery for physical/handmade; price for fee drag on low tickets
- **Both** — log every order in one CSV; monthly summary shows which channel actually paid last month

Full workbook: [EUR 9 checkout](https://buy.stripe.com/9B68wQc9g7TS1gOgkt5Ne0G?client_reference_id=etsy-gumroad-guide).
