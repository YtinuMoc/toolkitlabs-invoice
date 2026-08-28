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
    drag = []
    for platform, stats in ranked:
        eff = (stats["fees"] / stats["gross"] * 100) if stats["gross"] else 0
        drag.append((platform, eff, stats))
        print(
            f"  {platform:10} {stats['orders']:3} orders · gross ${stats['gross']:,.2f} · "
            f"fees ${stats['fees']:,.2f} ({eff:.1f}%) · net ${stats['net']:,.2f}"
        )
    if drag:
        highest = max(drag, key=lambda x: x[1])
        lowest = min(drag, key=lambda x: x[1])
        print(f"\n  Highest fee drag: {highest[0]} ({highest[1]:.1f}% of gross)")
        print(f"  Lowest fee drag:  {lowest[0]} ({lowest[1]:.1f}% of gross)")


def print_refund_impact(sales, expenses):
    gross = sum(r["gross"] for r in sales)
    fees = sum(r["fee"] for r in sales)
    net_sales = gross - fees
    refund_rows = [r for r in expenses if r["category"] in ("refund", "refunds")]
    if not refund_rows:
        return
    refund_total = sum(r["amount"] for r in expenses)
    refund_only = sum(r["amount"] for r in refund_rows)
    other_expense = refund_total - refund_only
    profit_with = net_sales - refund_total
    profit_without = net_sales - other_expense
    margin_with = (profit_with / gross * 100) if gross else 0
    margin_without = (profit_without / gross * 100) if gross else 0
    print("\n=== REFUND IMPACT (smadsby ejxcg / orion_operator/40gi shape) ===")
    print(f"  Refund events:       {len(refund_rows)}")
    print(f"  Refund total:        ${refund_only:,.2f}")
    print(f"  Refunds % of gross:  {(refund_only / gross * 100) if gross else 0:.1f}%")
    print(f"  Profit margin w/refunds:    {margin_with:.1f}%")
    print(f"  Profit margin w/o refunds:  {margin_without:.1f}%")
    print(f"  Margin lost to refunds:     {margin_without - margin_with:.1f} pts")
    for r in sorted(refund_rows, key=lambda x: x["date"]):
        print(f"    {r['date'].date()} · ${r['amount']:,.2f}")


def print_expense_drag(sales, expenses):
    gross = sum(r["gross"] for r in sales)
    if not expenses:
        return
    by_cat = defaultdict(float)
    for r in expenses:
        by_cat[r["category"]] += r["amount"]
    total = sum(by_cat.values())
    print("\n=== EXPENSE DRAG (after platform fees) ===")
    for cat, amt in sorted(by_cat.items(), key=lambda x: x[1], reverse=True):
        pct_gross = (amt / gross * 100) if gross else 0
        pct_exp = (amt / total * 100) if total else 0
        print(f"  {cat:12} ${amt:,.2f} · {pct_gross:.1f}% of gross · {pct_exp:.0f}% of expenses")
    print(f"  {'TOTAL':12} ${total:,.2f} · {(total / gross * 100) if gross else 0:.1f}% of gross sales")


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


def print_profit_margins(sales, expenses):
    gross = sum(r["gross"] for r in sales)
    fees = sum(r["fee"] for r in sales)
    expense_total = sum(r["amount"] for r in expenses)
    net_sales = gross - fees
    profit = net_sales - expense_total
    margin = (profit / gross * 100) if gross else 0
    print("\n=== PROFIT MARGINS AT A GLANCE (smadsby ejxcg / faisalmq/3cpo shape) ===")
    print(f"  Gross sales:         ${gross:,.2f}")
    print(f"  Platform fees:       ${fees:,.2f}")
    print(f"  Expenses:            ${expense_total:,.2f}")
    print(f"  Real profit:         ${profit:,.2f}")
    print(f"  Profit margin:       {margin:.1f}%")
    by_product = defaultdict(lambda: {"orders": 0, "gross": 0.0, "fees": 0.0, "net": 0.0})
    for r in sales:
        p = by_product[r["product"]]
        p["orders"] += 1
        p["gross"] += r["gross"]
        p["fees"] += r["fee"]
        p["net"] += r["net"]
    print("\n  Per-SKU margin after platform fees (pricing decisions):")
    for product, stats in sorted(by_product.items(), key=lambda x: x[1]["net"], reverse=True):
        contrib = (stats["net"] / stats["gross"] * 100) if stats["gross"] else 0
        eff_fee = (stats["fees"] / stats["gross"] * 100) if stats["gross"] else 0
        print(
            f"    {product[:28]:28} {stats['orders']:2} orders · gross ${stats['gross']:,.2f} · "
            f"fees {eff_fee:.1f}% · net ${stats['net']:,.2f} · contrib {contrib:.1f}%"
        )
    if expenses:
        by_cat = defaultdict(float)
        for r in expenses:
            by_cat[r["category"]] += r["amount"]
        print("\n  Expense drag by category (margin killers):")
        for cat, amt in sorted(by_cat.items(), key=lambda x: x[1], reverse=True):
            pct = (amt / gross * 100) if gross else 0
            print(f"    {cat:12} ${amt:,.2f} · {pct:.1f}% of gross sales")


def print_worst_order(sales):
    if not sales:
        return
    worst = min(sales, key=lambda r: r["net"])
    print("\n=== LOWEST-NET ORDER (fee drag check) ===")
    print(f"  {worst['date'].date()} · {worst['product'][:30]} · {worst['platform']} · net ${worst['net']:,.2f}")


def print_etsy_gumroad_compare(sales):
    targets = {"etsy", "gumroad"}
    subset = [r for r in sales if r["platform"] in targets]
    if not subset:
        print("\n=== ETSY VS GUMROAD (no rows) ===")
        return
    by_platform = defaultdict(lambda: {"orders": 0, "gross": 0.0, "fees": 0.0, "net": 0.0})
    for r in subset:
        p = by_platform[r["platform"]]
        p["orders"] += 1
        p["gross"] += r["gross"]
        p["fees"] += r["fee"]
        p["net"] += r["net"]
    print("\n=== ETSY VS GUMROAD FEE SHAPES ===")
    rows = []
    for platform in ("gumroad", "etsy"):
        if platform not in by_platform:
            continue
        stats = by_platform[platform]
        eff = (stats["fees"] / stats["gross"] * 100) if stats["gross"] else 0
        avg_net = stats["net"] / stats["orders"] if stats["orders"] else 0
        rows.append((platform, eff, avg_net, stats))
        print(
            f"  {platform:8} {stats['orders']:3} orders · gross ${stats['gross']:,.2f} · "
            f"fees ${stats['fees']:,.2f} ({eff:.1f}%) · net ${stats['net']:,.2f} · "
            f"avg net/order ${avg_net:,.2f}"
        )
    if len(rows) == 2:
        winner = max(rows, key=lambda x: x[3]["net"])
        print(f"\n  Higher net volume: {winner[0]} (${winner[3]['net']:,.2f})")
        lower_drag = min(rows, key=lambda x: x[1])
        print(f"  Lower fee drag:    {lower_drag[0]} ({lower_drag[1]:.1f}% of gross)")


def main():
    args = [a for a in sys.argv[1:] if not a.startswith("--")]
    flags = {a for a in sys.argv[1:] if a.startswith("--")}
    if len(args) < 2:
        print("Usage: seller_profit_fee_tracker.py sales.csv expenses.csv [--etsy-gumroad]")
        sys.exit(1)
    sales = load_sales(args[0])
    expenses = load_expenses(args[1])
    print(f"Sales rows: {len(sales)} · Expense rows: {len(expenses)}")
    print_dashboard(sales, expenses)
    print_profit_margins(sales, expenses)
    print_refund_impact(sales, expenses)
    print_platform_comparison(sales)
    print_expense_drag(sales, expenses)
    print_monthly_summary(sales, expenses)
    if "--etsy-gumroad" in flags:
        print_etsy_gumroad_compare(sales)
    print_worst_order(sales)
    print("\nClone target: smadsby.gumroad.com/l/ejxcg ($14.99 SimpleBizDash)")


if __name__ == "__main__":
    main()
