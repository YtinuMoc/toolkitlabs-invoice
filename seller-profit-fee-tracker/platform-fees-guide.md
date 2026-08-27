# Platform fee settings (smadsby ejxcg shape)

Default fee math in `seller_profit_fee_tracker.py`:

| Platform | Model |
|----------|--------|
| Gumroad | 10% + $0.30 |
| Etsy | $0.20 listing + 6.5% transaction + 3% processing + $0.25 |
| Shopify | 2.9% + $0.30 |
| eBay | 12.9% + $0.30 |
| Amazon | 15% referral |

Edit `PLATFORM_FEES` in the Python file if your account tier differs.

The Gumroad original promises **Platform Performance Comparison** — which channel actually pays after fees, not just gross leaderboard.
