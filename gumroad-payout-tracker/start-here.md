# Start here — Gumroad Payout Tracker with Charts

Clone of [Nagaraj inagaraj](https://inagaraj.gumroad.com/l/gumroad-payout-tracker-with-charts) ($10+ Gumroad, **31 sales**, 3 ratings).

## 1. Log payouts

One row per Gumroad payout in `payouts-template.csv`:

- `gross_sales` — sales in the payout period
- `fees` — Gumroad platform fees
- `commission_paid` — affiliate commissions you paid out
- `commission_received` — affiliate income you earned
- `net_payout` — what hit your bank (or leave blank to auto-calc)
- `status` — `pending`, `in_transit`, or `done`

## 2. Track affiliate commissions (optional)

Split detail in `commission-paid-template.csv` and `commission-received-template.csv`.

## 3. Run the CLI

```bash
python3 payout_dashboard.py payouts-template.csv commission-paid-template.csv commission-received-template.csv
```

See `payouts-sample.csv` for worked examples matching Nagaraj's dashboard + calendar + kanban promise.
