#!/usr/bin/env python3
"""Ultimate Finance Tracker — clone of simonotion.gumroad.com/l/finance-tracker ($47 · 109 ratings · 5.0★)."""
import csv
import math
import sys
from collections import defaultdict

DEFAULT_TAX_PCT = 25.0


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


def load_subscriptions(path):
    return load_csv(
        path,
        ["name", "category", "monthly_cost", "renewal_day", "active"],
        ["monthly_cost", "renewal_day"],
    )


def load_investments(path):
    return load_csv(
        path,
        ["asset", "type", "units", "cost_basis", "current_value"],
        ["units", "cost_basis", "current_value"],
    )


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


def debt_schedule(debts, extra_pool=0.0):
    ordered = sorted(debts, key=lambda d: (-d["apr"], -d["balance"]))
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


def month_key(date_str):
    parts = date_str.split("-")
    return f"{parts[0]}-{parts[1]}" if len(parts) >= 2 else date_str


def dashboard(income, expenses, debts, savings, accounts, subscriptions, investments):
    total_income = sum(i["amount"] for i in income)
    total_expenses = sum(e["amount"] for e in expenses)
    net_cash = total_income - total_expenses
    savings_rate = (net_cash / total_income * 100) if total_income else 0.0

    by_category = defaultdict(float)
    for e in expenses:
        by_category[e["category"]] += e["amount"]

    monthly_income = defaultdict(float)
    monthly_expense = defaultdict(float)
    for i in income:
        monthly_income[month_key(i["date"])] += i["amount"]
    for e in expenses:
        monthly_expense[month_key(e["date"])] += e["amount"]

    active_subs = [s for s in subscriptions if s.get("active", "").lower() in ("yes", "y", "1", "true")]
    sub_monthly = sum(s["monthly_cost"] for s in active_subs)
    sub_annual = sub_monthly * 12

    inv_cost = sum(i["cost_basis"] for i in investments)
    inv_value = sum(i["current_value"] for i in investments)
    inv_gain = inv_value - inv_cost

    total_debt = sum(d["balance"] for d in debts)
    bank_assets = sum(
        a["balance"] for a in accounts
        if a["type"].lower() in ("asset", "checking", "savings")
    )
    investment_accounts = sum(
        a["balance"] for a in accounts if a["type"].lower() == "investment"
    )
    liabilities = sum(a["balance"] for a in accounts if a["type"].lower() == "liability")
    liabilities += total_debt
    net_worth = bank_assets + investment_accounts + inv_value - liabilities

    print("=== ULTIMATE FINANCE TRACKER (simonotion clone) ===")
    print(f"  Total income:        {fmt_money(total_income)}")
    print(f"  Total expenses:      {fmt_money(total_expenses)}")
    print(f"  Net cash flow:       {fmt_money(net_cash)}")
    print(f"  Savings rate:        {savings_rate:.1f}%")
    print()
    print("--- Monthly overview ---")
    months = sorted(set(monthly_income) | set(monthly_expense))
    for m in months:
        inc = monthly_income.get(m, 0)
        exp = monthly_expense.get(m, 0)
        print(f"  {m}  income {fmt_money(inc):>12}  expense {fmt_money(exp):>12}  net {fmt_money(inc - exp):>12}")
    print()
    print("--- Expense breakdown ---")
    for cat, amt in sorted(by_category.items(), key=lambda x: -x[1]):
        pct = (amt / total_expenses * 100) if total_expenses else 0
        print(f"  {cat:<22} {fmt_money(amt)}  ({pct:.0f}%)")
    print()
    print("--- Subscriptions (active) ---")
    for s in sorted(active_subs, key=lambda x: -x["monthly_cost"]):
        print(f"  {s['name']:<22} {fmt_money(s['monthly_cost'])}/mo  renew day {int(s['renewal_day'])}")
    print(f"  Total subscriptions: {fmt_money(sub_monthly)}/mo  ({fmt_money(sub_annual)}/yr)")
    print()
    print("--- Investments ---")
    for inv in investments:
        gain = inv["current_value"] - inv["cost_basis"]
        pct = (gain / inv["cost_basis"] * 100) if inv["cost_basis"] else 0
        print(
            f"  {inv['asset']:<12} {inv['type']:<12} "
            f"value {fmt_money(inv['current_value']):>10}  "
            f"gain {fmt_money(gain):>10} ({pct:+.1f}%)"
        )
    print(f"  Portfolio total:     {fmt_money(inv_value)}  (gain {fmt_money(inv_gain)})")
    print()
    print("--- Debt & loans (avalanche: highest APR first) ---")
    for row in debt_schedule(debts):
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
    print(f"  Bank accounts:       {fmt_money(bank_assets)}")
    print(f"  Investment accounts: {fmt_money(investment_accounts)}")
    print(f"  Portfolio (tracked): {fmt_money(inv_value)}")
    print(f"  Liabilities:         {fmt_money(liabilities)}")
    print(f"  Net worth:           {fmt_money(net_worth)}")


def summarize_guesswork(income_path, expense_path, subs_path, tax_pct=DEFAULT_TAX_PCT):
    """faisalmq/54h7: guesswork → clarity — one file replaces mental math."""
    income = load_income(income_path)
    expenses = load_expenses(expense_path)
    subscriptions = load_subscriptions(subs_path)
    collected = sum(i["amount"] for i in income)
    deductible = sum(e["amount"] for e in expenses)
    active_subs = [s for s in subscriptions if s.get("active", "").lower() in ("yes", "y", "1", "true")]
    sub_monthly = sum(s["monthly_cost"] for s in active_subs)
    sub_annual = sub_monthly * 12
    net_profit = collected - deductible
    tax_set_aside = max(net_profit, 0) * (tax_pct / 100.0)
    safe_to_spend = max(net_profit - tax_set_aside, 0)

    print("=== GUESSWORK → CLARITY (faisalmq/54h7 shape) ===")
    print("  Flying blind on bank balance ≠ knowing your numbers.")
    print("  One tracker file replaces mental math + scattered subscriptions.")
    print()
    print(f"  Gross income YTD:    {fmt_money(collected)}")
    print(f"  Expenses YTD:        {fmt_money(deductible)}")
    print(f"  Net profit:          {fmt_money(net_profit)}")
    print(f"  Tax set-aside ({tax_pct:.0f}%): {fmt_money(tax_set_aside)}")
    print(f"  Safe to spend:       {fmt_money(safe_to_spend)}")
    print()
    print("--- Subscription drag (often invisible) ---")
    for s in sorted(active_subs, key=lambda x: -x["monthly_cost"]):
        print(f"  {s['name']:<22} {fmt_money(s['monthly_cost'])}/mo")
    print(f"  Total:               {fmt_money(sub_monthly)}/mo  ({fmt_money(sub_annual)}/yr)")
    if sub_annual > 0 and collected:
        print(f"  = {sub_annual / collected * 100:.1f}% of gross income — before tax")
    print()
    print("  Update in 5 minutes/week. Future self thanks you at tax season.")
    print("  Guide: guesswork-guide.md · subscriptions-sample.csv")


def main():
    args = sys.argv[1:]
    if len(args) >= 4 and args[0] == "--guesswork":
        pct = float(args[4]) if len(args) >= 5 else DEFAULT_TAX_PCT
        summarize_guesswork(args[1], args[2], args[3], pct)
        return
    if len(args) < 7:
        print(
            "Usage: ultimate_finance_tracker.py "
            "income.csv expenses.csv debts.csv savings.csv accounts.csv subscriptions.csv investments.csv",
            file=sys.stderr,
        )
        print(
            "       ultimate_finance_tracker.py --guesswork income.csv expenses.csv subscriptions.csv [tax_pct]",
            file=sys.stderr,
        )
        sys.exit(1)
    dashboard(
        load_income(args[0]),
        load_expenses(args[1]),
        load_debts(args[2]),
        load_savings(args[3]),
        load_accounts(args[4]),
        load_subscriptions(args[5]),
        load_investments(args[6]),
    )


if __name__ == "__main__":
    main()
