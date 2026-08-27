#!/usr/bin/env python3
"""Seller Profit & Fee Tracker — clone of smadsby.gumroad.com/l/ejxcg ($14.99)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime

PLATFORM_FEES = {
    "gumroad": {"pct": 0.10, "flat": 0.30},
    "etsy": {"listing": 0.20, "transaction_pct": 0.065, "processing_pct": 0.03, "processing_flat": 0.25},
    "shopify": {"pct": 0.029, "flat": 0.30},
    "ebay": {"pct": 0.129, "flat": 0.30},
    "amazon": {"pct": 0.15, "flat": 0.0},
    "other": {"pct": 0.0, "flat": 0.0},
}


def calc_platform_fee(platform, gross):
    platform = platform.lower()
    if platform == "etsy":
        f = PLATFORM_FEES["etsy"]
        return f["listing"] + gross * f["transaction_pct"] + gross * f["processing_pct"] + f["processing_flat"]
    cfg = PLATFORM_FEES.get(platform, PLATFORM_FEES["other"])
    return gross * cfg.get("pct", 0) + cfg.get("flat", 0)


def load_sales(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                gross = float(row["gross"])
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            platform = row.get("platform", "gumroad").strip().lower()
            fee = calc_platform_fee(platform, gross)
            rows.append({
                "date": dt,
                "product": row.get("product", row.get("sku", "product")).strip(),
                "platform": platform,
                "gross": gross,
                "fee": fee,
                "net": gross - fee,
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
            rows.append({
                "date": dt,
                "category": row.get("category", "other").strip().lower(),
                "amount": amt,
            })
    return rows


def month_key(dt):
    return dt.strftime("%Y-%m")


def print_dashboard(sales, expenses):
    gross = sum(r["gross"] for r in sales)
    fees = sum(r["fee"] for r in sales)
    net_sales = sum(r["net"] for r in sales)
    expense_total = sum(r["amount"] for r in expenses)
    profit = net_sales - expense_total
    margin = (profit / gross * 100) if gross else 0
    print("\n=== SELLER DASHBOARD (smadsby ejxcg clone) ===")
    print(f"  Gross sales:         ${gross:,.2f}")
    print(f"  Platform fees:       ${fees:,.2f}")
    print(f"  Net after fees:      ${net_sales:,.2f}")
    print(f"  Expenses:            ${expense_total:,.2f}")
    print(f"  Real profit:         ${profit:,.2f}")
    print(f"  Profit margin:       {margin:.1f}%")


def print_platform_comparison(sales):
    by_platform = defaultdict(lambda: {"orders": 0, "gross": 0.0, "fees": 0.0, "net": 0.0})
    for r in sales:
        p = by_platform[r["platform"]]
        p["orders"] += 1
        p["gross"] += r["gross"]
        p["fees"] += r["fee"]
        p["net"] += r["net"]
    print("\n=== PLATFORM PERFORMANCE COMPARISON ===")
    ranked = sorted(by_platform.items(), key=lambda x: x[1]["net"], reverse=True)
    for platform, stats in ranked:
        eff = (stats["fees"] / stats["gross"] * 100) if stats["gross"] else 0
        print(
            f"  {platform:10} {stats['orders']:3} orders · gross ${stats['gross']:,.2f} · "
            f"fees ${stats['fees']:,.2f} ({eff:.1f}%) · net ${stats['net']:,.2f}"
        )


def print_monthly_summary(sales, expenses):
    by_month = defaultdict(lambda: {"gross": 0.0, "fees": 0.0, "expense": 0.0})
    for r in sales:
        m = month_key(r["date"])
        by_month[m]["gross"] += r["gross"]
        by_month[m]["fees"] += r["fee"]
    for r in expenses:
        by_month[month_key(r["date"])]["expense"] += r["amount"]
    print("\n=== MONTHLY SUMMARY ===")
    for m in sorted(by_month.keys())[-6:]:
        d = by_month[m]
        profit = d["gross"] - d["fees"] - d["expense"]
        print(f"  {m}  gross ${d['gross']:,.2f} · fees ${d['fees']:,.2f} · exp ${d['expense']:,.2f} · profit ${profit:,.2f}")


def print_worst_order(sales):
    if not sales:
        return
    worst = min(sales, key=lambda r: r["net"])
    print("\n=== LOWEST-NET ORDER (fee drag check) ===")
    print(f"  {worst['date'].date()} · {worst['product'][:30]} · {worst['platform']} · net ${worst['net']:,.2f}")


def main():
    if len(sys.argv) < 3:
        print("Usage: seller_profit_fee_tracker.py sales.csv expenses.csv")
        sys.exit(1)
    sales = load_sales(sys.argv[1])
    expenses = load_expenses(sys.argv[2])
    print(f"Sales rows: {len(sales)} · Expense rows: {len(expenses)}")
    print_dashboard(sales, expenses)
    print_platform_comparison(sales)
    print_monthly_summary(sales, expenses)
    print_worst_order(sales)
    print("\nClone target: smadsby.gumroad.com/l/ejxcg ($14.99 SimpleBizDash)")


if __name__ == "__main__":
    main()
