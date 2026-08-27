# Expense drag (smadsby ejxcg shape)

Platform fees are only half the story. [SimpleBizDash](https://smadsby.gumroad.com/l/ejxcg) includes an **Expense Log** — ads, software, supplies, refunds — because Pinterest ads you forgot to log still eat profit.

## Run it

```bash
python3 seller_profit_fee_tracker.py sales-sample.csv expense-sample.csv
```

Look for the `EXPENSE DRAG` block:

- Each category as % of gross sales
- Total expenses as % of gross — the number your tax set-aside should use

## Categories

Use `expense-log-template.csv`: `date`, `category`, `amount`, `vendor`.

Common categories: `ads`, `software`, `supplies`, `refunds`, `shipping`, `other`.

## Why it matters

A seller doing $500 gross on Gumroad with $180 in unlogged Meta ads thinks margin is 70%. Real margin after fees **and** ads might be 12%. Expense drag surfaces that before month-end.
