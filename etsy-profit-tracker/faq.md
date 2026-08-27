# FAQ

**Why is my Etsy payout less than my sales dashboard?**
Etsy deducts listing fee ($0.20), transaction fee (6.5%), payment processing (3% + $0.25), and sometimes offsite ads (15%) before deposit. This tracker calculates all four on every row.

**Do I log gross or net?**
Log the sale price the buyer paid (`sale_price`). The CLI calculates fees and net profit.

**What is offsite_ad?**
Set `yes` when the sale came from Etsy's Offsite Ads program. The 15% (or 12% high-volume) fee applies only on those rows.

**Can I change fee rates?**
Edit the constants at the top of `etsy_dashboard.py`. PattyBun's Google Sheets Settings tab does the same thing.
