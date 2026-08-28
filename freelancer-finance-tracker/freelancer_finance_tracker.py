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
    if len(sys.argv) < 4:
        print("Usage: freelancer_finance_tracker.py income.csv expenses.csv invoices.csv [tax_pct]")
        print("Clone target: moonlight573.gumroad.com/l/unsjlk ($10 Freelancer Finance Tracker)")
        sys.exit(1)
    income = load_income(sys.argv[1])
    expenses = load_expenses(sys.argv[2])
    invoices = load_invoices(sys.argv[3])
    tax_pct = float(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_TAX_PCT
    d = dashboard(income, expenses, invoices, tax_pct)
    print_dashboard(d)


if __name__ == "__main__":
    main()
