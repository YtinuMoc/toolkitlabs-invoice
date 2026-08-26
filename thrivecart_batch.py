#!/usr/bin/env python3
"""ThriveCart transactions CSV → bulk invoice HTML (clone of csv2invoice.com ThriveCart flow).

Export: ThriveCart dashboard → Transactions → filters → Download CSV.
Purchase batch CLI pack (EUR 9, one-time):
https://buy.stripe.com/dRm9AUgpwb648Jg7NX5Ne0l?client_reference_id=thrivecart-batch-py
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

from invoice_batch import render_invoice

THRIVECART_MAP = {
    "invoice_number": lambda r: f"TC-{r.get('Transaction ID', '0001')[:16]}",
    "seller_name": lambda r: r.get("seller_name", "Your Business"),
    "seller_address": lambda r: r.get("seller_address", ""),
    "seller_email": lambda r: r.get("seller_email", ""),
    "seller_tax": lambda r: r.get("seller_tax", ""),
    "buyer_name": lambda r: r.get("Customer Name", r.get("buyer_name", "Customer")),
    "buyer_address": lambda r: r.get("Country", r.get("buyer_address", "")),
    "buyer_email": lambda r: r.get("Customer Email", ""),
    "invoice_date": lambda r: (r.get("Date", r.get("invoice_date", "")) or "")[:10],
    "due_date": lambda r: (r.get("Date", r.get("invoice_date", "")) or "")[:10],
    "tax_rate": lambda r: _tax_rate(r),
    "notes": lambda r: _notes(r),
    "items": lambda r: _items(r),
}


def _amount(row: dict, key: str) -> float:
    try:
        return float(re.sub(r"[^\d.\-]", "", str(row.get(key, 0) or 0)))
    except ValueError:
        return 0.0


def _tax_rate(row: dict) -> str:
    amt = _amount(row, "Amount")
    tax = _amount(row, "Tax Amount")
    if amt > 0 and tax > 0:
        return str(round(100 * tax / amt, 2))
    return row.get("tax_rate", "0")


def _notes(row: dict) -> str:
    parts = []
    if row.get("Payment Status"):
        parts.append(f"Status: {row['Payment Status']}")
    if row.get("Payment Processor"):
        parts.append(f"Processor: {row['Payment Processor']}")
    if row.get("Subscription ID"):
        parts.append(f"Subscription: {row['Subscription ID']} ({row.get('Subscription Status', '')})")
    if row.get("Coupon Code"):
        parts.append(f"Coupon: {row['Coupon Code']}")
    if _amount(row, "Refund Amount") > 0:
        parts.append("REFUNDED")
    if row.get("Transaction ID"):
        parts.append(f"ThriveCart transaction: {row['Transaction ID']}")
    return ". ".join(parts)


def _items(row: dict) -> str:
    title = row.get("Product Name") or "ThriveCart sale"
    amt = _amount(row, "Amount")
    return f"{title};1;{amt:.2f}"


def thrivecart_row_to_invoice(row: dict, seller_defaults: dict) -> dict:
    out = dict(seller_defaults)
    for key, fn in THRIVECART_MAP.items():
        out[key] = fn({**seller_defaults, **row})
    return out


def main() -> int:
    p = argparse.ArgumentParser(description="ThriveCart CSV → invoice HTML batch")
    p.add_argument("csv_path", type=Path)
    p.add_argument("-o", "--output", type=Path, default=Path("./thrivecart-output"))
    p.add_argument("--seller-name", default="Your Business")
    p.add_argument("--seller-address", default="")
    p.add_argument("--seller-email", default="")
    p.add_argument("--seller-tax", default="")
    args = p.parse_args()
    seller = {
        "seller_name": args.seller_name,
        "seller_address": args.seller_address,
        "seller_email": args.seller_email,
        "seller_tax": args.seller_tax,
    }
    args.output.mkdir(parents=True, exist_ok=True)
    with args.csv_path.open(newline="", encoding="utf-8-sig") as f:
        rows = list(csv.DictReader(f))
    if not rows:
        print("No rows in CSV", file=sys.stderr)
        return 1
    for i, row in enumerate(rows, 1):
        inv = thrivecart_row_to_invoice(row, seller)
        body = render_invoice(inv)
        slug = re.sub(r"[^\w-]", "", inv.get("invoice_number", f"inv-{i}"))
        out = args.output / f"{slug or f'invoice-{i}'}.html"
        out.write_text(body, encoding="utf-8")
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
