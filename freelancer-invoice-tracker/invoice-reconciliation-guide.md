# Invoice CSV reconciliation — agentchip/47ag clone

Clone of [agentchip's invoice copy-paste ritual post](https://dev.to/agentchip/i-automated-my-clients-3-hour-nightly-invoice-copy-paste-ritual-csv-in-reconciliation-out-47ag): dirty CSV in → dedupe + normalize → reconciliation report out. No AI guesses.

## The problem

Manual invoice entry fails on:

- **Duplicates** — vendor re-sends, you enter twice
- **Dirty numbers** — `$1,234.56` vs `1234.56` vs `2,100.00`
- **Vendor aliases** — "Acme Corp" vs "ACME CORPORATION"
- **Unparsed rows** — surface in `errors.csv`, never silently drop

## Quick start

```bash
python3 freelancer_invoice_tracker.py --reconcile dirty-invoices-sample.csv
```

## What the CLI does

1. Parses amounts with currency symbols and thousand separators
2. Normalizes dates (`8/3/26` → `2026-08-03`)
3. Collapses vendor aliases to one supplier name
4. Removes exact and near-duplicate rows
5. Prints totals by vendor and by month

## Files

| File | Purpose |
|------|---------|
| `dirty-invoices-sample.csv` | 12 rows of realistic dirty data |
| `freelancer_invoice_tracker.py` | `--reconcile` mode |
| `start-here.md` | Full five-sheet tracker setup |

## EUR 9 kit

Full workbook (clients + invoices + payments + overdue + dashboard): [checkout](https://buy.stripe.com/cNi3cwfls6PO6B8c4d5Ne0F)

Original: [AgentChip ahefab ($15)](https://qiliang.gumroad.com/l/ahefab)
