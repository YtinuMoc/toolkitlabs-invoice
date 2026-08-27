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


def summarize_bills(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = float(row["amount"])
            except (KeyError, ValueError):
                continue
            status = row.get("status", "pending").strip().lower() or "pending"
            rows.append({
                "bill": row.get("bill", "").strip(),
                "amount": amt,
                "frequency": row.get("frequency", "monthly").strip().lower(),
                "due_day": row.get("due_day", "").strip(),
                "status": status,
            })
    if not rows:
        return
    paid = [r for r in rows if r["status"] == "paid"]
    pending = [r for r in rows if r["status"] != "paid"]
    monthly_equiv = 0.0
    for r in rows:
        freq = r["frequency"]
        if freq == "monthly":
            monthly_equiv += r["amount"]
        elif freq == "quarterly":
            monthly_equiv += r["amount"] / 3
        elif freq == "yearly":
            monthly_equiv += r["amount"] / 12
        else:
            monthly_equiv += r["amount"]
    print("\n=== RECURRING BILLS (Quillenhart bills tab shape) ===")
    print(f"  Bills tracked: {len(rows)}")
    print(f"  Marked paid this cycle: {len(paid)} (${sum(r['amount'] for r in paid):,.2f})")
    print(f"  Still pending: {len(pending)} (${sum(r['amount'] for r in pending):,.2f})")
    print(f"  Est. monthly fixed load: ${monthly_equiv:,.2f}")


def summarize_debt(path, ytd_net=None):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                cur = float(row["current_balance"])
                min_p = float(row.get("min_payment", 0) or 0)
            except (KeyError, ValueError):
                continue
            rows.append({
                "creditor": row.get("creditor", "").strip(),
                "current_balance": cur,
                "min_payment": min_p,
                "due_day": row.get("due_day", "").strip(),
                "apr": row.get("apr", "").strip(),
            })
    if not rows:
        return
    total_balance = sum(r["current_balance"] for r in rows)
    total_min = sum(r["min_payment"] for r in rows)
    print("\n=== DEBT MINIMUMS (crazychief/jg5 shape) ===")
    print(f"  Accounts tracked: {len(rows)}")
    print(f"  Total current balance: ${total_balance:,.2f}")
    print(f"  Total minimum payments: ${total_min:,.2f}/month")
    for r in rows:
        apr = f" @ {r['apr']}%" if r["apr"] else ""
        print(f"    {r['creditor']}: ${r['current_balance']:,.2f} (min ${r['min_payment']:,.2f}{apr})")
    if ytd_net is not None:
        if ytd_net >= total_min:
            surplus = ytd_net - total_min
            print(f"  YTD net covers minimums: yes — ${surplus:,.2f} surplus after min payments")
        else:
            gap = total_min - ytd_net
            print(f"  YTD net covers minimums: NO — short ${gap:,.2f} (net profit < debt minimums)")


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
    bills_path = sys.argv[3] if len(sys.argv) > 3 else None
    debt_path = sys.argv[4] if len(sys.argv) > 4 else None
    rows = load_rows(path)
    if not rows:
        print("No transactions found.", file=sys.stderr)
        sys.exit(1)
    summarize(rows)
    ytd_net = None
    by_month = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    for r in rows:
        key = r["date"].strftime("%Y-%m")
        if r["type"] == "income" or r["amount"] > 0:
            by_month[key]["income"] += abs(r["amount"])
        else:
            by_month[key]["expense"] += abs(r["amount"])
    ytd_income = sum(m["income"] for m in by_month.values())
    ytd_expense = sum(m["expense"] for m in by_month.values())
    ytd_net = ytd_income - ytd_expense
    if invoice_path:
        summarize_invoices(invoice_path)
    if bills_path:
        summarize_bills(bills_path)
    if debt_path:
        summarize_debt(debt_path, ytd_net=ytd_net)


if __name__ == "__main__":
    main()
