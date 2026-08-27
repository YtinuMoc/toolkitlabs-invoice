# Etsy Shop Profit + Fees Tracker

Shameless clone of [PattyBun ejmzqy](https://pattybun.gumroad.com/l/ejmzqy) ($12.99 Gumroad).

PattyBun ships a 7-tab Google Sheets template. Our clone ships CSV sales log + Python CLI with the same modules:

- Sales Log — all 4 Etsy fees per row
- Dashboard — revenue, fees, net profit, margin %
- Monthly Summary — rolling 24 months
- Listing Performance — ranked by net profit
- Fee Calculator — what-if before you price
- Goals — revenue and profit targets

```bash
python3 etsy_dashboard.py sales-sample.csv
```

See [start-here.md](start-here.md) and [fee-settings.md](fee-settings.md).
