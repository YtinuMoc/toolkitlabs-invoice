# Start here — AI-Powered Invoice Tracker

Clone of Productive Club [productiveclub.gumroad.com/l/gnohas](https://productiveclub.gumroad.com/l/gnohas) ($19+).

## 1. Copy templates

```bash
cp clients-template.csv clients.csv
cp invoices-template.csv invoices.csv
cp payments-template.csv payments.csv
```

## 2. Fill clients

One row per client. Set `payment_terms_days` (default 30).

## 3. Log invoices

Each row = one invoice. Status: `pending`, `sent`, `paid`, or leave blank for auto-overdue detection.

## 4. Log payments

Each row links to `invoice_id`. Partial payments supported — CLI sums by invoice.

## 5. Run dashboard

```bash
python3 productiveclub_invoice_tracker.py clients.csv invoices.csv payments.csv
```

## 6. Preview follow-up cadence

```bash
python3 productiveclub_invoice_tracker.py --follow-up invoices.csv payments.csv
```

Overdue invoices flag automatically when `due_date` is past and balance remains.
