#!/usr/bin/env python3
"""Freelancer Income Tracker — clone of PattyBun dcklyf ($14.99 Gumroad)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime, timedelta

# Settings tab defaults (PattyBun Settings tab shape)
FEDERAL_RATE = 0.22
STATE_RATE = 0.05
SE_TAX_RATE = 0.153
SE_TAXABLE_RATIO = 0.9235
IRS_MILEAGE_RATE = 0.67

SCHEDULE_C_CATEGORIES = (
    "advertising", "contract_labor", "insurance", "legal_professional",
    "office_expense", "rent_lease", "supplies", "travel", "meals",
    "utilities", "software", "education", "other",
)


def load_income(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                gross = float(row["amount"])
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            rows.append({
                "date": dt,
                "client": row.get("client", "unknown").strip() or "unknown",
                "amount": gross,
                "method": row.get("payment_method", "transfer").strip(),
            })
    return rows


def load_expenses(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = float(row["amount"])
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            cat = row.get("category", "other").strip().lower() or "other"
            rows.append({"date": dt, "category": cat, "amount": amt, "vendor": row.get("vendor", "")})
    return rows


def load_mileage(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                miles = float(row["miles"])
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            rows.append({"date": dt, "miles": miles, "purpose": row.get("purpose", "")})
    return rows


def load_invoices(path):
    rows = []
    today = datetime.now().date()
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = float(row["amount"])
                due = datetime.strptime(row["due_date"].strip(), "%Y-%m-%d").date()
                sent = datetime.strptime(row["sent_date"].strip(), "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            paid = row.get("paid", "").strip().lower() in ("yes", "true", "1", "paid")
            overdue = not paid and due < today
            rows.append({
                "client": row.get("client", "unknown").strip(),
                "amount": amt,
                "sent_date": sent,
                "due_date": due,
                "paid": paid,
                "overdue": overdue,
            })
    return rows


def quarter_key(dt):
    return f"{dt.year}-Q{(dt.month - 1) // 3 + 1}"


def print_live_dashboard(income, expenses, mileage):
    gross = sum(r["amount"] for r in income)
    expense_total = sum(r["amount"] for r in expenses)
    mileage_deduction = sum(r["miles"] for r in mileage) * IRS_MILEAGE_RATE
    net_profit = gross - expense_total - mileage_deduction
    se_tax = max(0, net_profit * SE_TAXABLE_RATIO * SE_TAX_RATE)
    income_tax = max(0, net_profit * (FEDERAL_RATE + STATE_RATE))
    take_home = net_profit - se_tax - income_tax
    print("\n=== LIVE PROFIT DASHBOARD (PattyBun dcklyf clone) ===")
    print(f"  Gross income:        ${gross:,.2f}")
    print(f"  Expenses:            ${expense_total:,.2f}")
    print(f"  Mileage deduction:   ${mileage_deduction:,.2f} ({sum(r['miles'] for r in mileage):.0f} mi × ${IRS_MILEAGE_RATE})")
    print(f"  Net profit:          ${net_profit:,.2f}")
    print(f"  SE tax est (15.3%):  ${se_tax:,.2f}")
    print(f"  Income tax est:      ${income_tax:,.2f} (fed {FEDERAL_RATE*100:.0f}% + state {STATE_RATE*100:.0f}%)")
    print(f"  REAL TAKE-HOME:      ${take_home:,.2f}")


def print_quarterly_estimator(income, expenses, mileage):
    by_q = defaultdict(lambda: {"income": 0.0, "expense": 0.0, "mileage": 0.0})
    for r in income:
        by_q[quarter_key(r["date"])]["income"] += r["amount"]
    for r in expenses:
        by_q[quarter_key(r["date"])]["expense"] += r["amount"]
    for r in mileage:
        by_q[quarter_key(r["date"])]["mileage"] += r["miles"] * IRS_MILEAGE_RATE
    print("\n=== QUARTERLY TAX ESTIMATOR ===")
    print(f"  {'Quarter':<10} {'net profit':>12} {'SE tax':>10} {'income tax':>12} {'set aside':>12}")
    for q in sorted(by_q):
        d = by_q[q]
        net = d["income"] - d["expense"] - d["mileage"]
        se = max(0, net * SE_TAXABLE_RATIO * SE_TAX_RATE)
        inc = max(0, net * (FEDERAL_RATE + STATE_RATE))
        print(f"  {q:<10} ${net:>10,.2f} ${se:>8,.2f} ${inc:>10,.2f} ${se + inc:>10,.2f}")


def print_expense_breakdown(expenses):
    by_cat = defaultdict(float)
    for r in expenses:
        by_cat[r["category"]] += r["amount"]
    print("\n=== EXPENSE LOG (Schedule C categories) ===")
    for cat in sorted(by_cat, key=by_cat.get, reverse=True):
        print(f"  {cat:<22} ${by_cat[cat]:>10,.2f}")
    print(f"  {'TOTAL':<22} ${sum(by_cat.values()):>10,.2f}")


def print_mileage(mileage):
    total_miles = sum(r["miles"] for r in mileage)
    deduction = total_miles * IRS_MILEAGE_RATE
    print("\n=== MILEAGE TRACKER ===")
    print(f"  Total miles: {total_miles:.1f}")
    print(f"  IRS rate:    ${IRS_MILEAGE_RATE}/mi")
    print(f"  Deduction:   ${deduction:,.2f}")
    for r in mileage[:5]:
        print(f"  {r['date'].strftime('%Y-%m-%d')}  {r['miles']:>6.1f} mi  {r['purpose']}")


def print_invoices(invoices):
    print("\n=== CLIENT & INVOICE TRACKER ===")
    by_client = defaultdict(float)
    for inv in invoices:
        status = "PAID" if inv["paid"] else ("OVERDUE" if inv["overdue"] else "pending")
        flag = " *** OVERDUE ***" if inv["overdue"] else ""
        print(f"  {inv['client']:<20} ${inv['amount']:>8,.2f}  due {inv['due_date']}  [{status}]{flag}")
        if inv["paid"]:
            by_client[inv["client"]] += inv["amount"]
    print("\n  Top clients (paid):")
    for i, (client, amt) in enumerate(sorted(by_client.items(), key=lambda x: -x[1])[:5], 1):
        print(f"    #{i} {client:<18} ${amt:>10,.2f}")


def print_monthly_breakdown(income, expenses, mileage):
    by_month = defaultdict(lambda: {"income": 0.0, "expense": 0.0, "mileage": 0.0})
    for r in income:
        k = r["date"].strftime("%Y-%m")
        by_month[k]["income"] += r["amount"]
    for r in expenses:
        k = r["date"].strftime("%Y-%m")
        by_month[k]["expense"] += r["amount"]
    for r in mileage:
        k = r["date"].strftime("%Y-%m")
        by_month[k]["mileage"] += r["miles"] * IRS_MILEAGE_RATE
    print("\n=== MONTHLY BREAKDOWN (12-month profit view) ===")
    for m in sorted(by_month)[-12:]:
        d = by_month[m]
        net = d["income"] - d["expense"] - d["mileage"]
        bar = "#" * max(1, int(net / 200))
        print(f"  {m}  income ${d['income']:>8,.2f}  net ${net:>8,.2f}  {bar}")


def print_tax_reference():
    print("\n=== PLAIN-LANGUAGE TAX REFERENCE ===")
    print("  • Gross income = all 1099 payments before expenses")
    print("  • Net profit = gross − business expenses − mileage deduction")
    print(f"  • SE tax = 15.3% × 92.35% of net profit (self-employed)")
    print(f"  • Income tax reserve = federal + state rates on net profit")
    print("  • Quarterly payments: set aside SE + income tax each quarter")
    print("  • This is a planning tool — consult a CPA for filing.")


def main():
    if len(sys.argv) < 2:
        print("Usage: freelancer_dashboard.py <income.csv> [expenses.csv] [mileage.csv] [invoices.csv]")
        sys.exit(1)
    income = load_income(sys.argv[1])
    expenses = load_expenses(sys.argv[2]) if len(sys.argv) > 2 else []
    mileage = load_mileage(sys.argv[3]) if len(sys.argv) > 3 else []
    invoices = load_invoices(sys.argv[4]) if len(sys.argv) > 4 else []
    print_live_dashboard(income, expenses, mileage)
    print_quarterly_estimator(income, expenses, mileage)
    print_expense_breakdown(expenses) if expenses else None
    print_mileage(mileage) if mileage else None
    print_invoices(invoices) if invoices else None
    print_monthly_breakdown(income, expenses, mileage)
    print_tax_reference()


if __name__ == "__main__":
    main()
