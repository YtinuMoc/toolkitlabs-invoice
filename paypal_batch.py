#!/usr/bin/env python3
"""PayPal activity CSV → bulk invoice HTML (clone of csv2invoice.com PayPal flow).

Export: PayPal → Reports → Activity download → Balance affecting → CSV.
Purchase batch CLI pack (EUR 9, one-time):
https://buy.stripe.com/dRm9AUgpwb648Jg7NX5Ne0l?client_reference_id=paypal-batch-py
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

from invoice_batch import render_invoice

PAYPAL_MAP = {
    "invoice_number": lambda r: f"PP-{r.get('Transaction ID', r.get('Receipt ID', '0001'))[:16]}",
    "seller_name": lambda r: r.get("seller_name", "Your Business"),
    "seller_address": lambda r: r.get("seller_address", ""),
    "seller_email": lambda r: r.get("seller_email", ""),
    "seller_tax": lambda r: r.get("seller_tax", ""),
    "buyer_name": lambda r: r.get("Name", r.get("buyer_name", "Customer")),
    "buyer_address": lambda r: _buyer_address(r),
    "buyer_email": lambda r: r.get("From Email Address", r.get("To Email Address", "")),
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
    gross = _amount(row, "Gross")
    tax = _amount(row, "Sales Tax")
    if gross > 0 and tax > 0:
        return str(round(100 * tax / gross, 2))
    return row.get("tax_rate", "0")


def _buyer_address(row: dict) -> str:
    parts = [
        row.get("Address Line 1", ""),
        row.get("Town/City", ""),
        row.get("State/Province", ""),
        row.get("Zip/Postal Code", ""),
        row.get("Country Code", ""),
    ]
    if row.get("Shipping Address"):
        parts.insert(0, row["Shipping Address"])
    return ", ".join(p for p in parts if p)


def _notes(row: dict) -> str:
    parts = []
    if row.get("Type"):
        parts.append(f"PayPal type: {row['Type']}")
    if row.get("Status"):
        parts.append(f"Status: {row['Status']}")
    if row.get("Transaction ID"):
        parts.append(f"Transaction: {row['Transaction ID']}")
    if row.get("Tax ID"):
        parts.append(f"Buyer tax ID: {row['Tax ID']}")
    return ". ".join(parts)


def _items(row: dict) -> str:
    title = row.get("Item Title") or row.get("Name") or "PayPal payment"
    qty = row.get("Quantity", "1") or "1"
    gross = _amount(row, "Gross")
    return f"{title};{qty};{gross:.2f}"


def paypal_row_to_invoice(row: dict, seller_defaults: dict) -> dict:
    out = dict(seller_defaults)
    for key, fn in PAYPAL_MAP.items():
        out[key] = fn({**seller_defaults, **row})
    return out


def main() -> int:
    p = argparse.ArgumentParser(description="PayPal CSV → invoice HTML batch")
    p.add_argument("csv_path", type=Path)
    p.add_argument("-o", "--output", type=Path, default=Path("./paypal-output"))
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
        inv = paypal_row_to_invoice(row, seller)
        body = render_invoice(inv)
        slug = re.sub(r"[^\w-]", "", inv.get("invoice_number", f"inv-{i}"))
        out = args.output / f"{slug or f'invoice-{i}'}.html"
        out.write_text(body, encoding="utf-8")
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
