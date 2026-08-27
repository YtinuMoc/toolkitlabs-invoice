# Start here — Freelancer Invoice & Client Tracker

Clone of AgentChip [qiliang.gumroad.com/l/ahefab](https://qiliang.gumroad.com/l/ahefab) ($15).

## 1. Copy templates

```bash
cp clients-template.csv clients.csv
cp invoices-template.csv invoices.csv
cp payments-template.csv payments.csv
```

## 2. Fill clients

One row per client. Set `payment_terms_days` (default 30) and `hourly_rate`.

## 3. Log invoices

Each row = one invoice. Status: `pending`, `sent`, `paid`, or leave blank for auto-overdue detection.

## 4. Log payments

Each row links to `invoice_id`. Partial payments supported — CLI sums by invoice.

## 5. Run dashboard

```bash
python3 freelancer_invoice_tracker.py clients.csv invoices.csv payments.csv
```

Overdue invoices flag automatically when `due_date` is past and balance remains.

## Import to Google Sheets

File → Import → Upload each CSV into its own tab. Use `=TODAY()` and conditional formatting for red overdue rows — same workflow as the original Excel workbook.
