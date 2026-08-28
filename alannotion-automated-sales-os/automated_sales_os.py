#!/usr/bin/env python3
"""Automated Sales OS — clone of alannotion.gumroad.com/l/automatedsalesos ($15 · creator 5★/20 reviews)."""
from __future__ import annotations

import argparse
import csv
import sys
from collections import defaultdict
from datetime import datetime
from pathlib import Path

FIELDS = [
    "date",
    "platform",
    "transaction_id",
    "description",
    "category",
    "amount",
    "fee",
    "net",
    "buyer",
    "currency",
]


def _parse_date(raw: str) -> str:
    raw = (raw or "").strip()
    if not raw:
        return ""
    for fmt in ("%Y-%m-%d %H:%M:%S", "%Y-%m-%d %H:%M:%S UTC", "%Y-%m-%d"):
        try:
            return datetime.strptime(raw.replace(" UTC", ""), fmt.replace(" UTC", "")).strftime(
                "%Y-%m-%d"
            )
        except ValueError:
            continue
    return raw[:10]


def _money(raw: str | float | int) -> float:
    if raw is None or raw == "":
        return 0.0
    return float(str(raw).replace(",", "").replace("$", "").strip() or 0)


def parse_gumroad(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            subtotal = _money(row.get("Subtotal") or row.get("Sale Price") or row.get("Sale Price ($)"))
            tax = _money(row.get("Tax"))
            gross = subtotal + tax if subtotal else _money(row.get("Sale Price ($)"))
            fee = max(0.0, gross * 0.10) if gross else 0.0
            refunded = str(row.get("Fully Refunded?", "")).lower() in {"yes", "true", "1"}
            product = row.get("Product Name", "Gumroad sale")
            amount = -gross if refunded else gross
            net = amount - (0 if refunded else fee)
            rows.append(
                {
                    "date": _parse_date(row.get("Sale Timestamp", "")),
                    "platform": "gumroad",
                    "transaction_id": row.get("ID", ""),
                    "description": product,
                    "category": "Refund" if refunded else "Product Revenue",
                    "amount": f"{amount:.2f}",
                    "fee": f"{(0 if refunded else fee):.2f}",
                    "net": f"{net:.2f}",
                    "buyer": row.get("Buyer Email", row.get("Email", "")),
                    "currency": "USD",
                }
            )
    return rows


def parse_stripe(path: Path) -> list[dict]:
    rows: list[dict] = []
    with path.open(newline="", encoding="utf-8-sig") as f:
        for row in csv.DictReader(f):
            gross = _money(row.get("Amount"))
            fee = _money(row.get("Fee"))
            net = _money(row.get("Net")) or (gross - fee)
            refunded = _money(row.get("Amount Refunded")) > 0
            status = (row.get("Status") or "").lower()
            desc = row.get("Description", "Stripe payment")
            amount = gross if not refunded else -gross
            rows.append(
                {
                    "date": _parse_date(row.get("Created (UTC)", row.get("Created", ""))),
                    "platform": "stripe",
                    "transaction_id": row.get("id", row.get("ID", "")),
                    "description": desc,
                    "category": "Refund" if refunded or status == "refunded" else "Product Revenue",
                    "amount": f"{amount:.2f}",
                    "fee": f"{fee:.2f}",
                    "net": f"{net:.2f}",
                    "buyer": row.get("Customer Email", ""),
                    "currency": (row.get("Currency") or "eur").upper(),
                }
            )
    return rows


def detect_platform(path: Path) -> str:
    with path.open(newline="", encoding="utf-8-sig") as f:
        headers = {h.strip().lower() for h in (csv.reader(f).__next__() or [])}
    if "sale timestamp" in headers or "product name" in headers:
        return "gumroad"
    if "created (utc)" in headers or "customer email" in headers:
        return "stripe"
    raise ValueError(f"unknown CSV format: {path}")


def load_sales(paths: list[Path]) -> list[dict]:
    rows: list[dict] = []
    for path in paths:
        platform = detect_platform(path)
        rows.extend(parse_gumroad(path) if platform == "gumroad" else parse_stripe(path))
    return sorted(rows, key=lambda r: r["date"])


def print_daily_dashboard(rows: list[dict]) -> None:
    by_day: dict[str, float] = defaultdict(float)
    for row in rows:
        if row["category"] != "Product Revenue":
            continue
        by_day[row["date"]] += _money(row["net"])
    print("=== DAILY REVENUE (Automated Sales OS shape) ===")
    for day in sorted(by_day)[-7:]:
        print(f"  {day}  ${by_day[day]:>8,.2f}")


def print_weekly_dashboard(rows: list[dict]) -> None:
    by_week: dict[str, float] = defaultdict(float)
    for row in rows:
        if row["category"] != "Product Revenue":
            continue
        try:
            dt = datetime.strptime(row["date"], "%Y-%m-%d")
            key = dt.strftime("%Y-W%W")
        except ValueError:
            continue
        by_week[key] += _money(row["net"])
    print("=== WEEKLY TREND ===")
    for week in sorted(by_week)[-4:]:
        print(f"  {week}  ${by_week[week]:>8,.2f}")


def print_monthly_products(rows: list[dict]) -> None:
    by_month: dict[str, float] = defaultdict(float)
    by_product: dict[str, float] = defaultdict(float)
    for row in rows:
        if row["category"] != "Product Revenue":
            continue
        month = row["date"][:7] if row.get("date") else "unknown"
        by_month[month] += _money(row["net"])
        by_product[row["description"]] += _money(row["net"])
    print("=== MONTHLY SUMMARY ===")
    for month in sorted(by_month):
        print(f"  {month}  ${by_month[month]:>8,.2f}")
    print("=== BEST-SELLING PRODUCTS ===")
    for product, total in sorted(by_product.items(), key=lambda x: -x[1])[:5]:
        print(f"  {product[:40]:40}  ${total:>8,.2f}")


DEFAULT_TAX_PCT = 25.0
SE_IF_TAX = 0.153  # self-employment tax approximation (marginmap/14ag)


def print_net_income(rows: list[dict], reserve_pct: float = DEFAULT_TAX_PCT) -> None:
    """faisalmq/5797 shape — safe-to-spend after fees + tax reserve."""
    sales = [r for r in rows if r["category"] == "Product Revenue" and _money(r["net"]) > 0]
    gross = sum(_money(r["amount"]) for r in sales)
    fees = sum(_money(r["fee"]) for r in sales)
    net_profit = sum(_money(r["net"]) for r in sales)
    tax_set_aside = max(net_profit, 0) * reserve_pct / 100
    safe = max(net_profit - tax_set_aside, 0)
    take_home_rate = (safe / gross * 100) if gross else 0.0
    print("=== NET INCOME VISIBILITY (faisalmq/5797 shape) ===")
    print(f"  Gross collected:       ${gross:,.2f}")
    print(f"  Platform fees:         ${fees:,.2f}")
    print(f"  Net profit:            ${net_profit:,.2f}")
    print(f"  Tax set-aside ({reserve_pct:.0f}%):   ${tax_set_aside:,.2f}")
    print(f"  Safe to spend:         ${safe:,.2f}")
    print(f"  Take-home rate:        {take_home_rate:.1f}% of gross deposits")
    print("  Guide: net-income-guide.md · gumroad-sample.csv · stripe-sample.csv")


def print_take_home(rows: list[dict], reserve_pct: float = 28.0, state_rate: float = 4.4) -> None:
    """marginmap/14ag shape — gross sales → fees → SE tax → real take-home."""
    sales = [r for r in rows if r["category"] == "Product Revenue" and _money(r["amount"]) > 0]
    gross = sum(_money(r["amount"]) for r in sales)
    fees = sum(_money(r["fee"]) for r in sales)
    net = gross - fees
    se_tax = max(net, 0) * SE_IF_TAX
    se_deduction = se_tax * 0.5
    agi = max(net - se_deduction, 0)
    std_deduction = 15000.0
    taxable = max(agi - std_deduction, 0)
    federal = taxable * 0.113
    state = taxable * (state_rate / 100.0)
    total_tax = se_tax + federal + state
    take_home = max(net - total_tax, 0)
    effective = (total_tax / gross * 100) if gross else 0.0
    print("=== TAKE-HOME ESTIMATE (marginmap/14ag shape) ===")
    print("  Digital product sales ≠ what you keep after SE + income tax.")
    print(f"  Gross revenue:         ${gross:,.2f}")
    print(f"  Platform fees:         ${fees:,.2f}")
    print(f"  Net self-employment:   ${net:,.2f}")
    print(f"  SE tax (~15.3%):       ${se_tax:,.2f}")
    print(f"  Federal income (est.): ${federal:,.2f}")
    print(f"  State tax ({state_rate}%):     ${state:,.2f}")
    print(f"  Total taxes:           ${total_tax:,.2f}")
    print(f"  Take-home:             ${take_home:,.2f}")
    print(f"  Effective rate:        {effective:.1f}% of gross")
    print(f"  Reserve shortcut:      {reserve_pct:.0f}% of net → ${max(net, 0) * reserve_pct / 100:,.2f}")
    print("  Not tax advice. Confirm with a CPA.")
    print("  Guide: take-home-guide.md · gumroad-sample.csv · stripe-sample.csv")


def print_tax_buffer(rows: list[dict], reserve_pct: float = DEFAULT_TAX_PCT) -> None:
    """faisalmq/4gao shape for digital product sellers — buffer when sale revenue lands."""
    sales = [r for r in rows if r["category"] == "Product Revenue" and _money(r["net"]) > 0]
    net_total = sum(_money(r["net"]) for r in sales)
    tax_buffer = max(net_total, 0) * reserve_pct / 100
    safe = max(net_total - tax_buffer, 0)
    print("=== PER-SALE TAX BUFFER (faisalmq/4gao shape) ===")
    print("  Sale lands → five minutes of joy → tax panic → buffer same day.")
    print(f"  {'Product':<28} {'Net':>10} {'Buffer':>10} {'Safe':>12}")
    for row in sales:
        net = _money(row["net"])
        buf = net * reserve_pct / 100
        label = (row["description"] or row["platform"])[:28]
        print(f"  {label:<28} ${net:>8,.2f} ${buf:>8,.2f} ${net - buf:>10,.2f}")
    print()
    print("=== SALES REVENUE + TAX BUFFER ===")
    print(f"  Net sales (after fees): ${net_total:,.2f}")
    print(f"  Tax buffer ({reserve_pct:.0f}%):   ${tax_buffer:,.2f}")
    print(f"  Safe to spend:          ${safe:,.2f}")
    print("  Transfer buffer to tax-only savings when sale lands — not in April.")
    print("  Guide: tax-buffer-guide.md · gumroad-sample.csv · stripe-sample.csv")


def print_merge_summary(rows: list[dict], out_path: Path) -> None:
    gross = sum(_money(r["amount"]) for r in rows if r["category"] == "Product Revenue")
    fees = sum(_money(r["fee"]) for r in rows if r["category"] == "Product Revenue")
    net = sum(_money(r["net"]) for r in rows if r["category"] == "Product Revenue")
    print("=== UNIFIED SALES LEDGER (goldenalien/206o shape) ===")
    print(f"  Transactions:        {len(rows)}")
    print(f"  Gross:               ${gross:,.2f}")
    print(f"  Fees:                ${fees:,.2f}")
    print(f"  Net:                 ${net:,.2f}")
    print(f"  Wrote:               {out_path}")


def main() -> int:
    p = argparse.ArgumentParser(description="Automated Sales OS — merge Gumroad + Stripe sales CSVs.")
    p.add_argument("inputs", nargs="*", help="Gumroad and/or Stripe CSV exports")
    p.add_argument("-o", "--output", default="sales-ledger.csv", help="unified ledger CSV")
    p.add_argument(
        "--take-home",
        action="store_true",
        help="marginmap/14ag: take-home estimate from merged sales CSVs",
    )
    p.add_argument(
        "--net-income",
        action="store_true",
        help="faisalmq/5797: safe-to-spend visibility from merged sales CSVs",
    )
    p.add_argument(
        "--tax-buffer",
        action="store_true",
        help="faisalmq/4gao: per-sale tax buffer from merged sales CSVs",
    )
    p.add_argument(
        "--tax-pct",
        type=float,
        default=DEFAULT_TAX_PCT,
        help="tax reserve percentage (default 25)",
    )
    args = p.parse_args()

    if args.take_home:
        if not args.inputs:
            print("Usage: automated_sales_os.py --take-home gumroad.csv stripe.csv")
            return 1
        rows = load_sales([Path(inp) for inp in args.inputs])
        print_take_home(rows)
        return 0

    if args.net_income:
        if not args.inputs:
            print("Usage: automated_sales_os.py --net-income gumroad.csv stripe.csv")
            return 1
        rows = load_sales([Path(inp) for inp in args.inputs])
        print_net_income(rows, args.tax_pct)
        return 0

    if args.tax_buffer:
        if not args.inputs:
            print("Usage: automated_sales_os.py --tax-buffer gumroad.csv stripe.csv")
            return 1
        rows = load_sales([Path(inp) for inp in args.inputs])
        print_tax_buffer(rows, args.tax_pct)
        return 0

    if not args.inputs:
        p.print_help()
        return 1

    paths = [Path(inp) for inp in args.inputs]
    rows = load_sales(paths)
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(rows)

    print_merge_summary(rows, out)
    print_daily_dashboard(rows)
    print_weekly_dashboard(rows)
    print_monthly_products(rows)
    return 0


if __name__ == "__main__":
    sys.exit(main())
