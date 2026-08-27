#!/usr/bin/env python3
"""Small Business Finance Tracker — clone of Quillenhart qaduu dashboard tab."""
import csv
import sys
from collections import defaultdict
from datetime import datetime

TAX_SET_ASIDE_PCT = 25.0
TAKE_HOME_RESERVE_PCT = 28.0  # marginmap/14ag low-state band default
SE_TAX_RATE = 0.153
FEE_CATEGORIES = frozenset({
    "platform_fee", "fulfillment", "creator_commission", "ad_spend", "refund_fee",
})


def load_rows(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = float(row["amount"])
            except (KeyError, ValueError):
                continue
            try:
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except ValueError:
                continue
            rows.append({
                "date": dt,
                "type": row.get("type", "").strip().lower(),
                "category": row.get("category", "uncategorized").strip() or "uncategorized",
                "description": row.get("description", "").strip(),
                "amount": amt,
            })
    return rows


def summarize_invoices(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = float(row["amount"])
            except (KeyError, ValueError):
                continue
            status = row.get("status", "Pending").strip() or "Pending"
            rows.append({
                "invoice_num": row.get("invoice_num", "").strip(),
                "client": row.get("client", "").strip(),
                "amount": amt,
                "status": status,
            })
    if not rows:
        return
    paid = [r for r in rows if r["status"].lower() == "paid"]
    unpaid = [r for r in rows if r["status"].lower() != "paid"]
    overdue = [r for r in unpaid if r["status"].lower() == "overdue"]
    paid_total = sum(r["amount"] for r in paid)
    outstanding_total = sum(r["amount"] for r in unpaid)
    overdue_total = sum(r["amount"] for r in overdue)
    print("\n=== ACCOUNTS RECEIVABLE (agentchip/2b11 shape) ===")
    print(f"  Invoices tracked: {len(rows)}")
    print(f"  Paid: {len(paid)} (${paid_total:,.2f})")
    print(f"  Outstanding: {len(unpaid)} (${outstanding_total:,.2f})")
    if overdue:
        print(f"  Overdue: {len(overdue)} (${overdue_total:,.2f}) — chase these first")
    else:
        print("  Overdue: 0 — no flagged late invoices")


def summarize(rows):
    by_month = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    by_cat = defaultdict(float)
    for r in rows:
        key = r["date"].strftime("%Y-%m")
        if r["type"] == "income" or r["amount"] > 0:
            by_month[key]["income"] += abs(r["amount"])
        else:
            by_month[key]["expense"] += abs(r["amount"])
        by_cat[r["category"]] += r["amount"]

    print("=== MONTHLY P&L ===")
    ytd_income = ytd_expense = 0.0
    for month in sorted(by_month):
        inc = by_month[month]["income"]
        exp = by_month[month]["expense"]
        net = inc - exp
        ytd_income += inc
        ytd_expense += exp
        print(f"{month}  income ${inc:,.2f}  expense ${exp:,.2f}  net ${net:,.2f}")

    ytd_net = ytd_income - ytd_expense
    print(f"\nYTD income ${ytd_income:,.2f}  expense ${ytd_expense:,.2f}  net ${ytd_net:,.2f}")

    print("\n=== CATEGORY BREAKDOWN (net) ===")
    for cat in sorted(by_cat, key=lambda c: -abs(by_cat[c])):
        print(f"  {cat}: ${by_cat[cat]:,.2f}")

    quarterly = ytd_net * (TAX_SET_ASIDE_PCT / 100) / max(1, len(by_month) / 3)
    print(f"\n=== QUARTERLY TAX SET-ASIDE ({TAX_SET_ASIDE_PCT:.0f}% of net) ===")
    print(f"  Estimated per quarter: ${quarterly:,.2f}")
    print(f"  YTD set-aside target: ${ytd_net * (TAX_SET_ASIDE_PCT / 100):,.2f}")

    print("\n=== ANNUAL SUMMARY (month | income | expense | net | set-aside) ===")
    for month in sorted(by_month):
        inc = by_month[month]["income"]
        exp = by_month[month]["expense"]
        net = inc - exp
        aside = net * (TAX_SET_ASIDE_PCT / 100)
        print(f"  {month}  ${inc:,.2f}  ${exp:,.2f}  ${net:,.2f}  ${aside:,.2f}")
    print(f"  YTD  ${ytd_income:,.2f}  ${ytd_expense:,.2f}  ${ytd_net:,.2f}  ${ytd_net * (TAX_SET_ASIDE_PCT / 100):,.2f}")

    fee_expense = sum(abs(r["amount"]) for r in rows if r["type"] != "income" and r["amount"] < 0 and r["category"] in FEE_CATEGORIES)
    other_expense = ytd_expense - fee_expense
    if ytd_income > 0:
        print(f"\n=== 1099-K RECONCILIATION (l_d/5284 shape) ===")
        print(f"  Gross payments (1099-K box 1 equivalent): ${ytd_income:,.2f}")
        print(f"  Deductible platform/fulfillment/commission/ad fees: ${fee_expense:,.2f}")
        print(f"  Other business expenses: ${other_expense:,.2f}")
        print(f"  Taxable net profit (gross − all expenses): ${ytd_net:,.2f}")
        if ytd_income > 0:
            overpay_risk = (ytd_income - ytd_net) * (TAX_SET_ASIDE_PCT / 100)
            print(f"  Extra tax if you set aside on gross instead of net: ~${overpay_risk:,.2f}/quarter habit")

    if ytd_net > 0:
        se_tax = ytd_net * SE_TAX_RATE
        reserve_total = ytd_net * (TAKE_HOME_RESERVE_PCT / 100)
        take_home = ytd_net - reserve_total
        print(f"\n=== TAKE-HOME ESTIMATE (marginmap/14ag shape, {TAKE_HOME_RESERVE_PCT:.0f}% reserve) ===")
        print(f"  YTD gross income: ${ytd_income:,.2f}")
        print(f"  YTD expenses: ${ytd_expense:,.2f}")
        print(f"  YTD net profit: ${ytd_net:,.2f}")
        print(f"  Est. SE tax component (15.3% of net): ${se_tax:,.2f}")
        print(f"  Planned tax reserve ({TAKE_HOME_RESERVE_PCT:.0f}% of net): ${reserve_total:,.2f}")
        print(f"  Est. take-home after reserve: ${take_home:,.2f}")
        print(f"  Effective reserve rate on gross: {(reserve_total / ytd_income * 100):.1f}%")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "sample-transactions.csv"
    invoice_path = sys.argv[2] if len(sys.argv) > 2 else None
    rows = load_rows(path)
    if not rows:
        print("No transactions found.", file=sys.stderr)
        sys.exit(1)
    summarize(rows)
    if invoice_path:
        summarize_invoices(invoice_path)


if __name__ == "__main__":
    main()
