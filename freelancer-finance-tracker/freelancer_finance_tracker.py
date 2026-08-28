#!/usr/bin/env python3
"""Freelancer Finance Tracker — clone of moonlight573.gumroad.com/l/unsjlk ($10)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime

DEFAULT_TAX_PCT = 25.0


def load_income(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                rows.append({
                    "date": row.get("date", "").strip(),
                    "client": row.get("client", "").strip(),
                    "project": row.get("project", "").strip(),
                    "amount": float(row.get("amount") or 0),
                    "status": row.get("status", "paid").strip().lower(),
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


def load_invoices(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amount = float(row.get("amount") or 0)
                due = row.get("due_date", "").strip()
                status = row.get("status", "unpaid").strip().lower()
                if status != "paid" and due:
                    try:
                        if datetime.strptime(due, "%Y-%m-%d") < datetime.now():
                            status = "overdue"
                    except ValueError:
                        pass
                rows.append({
                    "invoice_id": row.get("invoice_id", "").strip(),
                    "client": row.get("client", "").strip(),
                    "amount": amount,
                    "due_date": due,
                    "status": status,
                })
            except (KeyError, ValueError):
                continue
    return rows


def dashboard(income, expenses, invoices, tax_pct=DEFAULT_TAX_PCT):
    total_income = sum(i["amount"] for i in income if i["status"] == "paid")
    total_expenses = sum(e["amount"] for e in expenses)
    deductible = sum(e["amount"] for e in expenses if e["deductible"])
    net_profit = total_income - total_expenses
    outstanding = sum(i["amount"] for i in invoices if i["status"] in ("unpaid", "overdue"))
    overdue = sum(i["amount"] for i in invoices if i["status"] == "overdue")
    tax_set_aside = max(net_profit, 0) * (tax_pct / 100.0)
    safe_to_spend = max(net_profit - tax_set_aside, 0)

    by_client = defaultdict(float)
    for i in income:
        if i["status"] == "paid":
            by_client[i["client"]] += i["amount"]

    by_category = defaultdict(float)
    for e in expenses:
        by_category[e["category"]] += e["amount"]

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "deductible_expenses": deductible,
        "net_profit": net_profit,
        "outstanding_invoices": outstanding,
        "overdue_invoices": overdue,
        "tax_set_aside": tax_set_aside,
        "safe_to_spend": safe_to_spend,
        "tax_pct": tax_pct,
        "by_client": dict(by_client),
        "by_category": dict(by_category),
    }


def fmt_money(n):
    return f"${n:,.2f}"


def summarize_net_income(income, expenses, tax_pct=DEFAULT_TAX_PCT):
    """faisalmq/5797: net income visibility — safe-to-spend after tax + subscriptions."""
    paid = [i for i in income if i["status"] == "paid"]
    collected = sum(i["amount"] for i in paid)
    deductible = sum(e["amount"] for e in expenses if e["deductible"])
    subs = sum(
        e["amount"] for e in expenses
        if e["deductible"] and e["category"].lower() in ("software", "subscriptions", "saas", "tools")
    )
    net_profit = collected - deductible
    tax_set_aside = max(net_profit, 0) * (tax_pct / 100.0)
    safe_to_spend = max(net_profit - tax_set_aside, 0)
    print("\n=== NET INCOME VISIBILITY (faisalmq/5797 shape) ===")
    print(f"  Gross collected:     {fmt_money(collected)}")
    print(f"  Expenses (deductible): {fmt_money(deductible)}")
    if subs:
        print(f"    subscriptions/SaaS:  {fmt_money(subs)}")
    print(f"  Net profit:            {fmt_money(net_profit)}")
    print(f"  Tax set-aside ({tax_pct:.0f}%): {fmt_money(tax_set_aside)}")
    print(f"  Safe to spend:         {fmt_money(safe_to_spend)}")
    if collected:
        print(f"  Take-home rate:        {safe_to_spend / collected * 100:.1f}% of gross deposits")
    print("\n  Gross deposits lie. Safe-to-spend is what you can actually use.")
    print("  Guide: net-income-guide.md · income-sample.csv · expenses-sample.csv")


def summarize_invoice_panic(invoices):
    """faisalmq/43dl: end-of-month panic → invoice status log + overdue flags."""
    paid = [i for i in invoices if i["status"] == "paid"]
    sent = [i for i in invoices if i["status"] in ("sent", "unpaid")]
    overdue = [i for i in invoices if i["status"] == "overdue"]
    collected = sum(i["amount"] for i in paid)
    awaiting = sum(i["amount"] for i in sent)
    overdue_amt = sum(i["amount"] for i in overdue)

    by_client = defaultdict(lambda: {"invoiced": 0.0, "paid": 0.0, "outstanding": 0.0})
    for i in invoices:
        by_client[i["client"]]["invoiced"] += i["amount"]
        if i["status"] == "paid":
            by_client[i["client"]]["paid"] += i["amount"]
        elif i["status"] in ("sent", "unpaid", "overdue"):
            by_client[i["client"]]["outstanding"] += i["amount"]

    print("\n=== INVOICE TRACKER WITHOUT END-OF-MONTH PANIC (faisalmq/43dl shape) ===")
    print(f"  Invoices logged:     {len(invoices)}")
    print(f"  Collected (paid):    {fmt_money(collected)}")
    print(f"  Awaiting payment:    {fmt_money(awaiting)}")
    print(f"  Overdue (late):      {len(overdue)} invoices · {fmt_money(overdue_amt)}")
    if overdue:
        print("\n--- Overdue invoices ---")
        for i in overdue:
            print(f"  {i['invoice_id']:16s} {i['client'][:16]:<16} {fmt_money(i['amount']):>12} due {i['due_date']}")
    if by_client:
        print("\n--- Per-client totals ---")
        for client, totals in sorted(by_client.items(), key=lambda x: -x[1]["invoiced"]):
            print(
                f"  {client[:20]:<20} invoiced {fmt_money(totals['invoiced']):>12} "
                f"paid {fmt_money(totals['paid']):>12} outstanding {fmt_money(totals['outstanding']):>12}"
            )
    print("\n  Log every invoice when sent. Mark paid when deposit lands. Run weekly — not in panic.")
    print("  Guide: invoice-panic-guide.md · invoices-sample.csv · start-here.md")


def summarize_tax_buffer(income, expenses, tax_pct=DEFAULT_TAX_PCT):
    """faisalmq/4gao: per-payment set-aside + YTD safe-to-spend."""
    paid = [i for i in income if i["status"] == "paid"]
    collected = sum(i["amount"] for i in paid)
    total_expenses = sum(e["amount"] for e in expenses)
    deductible = sum(e["amount"] for e in expenses if e["deductible"])
    net_profit = collected - deductible
    tax_set_aside = max(net_profit, 0) * (tax_pct / 100.0)
    safe_to_spend = max(net_profit - tax_set_aside, 0)
    print("\n=== PER-PAYMENT TAX SET-ASIDE (faisalmq/4gao shape) ===")
    print(f"  {'Client':<16} {'Collected':>12} {'Set-aside':>12} {'Safe':>12}")
    for i in paid:
        share = i["amount"] / collected if collected else 0
        buf = net_profit * share * tax_pct / 100 if net_profit > 0 else 0
        safe = i["amount"] - buf
        print(f"  {i['client'][:16]:<16} ${i['amount']:>10,.2f} ${buf:>10,.2f} ${safe:>10,.2f}")
    print("\n=== EXPENSE + TAX SET-ASIDE ===")
    print(f"  Expenses YTD:        {fmt_money(total_expenses)} ({fmt_money(deductible)} deductible)")
    print(f"  Net profit (paid):   {fmt_money(net_profit)}")
    print(f"  Tax set-aside ({tax_pct:.0f}%): {fmt_money(tax_set_aside)}")
    print(f"  Safe to spend:       {fmt_money(safe_to_spend)}")
    print("  Transfer set-aside to tax-only savings when payment lands — not in April.")
    print("  Guide: tax-set-aside-guide.md · income-sample.csv · expenses-sample.csv")


def print_dashboard(d):
    print("=== FREELANCER FINANCE TRACKER (moonlight573 unsjlk clone) ===")
    print(f"  Total income:        {fmt_money(d['total_income'])}")
    print(f"  Total expenses:      {fmt_money(d['total_expenses'])}")
    print(f"  Deductible expenses: {fmt_money(d['deductible_expenses'])}")
    print(f"  Net profit:          {fmt_money(d['net_profit'])}")
    print(f"  Outstanding invoices:{fmt_money(d['outstanding_invoices'])}")
    print(f"  Overdue invoices:    {fmt_money(d['overdue_invoices'])}")
    print(f"  Tax set-aside ({d['tax_pct']:.0f}%): {fmt_money(d['tax_set_aside'])}")
    print(f"  Safe to spend:       {fmt_money(d['safe_to_spend'])}")
    if d["by_client"]:
        print("\n--- Income by client (paid) ---")
        for client, amt in sorted(d["by_client"].items(), key=lambda x: -x[1]):
            print(f"  {client:24s} {fmt_money(amt)}")
    if d["by_category"]:
        print("\n--- Expenses by category ---")
        for cat, amt in sorted(d["by_category"].items(), key=lambda x: -x[1]):
            print(f"  {cat:24s} {fmt_money(amt)}")


def main():
    args = sys.argv[1:]
    if len(args) >= 2 and args[0] == "--invoice-panic":
        invoices = load_invoices(args[1])
        summarize_invoice_panic(invoices)
        return
    if len(args) >= 3 and args[0] == "--net-income":
        income = load_income(args[1])
        expenses = load_expenses(args[2])
        tax_pct = float(args[3]) if len(args) >= 4 else DEFAULT_TAX_PCT
        summarize_net_income(income, expenses, tax_pct)
        return
    if len(args) >= 4 and args[0] == "--tax-buffer":
        income = load_income(args[1])
        expenses = load_expenses(args[2])
        tax_pct = float(args[4]) if len(args) >= 5 else DEFAULT_TAX_PCT
        summarize_tax_buffer(income, expenses, tax_pct)
        return
    if len(args) < 3:
        print("Usage: freelancer_finance_tracker.py income.csv expenses.csv invoices.csv [tax_pct]")
        print("       freelancer_finance_tracker.py --invoice-panic invoices.csv")
        print("       freelancer_finance_tracker.py --net-income income.csv expenses.csv [tax_pct]")
        print("       freelancer_finance_tracker.py --tax-buffer income.csv expenses.csv invoices.csv [tax_pct]")
        print("Clone target: moonlight573.gumroad.com/l/unsjlk ($10 Freelancer Finance Tracker)")
        sys.exit(1)
    income = load_income(args[0])
    expenses = load_expenses(args[1])
    invoices = load_invoices(args[2])
    tax_pct = float(args[3]) if len(args) > 3 else DEFAULT_TAX_PCT
    d = dashboard(income, expenses, invoices, tax_pct)
    print_dashboard(d)


if __name__ == "__main__":
    main()
