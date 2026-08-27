# Hustle settings — PattyBun Settings tab clone

Default tax rates (edit in `side_hustle_dashboard.py` if your bracket differs):

| Setting | Default |
|---------|---------|
| Federal income tax | 22% |
| State income tax | 5% |
| Self-employment tax | 15.3% × 92.35% of net |

## Income categories (PattyBun shape)

`product_sales`, `freelance`, `gig`, `affiliate`, `rental`, `other`

## Expense categories

`supplies`, `software`, `marketing`, `mileage`, `fees`, `equipment`, `education`, `meals`, `other`

## Break-even defaults

Monthly fixed costs $420 · target take-home $1,500 · net per sale/gig $18.50 — edit in CLI or override when calling `print_break_even()`.
