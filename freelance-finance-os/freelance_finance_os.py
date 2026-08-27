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


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 freelance_finance_os.py invoice-log.csv expense-log.csv")
        sys.exit(1)

    invoices = load_invoices(sys.argv[1])
    expense_total, by_cat = load_expenses(sys.argv[2])

    invoiced = sum(r["amount"] for r in invoices)
    collected = sum(r["amount"] for r in invoices if r["status"] == "paid")
    awaiting = sum(r["amount"] for r in invoices if r["status"] == "sent")
    overdue_amt = sum(r["amount"] for r in invoices if r["overdue"])
    overdue_cnt = sum(1 for r in invoices if r["overdue"])

    net_profit = collected - expense_total
    tax_buffer = max(net_profit, 0) * TAX_BUFFER_PCT / 100
    safe_to_spend = max(net_profit - tax_buffer, 0)
    quarterly = max(net_profit, 0) * ESTIMATED_TAX_PCT / 100 / 4

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
    print()
    print("=== QUARTERLY TAX ESTIMATOR (1040-ES shape) ===")
    print(f"  Estimated annual tax ({ESTIMATED_TAX_PCT:.0f}% planning rate): ${max(net_profit,0)*ESTIMATED_TAX_PCT/100:,.2f}")
    print(f"  Suggested per deadline: ${quarterly:,.2f}")
    for q, deadline, period in QUARTERLY_DEADLINES:
        print(f"    {q} due {deadline:16} ({period})")
    print()
    print("=== FOUR TOOLS IN ONE BUNDLE ===")
    print("  1. Invoice tracker     [this run]")
    print("  2. Expense + buffer    [this run]")
    print("  3. Rate calculator     [open rate-calculator.html]")
    print("  4. Quarterly estimator [this run]")


if __name__ == "__main__":
    main()
