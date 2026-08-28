#!/usr/bin/env python3
"""2026 Personal Finance Tracker — clone of ohmygoshna.gumroad.com/l/2026 ($13 · 7 ratings · 5.0★)."""
import csv
import math
import sys
from collections import defaultdict


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


def load_debts(path):
    return load_csv(
        path,
        ["issuer", "balance", "apr", "minimum_payment", "extra_payment"],
        ["balance", "apr", "minimum_payment", "extra_payment"],
    )


def load_savings(path):
    return load_csv(path, ["goal", "target", "current"], ["target", "current"])


def load_accounts(path):
    return load_csv(path, ["name", "type", "balance"], ["balance"])


def fmt_money(n):
    return f"${n:,.2f}"


def payoff_months(balance, apr, payment):
    if balance <= 0 or payment <= 0:
        return 0
    monthly_rate = apr / 100.0 / 12.0
    if monthly_rate == 0:
        return math.ceil(balance / payment)
    if payment <= balance * monthly_rate:
        return 999
    try:
        return math.ceil(
            -math.log(1 - (balance * monthly_rate) / payment) / math.log(1 + monthly_rate)
        )
    except (ValueError, ZeroDivisionError):
        return 999


def snowball_schedule(debts, extra_pool=0.0):
    ordered = sorted(debts, key=lambda d: d["balance"])
    schedule = []
    freed = extra_pool
    for rank, debt in enumerate(ordered, 1):
        payment = debt["minimum_payment"] + debt["extra_payment"] + freed
        months = payoff_months(debt["balance"], debt["apr"], payment)
        schedule.append({
            "rank": rank,
            "issuer": debt["issuer"],
            "balance": debt["balance"],
            "apr": debt["apr"],
            "payment": payment,
            "months": months,
        })
        freed = payment
    return schedule


def dashboard(income, expenses, debts, savings, accounts):
    total_income = sum(i["amount"] for i in income)
    total_expenses = sum(e["amount"] for e in expenses)
    net_cash = total_income - total_expenses
    savings_rate = (net_cash / total_income * 100) if total_income else 0.0

    by_category = defaultdict(float)
    for e in expenses:
        by_category[e["category"]] += e["amount"]

    total_debt = sum(d["balance"] for d in debts)
    assets = sum(a["balance"] for a in accounts if a["type"].lower() in ("asset", "checking", "savings", "investment"))
    liabilities = sum(a["balance"] for a in accounts if a["type"].lower() == "liability")
    liabilities += total_debt
    net_worth = assets - liabilities

    print("=== 2026 PERSONAL FINANCE TRACKER (ohmygoshna clone) ===")
    print(f"  Total income:        {fmt_money(total_income)}")
    print(f"  Total expenses:      {fmt_money(total_expenses)}")
    print(f"  Net cash flow:       {fmt_money(net_cash)}")
    print(f"  Savings rate:        {savings_rate:.1f}%")
    print()
    print("--- Expense breakdown ---")
    for cat, amt in sorted(by_category.items(), key=lambda x: -x[1]):
        print(f"  {cat:<22} {fmt_money(amt)}")
    print()
    print("--- Debt snowball (smallest balance first) ---")
    for row in snowball_schedule(debts):
        print(
            f"  #{row['rank']} {row['issuer']:<18} "
            f"bal {fmt_money(row['balance']):>10}  "
            f"APR {row['apr']:>5.2f}%  "
            f"pay {fmt_money(row['payment']):>8}/mo  "
            f"~{row['months']} mo"
        )
    print()
    print("--- Savings goals ---")
    for s in savings:
        pct = (s["current"] / s["target"] * 100) if s["target"] else 0
        print(f"  {s['goal']:<22} {fmt_money(s['current'])} / {fmt_money(s['target'])} ({pct:.0f}%)")
    print()
    print("--- Net worth ---")
    print(f"  Assets:              {fmt_money(assets)}")
    print(f"  Liabilities:         {fmt_money(liabilities)}")
    print(f"  Net worth:           {fmt_money(net_worth)}")


def main():
    if len(sys.argv) < 6:
        print(
            "Usage: personal_finance_tracker_2026.py "
            "income.csv expenses.csv debts.csv savings.csv accounts.csv",
            file=sys.stderr,
        )
        sys.exit(1)
    dashboard(
        load_income(sys.argv[1]),
        load_expenses(sys.argv[2]),
        load_debts(sys.argv[3]),
        load_savings(sys.argv[4]),
        load_accounts(sys.argv[5]),
    )


if __name__ == "__main__":
    main()
