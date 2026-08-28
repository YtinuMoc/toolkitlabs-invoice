#!/usr/bin/env python3
"""Freelance Dashboard — clone of cedabranding.gumroad.com/l/pro-dashboard ($97 · 1251 sales)."""
import csv
import sys
from collections import defaultdict

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
    if len(sys.argv) >= 4 and sys.argv[1] == "--spreadsheet-trap":
        tax_pct = float(sys.argv[4]) if len(sys.argv) > 4 else DEFAULT_TAX_PCT
        summarize_spreadsheet_trap(sys.argv[2], sys.argv[3], tax_pct)
        return
    if len(sys.argv) < 3:
        print("Usage: freelance_dashboard_tracker.py revenue.csv expenses.csv [tax_pct]")
        print("       freelance_dashboard_tracker.py --daily-check revenue.csv expenses.csv [tax_pct]")
        print("       freelance_dashboard_tracker.py --spreadsheet-trap revenue.csv expenses.csv [tax_pct]")
        print("Clone target: cedabranding.gumroad.com/l/pro-dashboard ($97 · 1251 sales · 69 ratings)")
        sys.exit(1)
    revenue = load_revenue(sys.argv[1])
    expenses = load_expenses(sys.argv[2])
    tax_pct = float(sys.argv[3]) if len(sys.argv) > 3 else DEFAULT_TAX_PCT
    d = summarize(revenue, expenses, tax_pct)
    print_dashboard(d)


if __name__ == "__main__":
    main()
