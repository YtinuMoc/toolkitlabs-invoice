# Payment follow-up cadence — agentchip/11n6 clone

Clone of [agentchip's follow-up rhythm post](https://dev.to/agentchip/your-customers-arent-ghosting-you-your-follow-up-is-11n6): most lost deals die to silence, not competitors. Same cadence discipline applied to **overdue invoices** — preview only, you send.

## The problem

You sent an invoice. The client said "sounds good." Then silence. You wait because you don't want to seem pushy. The invoice ages past due and you never follow up consistently.

## Fixed cadence (after due date)

| Touch | Days after due | Action |
|-------|----------------|--------|
| 1 | +1 | Polite check-in |
| 2 | +3 | Reminder with invoice link |
| 3 | +7 | Firm but friendly nudge |
| 4 | +14 | Escalation note |
| 5 | +30 | Final notice before write-off |

No CRM. No subscription. One CSV + CLI preview.

## Quick start

```bash
python3 freelancer_invoice_tracker.py --follow-up invoices-sample.csv payments-sample.csv
```

## What the CLI does

1. Finds overdue invoices with unpaid balance
2. Maps each to the 1/3/7/14/30-day touch schedule
3. Flags which touch is **DUE NOW** (preview — no email sent)
4. Prints a copy/paste template with `{{client}}`, `{{invoice_id}}`, `{{balance}}`

## Files

| File | Purpose |
|------|---------|
| `invoices-sample.csv` | Sample overdue rows |
| `payments-sample.csv` | Partial payments (optional) |
| `freelancer_invoice_tracker.py` | `--follow-up` mode |

## EUR 9 kit

Full workbook: [checkout](https://buy.stripe.com/cNi3cwfls6PO6B8c4d5Ne0F)

Original: [AgentChip ahefab ($15)](https://qiliang.gumroad.com/l/ahefab) · follow-up shape from [agentchip/11n6](https://dev.to/agentchip/your-customers-arent-ghosting-you-your-follow-up-is-11n6).
