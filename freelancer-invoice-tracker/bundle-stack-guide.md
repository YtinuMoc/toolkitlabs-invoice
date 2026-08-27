# Freelancer finance stack — stop buying three spreadsheets separately (agentchip/2dgn shape)

Clone of [AgentChip's Freelancer Invoice & Client Tracker ($15)](https://qiliang.gumroad.com/l/ahefab) + [agentchip/2dgn](https://dev.to/agentchip/i-turned-22-solopreneur-tools-into-one-199-bundle-and-why-you-shouldnt-buy-them-separately-2dgn) buyer channel: separate tools priced individually → one connected workbook → stack upsell.

## The duct-tape problem

Freelancers buy one template for invoicing, another for SaaS renewal audits, another for cash runway — then type the same client name into three files.

[agentchip/2dgn](https://dev.to/agentchip/i-turned-22-solopreneur-tools-into-one-199-bundle-and-why-you-shouldnt-buy-them-separately-2dgn) frames the fix: **one stack, one price, zero dashboard sprawl.**

## What's in this kit (vs buying separately)

| Module | Buyer channel | Typical solo price | In this kit |
|--------|---------------|:------------------:|:-----------:|
| Invoice + overdue flags | [agentchip/2b11](https://dev.to/agentchip/i-fixed-my-freelance-invoicing-with-a-spreadsheet-that-does-the-math-for-me-2b11) | $15 (ahefab) | ✓ |
| Subscription auto-renewal audit | [agentchip/52g8](https://dev.to/agentchip/how-small-businesses-lose-real-money-to-auto-renewals-and-the-spreadsheet-that-stops-it-52g8) | ~$12 standalone | ✓ |
| Cash runway forecast | [agentchip/33mm](https://dev.to/agentchip/your-spreadsheet-cant-tell-you-the-month-youll-run-out-of-cash-this-can-33mm) | ~$12 standalone | ✓ |
| **Stack total (separate)** | — | **~$39** | **EUR 9** |

## CLI stack audit

```bash
python3 freelancer_invoice_tracker.py clients-sample.csv invoices-sample.csv payments-sample.csv subscriptions-sample.csv bills-sample.csv debt-sample.csv
```

Look for the `FREELANCER FINANCE STACK` block — lists every module, separate-price equivalent, and bundle savings.

## Why one workbook beats three tabs

1. **Shared client registry** — invoices, payments, and runway forecast pull from the same CSVs
2. **One CLI run** — overdue flags, subscription audit, and cash-gap alarm in one stdout
3. **Local only** — no SaaS account, no API key, no data leaves your machine

## Paid kit

Full stack: [Freelancer Invoice & Client Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelancer-invoice-tracker/) · EUR 9 one-time · same delivery shape as [AgentChip on Gumroad ($15)](https://qiliang.gumroad.com/l/ahefab).
