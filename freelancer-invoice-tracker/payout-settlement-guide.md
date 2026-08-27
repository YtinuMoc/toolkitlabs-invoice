# Client payout settlement — agentchip/52c0 clone

Clone of [agentchip's consignment payout post](https://dev.to/agentchip/the-spreadsheet-that-saves-consignment-shops-from-losing-money-and-friends-52c0): three money leaks — deadline drift, payout math errors, and no statements. Same discipline applied to **freelancer client balances**.

## The three leaks (freelancer edition)

**1. The stale open invoice nobody escalates.** Like consignment's 90-day rule, open invoices past 90 days need a decision: chase, discount, or write off. Without a countdown, they sit forever.

**2. The payout math.** Multiple invoices per client, partial payments, different amounts — manual arithmetic loses money and trust.

**3. No client statement.** "How much do I owe you?" should be one number, not a pile of receipts.

## Quick start

```bash
python3 freelancer_invoice_tracker.py --settlement clients-sample.csv invoices-sample.csv payments-sample.csv
```

## What the CLI does

1. Rolls up invoiced vs received per client
2. Lists open invoices with age in days
3. Flags **STALE** lines at 90+ days open (agentchip/52c0 countdown shape)
4. Prints portfolio balance due — your monthly statement draft

## Files

| File | Purpose |
|------|---------|
| `clients-sample.csv` | Client registry + payment terms |
| `invoices-sample.csv` | Invoice rows |
| `payments-sample.csv` | Partial/full payments |
| `freelancer_invoice_tracker.py` | `--settlement` mode |

## EUR 9 kit

Full workbook: [checkout](https://buy.stripe.com/cNi3cwfls6PO6B8c4d5Ne0F)

Original: [AgentChip ahefab ($15)](https://qiliang.gumroad.com/l/ahefab) · settlement shape from [agentchip/52c0](https://dev.to/agentchip/the-spreadsheet-that-saves-consignment-shops-from-losing-money-and-friends-52c0).
