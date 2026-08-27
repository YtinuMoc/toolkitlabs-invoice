# Complete freelance finance workbook — CSV + CLI, no Notion (By the Loop clone)

Clone of [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os). Buyer-channel shape: [hemantdev/1iae](https://dev.to/hemantdev/i-built-a-freepaid-finance-gst-tracker-for-indian-freelancers-excel-no-notion-needed-1iae).

## Why a file, not Notion

Notion templates need an account, sync, and block syntax. [hemantdev/1iae](https://dev.to/hemantdev/i-built-a-freepaid-finance-gst-tracker-for-indian-freelancers-excel-no-notion-needed-1iae) sells a **single workbook** that opens offline in Excel or Google Sheets — shaded cells only, everything else calculates. By the Loop ships the same offline shape as four connected CSV logs + Python CLI.

## Six connected views (hemantdev → By the Loop)

| hemantdev sheet | By the Loop tab | Our clone |
|-----------------|-----------------|-----------|
| Dashboard | Invoice + expense summary | CLI stdout — collected, net, safe-to-spend |
| Income | Invoice tracker | `invoice-log-template.csv` |
| Expenses | Expense + tax buffer | `expense-log-template.csv` |
| Clients | Invoice tracker (per-client) | per-client totals in CLI |
| Invoices | Invoice tracker (status) | draft / sent / paid / overdue flags |
| Tax Estimator | Quarterly tax estimator | 1040-ES deadlines in CLI |

## Free CLI preview

```bash
python3 freelance_finance_os.py invoice-log-sample.csv expense-log-sample.csv
```

Look for `COMPLETE WORKBOOK` in stdout — four tools, one log, zero Notion account.

## Paid kit

Full four-tool bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) · EUR 9 one-time · same delivery shape as [By the Loop on Gumroad ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).
