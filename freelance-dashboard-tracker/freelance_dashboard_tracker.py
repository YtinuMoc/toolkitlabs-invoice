#!/usr/bin/env python3
"""Freelance Dashboard — clone of cedabranding.gumroad.com/l/pro-dashboard ($97 · 1251 sales)."""
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


def fmt_money(n):
    return f"${n:,.2f}"


def summarize(revenue, expenses, tax_pct=DEFAULT_TAX_PCT):
    total_revenue = sum(r["amount"] for r in revenue)
    total_expenses = sum(e["amount"] for e in expenses)
    deductible = sum(e["amount"] for e in expenses if e["deductible"])
    net_profit = total_revenue - total_expenses
    tax_set_aside = max(net_profit, 0) * (tax_pct / 100.0)
    safe_to_spend = max(net_profit - tax_set_aside, 0)

    by_month = defaultdict(lambda: {"revenue": 0.0, "expense": 0.0})
    by_client = defaultdict(float)
    by_expense_cat = defaultdict(float)

    for r in revenue:
        by_month[month_key(r["date"])]["revenue"] += r["amount"]
        by_client[r["client"]] += r["amount"]

    for e in expenses:
        by_month[month_key(e["date"])]["expense"] += e["amount"]
        by_expense_cat[e["category"]] += e["amount"]

    months_with_data = [m for m in by_month if m != "unknown"]
    avg_monthly_expense = (
        sum(by_month[m]["expense"] for m in months_with_data) / len(months_with_data)
        if months_with_data else 0.0
    )
    cash_buffer = safe_to_spend
    runway_months = (cash_buffer / avg_monthly_expense) if avg_monthly_expense > 0 else 0.0

    return {
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "deductible_expenses": deductible,
        "net_profit": net_profit,
        "tax_set_aside": tax_set_aside,
        "safe_to_spend": safe_to_spend,
        "tax_pct": tax_pct,
        "by_month": dict(by_month),
        "by_client": dict(by_client),
        "by_expense_cat": dict(by_expense_cat),
        "avg_monthly_expense": avg_monthly_expense,
        "runway_months": runway_months,
    }


def summarize_spreadsheet_trap(revenue_path, expense_path, tax_pct=DEFAULT_TAX_PCT):
    """wilsonhoe/4383424 4khk: spreadsheet trap → planning-layer dashboard."""
    revenue = load_revenue(revenue_path)
    expenses = load_expenses(expense_path)
    d = summarize(revenue, expenses, tax_pct)
    print("=== SPREADSHEET TRAP → FREELANCE DASHBOARD (wilsonhoe/4khk shape) ===")
    print("  Tier 1 spreadsheet cost (hidden): ~$11K–$13K/year in errors + time + missed insight.")
    print("  Tier 2 accounting software: $1,680–$4,080/year subscription — ledger, not planning.")
    print("  Tier 3 planning layer: one dashboard that turns numbers into weekly decisions.")
    print()
    print("--- 15-minute weekly protocol ---")
    print("  1. Log weekend transactions (2 min)")
    print("  2. Check cash runway months at current burn (3 min)")
    print("  3. Review which clients drove revenue this week (5 min)")
    print("  4. Flag one decision: raise price, cut sub, chase invoice (5 min)")
    print()
    print_dashboard(d)
    print()
    print(f"  Cash runway:         {d['runway_months']:.1f} months at avg burn {fmt_money(d['avg_monthly_expense'])}/mo")
    print(f"  Safe to spend:       {fmt_money(d['safe_to_spend'])} (after {d['tax_pct']:.0f}% tax set-aside)")
    print("  Guide: spreadsheet-trap-guide.md · revenue-sample.csv · expenses-sample.csv")


def print_dashboard(d):
    print("=== FREELANCE DASHBOARD (cedabranding pro-dashboard clone) ===")
    print(f"  Total revenue:       {fmt_money(d['total_revenue'])}")
    print(f"  Total expenses:      {fmt_money(d['total_expenses'])}")
    print(f"  Net profit:          {fmt_money(d['net_profit'])}")
    print(f"  Tax set-aside ({d['tax_pct']:.0f}%): {fmt_money(d['tax_set_aside'])}")
    print(f"  Safe to spend:       {fmt_money(d['safe_to_spend'])}")

    if d["by_month"]:
        print("\n--- Monthly dashboard ---")
        for m in sorted(d["by_month"].keys()):
            if m == "unknown":
                continue
            rev = d["by_month"][m]["revenue"]
            exp = d["by_month"][m]["expense"]
            net = rev - exp
            margin = (net / rev * 100) if rev else 0.0
            reserve = max(net, 0) * (d["tax_pct"] / 100.0)
            home = max(net - reserve, 0)
            print(
                f"  {m}  rev {fmt_money(rev):>12}  exp {fmt_money(exp):>12}  "
                f"net {fmt_money(net):>12}  margin {margin:5.1f}%  take-home {fmt_money(home)}"
            )

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
    if len(sys.argv) >= 4 and sys.argv[1] == "--spreadsheet-trap":
        tax_pct = float(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_TAX_PCT
        summarize_spreadsheet_trap(sys.argv[2], sys.argv[3], tax_pct)
        return
    if len(sys.argv) < 3:
        print("Usage: freelance_dashboard_tracker.py revenue.csv expenses.csv [tax_pct]")
        print("       freelance_dashboard_tracker.py --spreadsheet-trap revenue.csv expenses.csv [tax_pct]")
        print("Clone target: cedabranding.gumroad.com/l/pro-dashboard ($97 · 1251 sales · 69 ratings)")
        sys.exit(1)
    revenue = load_revenue(sys.argv[1])
    expenses = load_expenses(sys.argv[2])
    tax_pct = float(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_TAX_PCT
    d = summarize(revenue, expenses, tax_pct)
    print_dashboard(d)


if __name__ == "__main__":
    main()
