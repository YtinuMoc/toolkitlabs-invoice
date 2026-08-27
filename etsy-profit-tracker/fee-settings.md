# Etsy fee defaults (PattyBun ejmzqy clone)

Clone of [PattyBun's Etsy Shop Profit + Fees Tracker](https://pattybun.gumroad.com/l/ejmzqy) ($12.99) — all 4 Etsy fees auto-calculated per sale. Override rates in `etsy_dashboard.py` if Etsy changes tiers.

| Fee | Default |
|-----|---------|
| Listing fee | $0.20 per quantity sold |
| Transaction fee | 6.5% of gross |
| Payment processing | 3% of gross + $0.25 flat |
| Offsite ads | 15% of gross (12% high-volume shop) — only when `offsite_ad=yes` |

Set `high_volume_shop=yes` on a row to use the 12% offsite ads rate instead of 15%.

These are planning defaults, not tax advice.
