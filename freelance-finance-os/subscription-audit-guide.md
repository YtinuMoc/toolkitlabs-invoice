# Freelance SaaS subscription audit — agentchip/52g8 shape (By the Loop clone)

Clone of [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os) expense tab + [agentchip/52g8](https://dev.to/agentchip/how-small-businesses-lose-real-money-to-auto-renewals-and-the-spreadsheet-that-stops-it-52g8) buyer channel: track **cancellation deadlines**, not renewal dates.

## The trap for freelancers

You signed up for Adobe, Canva, a domain, and a CRM during a client project. Calendar reminders ping on renewal day. Contracts with 30-day notice require action **before** renewal — so a "Sept 1 renewal" reminder on Sept 1 is too late.

## One row per subscription

| Contract | Vendor | Monthly $ | Auto-renew | Renewal date | Cancel by | Status |
|----------|--------|-----------|------------|--------------|-----------|--------|
| SUB-001 | Adobe CC | 54.99 | yes | 2026-09-15 | 2026-09-01 | renew now |

Use `subscriptions-sample.csv` in this kit. The CLI computes status:

- **EXPIRED** — past renewal date
- **RENEW NOW** — inside cancellation window
- **Renew soon** — within 30 days of cancel-by
- **Active** — safe for now

## Monthly ritual (10 minutes)

1. Update `subscriptions-sample.csv` when you add/cancel freelance SaaS
2. Run `freelance_finance_os.py` with invoice + expense + subscriptions paths
3. Act on any **RENEW NOW** rows before auto-renew locks you in

Free sample: [subscriptions-sample.csv](subscriptions-sample.csv) · [expense log template](expense-log-template.csv)

## Paid kit

Full four-tool bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) · EUR 9 one-time · same delivery shape as [By the Loop on Gumroad ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).
