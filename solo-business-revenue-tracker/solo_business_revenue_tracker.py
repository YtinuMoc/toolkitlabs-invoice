#!/usr/bin/env python3
"""Solo Business Revenue & Expense Tracker — clone of amyragland.gumroad.com/l/tckuq ($10)."""
import csv
import sys
from collections import defaultdict

DEFAULT_TAX_PCT = 25.0


def load_revenue(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                rows.append({
                    "date": row.get("date", "").strip(),
                    "client": row.get("client", "").strip(),
                    "description": row.get("description", "").strip(),
                    "amount": float(row.get("amount") or 0),
                    "category": row.get("category", "Services").strip(),
                })
            except (KeyError, ValueError):
                continue
    return rows


def load_expenses(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                rows.append({
                    "date": row.get("date", "").strip(),
                    "category": row.get("category", "Other").strip(),
                    "description": row.get("description", "").strip(),
                    "amount": float(row.get("amount") or 0),
                    "deductible": row.get("deductible", "yes").strip().lower() in ("yes", "y", "1", "true"),
                })
            except (KeyError, ValueError):
                continue
    return rows


def month_key(date_str):
    return date_str[:7] if len(date_str) >= 7 else "unknown"


def quarter_key(date_str):
    if len(date_str) < 7:
        return "unknown"
    y, m = date_str[:4], int(date_str[5:7])
    return f"{y}-Q{(m - 1) // 3 + 1}"


def fmt_money(n):
    return f"${n:,.2f}"


def summarize(revenue, expenses, tax_pct=DEFAULT_TAX_PCT):
    total_revenue = sum(r["amount"] for r in revenue)
    total_expenses = sum(e["amount"] for e in expenses)
    deductible = sum(e["amount"] for e in expenses if e["deductible"])
    net_profit = total_revenue - total_expenses
    tax_set_aside = max(net_profit, 0) * (tax_pct / 100.0)

    by_month = defaultdict(lambda: {"revenue": 0.0, "expense": 0.0})
    by_quarter = defaultdict(lambda: {"revenue": 0.0, "expense": 0.0})
    by_client = defaultdict(float)
    by_expense_cat = defaultdict(float)

    for r in revenue:
        by_month[month_key(r["date"])]["revenue"] += r["amount"]
        by_quarter[quarter_key(r["date"])]["revenue"] += r["amount"]
        by_client[r["client"]] += r["amount"]

    for e in expenses:
        by_month[month_key(e["date"])]["expense"] += e["amount"]
        by_quarter[quarter_key(e["date"])]["expense"] += e["amount"]
        by_expense_cat[e["category"]] += e["amount"]

    return {
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "deductible_expenses": deductible,
        "net_profit": net_profit,
        "tax_set_aside": tax_set_aside,
        "tax_pct": tax_pct,
        "by_month": dict(by_month),
        "by_quarter": dict(by_quarter),
        "by_client": dict(by_client),
        "by_expense_cat": dict(by_expense_cat),
    }


def summarize_portable(revenue_path, expense_path, tax_pct=DEFAULT_TAX_PCT):
    """faisalmq/3gcp: portable solo business tracker — single source of truth, any device."""
    revenue = load_revenue(revenue_path)
    expenses = load_expenses(expense_path)
    total_revenue = sum(r["amount"] for r in revenue)
    total_expenses = sum(e["amount"] for e in expenses)
    by_expense_cat = defaultdict(float)
    for e in expenses:
        by_expense_cat[e["category"]] += e["amount"]
    net_profit = total_revenue - total_expenses
    tax_set_aside = max(net_profit, 0) * (tax_pct / 100.0)
    take_home = max(net_profit - tax_set_aside, 0)
    rev_rows = len(revenue)
    exp_rows = len(expenses)
    print("=== PORTABLE SOLO BUSINESS TRACKER (faisalmq/3gcp shape) ===")
    print("  Vessel: plain CSV logs — sync via Dropbox/iCloud/Git; no Google account.")
    print("  Update from phone (any CSV editor) or desktop (Excel, Numbers, CLI).")
    print("  Single source of truth — stop winging it with mental math.")
    print()
    print("  Four metrics that matter:")
    print(f"    Income tracking:     ${total_revenue:,.2f} collected ({rev_rows} revenue rows)")
    print(f"    Expense categories:  ${total_expenses:,.2f} ({exp_rows} expense rows)")
    if by_expense_cat:
        for cat, amt in sorted(by_expense_cat.items(), key=lambda x: -x[1])[:4]:
            print(f"      · {cat}: ${amt:,.2f}")
    print(f"    Tax estimation:      ${tax_set_aside:,.2f} set aside ({tax_pct:.0f}% of net)")
    print(f"    Net profit view:     ${net_profit:,.2f} → take-home ${take_home:,.2f}")
    print()
    print("  Portability checklist:")
    print("    [x] Plain-text CSV — opens everywhere")
    print("    [x] No subscription — one-time kit")
    print("    [x] Offline CLI preview — python3 solo_business_revenue_tracker.py --portable …")
    print("    [x] Expandable — duplicate template rows as you grow")
    print("  Guide: portable-tracker-guide.md · revenue-sample.csv · expenses-sample.csv")


def print_dashboard(d):
    print("=== SOLO BUSINESS REVENUE TRACKER (amyragland tckuq clone) ===")
    print(f"  Total revenue:       {fmt_money(d['total_revenue'])}")
    print(f"  Total expenses:      {fmt_money(d['total_expenses'])}")
    print(f"  Deductible expenses: {fmt_money(d['deductible_expenses'])}")
    print(f"  Net profit:          {fmt_money(d['net_profit'])}")
    print(f"  Tax set-aside ({d['tax_pct']:.0f}%): {fmt_money(d['tax_set_aside'])}")

    if d["by_month"]:
        print("\n--- Monthly P&L ---")
        for m in sorted(d["by_month"].keys()):
            rev = d["by_month"][m]["revenue"]
            exp = d["by_month"][m]["expense"]
            net = rev - exp
            margin = (net / rev * 100) if rev else 0.0
            print(f"  {m}  revenue {fmt_money(rev):>12}  expense {fmt_money(exp):>12}  net {fmt_money(net):>12}  margin {margin:5.1f}%")

    if d["by_quarter"]:
        print("\n--- Quarterly P&L (YTD) ---")
        for q in sorted(d["by_quarter"].keys()):
            rev = d["by_quarter"][q]["revenue"]
            exp = d["by_quarter"][q]["expense"]
            net = rev - exp
            print(f"  {q}  revenue {fmt_money(rev):>12}  expense {fmt_money(exp):>12}  net {fmt_money(net):>12}")

    if d["by_client"]:
        total = d["total_revenue"]
        print("\n--- Revenue by client (% of total) ---")
        for client, amt in sorted(d["by_client"].items(), key=lambda x: -x[1]):
            pct = (amt / total * 100) if total else 0
            print(f"  {client:24s} {fmt_money(amt):>12}  ({pct:5.1f}%)")

    if d["by_expense_cat"]:
        print("\n--- Expenses by category ---")
        for cat, amt in sorted(d["by_expense_cat"].items(), key=lambda x: -x[1]):
            print(f"  {cat:24s} {fmt_money(amt)}")


def main():
    if len(sys.argv) >= 4 and sys.argv[1] == "--portable":
        tax_pct = float(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_TAX_PCT
        summarize_portable(sys.argv[2], sys.argv[3], tax_pct)
        return
    if len(sys.argv) < 3:
        print("Usage: solo_business_revenue_tracker.py revenue.csv expenses.csv [tax_pct]")
        print("       solo_business_revenue_tracker.py --portable revenue.csv expenses.csv [tax_pct]")
        print("Clone target: amyragland.gumroad.com/l/tckuq ($10 2026 Solo Business Revenue & Expense Tracker)")
        sys.exit(1)
    revenue = load_revenue(sys.argv[1])
    expenses = load_expenses(sys.argv[2])
    tax_pct = float(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_TAX_PCT
    d = summarize(revenue, expenses, tax_pct)
    print_dashboard(d)


if __name__ == "__main__":
    main()
