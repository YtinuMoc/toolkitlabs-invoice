# Freelance invoicing with overdue flags (agentchip/2b11 shape)

Clone of [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os) + [agentchip/2b11](https://dev.to/agentchip/i-fixed-my-freelance-invoicing-with-a-spreadsheet-that-does-the-math-for-me-2b11) buyer channel: invoicing embarrassment → status log → overdue flags → chase list.

Distinct from [invoice-panic-guide.md](invoice-panic-guide.md) (faisalmq/43dl end-of-month panic shape).

## The invisible cost

Freelancers lose 5–10% of revenue to invoices they forget to chase. Big invoicing SaaS tools charge $12–30/mo for "send a reminder." You need a receivables log that flags overdue rows the moment they're late.

## Five linked views (CSV + CLI)

1. **Clients** — per-client collected totals (from invoice log)
2. **Invoices** — one row per invoice: client, amount, sent date, due date, status
3. **Payments** — mark `paid` when the deposit lands
4. **Overdue** — `sent` rows past due date flag automatically
5. **Dashboard** — paid vs outstanding vs overdue split

## Status values

`draft` · `sent` · `paid` · `cancelled`

Log every invoice as `sent` when you email it. Flip to `paid` when money hits. Overdue flags appear on `sent` rows with past `due_date`.

## Worked example

```csv
date,client,description,amount,status,due_date
2026-01-05,Acme Corp,Website redesign,2500.00,paid,2026-01-20
2026-01-18,Beta LLC,Retainer,1200.00,sent,2026-02-01
2026-01-22,Gamma Inc,Audit,800.00,sent,2026-01-25
```

- **Outstanding:** $2,000 (sent rows)
- **Overdue:** 1 invoice · $800 — chase before writing it off mentally

## CLI check

```bash
python3 freelance_finance_os.py invoice-log-sample.csv expense-log-sample.csv
```

Look for the `ACCOUNTS RECEIVABLE (agentchip/2b11 shape)` block in stdout.

## When to run it

- **Weekly** — scan overdue flags before they become write-offs
- **Before month-end** — know exactly what's still outstanding
- **After sending invoices** — log status immediately, not when you remember

## Paid kit

Full four-tool bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) · EUR 9 one-time · same delivery shape as [By the Loop on Gumroad ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).
