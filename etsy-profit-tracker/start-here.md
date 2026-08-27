# Start here — Etsy Shop Profit + Fees Tracker

Clone of [PattyBun ejmzqy](https://pattybun.gumroad.com/l/ejmzqy) ($12.99 Gumroad).

1. Copy `sales-log-template.csv` → `my-sales.csv`
2. Log every Etsy sale: date, listing name, sale price, quantity
3. Set `offsite_ad=yes` when Etsy Offsite Ads drove the sale
4. Run:

```bash
python3 etsy_dashboard.py my-sales.csv
```

You get: sales log with all 4 fees per row, dashboard totals, monthly summary, listing performance, fee calculator, and goals.

Free sample: `python3 etsy_dashboard.py sales-sample.csv`
