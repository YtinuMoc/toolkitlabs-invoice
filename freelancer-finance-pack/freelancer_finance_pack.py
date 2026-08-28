#!/usr/bin/env python3
"""Freelancer Finance Pack — clone of saksham82.gumroad.com/l/cueko ($9)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime

US_SE_TAX_RATE = 0.153
US_STANDARD_DEDUCTION = 15000
US_QBI_DEDUCTION_PCT = 0.20
INDIA_44ADA_PCT = 0.50
INDIA_ADVANCE_THRESH = 10000


def load_invoices(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amount = float(row.get("amount") or row.get("total") or 0)
                hours = float(row.get("hours") or 0)
                rate = float(row.get("rate") or 0)
                if not amount and hours and rate:
                    amount = round(hours * rate, 2)
                due = row.get("due_date", "").strip()
                status = row.get("status", "Pending").strip()
                if status.lower() == "sent" and due:
                    try:
                        if datetime.strptime(due, "%Y-%m-%d") < datetime.now() and status.lower() != "paid":
                            status = "Overdue"
                    except ValueError:
                        pass
                rows.append({
                    "date": row.get("date", "").strip(),
                    "client": row.get("client", "").strip(),
                    "description": row.get("description", "").strip(),
                    "hours": hours,
                    "rate": rate,
                    "amount": amount,
                    "status": status,
                })
            except (KeyError, ValueError):
                continue
    return rows


def load_expenses(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                rows.append({
                    "date": row.get("date", "").strip(),
                    "category": row.get("category", "Other").strip(),
                    "description": row.get("description", "").strip(),
                    "amount": float(row.get("amount") or 0),
                    "deductible": row.get("deductible", "yes").strip().lower() in ("yes", "y", "1", "true"),
                })
            except (KeyError, ValueError):
                continue
    return rows


def invoice_summary(invoices):
    total = sum(i["amount"] for i in invoices)
    paid = sum(i["amount"] for i in invoices if i["status"].lower() == "paid")
    awaiting = sum(i["amount"] for i in invoices if i["status"].lower() in ("sent", "pending", "awaiting"))
    overdue = sum(i["amount"] for i in invoices if i["status"].lower() == "overdue")
    by_client = defaultdict(lambda: {"invoiced": 0.0, "paid": 0.0})
    for i in invoices:
        c = by_client[i["client"]]
        c["invoiced"] += i["amount"]
        if i["status"].lower() == "paid":
            c["paid"] += i["amount"]
    return {
        "total_invoiced": total,
        "collected": paid,
        "awaiting": awaiting,
        "overdue": overdue,
        "overdue_count": sum(1 for i in invoices if i["status"].lower() == "overdue"),
        "by_client": dict(by_client),
    }


def expense_summary(expenses):
    by_cat = defaultdict(float)
    by_month = defaultdict(float)
    deductible = 0.0
    for e in expenses:
        by_cat[e["category"]] += e["amount"]
        if e["date"]:
            by_month[e["date"][:7]] += e["amount"]
        if e["deductible"]:
            deductible += e["amount"]
    return {
        "total": sum(e["amount"] for e in expenses),
        "deductible": deductible,
        "by_category": dict(by_cat),
        "by_month": dict(sorted(by_month.items())),
    }


def us_tax_estimate(gross_income, deductible_expenses, state_rate=0.05):
    profit = max(gross_income - deductible_expenses, 0)
    se_tax = profit * US_SE_TAX_RATE
    qbi = profit * US_QBI_DEDUCTION_PCT
    taxable = max(profit - US_STANDARD_DEDUCTION - qbi, 0)
    federal = taxable * 0.22
    state = taxable * state_rate
    quarterly = (se_tax + federal + state) / 4
    return {
        "profit": profit,
        "se_tax": se_tax,
        "qbi_deduction": qbi,
        "taxable_income": taxable,
        "federal_est": federal,
        "state_est": state,
        "total_tax": se_tax + federal + state,
        "quarterly_payment": quarterly,
    }


def india_tax_estimate(gross_income, deductible_expenses, use_44ada=True):
    profit = max(gross_income - deductible_expenses, 0)
    presumed = profit * INDIA_44ADA_PCT if use_44ada else profit
    tax = presumed * 0.30 if presumed > 500000 else presumed * 0.20 if presumed > 300000 else presumed * 0.05
    advance = [tax * 0.15, tax * 0.45, tax * 0.75, tax]
    return {
        "profit": profit,
        "presumed_income": presumed,
        "estimated_tax": tax,
        "advance_instalments": advance,
        "gst_threshold_note": "Register for GST if turnover exceeds threshold (editable in workbook)",
    }


def detect_platform(headers):
    headers = [h.lower() for h in headers]
    if "sale id" in headers and "product name" in headers:
        return "Gumroad"
    if "transaction id" in headers and "stripe fee" in headers:
        return "Stripe"
    if "transaction id" in headers and "gross" in headers:
        return "PayPal"
    return None


def parse_ledger_row(platform, row):
    common = {"date": "", "platform": platform, "transaction_id": "", "description": "",
              "amount": "", "fee": "", "net": "", "buyer": ""}
    try:
        if platform == "Gumroad":
            common.update({
                "date": row["Sale creation date"],
                "transaction_id": row["Sale ID"],
                "description": row["Product name"],
                "amount": row["Price (including tax)"],
                "fee": str(float(row["Gumroad fee"]) + float(row.get("Additional fee", "0") or 0)),
                "net": row["Net"],
                "buyer": row.get("Customer email", ""),
            })
        elif platform == "Stripe":
            common.update({
                "date": row["Created (UTC)"],
                "transaction_id": row["Transaction ID"],
                "description": row.get("Description", ""),
                "amount": row["Gross"],
                "fee": row["Stripe fee"],
                "net": row["Net"],
                "buyer": row.get("Customer email", ""),
            })
        elif platform == "PayPal":
            common.update({
                "date": row["Date"],
                "transaction_id": row["Transaction ID"],
                "description": row.get("Subject", ""),
                "amount": row["Gross"],
                "fee": row["Fee"],
                "net": row["Net"],
                "buyer": row.get("Name", ""),
            })
    except KeyError as e:
        print(f"Missing column: {e}", file=sys.stderr)
    return common


def merge_ledgers(paths, out_path=None):
    rows = []
    for path in paths:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            platform = detect_platform(reader.fieldnames or [])
            if not platform:
                print(f"Unknown format: {path}", file=sys.stderr)
                continue
            for row in reader:
                if row and list(row.values())[0]:
                    rows.append(parse_ledger_row(platform, row))
    rows.sort(key=lambda r: r["date"])
    if out_path:
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
            if rows:
                w.writeheader()
                w.writerows(rows)
    return rows


def profit_dashboard(invoices, expenses, billable_hours=120, state_rate=0.05):
    inv = invoice_summary(invoices)
    exp = expense_summary(expenses)
    gross = inv["collected"]
    profit = gross - exp["deductible"]
    us = us_tax_estimate(gross, exp["deductible"], state_rate)
    take_home = profit - us["total_tax"]
    hourly = take_home / billable_hours if billable_hours else 0
    return {
        "gross_collected": gross,
        "expenses": exp["total"],
        "deductible_expenses": exp["deductible"],
        "net_profit": profit,
        "tax_set_aside": us["total_tax"],
        "take_home": take_home,
        "effective_hourly": hourly,
        "us_tax": us,
        "expense_detail": exp,
        "invoice_detail": inv,
    }


def print_report(invoices, expenses, billable_hours=120):
    d = profit_dashboard(invoices, expenses, billable_hours)
    inv = d["invoice_detail"]
    print("\n=== FREELANCER FINANCE PACK (saksham82 cueko clone) ===")
    print(f"  Total invoiced:      ${inv['total_invoiced']:,.2f}")
    print(f"  Collected:           ${inv['collected']:,.2f}")
    print(f"  Awaiting payment:    ${inv['awaiting']:,.2f}")
    print(f"  Overdue:             ${inv['overdue']:,.2f} ({inv['overdue_count']} invoice(s))")
    print(f"  Expenses:            ${d['expenses']:,.2f} (${d['deductible_expenses']:,.2f} deductible)")
    print(f"  Net profit:          ${d['net_profit']:,.2f}")
    print(f"  Tax set-aside (US):  ${d['tax_set_aside']:,.2f}")
    print(f"  Take-home estimate:  ${d['take_home']:,.2f}")
    print(f"  Effective hourly:    ${d['effective_hourly']:,.2f}/hr ({billable_hours} billable hrs)")
    us = d["us_tax"]
    print("\n=== US QUARTERLY TAX ESTIMATE (2026 planning) ===")
    print(f"  Self-employment tax: ${us['se_tax']:,.2f}")
    print(f"  Federal estimate:    ${us['federal_est']:,.2f}")
    print(f"  State estimate:      ${us['state_est']:,.2f}")
    print(f"  Quarterly payment:   ${us['quarterly_payment']:,.2f}")
    if inv["by_client"]:
        print("\n=== PER-CLIENT ROLLUP ===")
        for client, data in sorted(inv["by_client"].items()):
            out = data["invoiced"] - data["paid"]
            print(f"  {client}: invoiced ${data['invoiced']:,.2f} · paid ${data['paid']:,.2f} · outstanding ${out:,.2f}")


def main():
    args = sys.argv[1:]
    if "--merge" in args:
        idx = args.index("--merge")
        inputs = []
        i = idx + 1
        while i < len(args) and not args[i].startswith("-"):
            inputs.append(args[i])
            i += 1
        out = "ledger-merged.csv"
        if "-o" in args:
            out = args[args.index("-o") + 1]
        rows = merge_ledgers(inputs, out)
        gross = sum(float(r["amount"] or 0) for r in rows)
        fees = sum(float(r["fee"] or 0) for r in rows)
        net = sum(float(r["net"] or 0) for r in rows)
        print("\n=== UNIFIED PAYMENT LEDGER (goldenalien/206o shape) ===")
        print(f"  Transactions:        {len(rows)}")
        print(f"  Gross:               ${gross:,.2f}")
        print(f"  Fees:                ${fees:,.2f}")
        print(f"  Net:                 ${net:,.2f}")
        if out:
            print(f"  Wrote:               {out}")
        return
    inv_path = args[0] if args else "invoices-sample.csv"
    exp_path = args[1] if len(args) > 1 else "expenses-sample.csv"
    hours = float(args[2]) if len(args) > 2 else 120
    invoices = load_invoices(inv_path)
    expenses = load_expenses(exp_path)
    print_report(invoices, expenses, hours)
    india = india_tax_estimate(
        invoice_summary(invoices)["collected"],
        expense_summary(expenses)["deductible"],
    )
    print("\n=== INDIA ADVANCE TAX (Section 44ADA planning) ===")
    print(f"  Presumed income:     ₹{india['presumed_income']:,.0f}")
    print(f"  Estimated tax:       ₹{india['estimated_tax']:,.0f}")
    print(f"  Instalments:         {[round(x) for x in india['advance_instalments']]}")


if __name__ == "__main__":
    main()
