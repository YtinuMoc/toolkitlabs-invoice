# Freelancer Financial Command Center — 5-template stack

Clone of [timmothybuilder/4e81](https://dev.to/timmothybuilder/5-spreadsheet-templates-every-freelancer-needs-free-downloads-4e81) buyer channel + Quillenhart qaduu **9-tab system**.

Tools don't make you organized. Systems do. These five templates map to modules in our kit (and Quillenhart's $15 Gumroad tracker):

| # | Template | What it fixes | Our module |
|---|----------|---------------|------------|
| 1 | Personal finance tracker | Business vs personal blur | [transaction log](transaction-log-template.csv) + [savings goals](savings-goals-guide.md) |
| 2 | Client / proposal tracker | Forgotten follow-ups | [invoices receivable](invoices-guide.md) |
| 3 | Content calendar | Random posting | (outside kit — use your own calendar) |
| 4 | Daily productivity dashboard | No daily priorities | [monthly dashboard](dashboard-guide.md) month picker |
| 5 | **Financial command center** | Everything scattered | **Full 9-tab system** below |

## The command center (template #5)

Quillenhart ships one file with nine tabs. Our clone uses CSV + Python:

1. **Read Me** — [readme-guide.md](readme-guide.md)
2. **Setup** — [setup-guide.md](setup-guide.md)
3. **Transactions** — master log (150+ rows) — [transactions-log-guide.md](transactions-log-guide.md)
4. **Bills** — [bills-guide.md](bills-tracker.md)
5. **Savings** — [savings-goals-guide.md](savings-tracker.md)
6. **Debt** — [debt-guide.md](debt-tracker.md)
7. **Invoices** — [invoices-guide.md](invoices-tracker.md)
8. **Dashboard** — [dashboard-guide.md](dashboard-guide.md)
9. **Annual Summary** — [annual-summary.md](annual-summary.md) + [annual chart](annual-chart-guide.md)

## Run the command center preview

```bash
python3 monthly_dashboard.py sample-transactions.csv invoices-sample.csv bills-sample.csv debt-sample.csv savings-sample.csv
```

Read the **FREELANCER FINANCIAL COMMAND CENTER** block in stdout — it lists which modules are active and uncollected invoice totals.

## timmothybuilder/4e81 lesson

1. Pick a template
2. Use it for 2 weeks
3. Customize to your workflow
4. Never go back to chaos

Template #5 pays for itself when you find overdue invoices you forgot — run the invoices module monthly.
