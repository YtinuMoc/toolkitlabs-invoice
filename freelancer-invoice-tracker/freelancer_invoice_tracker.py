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


def _parse_iso_date(s):
    if not s:
        return None
    try:
        return datetime.strptime(s.strip(), "%Y-%m-%d").date()
    except ValueError:
        return None


def _subscription_status(renewal_date, cancel_by, today):
    """agentchip/52g8 four-state judgment from renewal + cancel-by dates."""
    if renewal_date and today > renewal_date:
        return "EXPIRED"
    if cancel_by and today >= cancel_by:
        return "RENEW NOW"
    if cancel_by:
        days_to_cancel = (cancel_by - today).days
        if 0 <= days_to_cancel <= 30:
            return "Renew soon"
    return "Active"


def summarize_subscription_audit(path):
    """agentchip/52g8: freelance SaaS auto-renewal creep — track cancel-by, not renewal."""
    rows = []
    today = date.today()
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                monthly = float(row.get("monthly_usd", row.get("amount", 0)))
            except (KeyError, ValueError):
                continue
            renewal = _parse_iso_date(row.get("renewal_date", ""))
            cancel_by = _parse_iso_date(row.get("cancel_by", ""))
            status = (row.get("status") or "").strip() or _subscription_status(
                renewal, cancel_by, today
            )
            rows.append({
                "contract": row.get("contract", "").strip(),
                "vendor": row.get("vendor", row.get("bill", "")).strip(),
                "monthly": monthly,
                "cancel_by": cancel_by,
                "status": status,
            })
    if not rows:
        return
    monthly_load = sum(r["monthly"] for r in rows)
    urgent = [r for r in rows if r["status"] in ("RENEW NOW", "Renew soon", "EXPIRED")]
    zombie = [r for r in rows if r["monthly"] >= 50 and r["status"] == "RENEW NOW"]
    print("\n=== SUBSCRIPTION AUTO-RENEWAL AUDIT (agentchip/52g8 shape) ===")
    print("  Track cancel-by deadlines — calendar renewal reminders arrive too late.")
    print(f"  Contracts tracked: {len(rows)} · est. monthly load: ${monthly_load:,.2f}")
    print("  contract   vendor          monthly  cancel_by    status")
    for r in rows:
        cancel = r["cancel_by"].isoformat() if r["cancel_by"] else "—"
        print(
            f"  {r['contract'] or '—':10} {r['vendor'][:14]:14} "
            f"${r['monthly']:>6.2f}  {cancel:10}  {r['status']}"
        )
    if urgent:
        print(f"  Action needed: {len(urgent)} contract(s) in renew/cancel window")
    if zombie:
        wasted = sum(r["monthly"] for r in zombie)
        print(
            f"  Zombie SaaS check: ${wasted:,.2f}/mo flagged RENEW NOW "
            "(unused tools still billing — agentchip/52g8 audit pays for itself)"
        )
    print("  Guide: subscription-audit-guide.md · subscriptions-sample.csv")


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
        print(
            "Usage: freelancer_invoice_tracker.py clients.csv invoices.csv payments.csv [subscriptions.csv]",
            file=sys.stderr,
        )
        sys.exit(1)
    clients = load_clients(sys.argv[1])
    invoices = load_invoices(sys.argv[2])
    payments = load_payments(sys.argv[3])
    print_report(clients, invoices, payments)
    if len(sys.argv) >= 5:
        summarize_subscription_audit(sys.argv[4])


if __name__ == "__main__":
    main()
