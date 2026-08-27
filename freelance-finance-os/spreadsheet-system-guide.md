# Spreadsheet System Guide — From Principles to Behavioral Code

Clone of [By the Loop's Freelance Finance OS ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os) + [crazychief/52ge](https://dev.to/crazychief/from-book-to-spreadsheet-to-system-turning-financial-principles-into-behavioral-code-52ge) buyer channel: principles without execution are specs; build the vessel first.

## The gap between knowing and doing

You can read every finance principle — fixed allocations, tax set-aside, invoice discipline — and still make no progress. Reading is ingestion. An **invoice log + expense log you actually fill** is digestion.

[crazychief's sequence](https://dev.to/crazychief/from-book-to-spreadsheet-to-system-turning-financial-principles-into-behavioral-code-52ge):

1. **Decompose** — not "save more" but "reserved container gets 25% of net on every CLI run"
2. **Prototype** — `invoice-log-template.csv` + `expense-log-template.csv` + `freelance_finance_os.py`
3. **Harden** — log long enough that filling the sheet is automatic
4. **Reapply** — same pattern for bills, debt, savings (other By the Loop modules)

[By the Loop on Gumroad](https://bytheloop.gumroad.com/l/freelance-finance-os) ships the hardened vessel: four tools in one bundle — invoice tracker, expense + tax buffer, rate calculator, quarterly tax estimator.

## Three containers (fixed rules)

| Container | What it holds | Fixed rule |
|-----------|---------------|------------|
| Income | Client payments (paid invoices) | Log when cleared |
| Expenses | Software, hosting, contractors | Log when charged |
| Reserved | Tax set-aside | 25% × net profit |

A system you override every week is a suggestion. Encode the rule in the CLI and let `freelance_finance_os.py` apply it.

## 5-minute prototype

1. Copy `invoice-log-template.csv` → `my-invoices.csv`
2. Copy `expense-log-template.csv` → `my-expenses.csv`
3. Add this month's rows
4. Run: `python3 freelance_finance_os.py --spreadsheet-system my-invoices.csv my-expenses.csv`
5. Look for `SPREADSHEET SYSTEM (crazychief/52ge shape)` in stdout

## Free CLI

```bash
python3 freelance_finance_os.py --spreadsheet-system invoice-log-sample.csv expense-log-sample.csv
```

Full OS with all modules wired in:

```bash
python3 freelance_finance_os.py invoice-log-sample.csv expense-log-sample.csv subscriptions-sample.csv bills-sample.csv debt-sample.csv savings-sample.csv
```

Free files: [invoice log sample](invoice-log-sample.csv) · [expense log sample](expense-log-sample.csv)

Full four-tool bundle: [Freelance Finance OS landing](https://ytinumoc.github.io/toolkitlabs-invoice/freelance-finance-os/) · EUR 9 one-time · same delivery shape as [By the Loop on Gumroad ($5)](https://bytheloop.gumroad.com/l/freelance-finance-os).
