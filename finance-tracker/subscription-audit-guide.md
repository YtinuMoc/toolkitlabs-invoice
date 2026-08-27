# Subscription Auto-Renewal Audit Guide

Clone of Quillenhart qaduu **bills tab** + [agentchip/52g8](https://dev.to/agentchip/how-small-businesses-lose-real-money-to-auto-renewals-and-the-spreadsheet-that-stops-it-52g8) buyer channel: track **cancellation deadlines**, not renewal dates.

## The trap

Calendar reminders ping on renewal day. Contracts with 30-day notice clauses require action **before** renewal — so a "Sept 1 renewal" reminder on Sept 1 is too late.

## One row per contract

| Contract | Vendor | Monthly $ | Term | Auto-renew | Renewal date | Cancel by | Status |
|----------|--------|-----------|------|------------|--------------|-----------|--------|
| CNT-001 | Zoho | 12.00 | 12mo | yes | 2026-09-01 | 2026-08-02 | renew now |

Use `subscriptions-sample.csv` in this kit. The CLI computes status:

- **EXPIRED** — past renewal date
- **RENEW NOW** — inside cancellation window
- **Renew soon** — within 30 days of cancel-by
- **Active** — safe for now

## Monthly ritual (10 minutes)

1. Export or update `subscriptions-sample.csv` when you add/cancel SaaS
2. Run `monthly_dashboard.py` with bills + subscriptions paths
3. Act on any **RENEW NOW** or **Renew soon** rows before auto-renew locks you in

Free sample: [subscriptions-sample.csv](subscriptions-sample.csv) · [bills guide](bills-guide.md)
