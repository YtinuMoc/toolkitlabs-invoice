#!/usr/bin/env python3
"""Seller Profit & Content Tracker — clone of AnahitDigitalStudio nxqiai ($14.99 Gumroad)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime
from urllib.parse import urlparse, parse_qs

PLATFORM_FEES = {
    "gumroad": {"pct": 0.10, "flat": 0.30},
    "etsy": {"listing": 0.20, "transaction_pct": 0.065, "processing_pct": 0.03, "processing_flat": 0.25},
    "shopify": {"pct": 0.029, "flat": 0.30},
    "other": {"pct": 0.0, "flat": 0.0},
}


def load_products(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                price = float(row["price"])
            except (KeyError, ValueError):
                continue
            rows.append({
                "sku": row.get("sku", "").strip(),
                "name": row.get("name", "product").strip(),
                "platform": row.get("platform", "gumroad").strip().lower(),
                "price": price,
            })
    return rows


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
            rows.append({
                "date": dt,
                "sku": row.get("sku", "").strip(),
                "product": row.get("product", "").strip(),
                "platform": platform,
                "gross": gross,
                "fee": calc_platform_fee(platform, gross),
            })
    for r in rows:
        r["net"] = r["gross"] - r["fee"]
    return rows


def calc_platform_fee(platform, gross):
    if platform == "etsy":
        f = PLATFORM_FEES["etsy"]
        return f["listing"] + gross * f["transaction_pct"] + gross * f["processing_pct"] + f["processing_flat"]
    cfg = PLATFORM_FEES.get(platform, PLATFORM_FEES["other"])
    return gross * cfg.get("pct", 0) + cfg.get("flat", 0)


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
                "vendor": row.get("vendor", "").strip(),
            })
    return rows


def load_content(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                clicks = int(row.get("clicks", 0) or 0)
                conv = int(row.get("conversions", 0) or 0)
                rev = float(row.get("revenue", 0) or 0)
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            rows.append({
                "date": dt,
                "channel": row.get("channel", "pinterest").strip().lower(),
                "pin_title": row.get("pin_title", "").strip(),
                "clicks": clicks,
                "conversions": conv,
                "revenue": rev,
            })
    return rows


def load_utm(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                clicks = int(row.get("clicks", 0) or 0)
                conv = int(row.get("conversions", 0) or 0)
                rev = float(row.get("revenue", 0) or 0)
            except (KeyError, ValueError):
                continue
            rows.append({
                "campaign": row.get("campaign", "").strip(),
                "utm_source": row.get("utm_source", "").strip(),
                "utm_medium": row.get("utm_medium", "").strip(),
                "url": row.get("url", "").strip(),
                "clicks": clicks,
                "conversions": conv,
                "revenue": rev,
            })
    return rows


def load_launches(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                d7 = float(row.get("revenue_7d", 0) or 0)
                d30 = float(row.get("revenue_30d", 0) or 0)
                launch = datetime.strptime(row["launch_date"].strip(), "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            rows.append({
                "product": row.get("product", "").strip(),
                "launch_date": launch,
                "promo": row.get("promo_notes", "").strip(),
                "revenue_7d": d7,
                "revenue_30d": d30,
                "rating": row.get("outcome_rating", "n/a").strip(),
            })
    return rows


def month_key(dt):
    return dt.strftime("%Y-%m")


def print_dashboard(sales, expenses, content):
    gross = sum(r["gross"] for r in sales)
    fees = sum(r["fee"] for r in sales)
    net_sales = sum(r["net"] for r in sales)
    expense_total = sum(r["amount"] for r in expenses)
    profit = net_sales - expense_total
    margin = (profit / gross * 100) if gross else 0
    content_rev = sum(r["revenue"] for r in content)
    content_clicks = sum(r["clicks"] for r in content)
    print("\n=== DASHBOARD (AnahitDigitalStudio nxqiai clone) ===")
    print(f"  YTD gross sales:     ${gross:,.2f}")
    print(f"  Platform fees paid:  ${fees:,.2f}")
    print(f"  YTD net revenue:     ${net_sales:,.2f}")
    print(f"  YTD expenses:        ${expense_total:,.2f}")
    print(f"  YTD profit:          ${profit:,.2f}")
    print(f"  Profit margin:       {margin:.1f}%")
    print(f"  Content clicks:      {content_clicks:,}")
    print(f"  Content revenue:     ${content_rev:,.2f}")


def print_product_performance(sales):
    by_product = defaultdict(lambda: {"units": 0, "gross": 0.0, "net": 0.0, "platforms": set()})
    for r in sales:
        key = r["product"] or r["sku"] or "unknown"
        by_product[key]["units"] += 1
        by_product[key]["gross"] += r["gross"]
        by_product[key]["net"] += r["net"]
        by_product[key]["platforms"].add(r["platform"])
    print("\n=== PRODUCT PERFORMANCE ===")
    ranked = sorted(by_product.items(), key=lambda x: x[1]["net"], reverse=True)
    for name, stats in ranked[:8]:
        plats = ", ".join(sorted(stats["platforms"]))
        print(f"  {name[:28]:28} {stats['units']:3} units · ${stats['net']:,.2f} net · {plats}")


def print_monthly_pnl(sales, expenses):
    by_month = defaultdict(lambda: {"gross": 0.0, "fees": 0.0, "expense": 0.0})
    for r in sales:
        m = month_key(r["date"])
        by_month[m]["gross"] += r["gross"]
        by_month[m]["fees"] += r["fee"]
    for r in expenses:
        by_month[month_key(r["date"])]["expense"] += r["amount"]
    print("\n=== MONTHLY P&L ===")
    for m in sorted(by_month.keys())[-6:]:
        d = by_month[m]
        net = d["gross"] - d["fees"] - d["expense"]
        print(f"  {m}  gross ${d['gross']:,.2f} · fees ${d['fees']:,.2f} · exp ${d['expense']:,.2f} · profit ${net:,.2f}")


def print_content_planner(content):
    by_channel = defaultdict(lambda: {"clicks": 0, "conv": 0, "rev": 0.0})
    for r in content:
        by_channel[r["channel"]]["clicks"] += r["clicks"]
        by_channel[r["channel"]]["conv"] += r["conversions"]
        by_channel[r["channel"]]["rev"] += r["revenue"]
    print("\n=== CONTENT PLANNER (Pinterest & social) ===")
    for ch, stats in sorted(by_channel.items(), key=lambda x: x[1]["rev"], reverse=True):
        ctr = (stats["conv"] / stats["clicks"] * 100) if stats["clicks"] else 0
        print(f"  {ch:12} {stats['clicks']:5} clicks · {stats['conv']:3} conv · ${stats['rev']:,.2f} rev · {ctr:.1f}% conv rate")


def print_utm_tracker(utm_rows):
    print("\n=== UTM CAMPAIGN TRACKER ===")
    ranked = sorted(utm_rows, key=lambda r: r["revenue"], reverse=True)
    for r in ranked[:6]:
        src = r["utm_source"] or parse_utm(r["url"]).get("utm_source", ["?"])[0]
        print(f"  {r['campaign'][:24]:24} src={src:10} ${r['revenue']:,.2f} · {r['clicks']} clicks · {r['conversions']} conv")


def parse_utm(url):
    if not url:
        return {}
    try:
        return parse_qs(urlparse(url).query)
    except Exception:
        return {}


def print_launch_planner(launches):
    print("\n=== LAUNCH PLANNER ===")
    for r in sorted(launches, key=lambda x: x["revenue_30d"], reverse=True):
        print(f"  {r['product'][:26]:26} 7d ${r['revenue_7d']:,.2f} · 30d ${r['revenue_30d']:,.2f} · {r['rating']}")


def print_break_even(sales, expenses, monthly_goal=1500.0):
    fixed = sum(r["amount"] for r in expenses if r["category"] in ("software", "ads", "subscription"))
    avg_net = (sum(r["net"] for r in sales) / max(len(sales), 1))
    needed = max(0, (monthly_goal + fixed) / max(avg_net, 1))
    print("\n=== GOALS & BREAK-EVEN ===")
    print(f"  Monthly fixed costs:   ${fixed:,.2f}")
    print(f"  Target take-home:      ${monthly_goal:,.2f}")
    print(f"  Avg net per sale:      ${avg_net:,.2f}")
    print(f"  Sales needed/month:    {needed:.0f}")


def main():
    if len(sys.argv) < 6:
        print("Usage: seller_dashboard.py products.csv sales.csv expenses.csv content.csv utm.csv [launches.csv]")
        sys.exit(1)
    products = load_products(sys.argv[1])
    sales = load_sales(sys.argv[2])
    expenses = load_expenses(sys.argv[3])
    content = load_content(sys.argv[4])
    utm_rows = load_utm(sys.argv[5])
    launches = load_launches(sys.argv[6]) if len(sys.argv) > 6 else []
    print(f"Catalog: {len(products)} SKUs · Sales: {len(sales)} rows")
    print_dashboard(sales, expenses, content)
    print_product_performance(sales)
    print_monthly_pnl(sales, expenses)
    print_content_planner(content)
    print_utm_tracker(utm_rows)
    if launches:
        print_launch_planner(launches)
    print_break_even(sales, expenses)
    print("\nClone target: anahitstudio.gumroad.com/l/nxqiai ($14.99)")


if __name__ == "__main__":
    main()
