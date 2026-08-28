#!/usr/bin/env python3
"""Automated E-Commerce Bookkeeping Dashboard — clone of vivre05.gumroad.com/l/xytjqh ($29+)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime

DEFAULT_TAX_RATE = 0.28

PLATFORM_FEES = {
    "etsy": {"listing": 0.20, "transaction_pct": 0.065, "processing_pct": 0.03, "processing_flat": 0.25},
    "gumroad": {"pct": 0.10, "flat": 0.30},
    "amazon": {"pct": 0.15, "flat": 0.0},
    "ebay": {"pct": 0.129, "flat": 0.30},
    "other": {"pct": 0.0, "flat": 0.0},
}


def calc_platform_fee(platform, gross):
    platform = platform.lower().replace(" ", "_")
    if platform == "etsy":
        f = PLATFORM_FEES["etsy"]
        return round(
            f["listing"] + gross * f["transaction_pct"] + gross * f["processing_pct"] + f["processing_flat"],
            2,
        )
    cfg = PLATFORM_FEES.get(platform, PLATFORM_FEES["other"])
    return round(gross * cfg.get("pct", 0) + cfg.get("flat", 0), 2)


def pricing_calculator(cogs, postage, packaging, platform, target_profit=None, target_margin=None):
    platform = platform.lower().replace(" ", "_")
    fixed = postage + packaging + cogs
    if platform == "etsy":
        f = PLATFORM_FEES["etsy"]
        rate = f["transaction_pct"] + f["processing_pct"]
        if target_profit is not None:
            sale = (target_profit + fixed + f["listing"] + f["processing_flat"]) / (1 - rate)
            return round(sale, 2)
        if target_margin is not None:
            m = target_margin / 100
            sale = (fixed + f["listing"] + f["processing_flat"]) / (1 - rate - m)
            return round(sale, 2)
    cfg = PLATFORM_FEES.get(platform, PLATFORM_FEES["other"])
    pct, flat = cfg.get("pct", 0), cfg.get("flat", 0)
    if target_profit is not None:
        return round((target_profit + fixed + flat) / (1 - pct), 2)
    if target_margin is not None:
        m = target_margin / 100
        return round((fixed + flat) / (1 - pct - m), 2)
    return None


def print_pricing_modes(args):
    if "--price-profit" in args:
        idx = args.index("--price-profit")
        target = float(args[idx + 1])
        cogs = float(args[idx + 2])
        postage = float(args[idx + 3])
        packaging = float(args[idx + 4])
        platform = args[idx + 5] if len(args) > idx + 5 else "etsy"
        sale = pricing_calculator(cogs, postage, packaging, platform, target_profit=target)
        print(f"\n=== PRICING CALCULATOR (target profit ${target:.2f}) ===")
        print(f"  Platform: {platform}")
        print(f"  Charge at least: ${sale:.2f}")
        return True
    if "--price-margin" in args:
        idx = args.index("--price-margin")
        margin = float(args[idx + 1])
        cogs = float(args[idx + 2])
        postage = float(args[idx + 3])
        packaging = float(args[idx + 4])
        platform = args[idx + 5] if len(args) > idx + 5 else "gumroad"
        sale = pricing_calculator(cogs, postage, packaging, platform, target_margin=margin)
        print(f"\n=== PRICING CALCULATOR (target margin {margin:.0f}%) ===")
        print(f"  Platform: {platform}")
        print(f"  Charge at least: ${sale:.2f}")
        return True
    return False


def load_transactions(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = float(row["amount"])
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            kind = row.get("type", "sale").strip().lower()
            category = row.get("category", "other").strip().lower()
            rows.append({
                "date": dt,
                "type": kind,
                "category": category,
                "description": row.get("description", "").strip(),
                "amount": amt,
                "platform": row.get("platform", "other").strip().lower(),
            })
    return rows


def print_dashboard(transactions, tax_rate=DEFAULT_TAX_RATE):
    sales = [t for t in transactions if t["type"] in ("sale", "income", "revenue")]
    expenses = [t for t in transactions if t["type"] in ("expense", "cost")]
    revenue = sum(t["amount"] for t in sales)
    costs = sum(t["amount"] for t in expenses)
    profit = round(revenue - costs, 2)
    margin = (profit / revenue * 100) if revenue else 0.0
    tax_est = round(max(profit, 0) * tax_rate, 2)
    take_home = round(profit - tax_est, 2)

    print("\n=== E-COMMERCE BOOKKEEPING DASHBOARD (vivre05 xytjqh clone) ===")
    print(f"  Transactions:        {len(transactions)}")
    print(f"  Total revenue:       ${revenue:,.2f}")
    print(f"  Total costs:         ${costs:,.2f}")
    print(f"  Take-home profit:    ${profit:,.2f}")
    print(f"  Profit margin:       {margin:.1f}%")
    print(f"  Tax set-aside ({tax_rate*100:.0f}%):  ${tax_est:,.2f}")
    print(f"  After tax reserve:   ${take_home:,.2f}")

    by_platform = defaultdict(lambda: {"revenue": 0.0, "costs": 0.0})
    for t in sales:
        by_platform[t["platform"]]["revenue"] += t["amount"]
    for t in expenses:
        by_platform[t["platform"]]["costs"] += t["amount"]

    if by_platform:
        print("\n=== BY PLATFORM ===")
        for plat in sorted(by_platform):
            r = by_platform[plat]["revenue"]
            c = by_platform[plat]["costs"]
            net = r - c
            print(f"  {plat:16}  revenue ${r:8.2f}  costs ${c:8.2f}  net ${net:8.2f}")

    by_cat = defaultdict(float)
    for t in expenses:
        by_cat[t["category"]] += t["amount"]
    if by_cat:
        print("\n=== EXPENSE BREAKDOWN ===")
        for cat in sorted(by_cat, key=by_cat.get, reverse=True):
            print(f"  {cat:20}  ${by_cat[cat]:,.2f}")

    by_month = defaultdict(lambda: {"revenue": 0.0, "costs": 0.0})
    for t in sales:
        key = t["date"].strftime("%Y-%m")
        by_month[key]["revenue"] += t["amount"]
    for t in expenses:
        key = t["date"].strftime("%Y-%m")
        by_month[key]["costs"] += t["amount"]
    if by_month:
        print("\n=== MONTHLY SUMMARY ===")
        for month in sorted(by_month):
            r = by_month[month]["revenue"]
            c = by_month[month]["costs"]
            net = r - c
            print(f"  {month}  revenue ${r:8.2f}  costs ${c:8.2f}  net ${net:8.2f}")


def main():
    tax_rate = DEFAULT_TAX_RATE
    args = sys.argv[1:]
    if print_pricing_modes(args):
        return
    if "--tax-rate" in args:
        idx = args.index("--tax-rate")
        tax_rate = float(args[idx + 1]) / 100
        args = args[:idx] + args[idx + 2:]
    if not args:
        print("Usage: python3 ecommerce_bookkeeping_dashboard.py transactions-sample.csv [--tax-rate 28]")
        print("       python3 ecommerce_bookkeeping_dashboard.py --price-profit 10 8 3 1 etsy")
        print("       python3 ecommerce_bookkeeping_dashboard.py --price-margin 40 6 0 0 gumroad")
        sys.exit(1)
    transactions = load_transactions(args[0])
    print_dashboard(transactions, tax_rate)


if __name__ == "__main__":
    main()
