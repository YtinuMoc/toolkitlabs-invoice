#!/usr/bin/env python3
"""Grace Finance Tracker — clone of gracedigitalsco.gumroad.com/l/FinanceTracker (3,000 sales · 91 ratings · 5.0★)."""
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
    common = {
        "date": "",
        "platform": platform,
        "transaction_id": "",
        "description": "",
        "amount": "",
        "fee": "",
        "net": "",
        "buyer": "",
    }
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

    print("=== FINANCE TRACKER 4.0 (jnkxstudio clone) ===")
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


def summarize_tax_buffer(income_path, expense_path, reserve_pct=DEFAULT_TAX_PCT):
    """faisalmq/4gao: deposit lands → per-payment buffer → tax-only savings → tracker upsell."""
    income = load_income(income_path)
    expenses = load_expenses(expense_path)
    collected = sum(i["amount"] for i in income)
    deductible = sum(e["amount"] for e in expenses)
    net_profit = collected - deductible
    tax_buffer = max(net_profit, 0) * reserve_pct / 100
    safe_to_spend = max(net_profit - tax_buffer, 0)
    print("=== PER-PAYMENT TAX BUFFER (faisalmq/4gao shape) ===")
    print("  Deposit lands → five minutes of joy → tax panic → buffer same day.")
    print(f"  {'Source':<20} {'Collected':>12} {'Buffer':>10} {'Safe':>12}")
    for i in income:
        share = i["amount"] / collected if collected else 0
        buf = net_profit * share * reserve_pct / 100 if net_profit > 0 else 0
        safe = i["amount"] - buf
        label = (i["source"] or i["category"] or "Payment")[:20]
        print(f"  {label:<20} ${i['amount']:>10,.2f} ${buf:>8,.2f} ${safe:>10,.2f}")
    print()
    print("=== EXPENSE + TAX BUFFER ===")
    print(f"  Expenses YTD:        ${deductible:,.2f}")
    print(f"  Net profit:            ${net_profit:,.2f}")
    print(f"  Tax buffer ({reserve_pct:.0f}%):   ${tax_buffer:,.2f}")
    print(f"  Safe to spend:       ${safe_to_spend:,.2f}")
    print("  Transfer buffer to tax-only savings when payment lands — not in April.")
    print("  Guide: tax-buffer-guide.md · income-sample.csv · expenses-sample.csv")


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
    print("=== NET INCOME VISIBILITY (faisalmq/5797 shape) ===")
    print(f"  Gross collected:     {fmt_money(collected)}")
    print(f"  Expenses (deductible): {fmt_money(deductible)}")
    if subs:
        print(f"    subscriptions/SaaS:  {fmt_money(subs)}")
    print(f"  Net profit:            {fmt_money(net_profit)}")
    print(f"  Tax set-aside ({tax_pct:.0f}%): {fmt_money(tax_set_aside)}")
    print(f"  Safe to spend:         {fmt_money(safe_to_spend)}")
    if collected:
        print(f"  Take-home rate:        {safe_to_spend / collected * 100:.1f}% of gross deposits")
    print("  Gross deposits lie. Safe-to-spend is what you can actually use.")
    print("  Guide: net-income-guide.md · income-sample.csv · expenses-sample.csv")


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


def summarize_take_home(income_path, expense_path, reserve_pct=28.0, state_rate=4.4):
    """marginmap/14ag: gross → net → SE tax → reserve → real take-home."""
    income = load_income(income_path)
    expenses = load_expenses(expense_path)
    gross = sum(i["amount"] for i in income)
    deductible = sum(e["amount"] for e in expenses)
    net = gross - deductible
    se_tax = max(net, 0) * SE_IF_TAX
    se_deduction = se_tax * 0.5
    agi = max(net - se_deduction, 0)
    std_deduction = 15000.0
    taxable = max(agi - std_deduction, 0)
    federal = taxable * 0.113
    state = taxable * (state_rate / 100.0)
    total_tax = se_tax + federal + state
    take_home = max(net - total_tax, 0)
    effective = (total_tax / gross * 100) if gross else 0
    print("=== TAKE-HOME ESTIMATE (marginmap/14ag shape) ===")
    print("  Freelancer tax guide: gross deposits ≠ what you keep.")
    print(f"  Gross revenue:         {fmt_money(gross)}")
    print(f"  Business expenses:     {fmt_money(deductible)}")
    print(f"  Net self-employment:   {fmt_money(net)}")
    print(f"  SE tax (~15.3%):       {fmt_money(se_tax)}")
    print(f"  Federal income (est.): {fmt_money(federal)}")
    print(f"  State tax ({state_rate}%):     {fmt_money(state)}")
    print(f"  Total taxes:           {fmt_money(total_tax)}")
    print(f"  Take-home:             {fmt_money(take_home)}")
    print(f"  Effective rate:        {effective:.1f}% of gross")
    print(f"  Reserve shortcut:      {reserve_pct:.0f}% of net → {fmt_money(max(net, 0) * reserve_pct / 100)}")
    print("  Not tax advice. Confirm with a CPA.")
    print("  Guide: take-home-guide.md · income-sample.csv · expenses-sample.csv")


def load_invoices(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                rows.append({
                    "invoice_id": row.get("invoice_id", "").strip(),
                    "client": row.get("client", "").strip(),
                    "sent_date": row.get("sent_date", "").strip(),
                    "due_date": row.get("due_date", "").strip(),
                    "amount": float(row.get("amount") or 0),
                    "status": row.get("status", "").strip().lower(),
                    "paid_date": row.get("paid_date", "").strip(),
                })
            except (KeyError, ValueError):
                continue
    return rows


def days_between(a, b):
    try:
        da = datetime.strptime(a[:10], "%Y-%m-%d")
        db = datetime.strptime(b[:10], "%Y-%m-%d")
        return (db - da).days
    except ValueError:
        return None


def summarize_late_payment(invoice_path, hourly_rate=75.0):
    """wilsonhoe/2gnj: late payment system — collection time, overdue %, revenue at risk."""
    invoices = load_invoices(invoice_path)
    if not invoices:
        print("No invoices found.")
        return

    paid = [i for i in invoices if i["status"] == "paid" and i["paid_date"]]
    overdue = [i for i in invoices if i["status"] == "overdue"]
    sent = [i for i in invoices if i["status"] == "sent"]
    total = len(invoices)
    total_amount = sum(i["amount"] for i in invoices)

    collection_days = []
    for i in paid:
        d = days_between(i["sent_date"], i["paid_date"])
        if d is not None:
            collection_days.append(d)
    avg_collection = sum(collection_days) / len(collection_days) if collection_days else 0

    overdue_pct = len(overdue) / total * 100 if total else 0
    overdue_amount = sum(i["amount"] for i in overdue)
    at_risk = overdue_amount + sum(i["amount"] for i in sent)

    by_client = defaultdict(lambda: {"count": 0, "late": 0, "amount": 0.0})
    for i in paid:
        by_client[i["client"]]["count"] += 1
        by_client[i["client"]]["amount"] += i["amount"]
        d = days_between(i["sent_date"], i["paid_date"])
        if d is not None and d > 15:
            by_client[i["client"]]["late"] += 1

    chasing_days_before = 20
    chasing_days_after = 4
    time_saved = (chasing_days_before - chasing_days_after) * 8 * hourly_rate

    print("=== LATE PAYMENT SYSTEM (wilsonhoe/2gnj shape) ===")
    print("  214 invoices / 6 months: avg collection 39 days → 11 days.")
    print(f"  Your sample: {total} invoices · ${total_amount:,.2f} total billed")
    print()
    print("--- Collection metrics ---")
    print(f"  Paid invoices:         {len(paid)}")
    print(f"  Avg collection time:   {avg_collection:.0f} days")
    print(f"  Overdue invoices:      {len(overdue)} ({overdue_pct:.0f}% of total)")
    print(f"  Outstanding (sent):    {len(sent)}")
    print(f"  Revenue at risk:       ${at_risk:,.2f}")
    print()
    print("--- Client payment patterns ---")
    for client, stats in sorted(by_client.items(), key=lambda x: -x[1]["amount"]):
        late_flag = " ⚠ late payer" if stats["late"] >= 2 else ""
        print(f"  {client:<18} ${stats['amount']:>10,.2f}  ({stats['count']} paid){late_flag}")
    print()
    print("--- Annual cost of late payments (est.) ---")
    print(f"  Chasing payments:      {chasing_days_before} days/yr × ${hourly_rate}/hr × 8h = ${chasing_days_before * 8 * hourly_rate:,.0f}")
    print(f"  With tracking system:  {chasing_days_after} days/yr = ${chasing_days_after * 8 * hourly_rate:,.0f}")
    print(f"  Time saved:            ~${time_saved:,.0f}/yr in billable capacity")
    print()
    print("  Fix: log every invoice at send → track due date → surface overdue in one CLI run.")
    print("  Guide: late-payment-guide.md · invoices-sample.csv")


def main():
    args = sys.argv[1:]
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
        print("  Guide: merge-ledger-guide.md · import into Notion Finance Tracker income log")
        return
    if not args:
        print("Usage: grace_finance_tracker.py <income> <expenses> <accounts> <goals> <debts> <subscriptions>")
        print("       grace_finance_tracker.py --take-home <income> <expenses>")
        print("       grace_finance_tracker.py --late-payment <invoices.csv>")
        print("       grace_finance_tracker.py --quarterly-tax <income> <expenses>")
        sys.exit(1)
    if args[0] == "--take-home":
        reserve = float(args[3]) if len(args) > 3 else 28.0
        summarize_take_home(args[1], args[2], reserve)
    elif args[0] == "--late-payment":
        summarize_late_payment(args[1])
    elif args[0] == "--tax-buffer":
        tax_pct = float(args[3]) if len(args) > 3 else DEFAULT_TAX_PCT
        summarize_tax_buffer(args[1], args[2], tax_pct)
    elif args[0] == "--net-income":
        tax_pct = float(args[3]) if len(args) > 3 else DEFAULT_TAX_PCT
        summarize_net_income(args[1], args[2], tax_pct)
    elif args[0] == "--quarterly-tax":
        summarize_quarterly_tax(args[1], args[2])
    else:
        if len(args) < 6:
            print("Need 6 CSV paths for dashboard mode")
            sys.exit(1)
        summarize_dashboard(*args[:6])


if __name__ == "__main__":
    main()
