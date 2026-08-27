#!/usr/bin/env python3
"""Gumroad Payout Tracker — clone of Nagaraj inagaraj ($10+ Gumroad, 31 sales)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime

STATUS_ORDER = ("pending", "in_transit", "done")


def load_payouts(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
                gross = float(row["gross_sales"])
                fees = float(row.get("fees", 0) or 0)
                comm_paid = float(row.get("commission_paid", 0) or 0)
                comm_recv = float(row.get("commission_received", 0) or 0)
                net = float(row.get("net_payout", gross - fees - comm_paid + comm_recv))
            except (KeyError, ValueError):
                continue
            rows.append({
                "date": dt,
                "gross_sales": gross,
                "fees": fees,
                "commission_paid": comm_paid,
                "commission_received": comm_recv,
                "net_payout": net,
                "status": row.get("status", "done").strip().lower(),
            })
    return rows


def load_commissions(path, kind):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
                amount = float(row["amount"])
            except (KeyError, ValueError):
                continue
            rows.append({
                "date": dt,
                "affiliate": row.get("affiliate", "").strip(),
                "product": row.get("product", "").strip(),
                "amount": amount,
                "kind": kind,
            })
    return rows


def print_dashboard(payouts):
    if not payouts:
        print("No payout rows loaded.")
        return
    total_gross = sum(p["gross_sales"] for p in payouts)
    total_fees = sum(p["fees"] for p in payouts)
    total_comm_paid = sum(p["commission_paid"] for p in payouts)
    total_comm_recv = sum(p["commission_received"] for p in payouts)
    total_net = sum(p["net_payout"] for p in payouts)
    months = sorted({p["date"].strftime("%Y-%m") for p in payouts})
    print("=== PAYOUT DASHBOARD (Nagaraj inagaraj clone) ===")
    print(f"  Payout rows:         {len(payouts)}")
    print(f"  Months tracked:      {len(months)}")
    print(f"  Gross sales:         ${total_gross:,.2f}")
    print(f"  Gumroad fees:        ${total_fees:,.2f}")
    print(f"  Commission paid:     ${total_comm_paid:,.2f}")
    print(f"  Commission received: ${total_comm_recv:,.2f}")
    print(f"  Net payouts:         ${total_net:,.2f}")
    if total_gross:
        print(f"  Fee rate:            {100 * total_fees / total_gross:.1f}% of gross")


def print_calendar(payouts):
    by_month = defaultdict(lambda: {"gross": 0.0, "net": 0.0, "count": 0})
    for p in payouts:
        key = p["date"].strftime("%Y-%m")
        by_month[key]["gross"] += p["gross_sales"]
        by_month[key]["net"] += p["net_payout"]
        by_month[key]["count"] += 1
    print("\n=== PAYOUT CALENDAR (monthly) ===")
    for month in sorted(by_month):
        m = by_month[month]
        print(f"  {month}  {m['count']} payout(s)  gross ${m['gross']:,.2f}  net ${m['net']:,.2f}")


def print_status_board(payouts):
    by_status = defaultdict(list)
    for p in payouts:
        by_status[p["status"]].append(p)
    print("\n=== PAYOUT BOARD (kanban) ===")
    for status in STATUS_ORDER:
        items = by_status.get(status, [])
        if not items:
            continue
        net = sum(p["net_payout"] for p in items)
        print(f"  {status.replace('_', ' ').title():14} {len(items)} row(s)  net ${net:,.2f}")


def print_commissions(paid_rows, recv_rows):
    print("\n=== COMMISSION TRACKER ===")
    if paid_rows:
        total = sum(r["amount"] for r in paid_rows)
        print(f"  Paid out:    ${total:,.2f} across {len(paid_rows)} affiliate row(s)")
    if recv_rows:
        total = sum(r["amount"] for r in recv_rows)
        print(f"  Received:    ${total:,.2f} across {len(recv_rows)} affiliate row(s)")


def main():
    if len(sys.argv) < 2:
        print("Usage: payout_dashboard.py payouts.csv [commission-paid.csv commission-received.csv]")
        sys.exit(1)
    payouts = load_payouts(sys.argv[1])
    paid = load_commissions(sys.argv[2], "paid") if len(sys.argv) > 2 else []
    recv = load_commissions(sys.argv[3], "received") if len(sys.argv) > 3 else []
    print_dashboard(payouts)
    print_calendar(payouts)
    print_status_board(payouts)
    print_commissions(paid, recv)


if __name__ == "__main__":
    main()
