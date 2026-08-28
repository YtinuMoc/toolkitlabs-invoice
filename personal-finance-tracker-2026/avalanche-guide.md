# Debt avalanche guide — highest APR first

Clone buyer-channel shape: [aissam_baidi/46bl Free Debt Avalanche Google Sheets Template (2026)](https://dev.to/aissam_baidi_2934207fc2c3/free-debt-avalanche-google-sheets-template-2026-46bl).

## Why avalanche

The debt avalanche orders accounts **highest APR first**. You pay minimums on everything, then throw all extra cash at the highest-rate balance until it clears. When that card hits zero, roll its payment into the next-highest APR.

Avalanche mathematically minimizes total interest. On realistic 3–6 card scenarios with mixed APRs, savings versus snowball are often **$150–$700** — sometimes more when APR spreads exceed 10 percentage points.

The tradeoff: the first payoff is often slower than snowball because the highest-APR card is rarely the smallest balance. Completion rates run slightly lower per Kellogg research. Use avalanche when discipline is strong and APRs differ meaningfully.

## How it works in this tracker

1. List every debt in `debts-template.csv` with balance, APR, and minimum payment.
2. Add any extra monthly payment pool (applied to the highest-APR card first).
3. Run the CLI — debts sort highest-APR-first automatically.
4. When a card clears, roll its payment into the next-highest APR.

## Free CLI preview

```bash
python3 personal_finance_tracker_2026.py --avalanche debts-sample.csv
```

Sample output:

```plaintext
=== DEBT AVALANCHE (aissam_baidi/46bl shape) ===
  #1 Store Card          bal    $890.00  APR 26.99%  pay  $185.00/mo  ~5 mo
  #2 Chase Visa          bal  $4,200.00  APR 22.99%  pay  $320.00/mo  ~16 mo
  #3 Capital One         bal  $1,800.00  APR 19.99%  pay  $135.00/mo  ~14 mo
```

## Snowball vs avalanche

| Method | Order | Best for |
|--------|-------|----------|
| Snowball | Smallest balance first | Motivation, quick wins, first-time payoff |
| Avalanche | Highest APR first | Minimizing interest, disciplined payers |

ohmygoshna's **2026 Personal Finance Tracker** defaults to snowball psychology in the Gumroad listing. This guide clones the separate [aissam_baidi/46bl](https://dev.to/aissam_baidi_2934207fc2c3/free-debt-avalanche-google-sheets-template-2026-46bl) buyer channel for users who want the math-first path.

## Pair with

- [debt-snowball-guide.md](debt-snowball-guide.md) — aissam_baidi/37m7 buyer channel (run287)
- [tax-buffer-guide.md](tax-buffer-guide.md) — faisalmq/4gao deposit-day transfers (run288)
- [net-income-guide.md](net-income-guide.md) — faisalmq/5797 safe-to-spend (run289)
- [start-here.md](start-here.md) — full income, expense, debt, savings setup

Full bundle: [2026 Personal Finance Tracker landing](https://ytinumoc.github.io/toolkitlabs-invoice/personal-finance-tracker-2026/) — income + expense + debt + savings + account CSVs, snowball + avalanche CLI, tax buffer, and net-income module.
