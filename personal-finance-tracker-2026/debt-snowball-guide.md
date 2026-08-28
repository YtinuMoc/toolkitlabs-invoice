# Debt snowball guide

Clone buyer-channel shape: [aissam_baidi/37m7 Free Debt Snowball Google Sheets Template (2026)](https://dev.to/aissam_baidi_2934207fc2c3/free-debt-snowball-google-sheets-template-2026-37m7).

## Why snowball beats willpower

Over 75% of people who start a debt payoff plan fail to complete it. The snowball method — paying smallest balances first — has higher completion rates than avalanche (highest APR first), per Northwestern Kellogg research.

## How it works in this tracker

1. List every debt in `debts-template.csv` with balance, APR, and minimum payment.
2. Add any extra monthly payment to the smallest debt row.
3. Run the CLI — debts sort smallest-to-largest automatically.
4. When a card clears, roll its payment into the next smallest balance.

## Sample snowball output

```plaintext
--- Debt snowball (smallest balance first) ---
  #1 Store Card          bal    $890.00  APR 26.99%  pay   $85.00/mo  ~11 mo
  #2 Capital One         bal  $1,800.00  APR 19.99%  pay  $130.00/mo  ~16 mo
  #3 Chase Visa          bal  $4,200.00  APR 22.99%  pay  $235.00/mo  ~24 mo
```

## When to switch to avalanche

If your APR spread is 10+ percentage points and you have strong discipline, avalanche may save $200–$800. This tracker defaults to snowball because completion beats optimization for most people.
