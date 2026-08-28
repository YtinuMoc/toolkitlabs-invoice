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


def detect_platform(headers):
    headers = [h.lower() for h in headers]
    if "sale id" in headers and "product name" in headers:
        return "Gumroad"
    if "transaction id" in headers and "stripe fee" in headers:
        return "Stripe"
    if "transaction id" in headers and "gross" in headers:
        return "PayPal"
    return None


def parse_ledger_row(platform, row):
    common = {"date": "", "platform": platform, "transaction_id": "", "description": "",
              "amount": "", "fee": "", "net": "", "buyer": ""}
    try:
        if platform == "Gumroad":
            common.update({
                "date": row["Sale creation date"],
                "transaction_id": row["Sale ID"],
                "description": row["Product name"],
                "amount": row["Price (including tax)"],
                "fee": str(float(row["Gumroad fee"]) + float(row.get("Additional fee", "0") or 0)),
                "net": row["Net"],
                "buyer": row.get("Customer email", ""),
            })
        elif platform == "Stripe":
            common.update({
                "date": row["Created (UTC)"],
                "transaction_id": row["Transaction ID"],
                "description": row.get("Description", ""),
                "amount": row["Gross"],
                "fee": row["Stripe fee"],
                "net": row["Net"],
                "buyer": row.get("Customer email", ""),
            })
        elif platform == "PayPal":
            common.update({
                "date": row["Date"],
                "transaction_id": row["Transaction ID"],
                "description": row.get("Subject", ""),
                "amount": row["Gross"],
                "fee": row["Fee"],
                "net": row["Net"],
                "buyer": row.get("Name", ""),
            })
    except KeyError as e:
        print(f"Missing column: {e}", file=sys.stderr)
    return common


def merge_ledgers(paths, out_path=None):
    rows = []
    for path in paths:
        with open(path, newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            platform = detect_platform(reader.fieldnames or [])
            if not platform:
                print(f"Unknown format: {path}", file=sys.stderr)
                continue
            for row in reader:
                if row and list(row.values())[0]:
                    rows.append(parse_ledger_row(platform, row))
    rows.sort(key=lambda r: r["date"])
    if out_path:
        with open(out_path, "w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=rows[0].keys() if rows else [])
            if rows:
                w.writeheader()
                w.writerows(rows)
    return rows


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
    print(f"  Net profit:            ${net_profit:,.2f}")
    print(f"  Tax buffer ({reserve_pct:.0f}%):   ${tax_buffer:,.2f}")
    print(f"  Safe to spend:       ${safe_to_spend:,.2f}")
    print("  Transfer buffer to tax-only savings when payment lands — not in April.")
    print("  Guide: tax-buffer-guide.md · income-sample.csv · expenses-sample.csv")


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
    if len(args) >= 3 and args[0] == "--tax-buffer":
        pct = float(args[3]) if len(args) >= 4 else DEFAULT_TAX_PCT
        summarize_tax_buffer(args[1], args[2], pct)
        return
    if "--merge" in args:
        idx = args.index("--merge")
        inputs = []
        i = idx + 1
        while i < len(args) and not args[i].startswith("-"):
            inputs.append(args[i])
            i += 1
        out = "ledger-merged.csv"
        if "-o" in args:
            out = args[args.index("-o") + 1]
        rows = merge_ledgers(inputs, out)
        gross = sum(float(r["amount"] or 0) for r in rows)
        fees = sum(float(r["fee"] or 0) for r in rows)
        net = sum(float(r["net"] or 0) for r in rows)
        print("\n=== UNIFIED PAYMENT LEDGER (goldenalien/206o shape) ===")
        print(f"  Transactions:        {len(rows)}")
        print(f"  Gross:               ${gross:,.2f}")
        print(f"  Fees:                ${fees:,.2f}")
        print(f"  Net:                 ${net:,.2f}")
        if out:
            print(f"  Wrote:               {out}")
        print("  Guide: merge-ledger-guide.md · import into Finance OS income log")
        return
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
