#!/usr/bin/env python3
"""Finance OS — clone of heyismail.gumroad.com/l/TheUltimateFinanceTracker ($29+ · 15,254 sales)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime

DEFAULT_TAX_PCT = 25.0
UK_PERSONAL_ALLOWANCE = 12570.0
UK_INCOME_TAX_RATE = 0.20
UK_CLASS4_LOWER = 12570.0
UK_CLASS4_UPPER = 50270.0
UK_CLASS4_RATE = 0.09
UK_TAX_POT_PCT = 28.0  # landolio/5hae 25-30% band


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


def summarize_profit_margins(income, expenses, month=None):
    """faisalmq/3cpo: monthly margin % + categorized breakdown + per-source rank."""
    by_month = defaultdict(
        lambda: {
            "income": 0.0,
            "expense": 0.0,
            "categories": defaultdict(lambda: {"income": 0.0, "expense": 0.0}),
        }
    )
    by_source = defaultdict(float)
    for i in income:
        if not i["date"]:
            continue
        key = i["date"][:7]
        by_month[key]["income"] += i["amount"]
        cat = i.get("category") or "other"
        by_month[key]["categories"][cat]["income"] += i["amount"]
        by_source[i.get("source") or "unknown"] += i["amount"]
    for e in expenses:
        if not e["date"]:
            continue
        key = e["date"][:7]
        by_month[key]["expense"] += e["amount"]
        cat = e.get("category") or "other"
        by_month[key]["categories"][cat]["expense"] += e["amount"]

    months = sorted(by_month.keys())
    active = month or (months[-1] if months else None)
    print("\n=== PROFIT MARGINS AT A GLANCE (faisalmq/3cpo shape) ===")
    if active:
        print(f"  Active month: {active}")
    for m in months:
        inc = by_month[m]["income"]
        exp = by_month[m]["expense"]
        net = inc - exp
        margin = (net / inc * 100) if inc else 0.0
        flag = " ← selected" if m == active else ""
        print(f"    {m}  income ${inc:,.2f}  expense ${exp:,.2f}  net ${net:,.2f}  margin {margin:.1f}%{flag}")

    if active and active in by_month:
        print(f"\n  Categorized breakdown ({active}) — tax preparedness:")
        cats = by_month[active]["categories"]
        for cat in sorted(cats.keys()):
            c = cats[cat]
            if c["income"] or c["expense"]:
                net = c["income"] - c["expense"]
                print(f"    {cat}: income ${c['income']:,.2f}  expense ${c['expense']:,.2f}  net ${net:,.2f}")

    if by_source:
        total_source = sum(by_source.values())
        print("\n  Per-source income rank — price the next offer:")
        for source, amt in sorted(by_source.items(), key=lambda x: -x[1]):
            share = (amt / total_source * 100) if total_source else 0
            print(f"    {source}: ${amt:,.2f} ({share:.0f}% of collected)")

    ytd_income = sum(m["income"] for m in by_month.values())
    ytd_expense = sum(m["expense"] for m in by_month.values())
    ytd_net = ytd_income - ytd_expense
    ytd_margin = (ytd_net / ytd_income * 100) if ytd_income else 0.0
    print(f"\n  YTD profit margin: {ytd_margin:.1f}%  (${ytd_net:,.2f} net on ${ytd_income:,.2f} income)")
    print("  Guide: profit-margins-guide.md · income-sample.csv · expenses-sample.csv")


def summarize_net_income(income_path, expense_path, tax_pct=DEFAULT_TAX_PCT):
    """faisalmq/5797: net income visibility — safe-to-spend after tax + subscriptions."""
    income = load_income(income_path)
    expenses = load_expenses(expense_path)
    collected = sum(i["amount"] for i in income)
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
    print("  Guide: net-income-guide.md · income-sample.csv · expenses-sample.csv")


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


def load_self_assessment_rows(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = float(row["amount"])
            except (KeyError, ValueError):
                continue
            month = (row.get("date") or "")[:7] or "unknown"
            rows.append({
                "month": month,
                "type": (row.get("type") or "").strip().lower(),
                "category": (row.get("category") or "other").strip().lower() or "other",
                "amount": amt,
            })
    return rows


def summarize_self_assessment(path):
    """landolio/5hae: monthly P&L + UK self-assessment tax pot planning."""
    rows = load_self_assessment_rows(path)
    if not rows:
        print("No rows in transaction log.")
        return
    by_month = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    for r in rows:
        if r["amount"] > 0:
            by_month[r["month"]]["income"] += r["amount"]
        else:
            by_month[r["month"]]["expense"] += abs(r["amount"])
    ytd_income = sum(m["income"] for m in by_month.values())
    ytd_expense = sum(m["expense"] for m in by_month.values())
    ytd_net = ytd_income - ytd_expense
    print("\n=== MONTHLY P&L (landolio/5hae shape) ===")
    for month in sorted(by_month):
        inc = by_month[month]["income"]
        exp = by_month[month]["expense"]
        net = inc - exp
        print(f"  {month}  income ${inc:,.2f}  expense ${exp:,.2f}  net ${net:,.2f}")
    print(f"  YTD  income ${ytd_income:,.2f}  expense ${ytd_expense:,.2f}  net ${ytd_net:,.2f}")
    if ytd_net <= 0:
        return
    taxable = max(0.0, ytd_net - UK_PERSONAL_ALLOWANCE)
    income_tax_est = taxable * UK_INCOME_TAX_RATE
    class4_base = max(0.0, min(ytd_net, UK_CLASS4_UPPER) - UK_CLASS4_LOWER)
    class4_ni = class4_base * UK_CLASS4_RATE
    tax_pot = ytd_net * (UK_TAX_POT_PCT / 100)
    months_logged = max(1, len(by_month))
    monthly_pot = tax_pot / months_logged
    print(f"\n=== SELF-ASSESSMENT TAX POT (landolio/5hae shape, UK planning) ===")
    print(f"  Profit (income − allowable expenses): ${ytd_net:,.2f}")
    print(f"  Income tax estimate (above ${UK_PERSONAL_ALLOWANCE:,.0f} allowance @ {UK_INCOME_TAX_RATE*100:.0f}%): ${income_tax_est:,.2f}")
    print(f"  Class 4 NI estimate (${UK_CLASS4_LOWER:,.0f}–${UK_CLASS4_UPPER:,.0f} band @ {UK_CLASS4_RATE*100:.0f}%): ${class4_ni:,.2f}")
    print(f"  Combined tax liability estimate: ${income_tax_est + class4_ni:,.2f}")
    print(f"  Tax pot to set aside ({UK_TAX_POT_PCT:.0f}% rule): ${tax_pot:,.2f}")
    print(f"  Avg monthly set-aside ({months_logged} months logged): ${monthly_pot:,.2f}/mo")
    print("  Planning only — confirm rates with a qualified tax professional.")
    print("  Guide: self-assessment-guide.md · self-assessment-sample.csv")


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
    if len(args) >= 2 and args[0] == "--invoice-panic":
        summarize_invoice_panic(load_invoices(args[1]))
        return
    if len(args) >= 3 and args[0] == "--profit-margins":
        month = args[3] if len(args) >= 4 and not args[3].startswith("-") else None
        summarize_profit_margins(load_income(args[1]), load_expenses(args[2]), month)
        return
    if len(args) >= 3 and args[0] == "--net-income":
        pct = float(args[3]) if len(args) >= 4 else DEFAULT_TAX_PCT
        summarize_net_income(args[1], args[2], pct)
        return
    if len(args) >= 3 and args[0] == "--tax-buffer":
        pct = float(args[3]) if len(args) >= 4 else DEFAULT_TAX_PCT
        summarize_tax_buffer(args[1], args[2], pct)
        return
    if len(args) >= 3 and args[0] == "--self-assessment":
        summarize_self_assessment(args[1])
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
