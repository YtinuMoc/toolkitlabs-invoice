#!/usr/bin/env python3
"""Small Business Finance Tracker — clone of Quillenhart qaduu dashboard tab."""
import csv
import os
import sys
from collections import defaultdict
from datetime import datetime

TAX_SET_ASIDE_PCT = 25.0
TAKE_HOME_RESERVE_PCT = 28.0  # marginmap/14ag low-state band default
SE_TAX_RATE = 0.153
UK_PERSONAL_ALLOWANCE = 12570.0
UK_CLASS4_LOWER = 12570.0
UK_CLASS4_UPPER = 50270.0
UK_CLASS4_RATE = 0.09
UK_INCOME_TAX_RATE = 0.20  # basic rate planning default
UK_TAX_POT_PCT = 28.0  # landolio/5hae 25-30% band
FEE_CATEGORIES = frozenset({
    "platform_fee", "fulfillment", "creator_commission", "ad_spend", "refund_fee",
})
DEDUCTION_CATEGORIES = {
    "home_office": "Home office",
    "software": "Software subscriptions",
    "internet_phone": "Internet/phone (business %)",
    "health_insurance": "Health insurance premiums",
    "professional_dev": "Professional development",
    "mileage": "Mileage",
    "equipment": "Equipment (Section 179)",
}


def load_rows(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = float(row["amount"])
            except (KeyError, ValueError):
                continue
            try:
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except ValueError:
                continue
            rows.append({
                "date": dt,
                "type": row.get("type", "").strip().lower(),
                "category": row.get("category", "uncategorized").strip() or "uncategorized",
                "description": row.get("description", "").strip(),
                "amount": amt,
            })
    return rows


def summarize_bills(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = float(row["amount"])
            except (KeyError, ValueError):
                continue
            status = row.get("status", "pending").strip().lower() or "pending"
            rows.append({
                "bill": row.get("bill", "").strip(),
                "amount": amt,
                "frequency": row.get("frequency", "monthly").strip().lower(),
                "due_day": row.get("due_day", "").strip(),
                "status": status,
            })
    if not rows:
        return
    paid = [r for r in rows if r["status"] == "paid"]
    pending = [r for r in rows if r["status"] != "paid"]
    monthly_equiv = 0.0
    for r in rows:
        freq = r["frequency"]
        if freq == "monthly":
            monthly_equiv += r["amount"]
        elif freq == "quarterly":
            monthly_equiv += r["amount"] / 3
        elif freq == "yearly":
            monthly_equiv += r["amount"] / 12
        else:
            monthly_equiv += r["amount"]
    print("\n=== RECURRING BILLS (Quillenhart bills tab shape) ===")
    print(f"  Bills tracked: {len(rows)}")
    print(f"  Marked paid this cycle: {len(paid)} (${sum(r['amount'] for r in paid):,.2f})")
    print(f"  Still pending: {len(pending)} (${sum(r['amount'] for r in pending):,.2f})")
    print(f"  Est. monthly fixed load: ${monthly_equiv:,.2f}")


def summarize_debt(path, ytd_net=None):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                cur = float(row["current_balance"])
                min_p = float(row.get("min_payment", 0) or 0)
            except (KeyError, ValueError):
                continue
            rows.append({
                "creditor": row.get("creditor", "").strip(),
                "current_balance": cur,
                "min_payment": min_p,
                "due_day": row.get("due_day", "").strip(),
                "apr": row.get("apr", "").strip(),
            })
    if not rows:
        return
    total_balance = sum(r["current_balance"] for r in rows)
    total_min = sum(r["min_payment"] for r in rows)
    print("\n=== DEBT MINIMUMS (crazychief/jg5 shape) ===")
    print(f"  Accounts tracked: {len(rows)}")
    print(f"  Total current balance: ${total_balance:,.2f}")
    print(f"  Total minimum payments: ${total_min:,.2f}/month")
    for r in rows:
        apr = f" @ {r['apr']}%" if r["apr"] else ""
        print(f"    {r['creditor']}: ${r['current_balance']:,.2f} (min ${r['min_payment']:,.2f}{apr})")
    if ytd_net is not None:
        if ytd_net >= total_min:
            surplus = ytd_net - total_min
            print(f"  YTD net covers minimums: yes — ${surplus:,.2f} surplus after min payments")
        else:
            gap = total_min - ytd_net
            print(f"  YTD net covers minimums: NO — short ${gap:,.2f} (net profit < debt minimums)")


def summarize_savings(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                target = float(row["target"])
                saved = float(row.get("saved", 0) or 0)
                weekly = float(row.get("weekly_target", 0) or 0)
            except (KeyError, ValueError):
                continue
            rows.append({
                "goal": row.get("goal", "").strip(),
                "target": target,
                "saved": saved,
                "weekly_target": weekly,
                "status": row.get("status", "active").strip().lower() or "active",
            })
    if not rows:
        return
    print("\n=== SAVINGS GOALS (stephane/5629 + Quillenhart savings tab) ===")
    total_target = total_saved = 0.0
    for r in rows:
        pct = (r["saved"] / r["target"] * 100) if r["target"] > 0 else 0.0
        remaining = max(0.0, r["target"] - r["saved"])
        weeks_left = (remaining / r["weekly_target"]) if r["weekly_target"] > 0 else 0.0
        print(
            f"  {r['goal']}: ${r['saved']:,.2f} / ${r['target']:,.2f} "
            f"({pct:.0f}% complete, ${remaining:,.2f} left"
            + (f", ~{weeks_left:.0f} weeks at ${r['weekly_target']:,.0f}/wk" if weeks_left else "")
            + ")"
        )
        total_target += r["target"]
        total_saved += r["saved"]
    overall = (total_saved / total_target * 100) if total_target > 0 else 0.0
    print(f"  Portfolio: ${total_saved:,.2f} / ${total_target:,.2f} ({overall:.0f}% across {len(rows)} goals)")


def months_to_goal(target, initial, monthly, annual_rate_pct):
    if target <= initial:
        return 0, 0.0, 0.0, initial
    if monthly <= 0:
        return None, 0.0, 0.0, initial
    rate = annual_rate_pct / 100 / 12
    balance = initial
    months = 0
    contributed = 0.0
    while balance < target and months < 1200:
        balance += monthly
        contributed += monthly
        if rate > 0:
            balance *= 1 + rate
        months += 1
    if balance < target:
        return None, contributed, 0.0, balance
    interest = balance - initial - contributed
    return months, contributed, interest, balance


def compound_growth(principal, monthly, annual_rate_pct, years):
    rate = annual_rate_pct / 100 / 12
    months = int(years * 12)
    balance = principal
    contributed = 0.0
    for _ in range(months):
        balance += monthly
        contributed += monthly
        if rate > 0:
            balance *= 1 + rate
    interest = balance - principal - contributed
    return balance, contributed, interest


def months_to_fire(net_worth, monthly_savings, annual_return_pct, target):
    rate = annual_return_pct / 100 / 12
    balance = net_worth
    months = 0
    contributed = 0.0
    while balance < target and months < 1200:
        balance += monthly_savings
        contributed += monthly_savings
        if rate > 0:
            balance *= 1 + rate
        months += 1
    if balance < target:
        return None, contributed, balance
    return months, contributed, balance


def freelance_hourly_rate(target_income, hours_per_week, admin_pct, benefits_pct, weeks_off=2):
    billable_weeks = 52 - weeks_off
    billable_hours = billable_weeks * hours_per_week * (1 - admin_pct / 100)
    if billable_hours <= 0:
        return None
    gross_needed = target_income * (1 + benefits_pct / 100) / 0.70
    return gross_needed / billable_hours, billable_hours, gross_needed


def dca_future_value(monthly, annual_rate_pct, years):
    rate = annual_rate_pct / 100 / 12
    months = int(years * 12)
    balance = 0.0
    for _ in range(months):
        balance = (balance + monthly) * (1 + rate) if rate > 0 else balance + monthly
    invested = monthly * months
    gain = balance - invested
    return balance, invested, gain


def summarize_finance_calculators(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows.append(row)
    if not rows:
        return
    print("\n=== FINANCE CALCULATORS HUB (profiterole/1pnb shape) ===")
    for row in rows:
        calc = row.get("calculator", "").strip().lower()
        label = row.get("label", calc).strip() or calc
        if calc == "compound":
            principal = float(row.get("principal") or 0)
            monthly = float(row.get("monthly_contribution") or 0)
            rate = float(row.get("annual_rate") or 0)
            years = float(row.get("years") or 0)
            final, contributed, interest = compound_growth(principal, monthly, rate, years)
            print(f"  {label} (compound interest): ${principal:,.2f} start · ${monthly:,.2f}/mo · {rate:.1f}% · {years:.0f}y")
            print(f"    Final balance: ${final:,.2f}")
            print(f"    Total contributed: ${contributed:,.2f}")
            print(f"    Interest earned: ${interest:,.2f}")
        elif calc == "fire":
            net_worth = float(row.get("principal") or 0)
            monthly = float(row.get("monthly_contribution") or 0)
            rate = float(row.get("annual_rate") or 7)
            spending = float(row.get("annual_spending") or 0)
            wr = float(row.get("withdrawal_rate") or 4)
            target = spending / (wr / 100) if wr else 0
            months, contributed, final = months_to_fire(net_worth, monthly, rate, target)
            print(f"  {label} (FIRE / {wr:.0f}% rule): ${spending:,.0f}/yr spending → ${target:,.0f} target")
            print(f"    Current net worth: ${net_worth:,.2f} · saving ${monthly:,.2f}/mo · {rate:.1f}% return")
            if months is None:
                print("    Projected: target not reached in 100 years at this pace")
            else:
                yrs, rem = divmod(months, 12)
                when = f"{months} months" if yrs == 0 else f"{yrs}y {rem}m ({months} months)"
                print(f"    Projected FIRE date: {when}")
                print(f"    Balance at FIRE: ${final:,.2f}")
        elif calc == "freelance":
            target_income = float(row.get("target_income") or 0)
            hours = float(row.get("hours_per_week") or 30)
            admin = float(row.get("admin_pct") or 20)
            benefits = float(row.get("benefits_pct") or 15)
            hourly, billable, gross = freelance_hourly_rate(target_income, hours, admin, benefits)
            if hourly is None:
                continue
            print(f"  {label} (freelance rate): ${target_income:,.0f} take-home target")
            print(f"    {hours:.0f}h/wk · {admin:.0f}% admin · {benefits:.0f}% benefits load")
            print(f"    Billable hours/year: {billable:,.0f}")
            print(f"    Gross revenue needed: ${gross:,.0f}")
            print(f"    Hourly rate to charge: ${hourly:,.2f}/hr")
        elif calc == "dca":
            monthly = float(row.get("monthly_contribution") or 0)
            rate = float(row.get("annual_rate") or 0)
            years = float(row.get("years") or 0)
            final, invested, gain = dca_future_value(monthly, rate, years)
            print(f"  {label} (DCA): ${monthly:,.2f}/mo · {rate:.1f}% · {years:.0f}y")
            print(f"    Total invested: ${invested:,.2f}")
            print(f"    Portfolio value: ${final:,.2f}")
            print(f"    Market gains: ${gain:,.2f}")
        elif calc == "savings":
            target = float(row.get("target") or row.get("principal") or 0)
            initial = float(row.get("initial") or row.get("initial_balance") or 0)
            monthly = float(row.get("monthly_contribution") or 0)
            rate = float(row.get("annual_rate") or 0)
            months, contributed, interest, final = months_to_goal(target, initial, monthly, rate)
            if months is None:
                print(f"  {label} (savings goal): unreachable at ${monthly:,.2f}/mo")
                continue
            yrs, rem = divmod(months, 12)
            when = f"{months} months" if yrs == 0 else f"{yrs}y {rem}m ({months} months)"
            print(f"  {label} (savings goal): ${target:,.2f} · ${initial:,.2f} start · ${monthly:,.2f}/mo · {rate:.1f}% APR")
            print(f"    Time to goal: {when} · final ${final:,.2f}")


def summarize_savings_calculator(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                target = float(row["target"])
                initial = float(row.get("initial_balance", 0) or 0)
                monthly = float(row.get("monthly_contribution", 0) or 0)
                rate = float(row.get("annual_interest_rate", 0) or 0)
            except (KeyError, ValueError):
                continue
            rows.append({
                "goal": row.get("goal", "").strip(),
                "target": target,
                "initial": initial,
                "monthly": monthly,
                "rate": rate,
            })
    if not rows:
        return
    print("\n=== SAVINGS GOAL CALCULATOR (tatelyman/4kcj shape) ===")
    for r in rows:
        months, contributed, interest, final = months_to_goal(
            r["target"], r["initial"], r["monthly"], r["rate"],
        )
        label = r["goal"] or "Goal"
        if months is None:
            print(
                f"  {label}: ${r['target']:,.2f} target — unreachable at "
                f"${r['monthly']:,.2f}/mo from ${r['initial']:,.2f} "
                f"({r['rate']:.1f}% APR)"
            )
            continue
        yrs = months // 12
        rem = months % 12
        when = f"{months} months" if yrs == 0 else f"{yrs}y {rem}m ({months} months)"
        print(f"  {label}: ${r['target']:,.2f} goal · ${r['initial']:,.2f} starting · ${r['monthly']:,.2f}/mo · {r['rate']:.1f}% APR")
        print(f"    Time to goal: {when}")
        print(f"    Total contributed: ${contributed:,.2f}")
        print(f"    Interest earned: ${interest:,.2f}")
        print(f"    Final balance: ${final:,.2f}")


def summarize_invoices(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = float(row["amount"])
            except (KeyError, ValueError):
                continue
            status = row.get("status", "Pending").strip() or "Pending"
            rows.append({
                "invoice_num": row.get("invoice_num", "").strip(),
                "client": row.get("client", "").strip(),
                "amount": amt,
                "status": status,
            })
    if not rows:
        return
    paid = [r for r in rows if r["status"].lower() == "paid"]
    unpaid = [r for r in rows if r["status"].lower() != "paid"]
    overdue = [r for r in unpaid if r["status"].lower() == "overdue"]
    paid_total = sum(r["amount"] for r in paid)
    outstanding_total = sum(r["amount"] for r in unpaid)
    overdue_total = sum(r["amount"] for r in overdue)
    print("\n=== ACCOUNTS RECEIVABLE (agentchip/2b11 shape) ===")
    print(f"  Invoices tracked: {len(rows)}")
    print(f"  Paid: {len(paid)} (${paid_total:,.2f})")
    print(f"  Outstanding: {len(unpaid)} (${outstanding_total:,.2f})")
    if overdue:
        print(f"  Overdue: {len(overdue)} (${overdue_total:,.2f}) — chase these first")
    else:
        print("  Overdue: 0 — no flagged late invoices")


def summarize_monthly_dashboard(rows, month=None):
    """Quillenhart Dashboard tab — pick one month, see P&L + categories + set-aside."""
    by_month = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    by_cat_month = defaultdict(float)
    for r in rows:
        key = r["date"].strftime("%Y-%m")
        if r["type"] == "income" or r["amount"] > 0:
            by_month[key]["income"] += abs(r["amount"])
        else:
            by_month[key]["expense"] += abs(r["amount"])
        if month is None or key == month:
            by_cat_month[r["category"]] += r["amount"]
    if not by_month:
        return
    if month is None:
        month = sorted(by_month)[-1]
    if month not in by_month:
        print(f"\n=== FREELANCE MONTHLY DASHBOARD (Quillenhart Dashboard tab shape) ===")
        print(f"  Selected month: {month} — no transactions logged")
        return
    inc = by_month[month]["income"]
    exp = by_month[month]["expense"]
    net = inc - exp
    aside = net * (TAX_SET_ASIDE_PCT / 100)
    txn_count = sum(1 for r in rows if r["date"].strftime("%Y-%m") == month)
    print(f"\n=== FREELANCE MONTHLY DASHBOARD (Quillenhart Dashboard tab shape) ===")
    print(f"  Selected month: {month}  ({txn_count} transactions)")
    print(f"  Income: ${inc:,.2f}")
    print(f"  Expenses: ${exp:,.2f}")
    print(f"  Net profit: ${net:,.2f}")
    print(f"  Tax set-aside ({TAX_SET_ASIDE_PCT:.0f}% of net): ${aside:,.2f}")
    if by_cat_month:
        print("  Top categories this month:")
        for cat in sorted(by_cat_month, key=lambda c: -abs(by_cat_month[c]))[:6]:
            print(f"    {cat}: ${by_cat_month[cat]:,.2f}")
    months_available = ", ".join(sorted(by_month))
    print(f"  Other months in log: {months_available}")


def print_annual_income_expense_chart(by_month, width=20):
    """Quillenhart qaduu Annual Summary tab: 12-month income vs expenses chart."""
    if not by_month:
        return
    peak = max(
        max(m["income"], m["expense"]) for m in by_month.values()
    ) or 1.0

    def bar(value):
        blocks = int(round((value / peak) * width))
        return "█" * blocks + "░" * (width - blocks)

    print("\n=== ANNUAL INCOME VS EXPENSES CHART (Quillenhart qaduu shape) ===")
    for month in sorted(by_month):
        inc = by_month[month]["income"]
        exp = by_month[month]["expense"]
        net = inc - exp
        print(
            f"  {month}  in {bar(inc)} ${inc:>9,.0f}  "
            f"out {bar(exp)} ${exp:>9,.0f}  net ${net:>9,.0f}"
        )
    ytd_in = sum(m["income"] for m in by_month.values())
    ytd_out = sum(m["expense"] for m in by_month.values())
    ytd_net = ytd_in - ytd_out
    print(
        f"  YTD    in {bar(ytd_in)} ${ytd_in:>9,.0f}  "
        f"out {bar(ytd_out)} ${ytd_out:>9,.0f}  net ${ytd_net:>9,.0f}"
    )


def summarize(rows):
    by_month = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    by_cat = defaultdict(float)
    for r in rows:
        key = r["date"].strftime("%Y-%m")
        if r["type"] == "income" or r["amount"] > 0:
            by_month[key]["income"] += abs(r["amount"])
        else:
            by_month[key]["expense"] += abs(r["amount"])
        by_cat[r["category"]] += r["amount"]

    print("=== MONTHLY P&L ===")
    ytd_income = ytd_expense = 0.0
    for month in sorted(by_month):
        inc = by_month[month]["income"]
        exp = by_month[month]["expense"]
        net = inc - exp
        ytd_income += inc
        ytd_expense += exp
        print(f"{month}  income ${inc:,.2f}  expense ${exp:,.2f}  net ${net:,.2f}")

    ytd_net = ytd_income - ytd_expense
    print(f"\nYTD income ${ytd_income:,.2f}  expense ${ytd_expense:,.2f}  net ${ytd_net:,.2f}")

    print("\n=== CATEGORY BREAKDOWN (net) ===")
    for cat in sorted(by_cat, key=lambda c: -abs(by_cat[c])):
        print(f"  {cat}: ${by_cat[cat]:,.2f}")

    quarterly = ytd_net * (TAX_SET_ASIDE_PCT / 100) / max(1, len(by_month) / 3)
    print(f"\n=== QUARTERLY TAX SET-ASIDE ({TAX_SET_ASIDE_PCT:.0f}% of net) ===")
    print(f"  Estimated per quarter: ${quarterly:,.2f}")
    print(f"  YTD set-aside target: ${ytd_net * (TAX_SET_ASIDE_PCT / 100):,.2f}")

    print("\n=== ANNUAL SUMMARY (month | income | expense | net | set-aside) ===")
    for month in sorted(by_month):
        inc = by_month[month]["income"]
        exp = by_month[month]["expense"]
        net = inc - exp
        aside = net * (TAX_SET_ASIDE_PCT / 100)
        print(f"  {month}  ${inc:,.2f}  ${exp:,.2f}  ${net:,.2f}  ${aside:,.2f}")
    print(f"  YTD  ${ytd_income:,.2f}  ${ytd_expense:,.2f}  ${ytd_net:,.2f}  ${ytd_net * (TAX_SET_ASIDE_PCT / 100):,.2f}")
    print_annual_income_expense_chart(by_month)

    fee_expense = sum(abs(r["amount"]) for r in rows if r["type"] != "income" and r["amount"] < 0 and r["category"] in FEE_CATEGORIES)
    other_expense = ytd_expense - fee_expense
    if ytd_income > 0:
        print(f"\n=== 1099-K RECONCILIATION (l_d/5284 shape) ===")
        print(f"  Gross payments (1099-K box 1 equivalent): ${ytd_income:,.2f}")
        print(f"  Deductible platform/fulfillment/commission/ad fees: ${fee_expense:,.2f}")
        print(f"  Other business expenses: ${other_expense:,.2f}")
        print(f"  Taxable net profit (gross − all expenses): ${ytd_net:,.2f}")
        if ytd_income > 0:
            overpay_risk = (ytd_income - ytd_net) * (TAX_SET_ASIDE_PCT / 100)
            print(f"  Extra tax if you set aside on gross instead of net: ~${overpay_risk:,.2f}/quarter habit")

    if ytd_net > 0:
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

    if ytd_net > 0:
        se_tax = ytd_net * SE_TAX_RATE
        reserve_total = ytd_net * (TAKE_HOME_RESERVE_PCT / 100)
        take_home = ytd_net - reserve_total
        print(f"\n=== TAKE-HOME ESTIMATE (marginmap/14ag shape, {TAKE_HOME_RESERVE_PCT:.0f}% reserve) ===")
        print(f"  YTD gross income: ${ytd_income:,.2f}")
        print(f"  YTD expenses: ${ytd_expense:,.2f}")
        print(f"  YTD net profit: ${ytd_net:,.2f}")
        print(f"  Est. SE tax component (15.3% of net): ${se_tax:,.2f}")
        print(f"  Planned tax reserve ({TAKE_HOME_RESERVE_PCT:.0f}% of net): ${reserve_total:,.2f}")
        print(f"  Est. take-home after reserve: ${take_home:,.2f}")
        print(f"  Effective reserve rate on gross: {(reserve_total / ytd_income * 100):.1f}%")


def summarize_tax_stack(rows, ytd_net):
    """tatelyman/3427384: freelancer tax stack checklist + deduction totals."""
    by_cat = defaultdict(float)
    for r in rows:
        if r["type"] != "income" and r["amount"] < 0:
            by_cat[r["category"]] += abs(r["amount"])
    print("\n=== FREELANCER TAX STACK (tatelyman/3427384 shape) ===")
    print("  1. Quarterly estimates → QUARTERLY TAX SET-ASIDE block above")
    print("  2. Invoice tracking → invoices-tracker.md + ACCOUNTS RECEIVABLE block")
    print("  3. Rate calculation → take-home-guide.md + TAKE-HOME ESTIMATE block")
    print("  4. Deduction categories logged in transaction CSV:")
    logged = False
    for key, label in DEDUCTION_CATEGORIES.items():
        amt = by_cat.get(key, 0.0)
        if amt > 0:
            print(f"     {label}: ${amt:,.2f}")
            logged = True
    other = sum(
        amt for cat, amt in by_cat.items()
        if cat not in DEDUCTION_CATEGORIES and cat not in FEE_CATEGORIES
    )
    if other > 0:
        print(f"     Other business expenses: ${other:,.2f}")
        logged = True
    if not logged:
        print("     (none yet — use category keys from tax-stack-guide.md)")
    print("  5. Retirement — SEP-IRA planning (outside CSV; confirm with CPA)")
    if ytd_net and ytd_net > 0:
        se = ytd_net * SE_TAX_RATE
        print(f"  Stack check: YTD net ${ytd_net:,.2f} · SE tax component ${se:,.2f}")


COLORWAYS = (
    ("Terracotta", "warm clay + burnt orange accents", 15),
    ("Rose", "soft blush + muted mauve headers", 15),
    ("Twilight Garden", "deep green + dusk purple highlights", 15),
    ("Arctic Shades", "cool gray + ice blue grid lines", 15),
    ("Sunset Meadows", "golden hour + sage green cells", 15),
    ("Pink & Green Grid", "retro ledger pink headers + green income rows", 15),
)
COLORWAYS_BUNDLE_PRICE = 34
COLORWAYS_SINGLE_PRICE = 15


def summarize_colorways():
    """Quillenhart qaduu Gumroad colorway variants + All-6 bundle upsell."""
    singles_total = len(COLORWAYS) * COLORWAYS_SINGLE_PRICE
    savings = singles_total - COLORWAYS_BUNDLE_PRICE
    print("\n=== COLORWAYS (Quillenhart qaduu — 6 palettes + All-6 bundle) ===")
    print("  Same 9-tab tracker in every colorway — only the palette changes.")
    for name, vibe, price in COLORWAYS:
        print(f"  {name:20} | ${price:>2} | {vibe}")
    print(f"  {'All 6 Colorways':20} | ${COLORWAYS_BUNDLE_PRICE:>2} | Best Value — save ${savings} vs 6×${COLORWAYS_SINGLE_PRICE}")
    print(f"  Bundle math: 6 singles ${singles_total} → bundle ${COLORWAYS_BUNDLE_PRICE} ({100 * savings // singles_total}% off)")
    print("  Guide: colorways-guide.md · Gumroad: quillenhart.gumroad.com/l/qaduu")


def summarize_setup_readme():
    """Quillenhart Read Me + Setup tabs; datanestdigital/4l0h dashboard-setup-guide shape."""
    print("\n=== READ ME (Quillenhart qaduu tab 1 — plain-English setup) ===")
    print("  9-tab system: Read Me · Setup · Transactions · Bills · Savings · Debt · Invoices · Dashboard · Annual Summary")
    print("  Rule: only shaded cells get typed — in this kit: CSV rows + setup-guide.md fields")
    print("  Guides: readme-guide.md · start-here.md · dashboard-setup steps in setup-guide.md")
    print("\n=== SETUP TAB (Quillenhart qaduu tab 2 — configure once) ===")
    print("  Field              | Your value (edit setup-guide.md)")
    print("  -------------------|----------------------------------")
    print("  Business name      | ________________________________")
    print("  Tax year           | 2026")
    print(f"  Tax set-aside %    | {TAX_SET_ASIDE_PCT:.0f}")
    print("  Financial year     | January start")
    print("  Quick start (datanestdigital/4l0h):")
    print("    1. Extract zip → 2. Fill setup-guide.md → 3. Copy transaction log")
    print("    4. Log first month → 5. Run this script → 6. Mark bills in bills-tracker.md")


def summarize_transactions_log(rows):
    """Quillenhart Transactions tab + orion_operator/40gi single-source-of-truth."""
    months = sorted({r["date"].strftime("%Y-%m") for r in rows})
    income_rows = [r for r in rows if r["type"] == "income" or r["amount"] > 0]
    expense_rows = [r for r in rows if r["type"] != "income" and r["amount"] < 0]
    categories = len({r["category"] for r in rows})
    span = f"{months[0]} … {months[-1]}" if months else "—"
    print("\n=== TRANSACTIONS LOG (Quillenhart tab 3 + orion/40gi single source) ===")
    print(f"  Rows logged: {len(rows)} (template supports 150+)")
    print(f"  Months covered: {len(months)} ({span})")
    print(f"  Income events: {len(income_rows)} · Expense events: {len(expense_rows)}")
    print(f"  Categories in use: {categories}")
    print("  Rule: one row per money event — dashboard, annual, tax set-aside all pull from here")
    print("  Guide: transactions-log-guide.md · template: transaction-log-template.csv")


def summarize_command_center(rows, invoice_path=None):
    """timmothybuilder/4e81: five-template stack ending in unified command center."""
    overdue_total = 0.0
    overdue_count = 0
    if invoice_path:
        with open(invoice_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                status = row.get("status", "Pending").strip().lower()
                if status == "overdue":
                    try:
                        overdue_total += float(row["amount"])
                        overdue_count += 1
                    except (KeyError, ValueError):
                        pass
    tx_count = len(rows)
    print("\n=== FREELANCER FINANCIAL COMMAND CENTER (timmothybuilder/4e81 shape) ===")
    print("  Five templates every freelancer needs — #5 unifies the rest:")
    print(f"  1. Personal finance tracker → transaction log + savings [{('active' if tx_count else 'add rows')}]")
    print("  2. Client / proposal tracker → invoices receivable module [see AR block if loaded]")
    print("  3. Content calendar → outside kit [use your own calendar]")
    print(f"  4. Daily productivity dashboard → monthly dashboard tab [{('active' if tx_count else 'add rows')}]")
    print(f"  5. Financial command center → full 9-tab Quillenhart system [{('active' if tx_count else 'add rows')}]")
    if overdue_total > 0:
        print(
            f"  Uncollected overdue invoices: ${overdue_total:,.2f} ({overdue_count}) — "
            "template #5 pays for itself when you find these"
        )
    print("  Guide: command-center-guide.md · timmothybuilder/4e81 buyer channel clone")


def summarize_spreadsheet_system(rows):
    """crazychief/52ge: book principles → transaction log vessel → hardened behavior."""
    months = sorted({r["date"].strftime("%Y-%m") for r in rows})
    tx_count = len(rows)
    income = sum(abs(r["amount"]) for r in rows if r["type"] == "income" or r["amount"] > 0)
    expense = sum(abs(r["amount"]) for r in rows if r["type"] != "income" and r["amount"] < 0)
    net = income - expense
    reserve = net * (TAX_SET_ASIDE_PCT / 100) if net > 0 else 0.0
    phase = "HARDENED" if tx_count >= 10 and len(months) >= 2 else "PROTOTYPE"
    print("\n=== SPREADSHEET SYSTEM (crazychief/52ge shape) ===")
    print("  Sequence: Read → Decompose → Prototype → Harden → Reapply")
    print(f"  Vessel: transaction log ({tx_count} rows, {len(months)} month(s))")
    print(f"  Fixed rule: tax set-aside {TAX_SET_ASIDE_PCT:.0f}% of net profit")
    print("  Three containers:")
    print(f"    Income    ${income:,.2f}")
    print(f"    Expenses  ${expense:,.2f}")
    print(f"    Reserved  ${reserve:,.2f}  (set-aside, not spendable)")
    print(f"  System phase: {phase}")


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "sample-transactions.csv"
    invoice_path = sys.argv[2] if len(sys.argv) > 2 else None
    bills_path = sys.argv[3] if len(sys.argv) > 3 else None
    debt_path = sys.argv[4] if len(sys.argv) > 4 else None
    savings_path = sys.argv[5] if len(sys.argv) > 5 else None
    calc_path = sys.argv[6] if len(sys.argv) > 6 else None
    calculators_path = sys.argv[7] if len(sys.argv) > 7 else None
    month_arg = sys.argv[8] if len(sys.argv) > 8 else None
    month_arg = month_arg or os.environ.get("FINANCE_MONTH")
    if month_arg == "":
        month_arg = None
    rows = load_rows(path)
    if not rows:
        print("No transactions found.", file=sys.stderr)
        sys.exit(1)
    summarize_setup_readme()
    summarize_colorways()
    summarize_transactions_log(rows)
    summarize_monthly_dashboard(rows, month=month_arg)
    summarize(rows)
    summarize_spreadsheet_system(rows)
    ytd_net = None
    by_month = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    for r in rows:
        key = r["date"].strftime("%Y-%m")
        if r["type"] == "income" or r["amount"] > 0:
            by_month[key]["income"] += abs(r["amount"])
        else:
            by_month[key]["expense"] += abs(r["amount"])
    ytd_income = sum(m["income"] for m in by_month.values())
    ytd_expense = sum(m["expense"] for m in by_month.values())
    ytd_net = ytd_income - ytd_expense
    summarize_tax_stack(rows, ytd_net)
    if invoice_path:
        summarize_invoices(invoice_path)
    if bills_path:
        summarize_bills(bills_path)
    if debt_path:
        summarize_debt(debt_path, ytd_net=ytd_net)
    if savings_path:
        with open(savings_path, newline="", encoding="utf-8") as f:
            hdr = csv.DictReader(f).fieldnames or []
        if "monthly_contribution" in hdr:
            summarize_savings_calculator(savings_path)
        else:
            summarize_savings(savings_path)
    if calc_path:
        with open(calc_path, newline="", encoding="utf-8") as f:
            hdr = csv.DictReader(f).fieldnames or []
        if "calculator" in hdr:
            summarize_finance_calculators(calc_path)
        else:
            summarize_savings_calculator(calc_path)
    if calculators_path:
        summarize_finance_calculators(calculators_path)
    summarize_command_center(rows, invoice_path=invoice_path)


if __name__ == "__main__":
    main()
