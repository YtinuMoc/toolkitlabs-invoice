#!/usr/bin/env python3
"""Shopify orders CSV → bulk invoice HTML (clone of csv2invoice.com Shopify flow).

Export: Shopify Admin → Orders → Export → CSV.
Purchase batch CLI pack (EUR 9, one-time):
https://buy.stripe.com/dRm9AUgpwb648Jg7NX5Ne0l?client_reference_id=shopify-batch-py
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

from invoice_batch import render_invoice

SHOPIFY_MAP = {
    "invoice_number": lambda r: f"SH-{re.sub(r'[^A-Za-z0-9]', '', r.get('Name', r.get('name', '0001')))[:16]}",
    "seller_name": lambda r: r.get("seller_name", "Your Business"),
    "seller_address": lambda r: r.get("seller_address", ""),
    "seller_email": lambda r: r.get("seller_email", ""),
    "seller_tax": lambda r: r.get("seller_tax", ""),
    "buyer_name": lambda r: r.get("buyer_name", r.get("Billing Name", r.get("Email", "Customer"))),
    "buyer_address": lambda r: _buyer_address(r),
    "buyer_email": lambda r: r.get("Email", ""),
    "invoice_date": lambda r: (r.get("Paid at", r.get("Created at", r.get("invoice_date", ""))) or "")[:10],
    "due_date": lambda r: (r.get("Paid at", r.get("Created at", r.get("invoice_date", ""))) or "")[:10],
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
    sub = _amount(row, "Subtotal")
    tax = _amount(row, "Taxes")
    if sub > 0 and tax > 0:
        return str(round(100 * tax / sub, 2))
    return row.get("tax_rate", "0")


def _buyer_address(row: dict) -> str:
    parts = [
        row.get("Billing Address1", row.get("Billing Street", "")),
        row.get("Billing Address2", ""),
        row.get("Billing City", ""),
        row.get("Billing Province", ""),
        row.get("Billing Zip", ""),
        row.get("Billing Country", ""),
    ]
    return ", ".join(p for p in parts if p)


def _notes(row: dict) -> str:
    parts = []
    status = row.get("Financial Status", "")
    if status and status.lower() not in ("paid", "partially_paid"):
        parts.append(f"Financial status: {status}")
    if row.get("Fulfillment Status"):
        parts.append(f"Fulfillment: {row['Fulfillment Status']}")
    if row.get("Name"):
        parts.append(f"Shopify order: {row['Name']}")
    return ". ".join(parts)


def _items(row: dict) -> str:
    name = row.get("Lineitem name") or row.get("Lineitem title") or "Shopify order"
    qty = row.get("Lineitem quantity", "1") or "1"
    price = _amount(row, "Lineitem price")
    if price <= 0:
        price = _amount(row, "Subtotal")
    return f"{name};{qty};{price:.2f}"


def shopify_row_to_invoice(row: dict, seller_defaults: dict) -> dict:
    out = dict(seller_defaults)
    for key, fn in SHOPIFY_MAP.items():
        out[key] = fn({**seller_defaults, **row})
    return out


def main() -> int:
    p = argparse.ArgumentParser(description="Shopify orders CSV → invoice HTML batch")
    p.add_argument("csv_path", type=Path)
    p.add_argument("-o", "--output", type=Path, default=Path("./shopify-output"))
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
        inv = shopify_row_to_invoice(row, seller)
        body = render_invoice(inv)
        slug = re.sub(r"[^\w-]", "", inv.get("invoice_number", f"inv-{i}"))
        out = args.output / f"{slug or f'invoice-{i}'}.html"
        out.write_text(body, encoding="utf-8")
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
