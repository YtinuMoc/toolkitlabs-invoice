#!/usr/bin/env python3
"""Gumroad CSV → bulk invoice HTML (clone of csv2invoice.com Gumroad flow).

Export: Gumroad → Customers → Export CSV.
Purchase batch CLI pack (EUR 9, one-time):
https://buy.stripe.com/dRm9AUgpwb648Jg7NX5Ne0l?client_reference_id=gumroad-batch-py
"""
from __future__ import annotations

import argparse
import csv
import html
import re
import sys
from pathlib import Path

from invoice_batch import TEMPLATE_HEAD, TEMPLATE_TAIL, money, render_invoice

GUMROAD_MAP = {
    "invoice_number": lambda r: f"GR-{r.get('ID', r.get('id', '0001'))[:12]}",
    "seller_name": lambda r: r.get("seller_name", "Your Business"),
    "seller_address": lambda r: r.get("seller_address", ""),
    "seller_email": lambda r: r.get("seller_email", r.get("Email", "")),
    "seller_tax": lambda r: r.get("seller_tax", r.get("Customer Tax ID", "")),
    "buyer_name": lambda r: r.get("buyer_name", r.get("Buyer Email", "Customer")),
    "buyer_address": lambda r: r.get("buyer_address", r.get("Country", "")),
    "buyer_email": lambda r: r.get("Buyer Email", r.get("Email", "")),
    "invoice_date": lambda r: (r.get("Sale Timestamp", r.get("invoice_date", "")) or "")[:10],
    "due_date": lambda r: (r.get("Sale Timestamp", r.get("invoice_date", "")) or "")[:10],
    "tax_rate": lambda r: _tax_rate(r),
    "notes": lambda r: _notes(r),
    "items": lambda r: _items(r),
}


def _tax_rate(row: dict) -> str:
    try:
        sub = float(row.get("Subtotal", 0) or 0)
        tax = float(row.get("Tax", 0) or 0)
        if sub > 0 and tax > 0:
            return str(round(100 * tax / sub, 2))
    except ValueError:
        pass
    return row.get("tax_rate", "0")


def _notes(row: dict) -> str:
    parts = []
    if row.get("Fully Refunded?", "").lower().startswith("y"):
        parts.append("REFUNDED")
    if row.get("Recurrence"):
        parts.append(f"Recurrence: {row['Recurrence']}")
    if row.get("Variant"):
        parts.append(f"Variant: {row['Variant']}")
    ref = row.get("ID", "")
    if ref:
        parts.append(f"Gumroad sale ID: {ref}")
    return ". ".join(parts)


def _items(row: dict) -> str:
    name = row.get("Product Name", "Gumroad sale")
    qty = row.get("Quantity", "1") or "1"
    price = row.get("Subtotal") or row.get("Sale Price ($)") or row.get("Sale Price") or "0"
    try:
        unit = float(re.sub(r"[^\d.]", "", str(price))) / max(float(qty), 1)
    except ValueError:
        unit = 0
    return f"{name};{qty};{unit:.2f}"


def gumroad_row_to_invoice(row: dict, seller_defaults: dict) -> dict:
    out = dict(seller_defaults)
    for key, fn in GUMROAD_MAP.items():
        out[key] = fn({**seller_defaults, **row})
    return out


def main() -> int:
    p = argparse.ArgumentParser(description="Gumroad CSV → invoice HTML batch")
    p.add_argument("csv_path", type=Path)
    p.add_argument("-o", "--output", type=Path, default=Path("./gumroad-output"))
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
        inv = gumroad_row_to_invoice(row, seller)
        body = render_invoice(inv)
        slug = re.sub(r"[^\w-]", "", inv.get("invoice_number", f"inv-{i}"))
        out = args.output / f"{slug or f'invoice-{i}'}.html"
        out.write_text(body, encoding="utf-8")
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
