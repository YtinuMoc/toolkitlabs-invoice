# Gumroad seller finance tracker — five-tab system

Clone of [orion_operator/40gi](https://dev.to/orion_operator/the-solo-gumroad-sellers-guide-to-tracking-income-expenses-quarterly-taxes-with-a-google-sheet-40gi) buyer channel + Quillenhart qaduu **9-tab** finance tracker on Gumroad ($15, 7 ratings).

Orion's SellerLedger post maps five spreadsheet tabs. Quillenhart ships nine. This guide maps Orion's structure onto our CSV + Python clone.

## Orion tab → Quillenhart tab → our kit

| Orion (40gi) | Quillenhart qaduu | Our file |
|--------------|-------------------|----------|
| Transactions | Transactions | `transaction-log-template.csv` |
| P&L Dashboard | Dashboard | `monthly_dashboard.py` + `dashboard-guide.md` |
| Tax Summary | Annual Summary | `annual-summary.md` + YTD block |
| Tax Estimator | Quarterly set-aside | `tax-withholding-guide.md` |
| Instructions | Read Me + Setup | `readme-guide.md` + `setup-guide.md` |

Quillenhart adds Bills, Savings, Debt, and Invoices tabs — same transaction log, no re-typing.

## Category tags (Gumroad seller)

Use consistent categories so P&L and tax summary derive automatically:

- Income: `product_sales`, `client_work`, `other_income`
- Fees: `platform_fee`, `fulfillment`, `creator_commission`, `ad_spend`
- Expenses: `software`, `marketing`, `contractor`, `equipment`, `home_office`
- Adjustments: `refund_fee`, `other`

## CSV import habit

1. Gumroad → Sales → Export CSV
2. Stripe → Balance → Export payments CSV
3. Map columns → append rows to your transaction log (one row per money event)
4. Run `python3 monthly_dashboard.py my-transactions.csv`

Manual entry works — the importer is a time-saver, not a requirement.

## Three numbers that matter

1. **Real net profit** — gross minus fees, ads, refunds
2. **Categorized record** — hand to accountant without apologizing
3. **Running tax set-aside** — quarterly estimates from actual profit, not vibes

## Free samples

- [sample-transactions.csv](sample-transactions.csv)
- [transactions-log-guide.md](transactions-log-guide.md)
- [ytd-totals-guide.md](ytd-totals-guide.md)
- [free-preview.md](free-preview.md)
