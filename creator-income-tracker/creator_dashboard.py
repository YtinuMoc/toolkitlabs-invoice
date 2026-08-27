#!/usr/bin/env python3
"""Digital Product Creator Income Tracker — clone of PattyBun rauxja ($14.99 Gumroad)."""
import csv
import re
import sys
from collections import defaultdict
from datetime import datetime, timedelta

PLATFORM_FEES = {
    "gumroad": lambda g: g * 0.10 + 0.50,
    "etsy": lambda g: g * 0.065 + g * 0.03,
    "shopify": lambda g: g * 0.029 + 0.30,
    "payhip": lambda g: g * 0.05,
    "other": lambda g: 0.0,
}
SE_TAX_RATE = 0.153
SE_TAXABLE_RATIO = 0.9235
INCOME_TAX_RESERVE_PCT = 12.0


def parse_fee_override(notes):
    m = re.search(r"fee=([\d.]+)", notes or "", re.I)
    return float(m.group(1)) if m else None


def load_rows(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                gross = float(row["gross"])
            except (KeyError, ValueError):
                continue
            try:
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except ValueError:
                continue
            platform = row.get("platform", "other").strip().lower() or "other"
            override = parse_fee_override(row.get("notes", ""))
            if override is not None:
                fee = override
            else:
                fn = PLATFORM_FEES.get(platform, PLATFORM_FEES["other"])
                fee = fn(gross)
            rows.append({
                "date": dt,
                "platform": platform,
                "product": row.get("product", "unknown").strip() or "unknown",
                "gross": gross,
                "fee": round(fee, 2),
                "net": round(gross - fee, 2),
                "notes": row.get("notes", "").strip(),
                "launch": "launch" in (row.get("notes", "") or "").lower(),
            })
    return rows


def quarter_key(dt):
    return f"{dt.year}-Q{(dt.month - 1) // 3 + 1}"


def print_dashboard(rows):
    gross = sum(r["gross"] for r in rows)
    fees = sum(r["fee"] for r in rows)
    net = sum(r["net"] for r in rows)
    by_platform = defaultdict(float)
    by_product = defaultdict(lambda: {"units": 0, "gross": 0.0, "net": 0.0})
    for r in rows:
        by_platform[r["platform"]] += r["net"]
        p = by_product[r["product"]]
        p["units"] += 1
        p["gross"] += r["gross"]
        p["net"] += r["net"]
    best_platform = max(by_platform, key=by_platform.get) if by_platform else "n/a"
    best_product = max(by_product, key=lambda k: by_product[k]["net"]) if by_product else "n/a"
    print("\n=== DASHBOARD (PattyBun rauxja clone) ===")
    print(f"  Sales logged: {len(rows)}")
    print(f"  YTD gross: ${gross:,.2f}")
    print(f"  YTD fees:  ${fees:,.2f}")
    print(f"  YTD net:   ${net:,.2f}")
    print(f"  Best platform (net): {best_platform} (${by_platform.get(best_platform, 0):,.2f})")
    print(f"  Best product (net):  {best_product} (${by_product[best_product]['net']:,.2f})")


def effective_fee_pct(gross, fee):
    return (fee / gross * 100) if gross else 0.0


def print_platform_summary(rows):
    monthly = defaultdict(lambda: defaultdict(lambda: {"gross": 0.0, "fee": 0.0, "net": 0.0}))
    totals = defaultdict(lambda: {"gross": 0.0, "fee": 0.0, "net": 0.0})
    for r in rows:
        mk = r["date"].strftime("%Y-%m")
        for bucket in (monthly[mk][r["platform"]], totals[r["platform"]]):
            bucket["gross"] += r["gross"]
            bucket["fee"] += r["fee"]
            bucket["net"] += r["net"]
    print("\n=== PLATFORM SUMMARY (PattyBun tab 3) ===")
    eff_by_platform = {}
    for platform in sorted(totals):
        t = totals[platform]
        eff = effective_fee_pct(t["gross"], t["fee"])
        eff_by_platform[platform] = eff
        print(
            f"  {platform:10s}  gross ${t['gross']:8,.2f}  fees ${t['fee']:7,.2f}  "
            f"net ${t['net']:8,.2f}  eff fee {eff:5.1f}%"
        )
    if eff_by_platform:
        worst = max(eff_by_platform, key=eff_by_platform.get)
        best = min(eff_by_platform, key=eff_by_platform.get)
        print(f"\n  Highest fee drag: {worst} ({eff_by_platform[worst]:.1f}% of gross)")
        print(f"  Lowest fee drag:  {best} ({eff_by_platform[best]:.1f}% of gross)")
    print("\n  Monthly net by platform:")
    for mk in sorted(monthly):
        parts = ", ".join(f"{p} ${d['net']:,.2f}" for p, d in sorted(monthly[mk].items()))
        print(f"    {mk}: {parts}")


def print_product_performance(rows):
    perf = defaultdict(lambda: {"units": 0, "gross": 0.0, "net": 0.0, "platforms": set(), "last": None})
    for r in rows:
        p = perf[r["product"]]
        p["units"] += 1
        p["gross"] += r["gross"]
        p["net"] += r["net"]
        p["platforms"].add(r["platform"])
        if p["last"] is None or r["date"] > p["last"]:
            p["last"] = r["date"]
    anchor = max(r["date"] for r in rows) if rows else None
    ranked = sorted(perf, key=lambda k: perf[k]["net"], reverse=True)
    print("\n=== PRODUCT PERFORMANCE (PattyBun tab 4) ===")
    for rank, product in enumerate(ranked, 1):
        p = perf[product]
        plats = ",".join(sorted(p["platforms"]))
        last = p["last"].strftime("%Y-%m-%d") if p["last"] else "n/a"
        margin = (p["net"] / p["gross"] * 100) if p["gross"] else 0.0
        days_ago = (anchor - p["last"]).days if anchor and p["last"] else None
        stale = f"  ({days_ago}d ago)" if days_ago is not None else ""
        print(
            f"  #{rank} {product:20s}  units {p['units']:3d}  gross ${p['gross']:8,.2f}  "
            f"net ${p['net']:8,.2f}  margin {margin:5.1f}%  platforms [{plats}]  last {last}{stale}"
        )
    if len(ranked) >= 2:
        top, bottom = ranked[0], ranked[-1]
        t, b = perf[top], perf[bottom]
        print(f"\n  Top earner: {top} (${t['net']:,.2f} net) · Lowest net: {bottom} (${b['net']:,.2f})")


def launch_window_totals(sales, start, days):
    end = start + timedelta(days=days - 1)
    window = [s for s in sales if start <= s["date"] <= end]
    return window, sum(s["gross"] for s in window), sum(s["net"] for s in window)


def launch_outcome(net_7d):
    if net_7d >= 200:
        return "strong"
    if net_7d >= 50:
        return "ok"
    if net_7d > 0:
        return "weak"
    return "no traction"


def print_launch_tracker(rows):
    launches = [r for r in rows if r["launch"]]
    print("\n=== LAUNCH TRACKER (PattyBun tab 5 — 7-day + 30-day windows) ===")
    if not launches:
        print("  No launch-tagged rows. Add 'launch' to notes on first-week sales.")
        return
    by_product = defaultdict(list)
    for r in launches:
        by_product[r["product"]].append(r)
    for product, sales in sorted(by_product.items()):
        sales.sort(key=lambda s: s["date"])
        start = sales[0]["date"]
        w7, gross7, net7 = launch_window_totals(sales, start, 7)
        w30, gross30, net30 = launch_window_totals(sales, start, 30)
        promo = next((s["notes"] for s in sales if s["notes"] and "launch" not in s["notes"].lower()), "")
        print(f"  {product}:")
        print(f"    launch start: {start.strftime('%Y-%m-%d')}  promo: {promo or 'n/a'}")
        print(f"    7-day:  {len(w7):2d} sales  gross ${gross7:8,.2f}  net ${net7:8,.2f}  outcome {launch_outcome(net7)}")
        print(f"    30-day: {len(w30):2d} sales  gross ${gross30:8,.2f}  net ${net30:8,.2f}")


def quarterly_tax_lines(net):
    se_base = net * SE_TAXABLE_RATIO
    se_tax = se_base * SE_TAX_RATE
    income_reserve = net * (INCOME_TAX_RESERVE_PCT / 100)
    payment = se_tax + income_reserve
    return se_tax, income_reserve, payment


def print_tax_summary(rows):
    quarterly = defaultdict(float)
    for r in rows:
        quarterly[quarter_key(r["date"])] += r["net"]
    print("\n=== TAX & ANNUAL SUMMARY (PattyBun tab 6 — SE + income reserve) ===")
    ytd_net = sum(r["net"] for r in rows)
    ytd_se = ytd_income = ytd_payment = 0.0
    print(f"  YTD net revenue: ${ytd_net:,.2f}")
    print(f"  Defaults: SE {SE_TAX_RATE * 100:.1f}% on {SE_TAXABLE_RATIO * 100:.2f}% of net · income reserve {INCOME_TAX_RESERVE_PCT:.0f}%")
    print("\n  Quarter        net revenue   SE tax est.   income reserve   suggested payment")
    for q in sorted(quarterly):
        net = quarterly[q]
        se_tax, income_reserve, payment = quarterly_tax_lines(net)
        ytd_se += se_tax
        ytd_income += income_reserve
        ytd_payment += payment
        print(
            f"  {q:12s}  ${net:10,.2f}  ${se_tax:10,.2f}  ${income_reserve:14,.2f}  ${payment:16,.2f}"
        )
    print(
        f"\n  YTD totals: SE tax ${ytd_se:,.2f} · income reserve ${ytd_income:,.2f} · "
        f"suggested payments ${ytd_payment:,.2f}"
    )


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "sample-revenue.csv"
    rows = load_rows(path)
    if not rows:
        print("No rows loaded.", file=sys.stderr)
        sys.exit(1)
    print(f"Loaded {len(rows)} sales from {path}")
    print_dashboard(rows)
    print_platform_summary(rows)
    print_product_performance(rows)
    print_launch_tracker(rows)
    print_tax_summary(rows)
    print("\nClone target: pattybun.gumroad.com/l/rauxja ($14.99)")


if __name__ == "__main__":
    main()
