# Late payment system guide

Clone of [wilsonhoe/2gnj](https://dev.to/wilsonhoe/i-tracked-200-invoices-in-notion-for-6-months-the-late-payment-system-that-saved-me-12000-2gnj) buyer channel + [jnkxstudio Finance Tracker 4.0 (2,995 sales)](https://jnkxstudio.gumroad.com/l/Finance_Tracker_3).

[wilsonhoe's post](https://dev.to/wilsonhoe/i-tracked-200-invoices-in-notion-for-6-months-the-late-payment-system-that-saved-me-12000-2gnj) tracked 214 invoices over 6 months. Average collection time dropped from 39 days to 11 days. Overdue invoices fell from 29% to 6%. The system saved ~$12,000/year in lost billable time chasing payments.

## The 4-database problem (solved with CSV)

1. **Invoice log** — sent date, due date, amount, status, paid date
2. **Client patterns** — which clients pay late repeatedly
3. **Cash flow projection** — what's outstanding vs. what's at risk
4. **Collection metrics** — avg days to payment, overdue %

Our clone ships all four as one `invoices.csv` + CLI.

## Run it

```bash
python3 finance_tracker_4.py --late-payment invoices-sample.csv
```

## What to track

| Column | Purpose |
| --- | --- |
| `invoice_id` | Unique reference |
| `client` | Who owes you |
| `sent_date` | When you sent it |
| `due_date` | Net-15 or Net-30 deadline |
| `amount` | Invoice total |
| `status` | `sent`, `paid`, or `overdue` |
| `paid_date` | When money actually arrived |

## Weekly routine

1. Add new invoices when sent (status = `sent`).
2. Mark `paid` + `paid_date` when payment lands.
3. Run `--late-payment` every Monday.
4. Follow up on anything overdue before it hits 30 days.

Five minutes a week beats 20 days a year chasing payments.
