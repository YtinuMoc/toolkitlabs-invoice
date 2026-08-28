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
    p.add_argument("inputs", nargs="+", help="Gumroad and/or Stripe CSV exports")
    p.add_argument("-o", "--output", default="sales-ledger.csv", help="unified ledger CSV")
    args = p.parse_args()

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
