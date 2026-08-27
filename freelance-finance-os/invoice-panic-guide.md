# Invoice tracker without end-of-month panic

Clone of tool #1 in [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os). Buyer-channel shape: [faisalmq/43dl](https://dev.to/faisalmq/freelance-finance-tracker-google-sheets-43dl).

## The panic

You finish a project, send the invoice, and see the deposit hit. For five minutes you feel successful. Then:

- Did that other client ever pay?
- Which invoices are overdue?
- How much is actually collected vs still outstanding?

Checking your bank balance is reactive. You need a **status log** — draft / sent / paid / cancelled — with overdue flags.

## Five-minute habit

1. Log every invoice when you send it (status = `sent`, due date set).
2. Mark `paid` when the deposit lands.
3. Run the dashboard weekly — overdue rows flag automatically.

```csv
date,client,description,amount,status,due_date
2026-01-05,Acme Corp,Website redesign,2500.00,paid,2026-01-20
2026-01-18,Beta LLC,Retainer,1200.00,sent,2026-02-01
2026-01-22,Gamma Inc,Audit,800.00,sent,2026-01-25
```

```bash
python3 freelance_finance_os.py invoice-log-sample.csv expense-log-sample.csv
```

Overdue `sent` invoices with past due dates print in the overdue block.

Full bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) — invoice tracker + tax buffer + rate calculator + quarterly estimator.
