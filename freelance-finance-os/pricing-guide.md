# Freelance pricing floor — price from your numbers

Clone of [datanestdigital/3ma7](https://dev.to/datanestdigital/how-to-price-freelance-work-without-undercharging-3ma7) buyer channel + [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os) rate calculator (tool #3).

[datanestdigital's guide](https://dev.to/datanestdigital/how-to-price-freelance-work-without-undercharging-3ma7) nails the fix: **start from the income and costs you need to cover, not from what feels polite to ask.** Set a floor rate from your numbers, sanity-check against your niche, then quote per project or on value.

## The five inputs

| Input | Example | Why it matters |
|-------|---------|----------------|
| Net income target | $90,000 | What you actually need to keep after tax |
| Tax gross-up divisor | 0.65 | Converts net → gross (≈35% effective load) |
| Annual business expenses | $8,000 | Software, insurance, equipment |
| Margin buffer | 18% | Scope creep, slow months, unpaid admin |
| Billable hours / year | 1,044 | ~20 hrs/wk at 70% billable share |

## CLI floor rate

```bash
python3 freelance_finance_os.py --pricing 90000 0.65 8000 18 1044 0.70
```

## Sample output

```
=== FREELANCE PRICING FLOOR (datanestdigital/3ma7 shape) ===
  Net income target:     $90,000
  Tax gross-up divisor:  0.65 → gross $138,462
  Annual business costs: $8,000
  Margin buffer:         18%
  Target gross revenue:  $172,885
  Billable hours/year:   1,044
  Minimum hourly floor:  $166/hr
  At 70% billable share: $237/hr required
  Daily (8h):            $1,326
  10h project + 25% buffer:$2,075
```

## Offline HTML calculator

Open [rate-calculator.html](rate-calculator.html) in any browser — same math, no account, works offline.

## Connect pricing to your logs

1. Log invoices and expenses in the CSV templates.
2. Run `--dashboard` or `--portable` to see real net profit.
3. If collected rate × hours is below your floor, raise prices — not hours.

## Paid kit

[Freelance Finance OS — EUR 9](https://buy.stripe.com/4gM3cw0qy8XWgbI2tD5Ne0E) — four tools in one bundle (invoice tracker, tax buffer, rate calculator, quarterly estimator). Same architecture as [By the Loop on Gumroad ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).
