# Platform fee defaults (PattyBun rauxja clone)

Clone of [PattyBun's Digital Product Creator Income Tracker](https://pattybun.gumroad.com/l/rauxja) ($14.99) — auto-calculated fees by platform. Override any row in `creator_dashboard.py` with a manual fee column later if your rate differs.

| Platform | Default fee model |
|----------|-------------------|
| gumroad | 10% of gross + $0.50 flat |
| etsy | 6.5% of gross + 3% payment processing |
| shopify | 2.9% + $0.30 payment processing |
| payhip | 5% of gross |
| other | 0% (enter fee manually in notes as `fee=12.34`) |

These are planning defaults, not tax advice. Adjust in the CLI source if your storefront uses different tiers.
