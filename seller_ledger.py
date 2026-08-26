#!/usr/bin/env python3
"""Merge Gumroad + Stripe CSV exports into one seller ledger with P&L summary.

Clone of SellerLedger (nexusai82.gumroad.com/l/kfyuh, $17) — same CSV → profit shape.
Purchase CLI pack (EUR 9, one-time):
https://buy.stripe.com/dRm9AUgpwb648Jg7NX5Ne0l?client_reference_id=seller-ledger-py
"""
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
            category = "Refund" if refunded else "Product Revenue"
            amount = -gross if refunded else gross
            net = amount - (0 if refunded else fee)
            rows.append(
                {
                    "date": _parse_date(row.get("Sale Timestamp", "")),
                    "platform": "gumroad",
                    "transaction_id": row.get("ID", ""),
                    "description": row.get("Product Name", "Gumroad sale"),
                    "category": category,
                    "amount": f"{amount:.2f}",
                    "fee": f"{(0 if refunded else fee):.2f}",
                    "net": f"{net:.2f}",
                    "buyer": row.get("Buyer Email", row.get("Email", "")),
                    "currency": "USD",
                }
            )
            if not refunded and fee:
                rows.append(
                    {
                        "date": _parse_date(row.get("Sale Timestamp", "")),
                        "platform": "gumroad",
                        "transaction_id": f"{row.get('ID', '')}-fee",
                        "description": f"Gumroad fee — {row.get('Product Name', '')}",
                        "category": "Platform Fee",
                        "amount": f"{-fee:.2f}",
                        "fee": "0.00",
                        "net": f"{-fee:.2f}",
                        "buyer": "",
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
            category = "Refund" if refunded or status == "refunded" else "Product Revenue"
            amount = gross if not refunded else -gross
            rows.append(
                {
                    "date": _parse_date(row.get("Created (UTC)", row.get("Created", ""))),
                    "platform": "stripe",
                    "transaction_id": row.get("id", row.get("ID", "")),
                    "description": row.get("Description", "Stripe payment"),
                    "category": category,
                    "amount": f"{amount:.2f}",
                    "fee": f"{fee:.2f}",
                    "net": f"{net:.2f}",
                    "buyer": row.get("Customer Email", ""),
                    "currency": (row.get("Currency") or "eur").upper(),
                }
            )
            if fee and not refunded:
                rows.append(
                    {
                        "date": _parse_date(row.get("Created (UTC)", row.get("Created", ""))),
                        "platform": "stripe",
                        "transaction_id": f"{row.get('id', row.get('ID', ''))}-fee",
                        "description": f"Stripe fee — {row.get('Description', '')}",
                        "category": "Platform Fee",
                        "amount": f"{-fee:.2f}",
                        "fee": "0.00",
                        "net": f"{-fee:.2f}",
                        "buyer": "",
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


def monthly_pnl(rows: list[dict]) -> dict[str, dict[str, float]]:
    """Monthly gross/fees/net — clone of Orion SellerLedger P&L Dashboard tab."""
    by_month: dict[str, dict[str, float]] = defaultdict(
        lambda: {"gross_revenue": 0.0, "platform_fees": 0.0, "refunds": 0.0, "net_profit": 0.0}
    )
    for row in rows:
        month = row["date"][:7] if row.get("date") else "unknown"
        cat = row["category"]
        if cat == "Product Revenue":
            by_month[month]["gross_revenue"] += _money(row["amount"])
        elif cat == "Platform Fee":
            by_month[month]["platform_fees"] += abs(_money(row["net"]))
        elif cat == "Refund":
            by_month[month]["refunds"] += _money(row["net"])
    for month, m in by_month.items():
        m["net_profit"] = m["gross_revenue"] - m["platform_fees"] + m["refunds"]
    return dict(sorted(by_month.items()))


def print_import_summary(summaries: list[dict]) -> None:
    """Per-file import counts — clone of Orion Apps Script Auto-Importer stdout."""
    print("--- CSV Auto-Importer (Gumroad + Stripe) ---")
    for s in summaries:
        print(
            f"{s['filename']} ({s['platform']}): "
            f"{s['rows']} rows imported, categorized automatically"
        )
    print("Supported: Gumroad payout export + Stripe payments export (mid-2026 column shapes).")


def print_mapping_rules() -> None:
    """Stdout mapping table — clone of Orion SellerLedger pre-built category rules."""
    print("--- Category mapping (Gumroad + Stripe CSV) ---")
    print("Gumroad sale row        → Product Revenue")
    print("Gumroad fee (10% est.)  → Platform Fee")
    print("Gumroad refund          → Refund")
    print("Stripe payment row      → Product Revenue")
    print("Stripe processing fee   → Platform Fee")
    print("Stripe refund           → Refund")
    print("Manual rows in ledger.csv: Ad Spend, Software, Contractors")


def category_breakdown(rows: list[dict]) -> dict[str, dict[str, float]]:
    """Per-category counts and net totals — clone of Orion Transactions Log tab."""
    by_cat: dict[str, dict[str, float]] = defaultdict(lambda: {"count": 0, "net": 0.0})
    for row in rows:
        cat = row["category"]
        by_cat[cat]["count"] += 1
        by_cat[cat]["net"] += _money(row["net"])
    return dict(sorted(by_cat.items()))


def summarize(rows: list[dict]) -> dict[str, float]:
    totals: dict[str, float] = defaultdict(float)
    for row in rows:
        cat = row["category"]
        totals[cat] += _money(row["net"])
    totals["net_profit"] = sum(_money(r["net"]) for r in rows if r["category"] != "Platform Fee") + sum(
        _money(r["net"]) for r in rows if r["category"] == "Platform Fee"
    )
    totals["gross_revenue"] = sum(
        _money(r["amount"]) for r in rows if r["category"] == "Product Revenue"
    )
    totals["platform_fees"] = abs(
        sum(_money(r["net"]) for r in rows if r["category"] == "Platform Fee")
    )
    totals["net_profit"] = totals["gross_revenue"] - totals["platform_fees"] + sum(
        _money(r["net"]) for r in rows if r["category"] == "Refund"
    )
    return dict(totals)


def main() -> int:
    p = argparse.ArgumentParser(description="Merge Gumroad/Stripe CSVs into a seller ledger.")
    p.add_argument("inputs", nargs="+", help="Gumroad and/or Stripe CSV exports")
    p.add_argument("-o", "--output", default="ledger.csv", help="output ledger CSV path")
    p.add_argument("--tax-rate", type=float, default=0.28, help="set-aside rate for summary (default 0.28)")
    args = p.parse_args()

    all_rows: list[dict] = []
    import_summaries: list[dict] = []
    for inp in args.inputs:
        path = Path(inp)
        platform = detect_platform(path)
        if platform == "gumroad":
            file_rows = parse_gumroad(path)
        else:
            file_rows = parse_stripe(path)
        all_rows.extend(file_rows)
        import_summaries.append(
            {"filename": path.name, "platform": platform, "rows": len(file_rows)}
        )

    all_rows.sort(key=lambda r: r["date"])
    out = Path(args.output)
    out.parent.mkdir(parents=True, exist_ok=True)
    with out.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=FIELDS)
        w.writeheader()
        w.writerows(all_rows)

    s = summarize(all_rows)
    months = monthly_pnl(all_rows)
    cats = category_breakdown(all_rows)
    set_aside = s["net_profit"] * args.tax_rate
    print_import_summary(import_summaries)
    print_mapping_rules()
    print(f"Wrote {len(all_rows)} rows → {out}")
    print(f"Gross revenue:   {s['gross_revenue']:.2f}")
    print(f"Platform fees:   {s['platform_fees']:.2f}")
    print(f"Net profit:      {s['net_profit']:.2f}")
    print(f"Set-aside @{args.tax_rate:.0%}: {set_aside:.2f}")
    if cats:
        print("--- Transactions Log (by category) ---")
        for cat, c in cats.items():
            print(f"{cat:20} count={int(c['count']):>3}  net={c['net']:>9.2f}")
        print(
            "Manual categories (add rows in ledger.csv): "
            "Ad Spend, Software, Contractors — same shape as Orion's sheet."
        )
    if months:
        print("--- P&L Dashboard (monthly) ---")
        for month, m in months.items():
            print(
                f"{month}  Gross: {m['gross_revenue']:>8.2f}  "
                f"Fees: {m['platform_fees']:>7.2f}  Net: {m['net_profit']:>8.2f}"
            )
        print("Annual total above matches gross/fees/net summary.")
    print("--- Tax-prep summary (US Schedule C organizer, 2026) ---")
    print(f"Line 1  Gross receipts/sales: {s['gross_revenue']:.2f}")
    print(f"Line 28 Total expenses:      {s['platform_fees']:.2f}")
    print(f"Line 31 Net profit (loss):    {s['net_profit']:.2f}")
    print("Data organizer for your accountant — not tax advice.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
