# Start here — Freelancer Finance Pack

Clone of [saksham82 cueko ($9)](https://saksham82.gumroad.com/l/cueko).

## Guide index

See [mesh-hub.md](mesh-hub.md) for all 5 dev.to buyer-channel guides.

## 15-minute monthly routine

1. Log new invoices in `invoices-template.csv` (or your copy).
2. Log expenses with category + deductible flag.
3. Run the CLI:

```bash
python3 freelancer_finance_pack.py invoices-sample.csv expenses-sample.csv 120
```

4. Move the **Tax set-aside** number to a separate savings account.
5. Export Gumroad/Stripe/PayPal CSVs and merge:

```bash
python3 freelancer_finance_pack.py --merge gumroad-sales.csv stripe-balance.csv -o ledger-merged.csv
```

## Status colors (workbook equivalent)

- **Paid** — collected
- **Sent / Awaiting** — outstanding
- **Overdue** — past due date (auto-flagged in CLI)

Not tax advice. Verify rates with a licensed CPA or CA before filing.
