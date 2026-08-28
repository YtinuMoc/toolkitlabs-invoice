# CEO weekly check-in — 10-minute Etsy money review

Clone of [sundayscope Profit After Fees ($27 on Gumroad)](https://sundayscope.gumroad.com/l/jmqyil) **CEO Weekly Check-In** tab.

Buyer-channel shape: [faisalmq/54h7 five-minute weekly check-in](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-54h7) — deposit anxiety → five-minute habit → P&L clarity → scale/hold/cut decisions from **net**, not dashboard ROAS.

## The 10-minute ritual (Etsy edition)

1. **Gross this period** — sum of order totals (not bank deposits yet)
2. **Fees paid to Etsy** — listing + transaction + processing + Offsite Ads
3. **Real profit** — net after fees and logged expenses
4. **Tax set-aside** — planning rate on net profit (default 28%)
5. **Decision** — scale ads, hold spend, or cut listings based on **NET profit**, not ROAS

If the system takes longer than ten minutes, you won't use it. One CSV row per sale, one CLI run, one decision.

## CLI workflow

```bash
python3 profit_after_fees_tracker.py sales-sample.csv expense-sample.csv ads-sample.csv
```

Look for the `CEO WEEKLY CHECK-IN` block at the end of stdout.

## Pair with

- [pay-yourself-guide.md](pay-yourself-guide.md) — faisalmq/5797 safe-to-spend after reserve
- [tax-set-aside-guide.md](tax-set-aside-guide.md) — quarterly set-aside from net
