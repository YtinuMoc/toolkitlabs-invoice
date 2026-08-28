#!/usr/bin/env python3
"""Notion Finance Tracker — clone of rosidssoy.gumroad.com/l/financetracker ($5+ · 190 ratings · 13,696 sales)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime

DEFAULT_TAX_PCT = 25.0
SE_IF_TAX = 0.153  # self-employment tax approximation


def load_csv(path, fields, float_fields=None):
    float_fields = float_fields or []
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                parsed = {k: row.get(k, "").strip() for k in fields}
                for ff in float_fields:
                    if ff in parsed:
                        parsed[ff] = float(parsed.get(ff) or 0)
                rows.append(parsed)
            except (KeyError, ValueError):
                continue
    return rows


def load_income(path):
    return load_csv(path, ["date", "source", "category", "amount"], ["amount"])


def load_expenses(path):
    return load_csv(path, ["date", "category", "description", "amount"], ["amount"])


def load_accounts(path):
    return load_csv(path, ["name", "type", "balance"], ["balance"])


def load_goals(path):
    return load_csv(path, ["goal", "target", "current", "deadline"], ["target", "current"])


def load_debts(path):
    return load_csv(
        path,
        ["issuer", "balance", "apr", "minimum_payment", "extra_payment"],
        ["balance", "apr", "minimum_payment", "extra_payment"],
    )


def load_subscriptions(path):
    return load_csv(
        path,
        ["name", "category", "monthly_cost", "renewal_day", "active"],
        ["monthly_cost", "renewal_day"],
    )


def fmt_money(n):
    return f"${n:,.2f}"


def quarter_key(date_str):
    try:
        dt = datetime.strptime(date_str[:10], "%Y-%m-%d")
        return f"{dt.year}-Q{(dt.month - 1) // 3 + 1}"
    except ValueError:
        return "unknown"


def summarize_dashboard(income_path, expense_path, accounts_path, goals_path, debts_path, subs_path):
    income = load_income(income_path)
    expenses = load_expenses(expense_path)
    accounts = load_accounts(accounts_path)
    goals = load_goals(goals_path)
    debts = load_debts(debts_path)
    subscriptions = load_subscriptions(subs_path)

    total_income = sum(i["amount"] for i in income)
    total_expenses = sum(e["amount"] for e in expenses)
    net_cash = total_income - total_expenses
    savings_rate = (net_cash / total_income * 100) if total_income else 0

    by_category = defaultdict(float)
    for e in expenses:
        by_category[e["category"]] += e["amount"]

    active_subs = [s for s in subscriptions if s.get("active", "").lower() in ("yes", "y", "1", "true")]
    sub_monthly = sum(s["monthly_cost"] for s in active_subs)

    assets = sum(a["balance"] for a in accounts if a["type"].lower() in ("asset", "checking", "savings", "investment"))
    liabilities = sum(a["balance"] for a in accounts if a["type"].lower() == "liability")
    liabilities += sum(d["balance"] for d in debts)
    net_worth = assets - liabilities

    print("=== NOTION FINANCE TRACKER (rosidssoy clone) ===")
    print(f"  Total income:        {fmt_money(total_income)}")
    print(f"  Total expenses:      {fmt_money(total_expenses)}")
    print(f"  Net cash flow:       {fmt_money(net_cash)}")
    print(f"  Savings rate:        {savings_rate:.1f}%")
    print()
    print("--- Expense breakdown ---")
    for cat, amt in sorted(by_category.items(), key=lambda x: -x[1]):
        pct = (amt / total_expenses * 100) if total_expenses else 0
        print(f"  {cat:<22} {fmt_money(amt)}  ({pct:.0f}%)")
    print()
    print("--- Subscriptions (active) ---")
    for s in sorted(active_subs, key=lambda x: -x["monthly_cost"]):
        print(f"  {s['name']:<22} {fmt_money(s['monthly_cost'])}/mo")
    print(f"  Total:               {fmt_money(sub_monthly)}/mo  ({fmt_money(sub_monthly * 12)}/yr)")
    print()
    print("--- Financial goals ---")
    for g in goals:
        pct = (g["current"] / g["target"] * 100) if g["target"] else 0
        print(f"  {g['goal']:<22} {fmt_money(g['current'])} / {fmt_money(g['target'])} ({pct:.0f}%)  due {g['deadline']}")
    print()
    print("--- Accounts & net worth ---")
    for a in accounts:
        print(f"  {a['name']:<22} {a['type']:<12} {fmt_money(a['balance'])}")
    print(f"  Net worth:           {fmt_money(net_worth)}")


def summarize_quarterly_tax(income_path, expense_path, tax_pct=DEFAULT_TAX_PCT, hourly_rate=75.0):
    """wilsonhoe/4lhd: tax season cash crunch → quarterly set-aside system."""
    income = load_income(income_path)
    expenses = load_expenses(expense_path)

    quarterly_income = defaultdict(float)
    quarterly_expense = defaultdict(float)
    for i in income:
        quarterly_income[quarter_key(i["date"])] += i["amount"]
    for e in expenses:
        quarterly_expense[quarter_key(e["date"])] += e["amount"]

    total_income = sum(i["amount"] for i in income)
    total_expenses = sum(e["amount"] for e in expenses)
    net_profit = total_income - total_expenses
    income_tax = max(net_profit, 0) * (tax_pct / 100.0)
    se_tax = max(net_profit, 0) * SE_IF_TAX
    total_tax = income_tax + se_tax
    workdays_lost = 33
    lost_earnings = workdays_lost * 8 * hourly_rate

    print("=== QUARTERLY TAX SYSTEM (wilsonhoe/4lhd shape) ===")
    print("  Xero 2026: solopreneurs lose ~33 workdays/year to tax chaos.")
    print(f"  At ${hourly_rate:.0f}/hr effective rate: ~{fmt_money(lost_earnings)} in lost earning capacity.")
    print()
    print("--- Quarterly income vs expenses ---")
    quarters = sorted(set(quarterly_income) | set(quarterly_expense))
    for q in quarters:
        inc = quarterly_income.get(q, 0)
        exp = quarterly_expense.get(q, 0)
        net = inc - exp
        q_tax = max(net, 0) * ((tax_pct + SE_IF_TAX * 100) / 100.0)
        print(f"  {q}  income {fmt_money(inc):>12}  expense {fmt_money(exp):>12}  net {fmt_money(net):>12}  set-aside {fmt_money(q_tax):>10}")
    print()
    print("--- Annual tax reserve (estimated) ---")
    print(f"  Gross profit YTD:    {fmt_money(net_profit)}")
    print(f"  Income tax ({tax_pct:.0f}%):     {fmt_money(income_tax)}")
    print(f"  SE tax (~15.3%):     {fmt_money(se_tax)}")
    print(f"  Total reserve:       {fmt_money(total_tax)}")
    print(f"  Per quarter (÷4):    {fmt_money(total_tax / 4 if total_tax else 0)}")
    print()
    print("  Fix: log income weekly → run this CLI each quarter → no April shoebox scramble.")
    print("  Guide: tax-quarter-guide.md")


def main():
    args = sys.argv[1:]
    if not args:
        print("Usage: notion_finance_tracker.py <income> <expenses> <accounts> <goals> <debts> <subscriptions>")
        print("       notion_finance_tracker.py --quarterly-tax <income> <expenses>")
        sys.exit(1)
    if args[0] == "--quarterly-tax":
        summarize_quarterly_tax(args[1], args[2])
    else:
        if len(args) < 6:
            print("Need 6 CSV paths for dashboard mode")
            sys.exit(1)
        summarize_dashboard(*args[:6])


if __name__ == "__main__":
    main()
