#!/usr/bin/env python3
"""Online Seller Profit & Fee Tracker — clone of ambrosetheshield.gumroad.com/l/xdjzq (£14.85)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime

PLATFORM_FEES = {
    "etsy": {"listing": 0.20, "transaction_pct": 0.065, "processing_pct": 0.03, "processing_flat": 0.25},
    "ebay": {"pct": 0.129, "flat": 0.30},
    "vinted": {"pct": 0.05, "flat": 0.70},
    "depop": {"pct": 0.10, "flat": 0.0},
    "amazon_handmade": {"pct": 0.15, "flat": 0.0},
    "gumroad": {"pct": 0.10, "flat": 0.30},
    "own_site": {"pct": 0.029, "flat": 0.30},
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


def load_orders(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                sale_price = float(row["sale_price"])
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            platform = row.get("platform", "etsy").strip().lower()
            postage = float(row.get("postage", "0") or "0")
            packaging = float(row.get("packaging", "0") or "0")
            cogs = float(row.get("cogs", "0") or "0")
            minutes = float(row.get("time_minutes", "0") or "0")
            fee = row.get("platform_fee", "").strip()
            platform_fee = float(fee) if fee else calc_platform_fee(platform, sale_price)
            total_costs = platform_fee + postage + packaging + cogs
            net = round(sale_price - total_costs, 2)
            margin = (net / sale_price * 100) if sale_price else 0.0
            hourly = (net / (minutes / 60)) if minutes > 0 else None
            rows.append({
                "date": dt,
                "order_id": row.get("order_id", "").strip(),
                "item": row.get("item", "item").strip(),
                "platform": platform,
                "sale_price": sale_price,
                "platform_fee": platform_fee,
                "postage": postage,
                "packaging": packaging,
                "cogs": cogs,
                "time_minutes": minutes,
                "net_profit": net,
                "margin_pct": margin,
                "hourly_rate": hourly,
            })
    return rows


def print_dashboard(orders):
    gross = sum(o["sale_price"] for o in orders)
    fees = sum(o["platform_fee"] for o in orders)
    postage = sum(o["postage"] for o in orders)
    packaging = sum(o["packaging"] for o in orders)
    cogs = sum(o["cogs"] for o in orders)
    net = sum(o["net_profit"] for o in orders)
    margin = (net / gross * 100) if gross else 0.0
    print("\n=== ONLINE SELLER DASHBOARD (ambrosetheshield xdjzq clone) ===")
    print(f"  Orders logged:       {len(orders)}")
    print(f"  Gross sales:         £{gross:,.2f}")
    print(f"  Platform fees:       £{fees:,.2f}")
    print(f"  Postage + packaging: £{postage + packaging:,.2f}")
    print(f"  COGS:                £{cogs:,.2f}")
    print(f"  Net profit:          £{net:,.2f}")
    print(f"  Profit margin:       {margin:.1f}%")
    if margin < 20:
        print("  ⚠ Margin below 20% — raise prices, cut costs, or stop selling that SKU.")


def print_platform_summary(orders):
    by_platform = defaultdict(lambda: {"orders": 0, "gross": 0.0, "net": 0.0})
    for o in orders:
        p = by_platform[o["platform"]]
        p["orders"] += 1
        p["gross"] += o["sale_price"]
        p["net"] += o["net_profit"]
    print("\n=== PROFIT BY PLATFORM ===")
    for platform, stats in sorted(by_platform.items(), key=lambda x: x[1]["net"], reverse=True):
        print(
            f"  {platform:16} {stats['orders']:3} orders · gross £{stats['gross']:,.2f} · "
            f"net £{stats['net']:,.2f}"
        )


def print_worst_order(orders):
    if not orders:
        return
    worst = min(orders, key=lambda o: o["net_profit"])
    print("\n=== WORST ORDER (ambrosetheshield promise) ===")
    print(f"  {worst['date'].strftime('%Y-%m-%d')} · {worst['platform']} · {worst['item']}")
    print(f"  Sale £{worst['sale_price']:.2f} → net £{worst['net_profit']:.2f} ({worst['margin_pct']:.1f}% margin)")
    if worst["hourly_rate"] is not None:
        print(f"  Effective hourly:    £{worst['hourly_rate']:.2f}/hr")


def print_hourly_rates(orders):
    timed = [o for o in orders if o["hourly_rate"] is not None]
    if not timed:
        return
    avg_hourly = sum(o["hourly_rate"] for o in timed) / len(timed)
    lowest = min(timed, key=lambda o: o["hourly_rate"])
    print("\n=== EFFECTIVE HOURLY RATE ===")
    print(f"  Average across timed orders: £{avg_hourly:.2f}/hr")
    print(f"  Lowest: {lowest['item']} at £{lowest['hourly_rate']:.2f}/hr")


def pricing_calculator(cogs, postage, packaging, platform, target_profit=None, target_margin=None):
    fee_cfg = PLATFORM_FEES.get(platform.lower().replace(" ", "_"), PLATFORM_FEES["other"])
    fixed = postage + packaging + cogs
    if platform.lower() == "etsy":
        f = PLATFORM_FEES["etsy"]
        if target_profit is not None:
            # sale - listing - sale*tx% - sale*proc% - proc_flat - fixed = target
            rate = f["transaction_pct"] + f["processing_pct"]
            sale = (target_profit + fixed + f["listing"] + f["processing_flat"]) / (1 - rate)
            return round(sale, 2)
        if target_margin is not None:
            m = target_margin / 100
            rate = f["transaction_pct"] + f["processing_pct"]
            sale = (fixed + f["listing"] + f["processing_flat"]) / (1 - rate - m)
            return round(sale, 2)
    pct = fee_cfg.get("pct", 0)
    flat = fee_cfg.get("flat", 0)
    if target_profit is not None:
        sale = (target_profit + fixed + flat) / (1 - pct)
        return round(sale, 2)
    if target_margin is not None:
        m = target_margin / 100
        sale = (fixed + flat) / (1 - pct - m)
        return round(sale, 2)
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
        print(f"\n=== PRICING CALCULATOR (target profit £{target:.2f}) ===")
        print(f"  Platform: {platform}")
        print(f"  Charge at least: £{sale:.2f}")
        return True
    if "--price-margin" in args:
        idx = args.index("--price-margin")
        margin = float(args[idx + 1])
        cogs = float(args[idx + 2])
        postage = float(args[idx + 3])
        packaging = float(args[idx + 4])
        platform = args[idx + 5] if len(args) > idx + 5 else "etsy"
        sale = pricing_calculator(cogs, postage, packaging, platform, target_margin=margin)
        print(f"\n=== PRICING CALCULATOR (target margin {margin:.0f}%) ===")
        print(f"  Platform: {platform}")
        print(f"  Charge at least: £{sale:.2f}")
        return True
    return False


def main():
    args = sys.argv[1:]
    if print_pricing_modes(args):
        return
    if not args:
        print("Usage: multi_platform_seller_tracker.py orders.csv")
        print("       multi_platform_seller_tracker.py --price-profit 8 6 3 1 etsy")
        print("       multi_platform_seller_tracker.py --price-margin 40 6 3 1 vinted")
        sys.exit(1)
    orders = load_orders(args[0])
    print_dashboard(orders)
    print_platform_summary(orders)
    print_worst_order(orders)
    print_hourly_rates(orders)


if __name__ == "__main__":
    main()
