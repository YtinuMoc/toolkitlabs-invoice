#!/usr/bin/env python3
"""Batch invoice HTML generator — reads CSV, writes printable invoice pages.

Purchase the batch CLI pack (EUR 9, one-time):
https://buy.stripe.com/3cI4gA8X44HGgbI6JT5Ne0j?client_reference_id=invoice-batch-py
"""
from __future__ import annotations

import argparse
import csv
import html
import sys
from pathlib import Path

TEMPLATE_HEAD = """<!doctype html>
<html lang="en"><head><meta charset="utf-8"><title>{inv_num}</title>
<style>
body{{margin:0;font:16px/1.5 -apple-system,Segoe UI,Helvetica,Arial,sans-serif;color:#1a1a1a}}
#invoice{{max-width:800px;margin:40px auto;padding:40px}}
.inv-head{{display:flex;justify-content:space-between;margin-bottom:32px}}
.inv-title{{font-size:2rem;font-weight:700}}
table{{width:100%;border-collapse:collapse;margin:24px 0}}
th,td{{padding:10px 8px;border-bottom:1px solid #ddd;text-align:left}}
.num{{text-align:right}}
.totals{{margin-left:auto;width:260px}}
.totals div{{display:flex;justify-content:space-between;padding:6px 0}}
.grand{{font-size:1.2rem;font-weight:700;border-top:2px solid #1a1a1a;margin-top:8px;padding-top:10px}}
@media print{{@page{{size:A4;margin:18mm}}}}
</style></head><body><div id="invoice">
"""

TEMPLATE_TAIL = "</div></body></html>\n"


def money(n: float) -> str:
    return f"{n:.2f}"


def render_invoice(row: dict) -> str:
    inv_num = row.get("invoice_number", "INV-0001")
    seller = row.get("seller_name", "")
    seller_addr = row.get("seller_address", "").replace("\\n", "\n")
    seller_email = row.get("seller_email", "")
    seller_tax = row.get("seller_tax", "")
    buyer = row.get("buyer_name", "")
    buyer_addr = row.get("buyer_address", "").replace("\\n", "\n")
    buyer_email = row.get("buyer_email", "")
    inv_date = row.get("invoice_date", "")
    due_date = row.get("due_date", "")
    tax_rate = float(row.get("tax_rate", 0) or 0)
    notes = row.get("notes", "")
    items_raw = row.get("items", "")
    lines = []
    sub = 0.0
    for part in items_raw.split("|"):
        part = part.strip()
        if not part:
            continue
        bits = [b.strip() for b in part.split(";")]
        desc = bits[0] if bits else ""
        qty = float(bits[1]) if len(bits) > 1 and bits[1] else 1.0
        rate = float(bits[2]) if len(bits) > 2 and bits[2] else 0.0
        amt = qty * rate
        sub += amt
        lines.append((desc, qty, rate, amt))
    tax = sub * tax_rate / 100
    total = sub + tax
    e = html.escape
    rows_html = "".join(
        f"<tr><td>{e(d)}</td><td class='num'>{qty:g}</td><td class='num'>{money(rate)}</td><td class='num'>{money(amt)}</td></tr>"
        for d, qty, rate, amt in lines
    ) or "<tr><td colspan='4' style='color:#999'>No line items</td></tr>"
    tax_row = f"<div><span>Tax ({tax_rate:g}%)</span><span>{money(tax)}</span></div>" if tax_rate else ""
    notes_block = f"<p style='white-space:pre-line;margin-top:28px'>{e(notes)}</p>" if notes else ""
    body = f"""<div class="inv-head"><div><div class="inv-title">INVOICE</div><p>{e(seller)}</p></div>
<div style="text-align:right"><div><strong>Invoice #</strong> {e(inv_num)}</div>
<div><strong>Date</strong> {e(inv_date)}</div><div><strong>Due</strong> {e(due_date)}</div></div></div>
<div style="display:flex;gap:40px"><div style="flex:1"><h3>From</h3><p><strong>{e(seller)}</strong><br>{e(seller_addr).replace(chr(10),'<br>')}
{f'<br>{e(seller_email)}' if seller_email else ''}{f'<br>Tax ID: {e(seller_tax)}' if seller_tax else ''}</p></div>
<div style="flex:1"><h3>Bill to</h3><p><strong>{e(buyer)}</strong><br>{e(buyer_addr).replace(chr(10),'<br>')}
{f'<br>{e(buyer_email)}' if buyer_email else ''}</p></div></div>
<table><thead><tr><th>Description</th><th class="num">Qty</th><th class="num">Rate</th><th class="num">Amount</th></tr></thead>
<tbody>{rows_html}</tbody></table>
<div class="totals"><div><span>Subtotal</span><span>{money(sub)}</span></div>{tax_row}
<div class="grand"><span>Total</span><span>€ {money(total)}</span></div></div>{notes_block}"""
    return TEMPLATE_HEAD.format(inv_num=e(inv_num)) + body + TEMPLATE_TAIL


def main() -> int:
    p = argparse.ArgumentParser(
        description="Batch printable invoice HTML from CSV",
        epilog="Buy batch CLI pack (EUR 9): https://buy.stripe.com/3cI4gA8X44HGgbI6JT5Ne0j?client_reference_id=invoice-batch-help",
    )
    p.add_argument("input", type=Path, help="CSV file (see sample.csv)")
    p.add_argument("-o", "--out", type=Path, default=Path("invoice-out"), help="output directory")
    args = p.parse_args()
    args.out.mkdir(parents=True, exist_ok=True)
    count = 0
    with args.input.open(encoding="utf-8", newline="") as f:
        for row in csv.DictReader(f):
            inv_num = row.get("invoice_number", f"inv-{count+1:04d}")
            safe = "".join(c if c.isalnum() or c in "-_" else "-" for c in inv_num)[:80]
            out = args.out / f"{safe}.html"
            out.write_text(render_invoice(row), encoding="utf-8")
            count += 1
    print(f"wrote {count} invoice(s) to {args.out}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
