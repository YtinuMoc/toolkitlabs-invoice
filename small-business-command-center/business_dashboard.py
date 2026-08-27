#!/usr/bin/env python3
"""Ultimate Small Business Command Center — clone of AnahitDigitalStudio tnjpdy ($12.99 Gumroad)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime

SCHEDULE_C = (
    "advertising", "contract_labor", "insurance", "legal_professional",
    "office_expense", "rent_lease", "supplies", "travel", "meals",
    "utilities", "software", "education", "other",
)


def load_csv(path, required=()):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if all(row.get(c, "").strip() for c in required):
                rows.append(row)
    return rows


def money(val):
    try:
        return float(str(val).replace("$", "").replace(",", "").strip())
    except ValueError:
        return 0.0


def parse_date(s):
    return datetime.strptime(s.strip(), "%Y-%m-%d")


def clients_summary(path):
    rows = load_csv(path, ("client_id", "name"))
    active = sum(1 for r in rows if r.get("status", "").strip().lower() == "active")
    print("\n=== CLIENT REGISTRY (AnahitDigitalStudio tnjpdy clone) ===")
    print(f"  Clients logged:  {len(rows)}")
    print(f"  Active clients:  {active}")
    if rows:
        print("\n  Top clients by service rate:")
        for r in sorted(rows, key=lambda x: money(x.get("rate", 0)), reverse=True)[:5]:
            print(f"    {r['name'][:30]:30} ${money(r.get('rate', 0)):,.2f}  {r.get('frequency', '')}")


def sales_summary(path):
    rows = load_csv(path, ("date", "amount"))
    total = sum(money(r["amount"]) for r in rows)
    by_client = defaultdict(float)
    for r in rows:
        by_client[r.get("client", "unknown")] += money(r["amount"])
    print("\n=== SALES LOG ===")
    print(f"  Transactions:    {len(rows)}")
    print(f"  Gross revenue:   ${total:,.2f}")
    if by_client:
        print("\n  Revenue by client:")
        for name, amt in sorted(by_client.items(), key=lambda x: -x[1])[:5]:
            print(f"    {name[:30]:30} ${amt:,.2f}")


def expenses_summary(path):
    rows = load_csv(path, ("date", "amount"))
    total = sum(money(r["amount"]) for r in rows)
    by_cat = defaultdict(float)
    for r in rows:
        by_cat[r.get("category", "other").strip().lower()] += money(r["amount"])
    print("\n=== EXPENSE LOG ===")
    print(f"  Expense lines:   {len(rows)}")
    print(f"  Total expenses:  ${total:,.2f}")
    if by_cat:
        print("\n  By category:")
        for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1])[:6]:
            print(f"    {cat:20} ${amt:,.2f}")


def invoices_summary(path):
    rows = load_csv(path, ("invoice_id", "amount"))
    today = datetime.now().date()
    unpaid = []
    overdue = []
    paid_total = 0.0
    outstanding = 0.0
    for r in rows:
        amt = money(r["amount"])
        paid = r.get("paid", "").strip().lower() in ("yes", "true", "1", "paid")
        if paid:
            paid_total += amt
        else:
            outstanding += amt
            unpaid.append(r)
            try:
                due = parse_date(r["due_date"]).date()
                if due < today:
                    overdue.append((r, amt, (today - due).days))
            except (KeyError, ValueError):
                pass
    print("\n=== INVOICE TRACKER ===")
    print(f"  Invoices logged: {len(rows)}")
    print(f"  Paid total:      ${paid_total:,.2f}")
    print(f"  Outstanding:     ${outstanding:,.2f}")
    print(f"  Unpaid count:    {len(unpaid)}")
    print(f"  Overdue count:   {len(overdue)}")
    if overdue:
        print("\n  Overdue invoices:")
        for r, amt, days in sorted(overdue, key=lambda x: -x[2])[:5]:
            print(f"    {r['invoice_id']:8} {r.get('client','')[:20]:20} ${amt:,.2f}  {days}d overdue")


def inventory_summary(path):
    rows = load_csv(path, ("item_id", "name"))
    low = [r for r in rows if money(r.get("qty_on_hand", 0)) <= money(r.get("reorder_level", 0))]
    print("\n=== INVENTORY LOG ===")
    print(f"  SKUs tracked:    {len(rows)}")
    print(f"  Low-stock items: {len(low)}")
    if low:
        print("\n  Reorder soon:")
        for r in low[:5]:
            print(f"    {r['name'][:28]:28} on hand {r.get('qty_on_hand','0')}  reorder {r.get('reorder_level','0')}")


def marketing_summary(path):
    rows = load_csv(path, ("campaign", "budget"))
    spend = sum(money(r.get("spend", 0)) for r in rows)
    budget = sum(money(r["budget"]) for r in rows)
    leads = sum(int(float(r.get("leads", 0) or 0)) for r in rows)
    conversions = sum(int(float(r.get("conversions", 0) or 0)) for r in rows)
    print("\n=== MARKETING CAMPAIGNS ===")
    print(f"  Campaigns:       {len(rows)}")
    print(f"  Budget total:    ${budget:,.2f}")
    print(f"  Spend total:     ${spend:,.2f}")
    print(f"  Leads:           {leads}")
    print(f"  Conversions:     {conversions}")
    if spend and conversions:
        print(f"  Cost per conv:   ${spend / conversions:,.2f}")


def launch_summary(path):
    rows = load_csv(path, ("launch_name", "target_date"))
    done = sum(1 for r in rows if r.get("status", "").strip().lower() == "done")
    print("\n=== PRODUCT LAUNCH PLANNER ===")
    print(f"  Launches tracked: {len(rows)}")
    print(f"  Completed:        {done}")
    if rows:
        print("\n  Upcoming / active:")
        for r in rows[:5]:
            print(f"    {r['launch_name'][:30]:30} {r.get('target_date','')}  {r.get('status','')}")


def pnl_block(sales_path, expense_path):
    sales = sum(money(r["amount"]) for r in load_csv(sales_path, ("date", "amount")))
    expenses = sum(money(r["amount"]) for r in load_csv(expense_path, ("date", "amount")))
    net = sales - expenses
    margin = (net / sales * 100) if sales else 0.0
    print("\n=== COMMAND CENTER DASHBOARD ===")
    print(f"  Gross revenue:   ${sales:,.2f}")
    print(f"  Total expenses:  ${expenses:,.2f}")
    print(f"  Net profit:      ${net:,.2f}")
    print(f"  Net margin:      {margin:.1f}%")
    print("\nClone target: anahitstudio.gumroad.com/l/tnjpdy ($12.99)")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 business_dashboard.py <sales> <expenses> <invoices> <clients> <inventory> <marketing> <launches>")
        print("Clone target: anahitstudio.gumroad.com/l/tnjpdy ($12.99)")
        sys.exit(1)
    paths = sys.argv[1:]
    labels = ["sales", "expenses", "invoices", "clients", "inventory", "marketing", "launches"]
    while len(paths) < 7:
        paths.append("")
    sales_path, exp_path, inv_path, cli_path, stock_path, mkt_path, launch_path = paths[:7]
    if sales_path and exp_path:
        pnl_block(sales_path, exp_path)
    if cli_path:
        clients_summary(cli_path)
    if sales_path:
        sales_summary(sales_path)
    if exp_path:
        expenses_summary(exp_path)
    if inv_path:
        invoices_summary(inv_path)
    if stock_path:
        inventory_summary(stock_path)
    if mkt_path:
        marketing_summary(mkt_path)
    if launch_path:
        launch_summary(launch_path)
    print("\nClone target: anahitstudio.gumroad.com/l/tnjpdy ($12.99)")


if __name__ == "__main__":
    main()
