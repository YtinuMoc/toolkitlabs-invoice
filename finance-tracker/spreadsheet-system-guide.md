# Spreadsheet System Guide — From Principles to Behavioral Code

Clone of Quillenhart qaduu **transaction log + setup** shape, using the buyer-channel narrative from [crazychief's book-to-spreadsheet-to-system post](https://dev.to/crazychief/from-book-to-spreadsheet-to-system-turning-financial-principles-into-behavioral-code-52ge): principles without execution are specs; build the vessel first.

## The gap between knowing and doing

You can read every finance principle — fixed allocations, tax set-aside, category discipline — and still make no progress. Reading is ingestion. A **transaction log you actually fill** is digestion.

[crazychief's sequence](https://dev.to/crazychief/from-book-to-spreadsheet-to-system-turning-financial-principles-into-behavioral-code-52ge):

1. **Decompose** — not "save more" but "this container gets 25% of net on every dashboard run"
2. **Prototype** — one CSV, five columns, a Python script that runs without you
3. **Harden** — log long enough that the behavior becomes automatic
4. **Reapply** — same pattern for bills, debt, invoices, savings tabs

Quillenhart's [$15 Gumroad tracker](https://quillenhart.gumroad.com/l/qaduu) (**7 ratings**) is the hardened vessel: log once on the master sheet → every tab (dashboard, bills, debt, tax) is a view.

## Three containers (fixed rules)

| Container | What it holds | Fixed rule |
|-----------|---------------|------------|
| Income | Client payments, product sales | Log when cleared |
| Expenses | Software, hosting, contractors | Log when charged |
| Reserved | Tax set-aside | `setup-guide.md` % × net profit |

A system you override every week is a suggestion. Encode the rule in `setup-guide.md` and let `monthly_dashboard.py` apply it.

## 5-minute prototype

1. Copy `transaction-log-template.csv` → `my-transactions.csv`
2. Fill `setup-guide.md` — business name, tax year, set-aside %
3. Add this month's rows (date, type, category, amount, description)
4. Run: `python3 monthly_dashboard.py my-transactions.csv`
5. Look for `SPREADSHEET SYSTEM (crazychief/52ge shape)` in stdout

## Free CLI

```bash
python3 monthly_dashboard.py sample-transactions.csv
```

The script reports transaction count, months covered, three-container totals, and whether your log is still **PROTOTYPE** or **HARDENED** (enough rows across enough months).

## Who it's for

- Developers who highlight finance books but never ship the spreadsheet
- Freelancers who need principles → execution, not another subscription dashboard
- Anyone cloning Quillenhart's master log without QuickBooks at $30/mo

Full EUR 9 kit: all nine Quillenhart tabs as CSV + Python modules.
