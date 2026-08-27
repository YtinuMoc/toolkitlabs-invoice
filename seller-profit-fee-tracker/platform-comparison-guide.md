# Platform performance comparison (smadsby ejxcg shape)

[SimpleBizDash on Gumroad](https://smadsby.gumroad.com/l/ejxcg) promises **Platform Performance Comparison** — gross leaderboards lie. This guide mirrors that tab.

## Run it

```bash
python3 seller_profit_fee_tracker.py sales-sample.csv expense-sample.csv
```

Look for the `PLATFORM PERFORMANCE COMPARISON` block:

- Gross, fees, effective fee %, and net per platform
- **Highest fee drag** / **Lowest fee drag** lines — which channel eats margin

## Etsy vs Gumroad fee shapes

| Platform | Why gross ≠ net |
|----------|-----------------|
| Gumroad | 10% + $0.30 flat — hurts low-ticket SKUs |
| Etsy | $0.20 listing + 6.5% + 3% processing + $0.25 |
| Shopify | 2.9% + $0.30 — looks cheap per order |
| eBay | 12.9% + $0.30 |
| Amazon | 15% referral |

Edit `PLATFORM_FEES` in `seller_profit_fee_tracker.py` if your tier differs.

## Decision rule

If Gumroad has the highest fee drag but also the highest net volume, keep selling there — but price with eyes open. If Etsy net is flat after fees, stop listing new SKUs until SEO justifies the drag.
