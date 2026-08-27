# Freelance SaaS trial stack audit — agentchip/4hc1 shape (AgentChip clone)

Clone of [agentchip/4hc1](https://dev.to/agentchip/free-trial-abuse-is-quietly-killing-your-saas-and-one-time-emails-are-only-half-the-problem-4hc1) buyer channel — adapted for **freelancers who stack free trials** during project spikes. Original sells [TrialShield ($49)](https://qiliang.gumroad.com/l/iizek) to SaaS founders blocking disposable-email abuse. Our shape tracks **your** active trials before they silently convert to paid plans.

## The leak for freelancers

During a client sprint you sign up for Figma, Notion, Linear, Miro — all free trials. One-time calendar reminders fail. Trials auto-convert on day 15 while you are on the next project. That is the freelancer-side mirror of "free trial abuse": tools billing you after you stopped using them.

## Three signals (agentchip/4hc1 mental model)

1. **Trial end date** — when the card gets charged if you do nothing
2. **Cancel-by window** — last safe day to cancel (often 2–3 days before trial_end)
3. **Stack load** — total monthly cost if every active trial converts

## One row per trial

| Trial | Tool | Trial end | Cancel by | Post-trial $/mo | Status |
|-------|------|-----------|-----------|-----------------|--------|
| TRIAL-003 | Linear | 2026-08-24 | 2026-08-22 | 8.00 | CANCEL NOW |

Use `trials-sample.csv`. The CLI computes status:

- **CONVERTED** — already moved to paid (migrate to subscriptions.csv)
- **EXPIRED** — past trial end without cancel flag
- **CANCEL NOW** — inside cancel-by window
- **CONVERTING SOON** — within 7 days of trial end
- **ACTIVE TRIAL** — safe for now

## Monthly ritual (5 minutes)

1. Add new tool trials to `trials-sample.csv` when you sign up
2. Run `freelancer_invoice_tracker.py --trial-audit trials-sample.csv`
3. Cancel any **CANCEL NOW** rows before auto-convert

```bash
python3 freelancer_invoice_tracker.py --trial-audit trials-sample.csv
```

Free sample: [trials-sample.csv](trials-sample.csv) · pairs with [subscription audit](subscription-audit-guide.md) after conversion

## Paid kit

Full workbook + all finance modules: [Freelancer Invoice & Client Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelancer-invoice-tracker/) · EUR 9 one-time · same delivery shape as [AgentChip on Gumroad ($15)](https://qiliang.gumroad.com/l/ahefab).

Original trial-abuse article: [agentchip/4hc1](https://dev.to/agentchip/free-trial-abuse-is-quietly-killing-your-saas-and-one-time-emails-are-only-half-the-problem-4hc1) · [TrialShield on Gumroad ($49)](https://qiliang.gumroad.com/l/iizek).
