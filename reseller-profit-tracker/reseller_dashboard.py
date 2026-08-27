#!/usr/bin/env python3
"""Reseller Profit Tracker — clone of Hustlin Hooks hustlinhooks2025 ($50, 7 ratings)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime, date


def calc_net(sale_price, platform_fee, shipping_cost, cogs):
    return round(sale_price - platform_fee - shipping_cost - cogs, 2)


def load_sales(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                sale_price = float(row["sale_price"])
                platform_fee = float(row.get("platform_fee", "0") or "0")
                shipping_cost = float(row.get("shipping_cost", "0") or "0")
                cogs = float(row.get("cogs", "0") or "0")
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            net = row.get("net_profit", "").strip()
            net_profit = float(net) if net else calc_net(sale_price, platform_fee, shipping_cost, cogs)
            rows.append({
                "date": dt,
                "platform": row.get("platform", "unknown").strip().lower() or "unknown",
                "item": row.get("item", "").strip() or "unknown",
                "sku": row.get("sku", "").strip(),
                "sale_price": sale_price,
                "platform_fee": platform_fee,
                "shipping_cost": shipping_cost,
                "cogs": cogs,
                "net_profit": net_profit,
                "status": row.get("status", "sold").strip().lower(),
            })
    return rows


def load_inventory(path):
    rows = []
    today = date.today()
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                acquired = datetime.strptime(row["acquired_date"].strip(), "%Y-%m-%d").date()
                cost = float(row.get("cost", "0") or "0")
                list_price = float(row.get("list_price", "0") or "0")
            except (KeyError, ValueError):
                continue
            days = row.get("days_listed", "").strip()
            if days:
                days_listed = int(float(days))
            else:
                days_listed = (today - acquired).days
            rows.append({
                "sku": row.get("sku", "").strip(),
                "item": row.get("item", "").strip() or "unknown",
                "platform": row.get("platform_listed", "unknown").strip().lower() or "unknown",
                "acquired_date": acquired,
                "cost": cost,
                "list_price": list_price,
                "days_listed": days_listed,
                "status": row.get("status", "listed").strip().lower(),
            })
    return rows


def load_expenses(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amount = float(row["amount"])
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            rows.append({
                "date": dt,
                "category": row.get("category", "other").strip().lower() or "other",
                "description": row.get("description", "").strip(),
                "amount": amount,
            })
    return rows


def print_dashboard(sales, expenses):
    gross = sum(s["sale_price"] for s in sales)
    fees = sum(s["platform_fee"] + s["shipping_cost"] for s in sales)
    cogs = sum(s["cogs"] for s in sales)
    net = sum(s["net_profit"] for s in sales)
    exp_total = sum(e["amount"] for e in expenses)
    take_home = net - exp_total
    margin = (net / gross * 100) if gross else 0.0
    print("\n=== RESELLER DASHBOARD (Hustlin Hooks clone) ===")
    print(f"  Sales logged:      {len(sales)}")
    print(f"  Gross revenue:     ${gross:,.2f}")
    print(f"  Platform + ship:   ${fees:,.2f}")
    print(f"  COGS:              ${cogs:,.2f}")
    print(f"  Net profit (sales):${net:,.2f}")
    print(f"  Expenses:          ${exp_total:,.2f}")
    print(f"  Take-home:         ${take_home:,.2f}")
    print(f"  Margin:            {margin:.1f}%")


def print_platform_summary(sales):
    plat = defaultdict(lambda: {"count": 0, "gross": 0.0, "fees": 0.0, "net": 0.0})
    for s in sales:
        p = plat[s["platform"]]
        p["count"] += 1
        p["gross"] += s["sale_price"]
        p["fees"] += s["platform_fee"] + s["shipping_cost"]
        p["net"] += s["net_profit"]
    print("\n=== PLATFORM SUMMARY ===")
    for name in sorted(plat, key=lambda k: plat[k]["net"], reverse=True):
        p = plat[name]
        margin = (p["net"] / p["gross"] * 100) if p["gross"] else 0.0
        print(
            f"  {name:12s}  sales {p['count']:3d}  gross ${p['gross']:8,.2f}  "
            f"fees ${p['fees']:7,.2f}  net ${p['net']:8,.2f}  margin {margin:5.1f}%"
        )


def print_monthly_summary(sales):
    monthly = defaultdict(lambda: {"gross": 0.0, "net": 0.0, "count": 0})
    for s in sales:
        mk = s["date"].strftime("%Y-%m")
        m = monthly[mk]
        m["gross"] += s["sale_price"]
        m["net"] += s["net_profit"]
        m["count"] += 1
    print("\n=== MONTHLY SALES SUMMARY ===")
    for mk in sorted(monthly):
        m = monthly[mk]
        print(f"  {mk}  sales {m['count']:3d}  gross ${m['gross']:8,.2f}  net ${m['net']:8,.2f}")


def print_aging_inventory(inv):
    listed = [r for r in inv if r["status"] == "listed"]
    if not listed:
        print("\n=== AGING INVENTORY ===\n  (no listed items)")
        return
    ranked = sorted(listed, key=lambda r: r["days_listed"], reverse=True)
    print("\n=== AGING INVENTORY (master sheet) ===")
    for r in ranked[:15]:
        print(
            f"  {r['days_listed']:4d}d  {r['sku']:8s}  {r['item'][:24]:24s}  "
            f"cost ${r['cost']:6.2f}  list ${r['list_price']:6.2f}  {r['platform']}"
        )
    stale = [r for r in listed if r["days_listed"] >= 90]
    if stale:
        tied = sum(r["cost"] for r in stale)
        print(f"\n  ⚠ {len(stale)} item(s) listed 90+ days — ${tied:,.2f} capital tied up")


def print_worst_order(sales):
    if not sales:
        return
    worst = min(sales, key=lambda s: s["net_profit"])
    print("\n=== WORST ORDER (names the single order that lost the most) ===")
    print(
        f"  {worst['date'].strftime('%Y-%m-%d')}  {worst['platform']}  {worst['item']}  "
        f"gross ${worst['sale_price']:.2f}  net ${worst['net_profit']:.2f}"
    )


def print_expense_breakdown(expenses):
    cats = defaultdict(float)
    for e in expenses:
        cats[e["category"]] += e["amount"]
    print("\n=== EXPENSE BREAKDOWN ===")
    for cat in sorted(cats, key=cats.get, reverse=True):
        print(f"  {cat:12s}  ${cats[cat]:8,.2f}")


def main():
    if len(sys.argv) < 4:
        print("Usage: reseller_dashboard.py <sales.csv> <inventory.csv> <expenses.csv>")
        sys.exit(1)
    sales = load_sales(sys.argv[1])
    inv = load_inventory(sys.argv[2])
    expenses = load_expenses(sys.argv[3])
    print_dashboard(sales, expenses)
    print_platform_summary(sales)
    print_monthly_summary(sales)
    print_aging_inventory(inv)
    print_worst_order(sales)
    print_expense_breakdown(expenses)


if __name__ == "__main__":
    main()
