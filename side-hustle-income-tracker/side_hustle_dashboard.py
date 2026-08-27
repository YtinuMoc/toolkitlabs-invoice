#!/usr/bin/env python3
"""Side Hustle Income + Expense Tracker — clone of PattyBun tdmuz ($9.99 Gumroad)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime

FEDERAL_RATE = 0.22
STATE_RATE = 0.05
SE_TAX_RATE = 0.153
SE_TAXABLE_RATIO = 0.9235
MAX_HUSTLES = 8

EXPENSE_CATEGORIES = (
    "supplies", "software", "marketing", "mileage", "fees",
    "equipment", "education", "meals", "other",
)


def load_income(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = float(row["amount"])
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            hustle = row.get("hustle", "hustle_1").strip() or "hustle_1"
            rows.append({
                "date": dt,
                "hustle": hustle,
                "source": row.get("source", "").strip(),
                "amount": amt,
                "category": row.get("category", "income").strip(),
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
            hustle = row.get("hustle", "shared").strip() or "shared"
            rows.append({
                "date": dt,
                "hustle": hustle,
                "category": row.get("category", "other").strip().lower(),
                "amount": amt,
                "vendor": row.get("vendor", "").strip(),
            })
    return rows


def quarter_key(dt):
    return f"{dt.year}-Q{(dt.month - 1) // 3 + 1}"


def month_key(dt):
    return dt.strftime("%Y-%m")


def print_dashboard(income, expenses):
    gross = sum(r["amount"] for r in income)
    expense_total = sum(r["amount"] for r in expenses)
    net = gross - expense_total
    se_tax = max(0, net * SE_TAXABLE_RATIO * SE_TAX_RATE)
    income_tax = max(0, net * (FEDERAL_RATE + STATE_RATE))
    tax_est = se_tax + income_tax
    by_hustle = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    for r in income:
        by_hustle[r["hustle"]]["income"] += r["amount"]
    for r in expenses:
        if r["hustle"] != "shared":
            by_hustle[r["hustle"]]["expense"] += r["amount"]
        else:
            for h in by_hustle:
                by_hustle[h]["expense"] += r["amount"] / max(len(by_hustle), 1)
    best = max(by_hustle, key=lambda h: by_hustle[h]["income"] - by_hustle[h]["expense"]) if by_hustle else "n/a"
    this_month = datetime.now().strftime("%Y-%m")
    month_net = sum(r["amount"] for r in income if month_key(r["date"]) == this_month)
    month_net -= sum(r["amount"] for r in expenses if month_key(r["date"]) == this_month)
    print("\n=== DASHBOARD (PattyBun tdmuz clone) ===")
    print(f"  Hustles tracked:   {min(len(by_hustle), MAX_HUSTLES)}")
    print(f"  YTD gross income:    ${gross:,.2f}")
    print(f"  YTD expenses:        ${expense_total:,.2f}")
    print(f"  YTD net:             ${net:,.2f}")
    print(f"  This month net:      ${month_net:,.2f}")
    print(f"  Best performer:      {best} (${by_hustle[best]['income'] - by_hustle[best]['expense']:,.2f} net)")
    print(f"  Tax estimate (YTD):  ${tax_est:,.2f}")


def print_hustle_tabs(income, expenses):
    by_hustle = defaultdict(lambda: {"income": 0.0, "expense": 0.0, "rows": 0})
    for r in income:
        by_hustle[r["hustle"]]["income"] += r["amount"]
        by_hustle[r["hustle"]]["rows"] += 1
    for r in expenses:
        by_hustle[r["hustle"]]["expense"] += r["amount"]
    print("\n=== HUSTLE TRACKER (8 tabs — PattyBun tdmuz clone) ===")
    print(f"  {'Hustle':<18} {'income':>10} {'expense':>10} {'net':>10} {'rows':>6}")
    ranked = sorted(by_hustle.items(), key=lambda x: x[1]["income"] - x[1]["expense"], reverse=True)
    for i, (name, d) in enumerate(ranked[:MAX_HUSTLES], 1):
        net = d["income"] - d["expense"]
        print(f"  {name:<18} ${d['income']:>8,.2f} ${d['expense']:>8,.2f} ${net:>8,.2f} {d['rows']:>6}")


def print_break_even(monthly_costs=420.0, target_net=1500.0, per_unit_profit=18.50):
    """PattyBun tab 3 — sales/gigs needed to hit target take-home."""
    needed = monthly_costs + target_net
    units = needed / per_unit_profit if per_unit_profit else 0
    print("\n=== BREAK-EVEN CALCULATOR (PattyBun tdmuz clone) ===")
    print(f"  Monthly fixed costs:     ${monthly_costs:,.2f}")
    print(f"  Target take-home:        ${target_net:,.2f}")
    print(f"  Net profit per sale/gig: ${per_unit_profit:,.2f}")
    print(f"  Sales/gigs needed/mo:    {units:,.0f}")
    print(f"  Weekly pace:             {units / 4.33:,.1f}")


def print_quarterly_tax(income, expenses):
    by_q = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    for r in income:
        by_q[quarter_key(r["date"])]["income"] += r["amount"]
    for r in expenses:
        by_q[quarter_key(r["date"])]["expense"] += r["amount"]
    print("\n=== QUARTERLY TAX PLANNER (PattyBun tdmuz clone) ===")
    print(f"  {'Quarter':<10} {'net':>10} {'owed est':>12} {'status':>10}")
    for q in sorted(by_q):
        net = by_q[q]["income"] - by_q[q]["expense"]
        se = max(0, net * SE_TAXABLE_RATIO * SE_TAX_RATE)
        inc = max(0, net * (FEDERAL_RATE + STATE_RATE))
        owed = se + inc
        print(f"  {q:<10} ${net:>8,.2f} ${owed:>10,.2f} {'due':>10}")


def print_expense_breakdown(expenses):
    by_cat = defaultdict(float)
    for r in expenses:
        by_cat[r["category"]] += r["amount"]
    print("\n=== EXPENSE LOG ===")
    for cat in sorted(by_cat, key=by_cat.get, reverse=True):
        print(f"  {cat:<18} ${by_cat[cat]:>10,.2f}")
    print(f"  {'TOTAL':<18} ${sum(by_cat.values()):>10,.2f}")


def main():
    if len(sys.argv) < 2:
        print("Usage: side_hustle_dashboard.py <income.csv> [expenses.csv]")
        sys.exit(1)
    income = load_income(sys.argv[1])
    expenses = load_expenses(sys.argv[2]) if len(sys.argv) > 2 else []
    print_dashboard(income, expenses)
    print_hustle_tabs(income, expenses)
    print_break_even()
    print_quarterly_tax(income, expenses)
    if expenses:
        print_expense_breakdown(expenses)


if __name__ == "__main__":
    main()
