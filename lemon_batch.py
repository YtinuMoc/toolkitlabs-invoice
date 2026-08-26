#!/usr/bin/env python3
"""Lemon Squeezy orders CSV → bulk invoice HTML (clone of csv2invoice.com Lemon Squeezy flow).

Export: Lemon Squeezy Dashboard → Orders → Export → CSV emailed to store owner.
Purchase batch CLI pack (EUR 9, one-time):
https://buy.stripe.com/dRm9AUgpwb648Jg7NX5Ne0l?client_reference_id=lemon-batch-py
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

from invoice_batch import render_invoice

LEMON_MAP = {
    "invoice_number": lambda r: f"LS-{r.get('order_number', r.get('identifier', '0001'))[:12]}",
    "seller_name": lambda r: r.get("seller_name", "Your Business"),
    "seller_address": lambda r: r.get("seller_address", ""),
    "seller_email": lambda r: r.get("seller_email", ""),
    "seller_tax": lambda r: r.get("seller_tax", ""),
    "buyer_name": lambda r: r.get("user_name", r.get("buyer_name", "Customer")),
    "buyer_address": lambda r: _buyer_address(r),
    "buyer_email": lambda r: r.get("user_email", ""),
    "invoice_date": lambda r: (r.get("date_utc", r.get("invoice_date", "")) or "")[:10],
    "due_date": lambda r: (r.get("date_utc", r.get("invoice_date", "")) or "")[:10],
    "tax_rate": lambda r: r.get("tax_rate", r.get("tax_rate", "0")) or "0",
    "notes": lambda r: _notes(r),
    "items": lambda r: _items(r),
}


def _amount(row: dict, key: str) -> float:
    try:
        return float(re.sub(r"[^\d.\-]", "", str(row.get(key, 0) or 0)))
    except ValueError:
        return 0.0


def _buyer_address(row: dict) -> str:
    parts = [
        row.get("city", ""),
        row.get("postal_code", ""),
        row.get("country", ""),
    ]
    return ", ".join(p for p in parts if p)


def _notes(row: dict) -> str:
    parts = []
    if row.get("tax_name"):
        parts.append(f"Tax: {row['tax_name']}")
    if row.get("tax_number"):
        parts.append(f"Tax number: {row['tax_number']}")
    if row.get("identifier"):
        parts.append(f"Lemon Squeezy order: {row['identifier']}")
    return ". ".join(parts)


def _items(row: dict) -> str:
    name = row.get("product_name", "Lemon Squeezy sale")
    variant = row.get("variant_name", "")
    if variant and variant != "Default":
        name = f"{name} ({variant})"
    sub = _amount(row, "subtotal")
    return f"{name};1;{sub:.2f}"


def lemon_row_to_invoice(row: dict, seller_defaults: dict) -> dict:
    out = dict(seller_defaults)
    for key, fn in LEMON_MAP.items():
        out[key] = fn({**seller_defaults, **row})
    return out


def main() -> int:
    p = argparse.ArgumentParser(description="Lemon Squeezy CSV → invoice HTML batch")
    p.add_argument("csv_path", type=Path)
    p.add_argument("-o", "--output", type=Path, default=Path("./lemon-output"))
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
        inv = lemon_row_to_invoice(row, seller)
        body = render_invoice(inv)
        slug = re.sub(r"[^\w-]", "", inv.get("invoice_number", f"inv-{i}"))
        out = args.output / f"{slug or f'invoice-{i}'}.html"
        out.write_text(body, encoding="utf-8")
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
