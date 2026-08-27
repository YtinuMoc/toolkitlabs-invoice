# Self-updating deliverable inventory — agentchip/5fca clone

Clone of [agentchip's inventory tracker post](https://dev.to/agentchip/i-built-a-self-updating-inventory-tracker-in-excel-no-monthly-saas-fees-5fca): live stock levels, low-stock alerts, movement log, revenue dashboard — without $20–40/month SaaS. Adapted to **freelancer service packages and deliverable SKUs** (retainer blocks, template packs, hour banks).

## The 4-sheet architecture (freelancer edition)

**1. Inventory** — one row per SKU: name, category, unit cost/price, reorder point.

**2. Stock Log** — append-only movements: Purchase / Sale / Adjustment / Return. Stock is **derived** from the log (SUMIF shape) — never typed by hand.

**3. Dashboard** — SKUs on hand, stock value at cost, potential revenue, LOW count.

**4. Status** — `LOW` when current stock ≤ reorder point. Red rows = reorder today.

## Quick start

```bash
python3 freelancer_invoice_tracker.py --inventory inventory-sample.csv stock-log-sample.csv
```

## What the CLI does

1. Sums signed quantities per SKU from the movement log
2. Flags **LOW** lines at or below reorder point (agentchip/5fca conditional-format shape)
3. Prints stock value at cost and potential revenue at price
4. Movement log stays the audit trail — "when did we lose 12 units of PKG-RETAINER?"

## Files

| File | Purpose |
|------|---------|
| `inventory-sample.csv` | SKU master + reorder points |
| `stock-log-sample.csv` | Append-only movement log |
| `freelancer_invoice_tracker.py` | `--inventory` mode |

## EUR 9 kit

Full workbook: [checkout](https://buy.stripe.com/cNi3cwfls6PO6B8c4d5Ne0F)

Original: [AgentChip ahefab ($15)](https://qiliang.gumroad.com/l/ahefab) · inventory shape from [agentchip/5fca](https://dev.to/agentchip/i-built-a-self-updating-inventory-tracker-in-excel-no-monthly-saas-fees-5fca).
