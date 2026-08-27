# Freelancer Financial Command Center — 5-template stack (By the Loop clone)

Clone of [timmothybuilder/4e81](https://dev.to/timmothybuilder/5-spreadsheet-templates-every-freelancer-needs-free-downloads-4e81) buyer channel + [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).

Tools don't make you organized. Systems do. These five templates map to modules in our EUR 9 kit (and By the Loop's $5 Gumroad bundle):

| # | Template | What it fixes | Our module |
|---|----------|---------------|------------|
| 1 | Personal finance tracker | Business vs personal blur | [expense log](expense-log-template.csv) + tax buffer |
| 2 | Client / proposal tracker | Forgotten follow-ups | [invoice log](invoice-log-template.csv) — overdue flags |
| 3 | Content calendar | Random posting | (outside kit — use your own calendar) |
| 4 | Daily productivity dashboard | No weekly money check-in | [rate calculator](rate-calculator.html) + five-minute weekly review |
| 5 | **Financial command center** | Everything scattered | **Full 4-tool bundle** below |

## The command center (template #5)

By the Loop ships four spreadsheets in one download. Our clone uses CSV + Python:

1. **Invoice tracker** — draft / sent / paid / overdue
2. **Expense + tax buffer** — categorized log → net profit → safe-to-spend
3. **Rate calculator** — take-home target → hourly floor (offline HTML)
4. **Quarterly tax estimator** — 1040-ES deadlines prefilled

## Run the command center preview

```bash
python3 freelance_finance_os.py invoice-log-sample.csv expense-log-sample.csv
```

Read the **FREELANCER FINANCIAL COMMAND CENTER** block in stdout — it lists which modules are active and uncollected invoice totals.

## timmothybuilder/4e81 lesson

1. Pick a template
2. Use it for 2 weeks
3. Customize to your workflow
4. Never go back to chaos

Template #5 pays for itself when you find overdue invoices you forgot — run the invoice module monthly.

## Paid kit

Full four-tool bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) · EUR 9 one-time · same delivery shape as [By the Loop on Gumroad ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).
