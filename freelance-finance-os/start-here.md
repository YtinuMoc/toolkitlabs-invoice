# Start here — Freelance Finance OS (By the Loop clone)

1. Copy `invoice-log-template.csv` → `invoice-log.csv` and log client invoices (status: draft/sent/paid/cancelled).
2. Copy `expense-log-template.csv` → `expense-log.csv` for monthly expenses.
3. Open `rate-calculator.html` in your browser for minimum hourly floor math.
4. Run `python3 freelance_finance_os.py invoice-log.csv expense-log.csv` for dashboard + tax buffer + quarterly estimate.

Tax buffer defaults to **25%** of net profit (edit `TAX_BUFFER_PCT` in the script).

Original: [bytheloop.gumroad.com/l/freelance-finance-os](https://bytheloop.gumroad.com/l/freelance-finance-os) ($5). Toolkit Labs clone: EUR 9 via Stripe.
