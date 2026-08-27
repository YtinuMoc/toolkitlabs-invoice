# Six-Month Reveal Guide — What Tracking Every Dollar Actually Shows

Clone of [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os) + [timmothybuilder/3fb2](https://dev.to/timmothybuilder/i-tracked-every-dollar-for-6-months-as-a-freelance-developer-heres-what-i-learned-3fb2) buyer channel: six months of logging → four surprises → pricing and client decisions → paid kit upsell.

## The four surprises (and what to measure)

| Surprise | What timmothybuilder found | What to log in this kit |
|----------|---------------------------|-------------------------|
| Undercharging | $75/hr billed → $32/hr effective | `client-hours-sample.csv` + paid invoices |
| Subscription creep | 12% of revenue on SaaS | `subscriptions-sample.csv` |
| Quarterly tax shock | Brain says "rich" when deposit lands | 30% tax bucket on every payment |
| Wrong best client | High revenue ≠ high effective rate | Per-client revenue ÷ hours |

[By the Loop on Gumroad](https://bytheloop.gumroad.com/l/freelance-finance-os) ships the hardened vessel: invoice tracker, expense + tax buffer, rate calculator, quarterly tax estimator — the four tools timmothybuilder's post ends up recommending.

## Key numbers every freelancer should know

- **Effective hourly rate** — total paid ÷ total hours (including admin, comms, revisions)
- **Monthly nut** — expenses + tax reserve + fixed bills
- **Cash runway** — savings ÷ monthly nut
- **Client concentration risk** — % of revenue from top client

## 5-minute weekly habit

1. Log every payment in `invoice-log-template.csv`
2. Log hours per client in `client-hours-template.csv`
3. Run the six-month reveal CLI
4. Open `rate-calculator.html` if effective rate is below your billed rate

## Free CLI

```bash
python3 freelance_finance_os.py --six-month-reveal invoice-log-sample.csv expense-log-sample.csv client-hours-sample.csv subscriptions-sample.csv
```

Sample output includes effective hourly rate, subscription load as % of revenue, tax reserve discipline, and per-client profitability scoreboard.

Full OS: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) — EUR 9 one-time via Stripe.
