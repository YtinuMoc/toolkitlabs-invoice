#!/usr/bin/env python3
"""Freelance Dashboard — clone of cedabranding.gumroad.com/l/pro-dashboard ($97 · 1251 sales)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime

DEFAULT_TAX_PCT = 25.0


def load_revenue(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                rows.append({
                    "date": row.get("date", "").strip(),
                    "client": row.get("client", "").strip(),
                    "description": row.get("description", "").strip(),
                    "amount": float(row.get("amount") or 0),
                    "category": row.get("category", "Services").strip(),
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


def month_key(date_str):
    return date_str[:7] if len(date_str) >= 7 else "unknown"


def fmt_money(n):
    return f"${n:,.2f}"


def summarize(revenue, expenses, tax_pct=DEFAULT_TAX_PCT):
    total_revenue = sum(r["amount"] for r in revenue)
    total_expenses = sum(e["amount"] for e in expenses)
    deductible = sum(e["amount"] for e in expenses if e["deductible"])
    net_profit = total_revenue - total_expenses
    tax_set_aside = max(net_profit, 0) * (tax_pct / 100.0)
    safe_to_spend = max(net_profit - tax_set_aside, 0)

    by_month = defaultdict(lambda: {"revenue": 0.0, "expense": 0.0})
    by_client = defaultdict(float)
    by_expense_cat = defaultdict(float)

    for r in revenue:
        by_month[month_key(r["date"])]["revenue"] += r["amount"]
        by_client[r["client"]] += r["amount"]

    for e in expenses:
        by_month[month_key(e["date"])]["expense"] += e["amount"]
        by_expense_cat[e["category"]] += e["amount"]

    months_with_data = [m for m in by_month if m != "unknown"]
    avg_monthly_expense = (
        sum(by_month[m]["expense"] for m in months_with_data) / len(months_with_data)
        if months_with_data else 0.0
    )
    cash_buffer = safe_to_spend
    runway_months = (cash_buffer / avg_monthly_expense) if avg_monthly_expense > 0 else 0.0

    return {
        "total_revenue": total_revenue,
        "total_expenses": total_expenses,
        "deductible_expenses": deductible,
        "net_profit": net_profit,
        "tax_set_aside": tax_set_aside,
        "safe_to_spend": safe_to_spend,
        "tax_pct": tax_pct,
        "by_month": dict(by_month),
        "by_client": dict(by_client),
        "by_expense_cat": dict(by_expense_cat),
        "avg_monthly_expense": avg_monthly_expense,
        "runway_months": runway_months,
    }


def day_key(date_str):
    return date_str[:10] if len(date_str) >= 10 else "unknown"


def summarize_daily_check(revenue_path, expense_path, tax_pct=DEFAULT_TAX_PCT):
    """wilsonhoe/4413368 2kdc: 5-minute daily money check → planning-layer dashboard."""
    revenue = load_revenue(revenue_path)
    expenses = load_expenses(expense_path)
    d = summarize(revenue, expenses, tax_pct)

    by_day_rev = defaultdict(float)
    by_day_exp = defaultdict(float)
    for r in revenue:
        by_day_rev[day_key(r["date"])] += r["amount"]
    for e in expenses:
        by_day_exp[day_key(e["date"])] += e["amount"]

    all_days = sorted(set(by_day_rev) | set(by_day_exp) - {"unknown"})
    recent_days = all_days[-7:] if all_days else []

    print("=== 5-MINUTE DAILY MONEY CHECK (wilsonhoe/2kdc shape) ===")
    print("  Monthly P&L is a tax record. Daily log = steering wheel.")
    print("  Solopreneurs who look daily catch problems ~3 weeks earlier.")
    print()
    print("--- 90-second daily protocol ---")
    print("  1. Log today's deposits and expenses (30 sec)")
    print("  2. Glance at 7-day rolling net — up, flat, or down? (30 sec)")
    print("  3. Flag one anomaly: late client, unusual charge, sub creep (30 sec)")
    print()

    if all_days:
        today = all_days[-1]
        rev_today = by_day_rev.get(today, 0.0)
        exp_today = by_day_exp.get(today, 0.0)
        print(f"--- Today ({today}) ---")
        print(f"  Revenue in:          {fmt_money(rev_today)}")
        print(f"  Expenses out:        {fmt_money(exp_today)}")
        print(f"  Net today:           {fmt_money(rev_today - exp_today)}")
        print()

    if recent_days:
        print("--- 7-day rolling trend ---")
        rolling_net = 0.0
        for day in recent_days:
            rev = by_day_rev.get(day, 0.0)
            exp = by_day_exp.get(day, 0.0)
            net = rev - exp
            rolling_net += net
            print(f"  {day}  in {fmt_money(rev):>10}  out {fmt_money(exp):>10}  net {fmt_money(net):>10}")
        avg_daily = rolling_net / len(recent_days)
        trend = "rising" if avg_daily > 50 else ("flat" if avg_daily >= -50 else "drifting down")
        print(f"  7-day net: {fmt_money(rolling_net)}  avg/day {fmt_money(avg_daily)}  trend: {trend}")
        print()

    flags = []
    if d["runway_months"] < 3:
        flags.append(f"LOW RUNWAY: {d['runway_months']:.1f} months at current burn")
    if d["by_client"]:
        top_client, top_amt = max(d["by_client"].items(), key=lambda x: x[1])
        pct = (top_amt / d["total_revenue"] * 100) if d["total_revenue"] else 0
        if pct > 50:
            flags.append(f"CLIENT CONCENTRATION: {top_client} = {pct:.0f}% of revenue")
    if d["by_expense_cat"]:
        top_cat, top_exp = max(d["by_expense_cat"].items(), key=lambda x: x[1])
        if top_exp > d["total_expenses"] * 0.4:
            flags.append(f"EXPENSE SPIKE WATCH: {top_cat} = {fmt_money(top_exp)}")

    print("--- Flags (catch problems early) ---")
    if flags:
        for f in flags:
            print(f"  ⚠ {f}")
    else:
        print("  ✓ No immediate flags — keep logging daily")
    print()
    print_dashboard(d)
    print()
    print(f"  Safe to spend:       {fmt_money(d['safe_to_spend'])} (after {d['tax_pct']:.0f}% tax set-aside)")
    print(f"  Cash runway:         {d['runway_months']:.1f} months")
    print("  Guide: daily-check-guide.md · revenue-sample.csv · expenses-sample.csv")


def summarize_finance_tracker(revenue_path, expense_path, tax_pct=DEFAULT_TAX_PCT):
    """faisalmq/5598: wing-it accounting → income vs expenses → tax set-aside → profit margins."""
    revenue = load_revenue(revenue_path)
    expenses = load_expenses(expense_path)
    d = summarize(revenue, expenses, tax_pct)
    margin_pct = (d["net_profit"] / d["total_revenue"] * 100) if d["total_revenue"] else 0.0
    print("=== FREELANCE FINANCE TRACKER (faisalmq/5598 shape) ===")
    print("  Wing-it accounting = mental tax. Simple tracker = peace of mind.")
    print("  Track income vs expenses · automate tax set-aside · monitor profit margins.")
    print()
    print(f"  Total income:        {fmt_money(d['total_revenue'])}")
    print(f"  Total expenses:      {fmt_money(d['total_expenses'])}")
    print(f"  Net profit:          {fmt_money(d['net_profit'])}")
    print(f"  Profit margin:       {margin_pct:.1f}%")
    print(f"  Tax set-aside ({d['tax_pct']:.0f}%): {fmt_money(d['tax_set_aside'])}")
    print(f"  Safe to spend:       {fmt_money(d['safe_to_spend'])}")
    print()
    if d["by_client"]:
        total = d["total_revenue"]
        print("--- Revenue by client (% of total) ---")
        for client, amt in sorted(d["by_client"].items(), key=lambda x: -x[1]):
            pct = (amt / total * 100) if total else 0
            print(f"  {client:24s} {fmt_money(amt):>12}  ({pct:5.1f}%)")
        print()
    if d["by_expense_cat"]:
        print("--- Expenses by category ---")
        for cat, amt in sorted(d["by_expense_cat"].items(), key=lambda x: -x[1]):
            print(f"  {cat:24s} {fmt_money(amt)}")
        print()
    print(f"  Cash runway:         {d['runway_months']:.1f} months at avg burn {fmt_money(d['avg_monthly_expense'])}/mo")
    print("  Guide: freelance-finance-tracker-guide.md · revenue-sample.csv · expenses-sample.csv")


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


def summarize_net_income(revenue_path, expense_path, tax_pct=DEFAULT_TAX_PCT):
    """faisalmq/5797: net income visibility — safe-to-spend after tax + subscriptions."""
    revenue = load_revenue(revenue_path)
    expenses = load_expenses(expense_path)
    collected = sum(r["amount"] for r in revenue)
    deductible = sum(e["amount"] for e in expenses)
    subs = sum(
        e["amount"] for e in expenses
        if e["category"].lower() in ("software", "subscriptions", "saas", "tools")
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
    print("  Guide: net-income-guide.md · revenue-sample.csv · expenses-sample.csv")


def summarize_tax_buffer(revenue_path, expense_path, reserve_pct=DEFAULT_TAX_PCT):
    """faisalmq/4gao: deposit lands → per-payment buffer → tax-only savings → dashboard upsell."""
    revenue = load_revenue(revenue_path)
    expenses = load_expenses(expense_path)
    collected = sum(r["amount"] for r in revenue)
    deductible = sum(e["amount"] for e in expenses)
    net_profit = collected - deductible
    tax_buffer = max(net_profit, 0) * reserve_pct / 100
    safe_to_spend = max(net_profit - tax_buffer, 0)
    print("\n=== PER-PAYMENT TAX BUFFER (faisalmq/4gao shape) ===")
    print("  Deposit lands → five minutes of joy → tax panic → buffer same day.")
    print(f"  {'Client':<20} {'Collected':>12} {'Buffer':>10} {'Safe':>12}")
    for r in revenue:
        share = r["amount"] / collected if collected else 0
        buf = net_profit * share * reserve_pct / 100 if net_profit > 0 else 0
        safe = r["amount"] - buf
        label = (r["client"] or r["description"] or "Payment")[:20]
        print(f"  {label:<20} ${r['amount']:>10,.2f} ${buf:>8,.2f} ${safe:>10,.2f}")
    print("\n=== EXPENSE + TAX BUFFER ===")
    print(f"  Expenses YTD:        ${deductible:,.2f}")
    print(f"  Net profit:            ${net_profit:,.2f}")
    print(f"  Tax buffer ({reserve_pct:.0f}%):   ${tax_buffer:,.2f}")
    print(f"  Safe to spend:       ${safe_to_spend:,.2f}")
    print("  Transfer buffer to tax-only savings when payment lands — not in April.")
    print("  Guide: tax-buffer-guide.md · revenue-sample.csv · expenses-sample.csv")


def summarize_spreadsheet_trap(revenue_path, expense_path, tax_pct=DEFAULT_TAX_PCT):
    """wilsonhoe/4383424 4khk: spreadsheet trap → planning-layer dashboard."""
    revenue = load_revenue(revenue_path)
    expenses = load_expenses(expense_path)
    d = summarize(revenue, expenses, tax_pct)
    print("=== SPREADSHEET TRAP → FREELANCE DASHBOARD (wilsonhoe/4khk shape) ===")
    print("  Tier 1 spreadsheet cost (hidden): ~$11K–$13K/year in errors + time + missed insight.")
    print("  Tier 2 accounting software: $1,680–$4,080/year subscription — ledger, not planning.")
    print("  Tier 3 planning layer: one dashboard that turns numbers into weekly decisions.")
    print()
    print("--- 15-minute weekly protocol ---")
    print("  1. Log weekend transactions (2 min)")
    print("  2. Check cash runway months at current burn (3 min)")
    print("  3. Review which clients drove revenue this week (5 min)")
    print("  4. Flag one decision: raise price, cut sub, chase invoice (5 min)")
    print()
    print_dashboard(d)
    print()
    print(f"  Cash runway:         {d['runway_months']:.1f} months at avg burn {fmt_money(d['avg_monthly_expense'])}/mo")
    print(f"  Safe to spend:       {fmt_money(d['safe_to_spend'])} (after {d['tax_pct']:.0f}% tax set-aside)")
    print("  Guide: spreadsheet-trap-guide.md · revenue-sample.csv · expenses-sample.csv")


def print_dashboard(d):
    print("=== FREELANCE DASHBOARD (cedabranding pro-dashboard clone) ===")
    print(f"  Total revenue:       {fmt_money(d['total_revenue'])}")
    print(f"  Total expenses:      {fmt_money(d['total_expenses'])}")
    print(f"  Net profit:          {fmt_money(d['net_profit'])}")
    print(f"  Tax set-aside ({d['tax_pct']:.0f}%): {fmt_money(d['tax_set_aside'])}")
    print(f"  Safe to spend:       {fmt_money(d['safe_to_spend'])}")

    if d["by_month"]:
        print("\n--- Monthly dashboard ---")
        for m in sorted(d["by_month"].keys()):
            if m == "unknown":
                continue
            rev = d["by_month"][m]["revenue"]
            exp = d["by_month"][m]["expense"]
            net = rev - exp
            margin = (net / rev * 100) if rev else 0.0
            reserve = max(net, 0) * (d["tax_pct"] / 100.0)
            home = max(net - reserve, 0)
            print(
                f"  {m}  rev {fmt_money(rev):>12}  exp {fmt_money(exp):>12}  "
                f"net {fmt_money(net):>12}  margin {margin:5.1f}%  take-home {fmt_money(home)}"
            )

    if d["by_client"]:
        total = d["total_revenue"]
        print("\n--- Revenue by client (% of total) ---")
        for client, amt in sorted(d["by_client"].items(), key=lambda x: -x[1]):
            pct = (amt / total * 100) if total else 0
            print(f"  {client:24s} {fmt_money(amt):>12}  ({pct:5.1f}%)")

    if d["by_expense_cat"]:
        print("\n--- Expenses by category ---")
        for cat, amt in sorted(d["by_expense_cat"].items(), key=lambda x: -x[1]):
            print(f"  {cat:24s} {fmt_money(amt)}")


def main():
    if len(sys.argv) >= 4 and sys.argv[1] == "--daily-check":
        tax_pct = float(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_TAX_PCT
        summarize_daily_check(sys.argv[2], sys.argv[3], tax_pct)
        return
    if len(sys.argv) >= 4 and sys.argv[1] == "--finance-tracker":
        tax_pct = float(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_TAX_PCT
        summarize_finance_tracker(sys.argv[2], sys.argv[3], tax_pct)
        return
    if len(sys.argv) >= 4 and sys.argv[1] == "--spreadsheet-trap":
        tax_pct = float(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_TAX_PCT
        summarize_spreadsheet_trap(sys.argv[2], sys.argv[3], tax_pct)
        return
    if len(sys.argv) >= 4 and sys.argv[1] == "--tax-buffer":
        tax_pct = float(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_TAX_PCT
        summarize_tax_buffer(sys.argv[2], sys.argv[3], tax_pct)
        return
    if len(sys.argv) >= 4 and sys.argv[1] == "--net-income":
        tax_pct = float(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_TAX_PCT
        summarize_net_income(sys.argv[2], sys.argv[3], tax_pct)
        return
    if len(sys.argv) >= 3 and sys.argv[1] == "--invoice-panic":
        summarize_invoice_panic(load_invoices(sys.argv[2]))
        return
    if len(sys.argv) < 3:
        print("Usage: freelance_dashboard_tracker.py revenue.csv expenses.csv [tax_pct]")
        print("       freelance_dashboard_tracker.py --daily-check revenue.csv expenses.csv [tax_pct]")
        print("       freelance_dashboard_tracker.py --finance-tracker revenue.csv expenses.csv [tax_pct]")
        print("       freelance_dashboard_tracker.py --spreadsheet-trap revenue.csv expenses.csv [tax_pct]")
        print("       freelance_dashboard_tracker.py --tax-buffer revenue.csv expenses.csv [tax_pct]")
        print("       freelance_dashboard_tracker.py --net-income revenue.csv expenses.csv [tax_pct]")
        print("       freelance_dashboard_tracker.py --invoice-panic invoices.csv")
        print("Clone target: cedabranding.gumroad.com/l/pro-dashboard ($97 · 1251 sales · 69 ratings)")
        sys.exit(1)
    revenue = load_revenue(sys.argv[1])
    expenses = load_expenses(sys.argv[2])
    tax_pct = float(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_TAX_PCT
    d = summarize(revenue, expenses, tax_pct)
    print_dashboard(d)


if __name__ == "__main__":
    main()
