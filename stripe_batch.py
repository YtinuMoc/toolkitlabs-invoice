#!/usr/bin/env python3
"""Stripe payments CSV → bulk invoice HTML (clone of csv2invoice.com Stripe flow).

Export: Stripe Dashboard → Payments → Export → CSV.
Purchase batch CLI pack (EUR 9, one-time):
https://buy.stripe.com/dRm9AUgpwb648Jg7NX5Ne0l?client_reference_id=stripe-batch-py
"""
from __future__ import annotations

import argparse
import csv
import re
import sys
from pathlib import Path

from invoice_batch import render_invoice

STRIPE_MAP = {
    "invoice_number": lambda r: f"ST-{r.get('id', r.get('Invoice Number', '0001'))[:16]}",
    "seller_name": lambda r: r.get("seller_name", "Your Business"),
    "seller_address": lambda r: r.get("seller_address", ""),
    "seller_email": lambda r: r.get("seller_email", ""),
    "seller_tax": lambda r: r.get("seller_tax", ""),
    "buyer_name": lambda r: r.get("buyer_name", r.get("Customer Email", "Customer")),
    "buyer_address": lambda r: _buyer_address(r),
    "buyer_email": lambda r: r.get("Customer Email", ""),
    "invoice_date": lambda r: (r.get("Created (UTC)", r.get("invoice_date", "")) or "")[:10],
    "due_date": lambda r: (r.get("Created (UTC)", r.get("invoice_date", "")) or "")[:10],
    "tax_rate": lambda r: _tax_rate(r),
    "notes": lambda r: _notes(r),
    "items": lambda r: _items(r),
}


def _amount(row: dict, key: str = "Amount") -> float:
    try:
        return float(re.sub(r"[^\d.\-]", "", str(row.get(key, 0) or 0)))
    except ValueError:
        return 0.0


def _tax_rate(row: dict) -> str:
    amt = _amount(row, "Amount")
    tax = _amount(row, "Tax")
    if amt > 0 and tax > 0:
        return str(round(100 * tax / amt, 2))
    return row.get("tax_rate", "0")


def _buyer_address(row: dict) -> str:
    parts = [
        row.get("Card Address Line1", ""),
        row.get("Card Address City", ""),
        row.get("Card Address State", ""),
        row.get("Card Address Country", ""),
        row.get("Card Address Zip", ""),
    ]
    return ", ".join(p for p in parts if p)


def _notes(row: dict) -> str:
    parts = []
    if _amount(row, "Amount Refunded") > 0:
        parts.append("REFUNDED")
    if row.get("Payment Intent ID"):
        parts.append(f"Payment intent: {row['Payment Intent ID']}")
    if row.get("id"):
        parts.append(f"Stripe charge: {row['id']}")
    return ". ".join(parts)


def _items(row: dict) -> str:
    desc = row.get("Description") or "Stripe payment"
    amt = _amount(row, "Amount")
    return f"{desc};1;{amt:.2f}"


def stripe_row_to_invoice(row: dict, seller_defaults: dict) -> dict:
    out = dict(seller_defaults)
    for key, fn in STRIPE_MAP.items():
        out[key] = fn({**seller_defaults, **row})
    return out


def main() -> int:
    p = argparse.ArgumentParser(description="Stripe CSV → invoice HTML batch")
    p.add_argument("csv_path", type=Path)
    p.add_argument("-o", "--output", type=Path, default=Path("./stripe-output"))
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
        inv = stripe_row_to_invoice(row, seller)
        body = render_invoice(inv)
        slug = re.sub(r"[^\w-]", "", inv.get("invoice_number", f"inv-{i}"))
        out = args.output / f"{slug or f'invoice-{i}'}.html"
        out.write_text(body, encoding="utf-8")
        print(out)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
