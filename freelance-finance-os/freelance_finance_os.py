#!/usr/bin/env python3
"""Freelance Finance OS — clone of By the Loop freelance-finance-os ($5 Gumroad)."""
import csv
import sys
from collections import defaultdict
from datetime import date, datetime

TAX_BUFFER_PCT = 25.0
ESTIMATED_TAX_PCT = 28.0  # planning default; not tax advice

QUARTERLY_DEADLINES = (
    ("Q1", "Apr 15", "Jan–Mar income"),
    ("Q2", "Jun 15", "Apr–May income"),
    ("Q3", "Sep 15", "Jun–Aug income"),
    ("Q4", "Jan 15 next year", "Sep–Dec income"),
)


def load_invoices(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = float(row["amount"])
            except (KeyError, ValueError):
                continue
            status = row.get("status", "draft").strip().lower()
            due = row.get("due_date", "").strip()
            overdue = False
            if status == "sent" and due:
                try:
                    overdue = datetime.strptime(due, "%Y-%m-%d").date() < date.today()
                except ValueError:
                    pass
            rows.append({
                "client": row.get("client", "unknown").strip() or "unknown",
                "amount": amt,
                "status": status,
                "overdue": overdue,
            })
    return rows


def load_expenses(path):
    total = 0.0
    by_cat = defaultdict(float)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = abs(float(row["amount"]))
            except (KeyError, ValueError):
                continue
            cat = row.get("category", "other").strip().lower() or "other"
            by_cat[cat] += amt
            total += amt
    return total, dict(by_cat)


def load_expense_rows(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = abs(float(row["amount"]))
            except (KeyError, ValueError):
                continue
            date_str = row.get("date", "").strip()
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                continue
            cat = row.get("category", "other").strip().lower() or "other"
            rows.append({"date": dt, "category": cat, "amount": amt})
    return rows


def print_category_breakdown(rows):
    """raxxostudios/5a8i + By the Loop expense tab: category-by-category every month."""
    print("\n=== CATEGORY BREAKDOWN BY MONTH (raxxostudios/5a8i + By the Loop) ===")
    print("  12 categories is the sweet spot — fewer and the P&L is useless")
    by_month_cat = defaultdict(lambda: defaultdict(float))
    cat_totals = defaultdict(float)
    for r in rows:
        key = r["date"].strftime("%Y-%m")
        by_month_cat[key][r["category"]] += r["amount"]
        cat_totals[r["category"]] += r["amount"]
    if not by_month_cat:
        print("  No expense rows yet — log amounts with date + category columns")
        return
    for month in sorted(by_month_cat):
        cats = by_month_cat[month]
        total = sum(cats.values())
        print(f"\n  {month} — expenses ${total:,.2f}")
        for cat in sorted(cats, key=lambda c: -cats[c]):
            pct = (cats[cat] / total * 100) if total else 0
            print(f"    {cat}: ${cats[cat]:,.2f} ({pct:.0f}%)")
    annual = sum(cat_totals.values())
    print(f"\n  YTD expense categories (${annual:,.2f} total):")
    for cat in sorted(cat_totals, key=lambda c: -cat_totals[c]):
        pct = (cat_totals[cat] / annual * 100) if annual else 0
        print(f"    {cat}: ${cat_totals[cat]:,.2f} ({pct:.0f}%)")


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 freelance_finance_os.py invoice-log.csv expense-log.csv")
        sys.exit(1)

    invoices = load_invoices(sys.argv[1])
    expense_path = sys.argv[2]
    expense_total, by_cat = load_expenses(expense_path)
    expense_rows = load_expense_rows(expense_path)

    invoiced = sum(r["amount"] for r in invoices)
    collected = sum(r["amount"] for r in invoices if r["status"] == "paid")
    awaiting = sum(r["amount"] for r in invoices if r["status"] == "sent")
    overdue_amt = sum(r["amount"] for r in invoices if r["overdue"])
    overdue_cnt = sum(1 for r in invoices if r["overdue"])

    net_profit = collected - expense_total
    tax_buffer = max(net_profit, 0) * TAX_BUFFER_PCT / 100
    safe_to_spend = max(net_profit - tax_buffer, 0)
    quarterly = max(net_profit, 0) * ESTIMATED_TAX_PCT / 100 / 4

    inv_rows = len(invoices)
    exp_rows = sum(1 for _ in open(sys.argv[2], encoding="utf-8")) - 1  # header

    print("=== BEGINNER-FRIENDLY (faisalmq/2fj6 — no formulas required) ===")
    print("  You only type into shaded cells. In this kit that's your CSV rows.")
    print("  Type here:     invoice + expense CSV columns (see templates)")
    print("  Auto-calculated: collected, net profit, tax buffer, safe-to-spend, quarterly")
    print(f"  Invoice log: {inv_rows} rows · Expense log: {exp_rows} rows (expandable — duplicate templates)")
    print()
    print("=== FREELANCE FINANCE OS (By the Loop clone) ===")
    print(f"  Invoices logged:     {len(invoices)}")
    print(f"  Total invoiced:      ${invoiced:,.2f}")
    print(f"  Collected (paid):    ${collected:,.2f}")
    print(f"  Awaiting payment:    ${awaiting:,.2f}")
    print(f"  Overdue (sent+late): {overdue_cnt} invoices · ${overdue_amt:,.2f}")
    print()
    print("=== EXPENSE + TAX BUFFER ===")
    print(f"  Expenses YTD:        ${expense_total:,.2f}")
    for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"    {cat:12} ${amt:,.2f}")
    print(f"  Net profit (paid):   ${net_profit:,.2f}")
    print(f"  Tax buffer ({TAX_BUFFER_PCT:.0f}%):   ${tax_buffer:,.2f}")
    print(f"  Safe to spend:       ${safe_to_spend:,.2f}")
    print_category_breakdown(expense_rows)
    print()
    margin_pct = (net_profit / collected * 100) if collected > 0 else 0.0
    print("=== PROFIT MARGINS AT A GLANCE (faisalmq/3cpo shape) ===")
    print(f"  Collected (paid):    ${collected:,.2f}")
    print(f"  Expenses YTD:        ${expense_total:,.2f}")
    print(f"  Net profit:          ${net_profit:,.2f}")
    print(f"  Profit margin:       {margin_pct:.1f}%")
    print("  Categorized breakdown (tax preparedness):")
    for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1]):
        pct_rev = (amt / collected * 100) if collected > 0 else 0.0
        print(f"    {cat:12} ${amt:,.2f}  ({pct_rev:.1f}% of revenue)")
    by_client = defaultdict(float)
    for r in invoices:
        if r["status"] == "paid":
            by_client[r["client"]] += r["amount"]
    if by_client:
        print("  Per-client collected (pricing decisions):")
        for client, amt in sorted(by_client.items(), key=lambda x: -x[1]):
            print(f"    {client:20} ${amt:,.2f}")
    print()
    print("=== QUARTERLY TAX ESTIMATOR (1040-ES shape) ===")
    print(f"  Estimated annual tax ({ESTIMATED_TAX_PCT:.0f}% planning rate): ${max(net_profit,0)*ESTIMATED_TAX_PCT/100:,.2f}")
    print(f"  Suggested per deadline: ${quarterly:,.2f}")
    for q, deadline, period in QUARTERLY_DEADLINES:
        print(f"    {q} due {deadline:16} ({period})")
    print()
    print("=== COMPLETE WORKBOOK (hemantdev/1iae — no Notion, offline file) ===")
    print("  Dashboard view:      collected, net profit, safe-to-spend (this stdout)")
    print("  Income log:          invoice-log.csv — one row per payment")
    print("  Expense log:         expense-log.csv — categorized, tax-deductible flags")
    print("  Clients view:        per-client collected totals (from invoice log)")
    print("  Invoices view:       draft/sent/paid/overdue from same log")
    print("  Tax estimator:       quarterly deadlines + suggested set-aside")
    print("  Zero onboarding:     open CSV, type shaded columns, run CLI — no account")
    print()
    print("=== FOUR TOOLS IN ONE BUNDLE ===")
    print("  1. Invoice tracker     [this run]")
    print("  2. Expense + buffer    [this run]")
    print("  3. Rate calculator     [open rate-calculator.html]")
    print("  4. Quarterly estimator [this run]")


if __name__ == "__main__":
    main()
