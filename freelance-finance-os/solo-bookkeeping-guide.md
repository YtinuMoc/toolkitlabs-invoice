# Solo bookkeeping in 90 minutes — category breakdown (By the Loop clone)

Clone of [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os). Buyer-channel shape: [raxxostudios/5a8i](https://dev.to/raxxostudios/solo-studio-bookkeeping-in-90-minutes-a-month-my-stack-and-routine-5a8i).

## The 12 starter categories

| Category | What goes here |
|----------|----------------|
| `software` | SaaS, hosting, domains |
| `marketing` | Ads, SEO tools |
| `contractor` | VA, outsourced dev |
| `platform_fee` | Gumroad/Stripe fees |
| `office` | Coworking, utilities |
| `equipment` | Monitor, peripherals |
| `education` | Courses, books |
| `travel` | Client trips |
| `meals` | Client lunches |
| `fees` | Bank charges |
| `taxes` | Quarterly payments |
| `other` | Catch-all (keep small) |

[raxxostudios/5a8i](https://dev.to/raxxostudios/solo-studio-bookkeeping-in-90-minutes-a-month-my-stack-and-routine-5a8i): *"Twelve is the sweet spot. Fewer and the P&L is useless."*

By the Loop's expense tab maps to the same workflow: log once in `expense-log.csv`, run CLI, read **CATEGORY BREAKDOWN BY MONTH**.

## Monthly close (90 minutes → 60 with a file)

1. **Reconcile** — every bank line has a receipt
2. **Categorize** — consistent tags from the same list
3. **P&L snapshot** — money in, expenses by category, net profit
4. **Year-end handoff** — YTD category totals to your tax advisor

## Free CLI preview

```bash
python3 freelance_finance_os.py invoice-log-sample.csv expense-log-sample.csv
```

Look for `CATEGORY BREAKDOWN BY MONTH` in stdout — per-month expense % and YTD rollup.

## Paid kit

Full four-tool bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) · EUR 9 one-time · same delivery shape as [By the Loop on Gumroad ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).
