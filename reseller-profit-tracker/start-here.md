# Start here — Reseller Profit Tracker

Clone of [Hustlin Hooks Reseller Spreadsheet 2025](https://hustlinhooks.gumroad.com/l/hustlinhooks2025).

## Step 1: Sales log

Open `sales-log-template.csv`. One row per sale:

| Column | What to enter |
|--------|---------------|
| date | Sale date YYYY-MM-DD |
| platform | ebay, poshmark, mercari, amazon |
| item | Product name |
| sku | Your SKU (links to inventory) |
| sale_price | What the buyer paid |
| platform_fee | Platform cut (Poshmark 20%, eBay ~13%, etc.) |
| shipping_cost | Postage you paid |
| cogs | What you paid for the item |
| net_profit | Leave blank — CLI calculates |
| status | sold |

## Step 2: Inventory master sheet

Open `inventory-template.csv`. Track every item from acquisition to sale:

- `days_listed` auto-computed if blank
- Status `listed` vs `sold`
- Aging report flags items listed 90+ days

## Step 3: Expenses

Open `expenses-template.csv`. Categories: supplies, mileage, rental.

## Step 4: Run dashboard

```bash
python3 reseller_dashboard.py sales-log.csv inventory.csv expenses.csv
```

Import CSVs into Google Sheets or Excel for charts — same workflow as Hustlin Hooks original.

## Fee reference (starting points — verify on each platform)

| Platform | Typical fee |
|----------|-------------|
| Poshmark | 20% flat |
| eBay | ~13% + $0.30 |
| Mercari | 10% |
| Amazon | ~15% referral |

Update your own rates in the sales log — platforms change.
