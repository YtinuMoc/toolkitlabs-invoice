#!/usr/bin/env python3
"""Freelancer Invoice & Client Tracker — clone of AgentChip qiliang.gumroad.com/l/ahefab ($15)."""
import csv
import sys
from collections import defaultdict
from datetime import date, datetime


def load_clients(path):
    clients = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = row.get("client_name", "").strip()
            if not name:
                continue
            rate = float(row.get("hourly_rate", "0") or 0)
            clients[name] = {
                "contact": row.get("contact", "").strip(),
                "payment_terms_days": int(row.get("payment_terms_days", "30") or 30),
                "hourly_rate": rate,
                "status": row.get("status", "active").strip().lower(),
            }
    return clients


def load_invoices(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amount = float(row.get("amount", "0") or 0)
                tax = float(row.get("tax", "0") or 0)
            except ValueError:
                continue
            inv_id = row.get("invoice_id", "").strip()
            if not inv_id:
                continue
            due = row.get("due_date", "").strip()
            status = row.get("status", "pending").strip().lower()
            overdue = False
            days_late = 0
            if due and status in ("pending", "sent", "overdue"):
                try:
                    due_d = datetime.strptime(due, "%Y-%m-%d").date()
                    if due_d < date.today():
                        overdue = True
                        days_late = (date.today() - due_d).days
                        status = "overdue"
                except ValueError:
                    pass
            rows.append({
                "invoice_id": inv_id,
                "client": row.get("client", "").strip(),
                "invoice_date": row.get("invoice_date", "").strip(),
                "description": row.get("description", "").strip(),
                "amount": amount,
                "tax": tax,
                "total": amount + tax,
                "status": status,
                "due_date": due,
                "overdue": overdue,
                "days_late": days_late,
            })
    return rows


def load_payments(path):
    paid = defaultdict(float)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            inv_id = row.get("invoice_id", "").strip()
            if not inv_id:
                continue
            try:
                amt = float(row.get("amount", "0") or 0)
            except ValueError:
                continue
            paid[inv_id] += amt
    return dict(paid)


def summarize(clients, invoices, payments):
    total_invoiced = sum(i["total"] for i in invoices)
    total_received = sum(payments.values())
    outstanding = 0.0
    overdue_total = 0.0
    overdue_count = 0
    paid_count = 0
    pending_count = 0

    for inv in invoices:
        paid_amt = payments.get(inv["invoice_id"], 0.0)
        balance = max(inv["total"] - paid_amt, 0.0)
        if balance <= 0.01:
            paid_count += 1
            continue
        pending_count += 1
        outstanding += balance
        if inv["overdue"]:
            overdue_count += 1
            overdue_total += balance

    active_clients = sum(1 for c in clients.values() if c["status"] == "active")
    return {
        "total_invoiced": total_invoiced,
        "total_received": total_received,
        "outstanding": outstanding,
        "overdue_total": overdue_total,
        "overdue_count": overdue_count,
        "paid_count": paid_count,
        "pending_count": pending_count,
        "active_clients": active_clients,
    }


def print_report(clients, invoices, payments):
    s = summarize(clients, invoices, payments)
    print("=== FREELANCER INVOICE & CLIENT TRACKER (AgentChip clone) ===")
    print(f"  Active clients:      {s['active_clients']}")
    print(f"  Total invoiced:      ${s['total_invoiced']:,.2f}")
    print(f"  Total received:      ${s['total_received']:,.2f}")
    print(f"  Outstanding:         ${s['outstanding']:,.2f}")
    print(f"  Overdue invoices:    {s['overdue_count']} · ${s['overdue_total']:,.2f}")
    print(f"  Paid / pending:      {s['paid_count']} paid · {s['pending_count']} open")

    overdue = [i for i in invoices if i["overdue"]]
    if overdue:
        print("\n=== OVERDUE FLAGS ===")
        for inv in sorted(overdue, key=lambda x: -x["days_late"]):
            bal = max(inv["total"] - payments.get(inv["invoice_id"], 0.0), 0.0)
            print(f"  {inv['invoice_id']} · {inv['client']} · {inv['days_late']}d late · ${bal:,.2f}")

    by_client = defaultdict(lambda: {"invoiced": 0.0, "received": 0.0})
    for inv in invoices:
        by_client[inv["client"]]["invoiced"] += inv["total"]
        by_client[inv["client"]]["received"] += payments.get(inv["invoice_id"], 0.0)
    if by_client:
        print("\n=== DASHBOARD BY CLIENT ===")
        for client, nums in sorted(by_client.items()):
            owed = nums["invoiced"] - nums["received"]
            print(f"  {client}: invoiced ${nums['invoiced']:,.2f} · received ${nums['received']:,.2f} · owed ${owed:,.2f}")


def main():
    if len(sys.argv) < 4:
        print("Usage: freelancer_invoice_tracker.py clients.csv invoices.csv payments.csv", file=sys.stderr)
        sys.exit(1)
    clients = load_clients(sys.argv[1])
    invoices = load_invoices(sys.argv[2])
    payments = load_payments(sys.argv[3])
    print_report(clients, invoices, payments)


if __name__ == "__main__":
    main()
