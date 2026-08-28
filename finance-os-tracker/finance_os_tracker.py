#!/usr/bin/env python3
"""Finance OS — clone of heyismail.gumroad.com/l/TheUltimateFinanceTracker ($29+ · 15,254 sales)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime

DEFAULT_TAX_PCT = 25.0


def load_csv(path, fields):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                parsed = {k: row.get(k, "").strip() for k in fields}
                if "amount" in parsed or "balance" in parsed or "target" in parsed:
                    for num_field in ("amount", "balance", "target", "current", "monthly_limit"):
                        if num_field in parsed:
                            parsed[num_field] = float(parsed.get(num_field) or 0)
                if "active" in parsed:
                    parsed["active"] = parsed["active"].lower() in ("yes", "y", "1", "true")
                rows.append(parsed)
            except (KeyError, ValueError):
                continue
    return rows


def load_income(path):
    return load_csv(path, ["date", "source", "category", "amount", "account"])


def load_expenses(path):
    return load_csv(path, ["date", "category", "description", "amount", "account"])


def load_budgets(path):
    return load_csv(path, ["category", "monthly_limit"])


def load_subscriptions(path):
    return load_csv(path, ["name", "amount", "renewal_day", "active"])


def load_accounts(path):
    return load_csv(path, ["name", "type", "balance"])


def load_goals(path):
    return load_csv(path, ["name", "target", "current"])


def month_key(date_str):
    return date_str[:7] if len(date_str) >= 7 else "unknown"


def fmt_money(n):
    return f"${n:,.2f}"


def dashboard(income, expenses, budgets, subscriptions, accounts, goals, tax_pct=DEFAULT_TAX_PCT):
    total_income = sum(i["amount"] for i in income)
    total_expenses = sum(e["amount"] for e in expenses)
    net = total_income - total_expenses
    margin = (net / total_income * 100) if total_income else 0.0
    tax_set_aside = max(net, 0) * (tax_pct / 100.0)

    by_month = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    by_category = defaultdict(float)
    for i in income:
        by_month[month_key(i["date"])]["income"] += i["amount"]
    for e in expenses:
        by_month[month_key(e["date"])]["expense"] += e["amount"]
        by_category[e["category"]] += e["amount"]

    budget_actual = {}
    for b in budgets:
        cat = b["category"]
        budget_actual[cat] = {"limit": b["monthly_limit"], "spent": by_category.get(cat, 0.0)}

    active_subs = [s for s in subscriptions if s.get("active", True)]
    sub_monthly = sum(s["amount"] for s in active_subs)

    assets = sum(a["balance"] for a in accounts if a["type"].lower() == "asset")
    liabilities = sum(a["balance"] for a in accounts if a["type"].lower() == "liability")
    net_worth = assets - liabilities

    goal_progress = []
    for g in goals:
        pct = (g["current"] / g["target"] * 100) if g["target"] else 0.0
        goal_progress.append({**g, "pct": pct})

    return {
        "total_income": total_income,
        "total_expenses": total_expenses,
        "net": net,
        "margin": margin,
        "tax_set_aside": tax_set_aside,
        "by_month": dict(by_month),
        "by_category": dict(by_category),
        "budget_actual": budget_actual,
        "sub_monthly": sub_monthly,
        "active_subs": active_subs,
        "assets": assets,
        "liabilities": liabilities,
        "net_worth": net_worth,
        "accounts": accounts,
        "goals": goal_progress,
        "tax_pct": tax_pct,
    }


def print_dashboard(d):
    print("=== FINANCE OS (heyismail TheUltimateFinanceTracker clone) ===")
    print(f"  Total income:        {fmt_money(d['total_income'])}")
    print(f"  Total expenses:      {fmt_money(d['total_expenses'])}")
    print(f"  Net cash flow:       {fmt_money(d['net'])}")
    print(f"  Profit margin:       {d['margin']:.1f}%")
    print(f"  Tax set-aside ({d['tax_pct']:.0f}%): {fmt_money(d['tax_set_aside'])}")

    if d["by_month"]:
        print("\n--- Monthly overview ---")
        for m in sorted(d["by_month"]):
            row = d["by_month"][m]
            net = row["income"] - row["expense"]
            print(f"  {m}  income {fmt_money(row['income']):>12}  expense {fmt_money(row['expense']):>12}  net {fmt_money(net):>12}")

    if d["budget_actual"]:
        print("\n--- Budget vs actual ---")
        for cat, row in sorted(d["budget_actual"].items()):
            spent = row["spent"]
            limit = row["limit"]
            pct = (spent / limit * 100) if limit else 0.0
            flag = " OVER" if limit and spent > limit else ""
            print(f"  {cat:20s} spent {fmt_money(spent):>10} / limit {fmt_money(limit):>10} ({pct:.0f}%){flag}")

    if d["active_subs"]:
        print(f"\n--- Subscriptions ({len(d['active_subs'])} active · {fmt_money(d['sub_monthly'])}/mo) ---")
        for s in sorted(d["active_subs"], key=lambda x: -x["amount"]):
            print(f"  {s['name']:24s} {fmt_money(s['amount']):>10}/mo  renews day {s.get('renewal_day', '?')}")

    if d["accounts"]:
        print(f"\n--- Net worth ---")
        print(f"  Assets:              {fmt_money(d['assets'])}")
        print(f"  Liabilities:         {fmt_money(d['liabilities'])}")
        print(f"  Net worth:           {fmt_money(d['net_worth'])}")
        for a in d["accounts"]:
            print(f"    {a['name']:22s} ({a['type']}) {fmt_money(a['balance'])}")

    if d["goals"]:
        print("\n--- Financial goals ---")
        for g in d["goals"]:
            print(f"  {g['name']:24s} {fmt_money(g['current']):>10} / {fmt_money(g['target']):>10} ({g['pct']:.0f}%)")


def main():
    args = sys.argv[1:]
    if len(args) < 5:
        print("Usage: finance_os_tracker.py income.csv expenses.csv budgets.csv subscriptions.csv accounts.csv [goals.csv] [tax_pct]")
        print("Clone target: heyismail.gumroad.com/l/TheUltimateFinanceTracker ($29+ · 15,254 sales)")
        sys.exit(1)

    income = load_income(args[0])
    expenses = load_expenses(args[1])
    budgets = load_budgets(args[2])
    subscriptions = load_subscriptions(args[3])
    accounts = load_accounts(args[4])
    goals = load_goals(args[5]) if len(args) > 5 and args[5].endswith(".csv") else []
    tax_arg_idx = 6 if goals else 5
    tax_pct = float(args[tax_arg_idx]) if len(args) > tax_arg_idx and not args[tax_arg_idx].endswith(".csv") else DEFAULT_TAX_PCT
    if len(args) > 5 and args[5].endswith(".csv") and len(args) > 6:
        tax_pct = float(args[6])

    d = dashboard(income, expenses, budgets, subscriptions, accounts, goals, tax_pct)
    print_dashboard(d)


if __name__ == "__main__":
    main()
