#!/usr/bin/env python3
"""2026 Personal Finance Tracker — clone of ohmygoshna.gumroad.com/l/2026 ($13 · 7 ratings · 5.0★)."""
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


def summarize_tax_buffer(income_path, expense_path, reserve_pct=DEFAULT_TAX_PCT):
    """faisalmq/4gao: per-payment buffer + YTD safe-to-spend."""
    income = load_income(income_path)
    expenses = load_expenses(expense_path)
    collected = sum(i["amount"] for i in income)
    deductible = sum(e["amount"] for e in expenses)
    net_profit = collected - deductible
    tax_buffer = max(net_profit, 0) * reserve_pct / 100
    safe_to_spend = max(net_profit - tax_buffer, 0)
    print("\n=== PER-PAYMENT TAX BUFFER (faisalmq/4gao shape) ===")
    print(f"  {'Source':<20} {'Collected':>12} {'Buffer':>10} {'Safe':>12}")
    for i in income:
        share = i["amount"] / collected if collected else 0
        buf = net_profit * share * reserve_pct / 100 if net_profit > 0 else 0
        safe = i["amount"] - buf
        print(f"  {i['source'][:20]:<20} ${i['amount']:>10,.2f} ${buf:>8,.2f} ${safe:>10,.2f}")
    print("\n=== EXPENSE + TAX BUFFER ===")
    print(f"  Expenses YTD:        ${deductible:,.2f}")
    print(f"  Net cash flow:         ${net_profit:,.2f}")
    print(f"  Tax buffer ({reserve_pct:.0f}%):   ${tax_buffer:,.2f}")
    print(f"  Safe to spend:       ${safe_to_spend:,.2f}")
    print("  Transfer buffer to tax-only savings when payment lands — not in April.")
    print("  Guide: tax-buffer-guide.md · income-sample.csv · expenses-sample.csv")


def main():
    args = sys.argv[1:]
    if len(args) >= 3 and args[0] == "--tax-buffer":
        pct = float(args[3]) if len(args) >= 4 else DEFAULT_TAX_PCT
        summarize_tax_buffer(args[1], args[2], pct)
        return
    if len(args) < 5:
        print(
            "Usage: personal_finance_tracker_2026.py "
            "income.csv expenses.csv debts.csv savings.csv accounts.csv",
            file=sys.stderr,
        )
        print(
            "       personal_finance_tracker_2026.py --tax-buffer income.csv expenses.csv [pct]",
            file=sys.stderr,
        )
        sys.exit(1)
    dashboard(
        load_income(args[0]),
        load_expenses(args[1]),
        load_debts(args[2]),
        load_savings(args[3]),
        load_accounts(args[4]),
    )


if __name__ == "__main__":
    main()
