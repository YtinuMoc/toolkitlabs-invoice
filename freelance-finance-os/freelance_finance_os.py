#!/usr/bin/env python3
"""Freelance Finance OS — clone of By the Loop freelance-finance-os ($5 Gumroad)."""
import csv
import os
import sys
from collections import defaultdict
from datetime import date, datetime

TAX_BUFFER_PCT = 25.0
ESTIMATED_TAX_PCT = 28.0  # planning default; not tax advice
SE_TAX_RATE = 0.153
TAKE_HOME_RESERVE_PCT = 28.0  # marginmap/14ag middle band; not tax advice
FEE_CATEGORIES = frozenset({
    "platform_fee", "fulfillment", "creator_commission", "ad_spend", "refund_fee",
})

QUARTERLY_DEADLINES = (
    ("Q1", "Apr 15", "Jan–Mar income"),
    ("Q2", "Jun 15", "Apr–May income"),
    ("Q3", "Sep 15", "Jun–Aug income"),
    ("Q4", "Jan 15 next year", "Sep–Dec income"),
)


def load_invoices(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = float(row["amount"])
            except (KeyError, ValueError):
                continue
            status = row.get("status", "draft").strip().lower()
            due = row.get("due_date", "").strip()
            overdue = False
            if status == "sent" and due:
                try:
                    overdue = datetime.strptime(due, "%Y-%m-%d").date() < date.today()
                except ValueError:
                    pass
            inv_date = _parse_iso_date(row.get("date", ""))
            rows.append({
                "client": row.get("client", "unknown").strip() or "unknown",
                "amount": amt,
                "status": status,
                "overdue": overdue,
                "date": inv_date,
            })
    return rows


def load_expenses(path):
    total = 0.0
    by_cat = defaultdict(float)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = abs(float(row["amount"]))
            except (KeyError, ValueError):
                continue
            cat = row.get("category", "other").strip().lower() or "other"
            by_cat[cat] += amt
            total += amt
    return total, dict(by_cat)


def load_expense_rows(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = abs(float(row["amount"]))
            except (KeyError, ValueError):
                continue
            date_str = row.get("date", "").strip()
            try:
                dt = datetime.strptime(date_str, "%Y-%m-%d").date()
            except ValueError:
                continue
            cat = row.get("category", "other").strip().lower() or "other"
            rows.append({"date": dt, "category": cat, "amount": amt})
    return rows


def summarize_accounts_receivable(invoices):
    """agentchip/2b11 buyer channel — paid vs outstanding vs overdue split."""
    if not invoices:
        return
    paid = [r for r in invoices if r["status"] == "paid"]
    unpaid = [r for r in invoices if r["status"] not in ("paid", "cancelled")]
    overdue = [r for r in unpaid if r["overdue"]]
    paid_total = sum(r["amount"] for r in paid)
    outstanding_total = sum(r["amount"] for r in unpaid)
    overdue_total = sum(r["amount"] for r in overdue)
    print()
    print("=== ACCOUNTS RECEIVABLE (agentchip/2b11 shape) ===")
    print(f"  Invoices tracked: {len(invoices)}")
    print(f"  Paid: {len(paid)} (${paid_total:,.2f})")
    print(f"  Outstanding: {len(unpaid)} (${outstanding_total:,.2f})")
    if overdue:
        print(f"  Overdue: {len(overdue)} (${overdue_total:,.2f}) — chase these first")
    else:
        print("  Overdue: 0 — no flagged late invoices")


def print_category_breakdown(rows):
    """raxxostudios/5a8i + By the Loop expense tab: category-by-category every month."""
    print("\n=== CATEGORY BREAKDOWN BY MONTH (raxxostudios/5a8i + By the Loop) ===")
    print("  12 categories is the sweet spot — fewer and the P&L is useless")
    by_month_cat = defaultdict(lambda: defaultdict(float))
    cat_totals = defaultdict(float)
    for r in rows:
        key = r["date"].strftime("%Y-%m")
        by_month_cat[key][r["category"]] += r["amount"]
        cat_totals[r["category"]] += r["amount"]
    if not by_month_cat:
        print("  No expense rows yet — log amounts with date + category columns")
        return
    for month in sorted(by_month_cat):
        cats = by_month_cat[month]
        total = sum(cats.values())
        print(f"\n  {month} — expenses ${total:,.2f}")
        for cat in sorted(cats, key=lambda c: -cats[c]):
            pct = (cats[cat] / total * 100) if total else 0
            print(f"    {cat}: ${cats[cat]:,.2f} ({pct:.0f}%)")
    annual = sum(cat_totals.values())
    print(f"\n  YTD expense categories (${annual:,.2f} total):")
    for cat in sorted(cat_totals, key=lambda c: -cat_totals[c]):
        pct = (cat_totals[cat] / annual * 100) if annual else 0
        print(f"    {cat}: ${cat_totals[cat]:,.2f} ({pct:.0f}%)")


def load_transaction_log(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = float(row["amount"])
            except (KeyError, ValueError):
                continue
            cat = row.get("category", "other").strip().lower() or "other"
            row_type = (row.get("type") or "").strip().lower()
            rows.append({"type": row_type, "category": cat, "amount": amt})
    return rows


def summarize_1099k_reconciliation(trans_rows):
    """l_d/5284: 1099-K gross payments vs deductible fees vs taxable net."""
    if not trans_rows:
        return
    gross = sum(r["amount"] for r in trans_rows if r["amount"] > 0)
    fee_expense = sum(
        abs(r["amount"]) for r in trans_rows
        if r["amount"] < 0 and r["category"] in FEE_CATEGORIES
    )
    other_expense = sum(
        abs(r["amount"]) for r in trans_rows
        if r["amount"] < 0 and r["category"] not in FEE_CATEGORIES
    )
    ytd_net = gross - fee_expense - other_expense
    print()
    print("=== 1099-K RECONCILIATION (l_d/5284 shape) ===")
    print(f"  Gross payments (1099-K box 1 equivalent): ${gross:,.2f}")
    print(f"  Deductible platform/fulfillment/commission/ad fees: ${fee_expense:,.2f}")
    print(f"  Other business expenses: ${other_expense:,.2f}")
    print(f"  Taxable net profit (gross − all expenses): ${ytd_net:,.2f}")
    if gross > ytd_net:
        overpay = (gross - ytd_net) * (TAX_BUFFER_PCT / 100) / 4
        print(f"  Extra tax if you set aside on gross instead of net: ~${overpay:,.2f}/quarter habit")
    quarterly = max(ytd_net, 0) * TAX_BUFFER_PCT / 100 / 4
    print()
    print(f"=== QUARTERLY TAX SET-ASIDE ({TAX_BUFFER_PCT:.0f}% of net) ===")
    print(f"  Estimated per quarter: ${quarterly:,.2f}")
    print("  Guide: 1099k-guide.md · 1099k-freelance-sample.csv")


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
    print("\n=== RECURRING BILLS (By the Loop expense tab + crazychief/jg5 shape) ===")
    print(f"  Bills tracked: {len(rows)}")
    print(f"  Marked paid this cycle: {len(paid)} (${sum(r['amount'] for r in paid):,.2f})")
    print(f"  Still pending: {len(pending)} (${sum(r['amount'] for r in pending):,.2f})")
    print(f"  Est. monthly fixed load: ${monthly_equiv:,.2f}")
    print("  Guide: bills-debt-guide.md · bills-sample.csv")


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
    print("  Guide: bills-debt-guide.md · debt-sample.csv")


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
    print("\n=== SAVINGS GOALS (stephane/5629 shape) ===")
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
    print("  Guide: savings-goals-guide.md · savings-sample.csv")


def load_client_hours(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                hours = float(row["hours_worked"])
            except (KeyError, ValueError):
                continue
            rows.append({
                "client": row.get("client", "unknown").strip() or "unknown",
                "hours": hours,
            })
    return rows


def summarize_six_month_reveal(invoice_path, expense_path, hours_path, subs_path=None):
    """timmothybuilder/3fb2: six months of tracking → four surprises → client scoreboard."""
    invoices = load_invoices(invoice_path)
    expense_total, by_cat = load_expenses(expense_path)
    hours_rows = load_client_hours(hours_path)
    collected = sum(r["amount"] for r in invoices if r["status"] == "paid")
    total_hours = sum(r["hours"] for r in hours_rows)
    effective_rate = (collected / total_hours) if total_hours > 0 else 0.0

    by_client_paid = defaultdict(float)
    for r in invoices:
        if r["status"] == "paid":
            by_client_paid[r["client"]] += r["amount"]
    by_client_hours = {r["client"]: r["hours"] for r in hours_rows}

    subs_monthly = 0.0
    if subs_path:
        with open(subs_path, newline="", encoding="utf-8") as f:
            for row in csv.DictReader(f):
                try:
                    subs_monthly += float(row.get("monthly_usd", row.get("amount", 0)))
                except (KeyError, ValueError):
                    continue
    subs_annual = subs_monthly * 12
    subs_pct = (subs_annual / collected * 100) if collected > 0 else 0.0
    tax_reserve = collected * 0.30

    print("=== SIX-MONTH REVEAL (timmothybuilder/3fb2 shape) ===")
    print("  Surprise #1 — effective hourly rate (paid ÷ all hours, not billable-only):")
    print(f"    Collected (paid):    ${collected:,.2f}")
    print(f"    Total hours logged:  {total_hours:.0f}")
    print(f"    Effective rate:      ${effective_rate:,.2f}/hr")
    print("  Surprise #2 — subscription load as % of revenue:")
    print(f"    SaaS monthly:        ${subs_monthly:,.2f} (${subs_annual:,.2f}/yr)")
    print(f"    As % of paid revenue:{subs_pct:.1f}%")
    print("  Surprise #3 — quarterly tax discipline:")
    print(f"    30% reserve on paid: ${tax_reserve:,.2f} (untouchable until estimates due)")
    print("  Surprise #4 — revenue ≠ profit per client:")
    print("  client               paid        hours   effective $/hr")
    clients = sorted(set(by_client_paid) | set(by_client_hours))
    for client in clients:
        paid = by_client_paid.get(client, 0.0)
        hrs = by_client_hours.get(client, 0.0)
        rate = (paid / hrs) if hrs > 0 else 0.0
        print(f"    {client:20} ${paid:>8,.2f}  {hrs:>5.0f}h   ${rate:>6,.0f}/hr")
    if by_client_paid:
        top_client = max(by_client_paid, key=by_client_paid.get)
        concentration = by_client_paid[top_client] / collected * 100 if collected > 0 else 0.0
        print(f"  Client concentration: {concentration:.0f}% from {top_client}")
        if concentration > 50:
            print("  WARNING: top client >50% — one email from financial crisis")
    print("  Guide: six-month-reveal-guide.md · rate-calculator.html · client-hours-sample.csv")


def summarize_dashboard_setup(invoice_path, expense_path, reserve_pct=TAX_BUFFER_PCT):
    """datanestdigital/4l0h: five-minute dashboard setup — monthly metrics at a glance."""
    invoices = load_invoices(invoice_path)
    expense_total, by_cat = load_expenses(expense_path)
    expense_rows = load_expense_rows(expense_path)
    collected = sum(r["amount"] for r in invoices if r["status"] == "paid")
    awaiting = sum(r["amount"] for r in invoices if r["status"] == "sent")
    overdue_amt = sum(r["amount"] for r in invoices if r["overdue"])
    net_profit = collected - expense_total
    tax_set_aside = max(net_profit, 0) * reserve_pct / 100
    take_home = max(net_profit - tax_set_aside, 0)
    margin_pct = (net_profit / collected * 100) if collected > 0 else 0.0
    by_month = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    for inv in invoices:
        if inv["status"] == "paid" and inv.get("date"):
            key = inv["date"].strftime("%B %Y")
            by_month[key]["income"] += inv["amount"]
    for r in expense_rows:
        key = r["date"].strftime("%B %Y")
        by_month[key]["expense"] += r["amount"]
    print("=== FREELANCE FINANCIAL DASHBOARD (datanestdigital/4l0h shape) ===")
    print("  Setup: copy invoice + expense templates → log rows → run this CLI.")
    print("  No bookkeeper required — dashboard metrics from your CSV logs.")
    print()
    if by_month:
        for month_label in sorted(by_month.keys(), key=lambda m: datetime.strptime(m, "%B %Y")):
            inc = by_month[month_label]["income"]
            exp = by_month[month_label]["expense"]
            net = inc - exp
            reserve = max(net, 0) * reserve_pct / 100
            home = max(net - reserve, 0)
            m_margin = (net / inc * 100) if inc > 0 else 0.0
            print(f"  ═══════════════ {month_label.upper()} ═══════════════")
            print(f"  Revenue:        ${inc:,.2f}")
            print(f"  Expenses:       ${exp:,.2f}")
            print(f"  Net Profit:     ${net:,.2f}    Margin: {m_margin:.1f}%")
            print(f"  Tax Set-Aside:  ${reserve:,.2f}  ({reserve_pct:.0f}% of net)")
            print(f"  Take-Home:      ${home:,.2f}")
            print()
    print("  ═══════════════ ALL-TIME SUMMARY ═══════════════")
    print(f"  Revenue (paid):    ${collected:,.2f}")
    print(f"  Expenses:          ${expense_total:,.2f}")
    print(f"  Net Profit:        ${net_profit:,.2f}    Margin: {margin_pct:.1f}%")
    print(f"  Tax Set-Aside:     ${tax_set_aside:,.2f}  ({reserve_pct:.0f}% effective rate on net)")
    print(f"  Take-Home:         ${take_home:,.2f}")
    print(f"  Outstanding:       ${awaiting:,.2f}  (sent, not paid)")
    if overdue_amt > 0:
        print(f"  Overdue:           ${overdue_amt:,.2f}  (flagged in invoice log)")
    if by_cat:
        print("  Expense categories:")
        for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1]):
            print(f"    {cat:16} ${amt:,.2f}")
    print("  Guide: dashboard-setup-guide.md · invoice-log-template.csv · expense-log-template.csv")


def summarize_pricing(
    net_target=90000.0,
    tax_divisor=0.65,
    annual_expenses=8000.0,
    margin_pct=18.0,
    billable_hours=1044.0,
    billable_share=0.70,
):
    """datanestdigital/3ma7: floor rate from income + costs you need to cover."""
    gross = net_target / tax_divisor
    target = gross + annual_expenses
    buffered = target * (1 + margin_pct / 100)
    hourly = buffered / billable_hours if billable_hours else 0.0
    adj_hourly = hourly / billable_share if billable_share else hourly
    daily = hourly * 8
    project10 = hourly * 10 * 1.25
    print("=== FREELANCE PRICING FLOOR (datanestdigital/3ma7 shape) ===")
    print("  Start from the income and costs you need to cover — not what feels polite.")
    print(f"  Net income target:     ${net_target:,.0f}")
    print(f"  Tax gross-up divisor:  {tax_divisor:.2f} → gross ${gross:,.0f}")
    print(f"  Annual business costs: ${annual_expenses:,.0f}")
    print(f"  Margin buffer:         {margin_pct:.0f}%")
    print(f"  Target gross revenue:  ${buffered:,.0f}")
    print(f"  Billable hours/year:   {billable_hours:,.0f}")
    print(f"  Minimum hourly floor:  ${hourly:,.0f}/hr")
    print(f"  At {billable_share * 100:.0f}% billable share: ${adj_hourly:,.0f}/hr required")
    print(f"  Daily (8h):            ${daily:,.0f}")
    print(f"  10h project + 25% buffer:${project10:,.0f}")
    print("  Guide: pricing-guide.md · rate-calculator.html · datanestdigital/3ma7 buyer channel")


def summarize_portable(invoice_path, expense_path, reserve_pct=TAX_BUFFER_PCT):
    """faisalmq/3gcp: portable freelance finance tracker — single source of truth, any device."""
    invoices = load_invoices(invoice_path)
    expense_total, by_cat = load_expenses(expense_path)
    collected = sum(r["amount"] for r in invoices if r["status"] == "paid")
    awaiting = sum(r["amount"] for r in invoices if r["status"] == "sent")
    net_profit = collected - expense_total
    tax_set_aside = max(net_profit, 0) * reserve_pct / 100
    take_home = max(net_profit - tax_set_aside, 0)
    inv_rows = len(invoices)
    exp_rows = len(load_expense_rows(expense_path))
    print("=== PORTABLE FREELANCE FINANCE TRACKER (faisalmq/3gcp shape) ===")
    print("  Vessel: plain CSV logs — sync via Dropbox/iCloud/Git; no Google account.")
    print("  Update from phone (any CSV editor) or desktop (Excel, Numbers, CLI).")
    print("  Single source of truth — stop winging it with mental math.")
    print()
    print("  Four metrics that matter:")
    print(f"    Income tracking:     ${collected:,.2f} collected ({inv_rows} invoice rows)")
    print(f"    Expense categories:  ${expense_total:,.2f} ({exp_rows} expense rows)")
    if by_cat:
        top_cats = sorted(by_cat.items(), key=lambda x: -x[1])[:4]
        for cat, amt in top_cats:
            print(f"      · {cat}: ${amt:,.2f}")
    print(f"    Tax estimation:      ${tax_set_aside:,.2f} set aside ({reserve_pct:.0f}% of net)")
    print(f"    Net profit view:     ${net_profit:,.2f} → take-home ${take_home:,.2f}")
    if awaiting > 0:
        print(f"    Awaiting payment:    ${awaiting:,.2f} (logged, not spendable)")
    print()
    print("  Portability checklist:")
    print("    [x] Plain-text CSV — opens everywhere")
    print("    [x] No subscription — one-time kit")
    print("    [x] Offline CLI preview — python3 freelance_finance_os.py --portable …")
    print("    [x] Expandable — duplicate template rows as you grow")
    print("  Guide: portable-tracker-guide.md · invoice-log-sample.csv · expense-log-sample.csv")


def summarize_take_home(invoice_path, expense_path, reserve_pct=TAKE_HOME_RESERVE_PCT):
    """marginmap/14ag: gross → net → SE tax component → reserve → take-home."""
    invoices = load_invoices(invoice_path)
    expense_total, _ = load_expenses(expense_path)
    collected = sum(r["amount"] for r in invoices if r["status"] == "paid")
    net_profit = collected - expense_total
    if net_profit <= 0:
        print("=== TAKE-HOME ESTIMATE (marginmap/14ag shape) ===")
        print("  No positive net profit yet — log paid invoices and expenses first.")
        print("  Guide: take-home-guide.md · rate-calculator.html")
        return
    se_tax = net_profit * SE_TAX_RATE
    reserve_total = net_profit * (reserve_pct / 100)
    take_home = net_profit - reserve_total
    effective_on_gross = (reserve_total / collected * 100) if collected > 0 else 0.0
    print("=== TAKE-HOME ESTIMATE (marginmap/14ag shape) ===")
    print(f"  Collected (gross paid): ${collected:,.2f}")
    print(f"  Business expenses:      ${expense_total:,.2f}")
    print(f"  Net self-employment:    ${net_profit:,.2f}")
    print(f"  Est. SE tax (15.3% net): ${se_tax:,.2f}")
    print(f"  Planned reserve ({reserve_pct:.0f}% of net): ${reserve_total:,.2f}")
    print(f"  Est. take-home after reserve: ${take_home:,.2f}")
    print(f"  Effective reserve on gross: {effective_on_gross:.1f}%")
    print("  The 30% gross shortcut often lies — reserve on net, not deposits.")
    print("  Guide: take-home-guide.md · rate-calculator.html · tax-buffer-guide.md")


def summarize_spreadsheet_system(invoice_path, expense_path):
    """crazychief/52ge: book principles → invoice+expense vessel → hardened behavior."""
    invoices = load_invoices(invoice_path)
    expense_rows = load_expense_rows(expense_path)
    income = sum(r["amount"] for r in invoices if r["status"] == "paid")
    expense = sum(r["amount"] for r in expense_rows)
    net = income - expense
    reserve = max(net, 0) * TAX_BUFFER_PCT / 100
    months = sorted({
        *(r["date"].strftime("%Y-%m") for r in invoices if r.get("date")),
        *(r["date"].strftime("%Y-%m") for r in expense_rows),
    })
    tx_count = len(invoices) + len(expense_rows)
    phase = "HARDENED" if tx_count >= 10 and len(months) >= 2 else "PROTOTYPE"
    print("\n=== SPREADSHEET SYSTEM (crazychief/52ge shape) ===")
    print("  Sequence: Read → Decompose → Prototype → Harden → Reapply")
    print(f"  Vessel: invoice + expense logs ({tx_count} rows, {len(months)} month(s))")
    print(f"  Fixed rule: tax set-aside {TAX_BUFFER_PCT:.0f}% of net profit")
    print("  Three containers:")
    print(f"    Income    ${income:,.2f}")
    print(f"    Expenses  ${expense:,.2f}")
    print(f"    Reserved  ${reserve:,.2f}  (set-aside, not spendable)")
    print(f"  System phase: {phase}")
    print("  Guide: spreadsheet-system-guide.md · invoice-log-sample.csv · expense-log-sample.csv")


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--1099k":
        summarize_1099k_reconciliation(load_transaction_log(sys.argv[2]))
        return
    if len(sys.argv) >= 4 and sys.argv[1] == "--bills-debt":
        summarize_bills(sys.argv[2])
        summarize_debt(sys.argv[3])
        return
    if len(sys.argv) >= 3 and sys.argv[1] == "--savings-goals":
        summarize_savings(sys.argv[2])
        return
    if len(sys.argv) >= 4 and sys.argv[1] == "--spreadsheet-system":
        summarize_spreadsheet_system(sys.argv[2], sys.argv[3])
        return
    if len(sys.argv) >= 5 and sys.argv[1] == "--six-month-reveal":
        subs = sys.argv[5] if len(sys.argv) >= 6 else None
        summarize_six_month_reveal(sys.argv[2], sys.argv[3], sys.argv[4], subs)
        return
    if len(sys.argv) >= 4 and sys.argv[1] == "--take-home":
        pct = float(sys.argv[4]) if len(sys.argv) >= 5 else TAKE_HOME_RESERVE_PCT
        summarize_take_home(sys.argv[2], sys.argv[3], reserve_pct=pct)
        return
    if len(sys.argv) >= 4 and sys.argv[1] == "--dashboard":
        pct = float(sys.argv[4]) if len(sys.argv) >= 5 else TAX_BUFFER_PCT
        summarize_dashboard_setup(sys.argv[2], sys.argv[3], reserve_pct=pct)
        return
    if len(sys.argv) >= 4 and sys.argv[1] == "--portable":
        pct = float(sys.argv[4]) if len(sys.argv) >= 5 else TAX_BUFFER_PCT
        summarize_portable(sys.argv[2], sys.argv[3], reserve_pct=pct)
        return
    if len(sys.argv) >= 2 and sys.argv[1] == "--pricing":
        args = [float(x) for x in sys.argv[2:8]]
        while len(args) < 6:
            defaults = [90000.0, 0.65, 8000.0, 18.0, 1044.0, 0.70]
            args.append(defaults[len(args)])
        summarize_pricing(*args)
        return
    if len(sys.argv) < 3:
        print("Usage: python3 freelance_finance_os.py invoice-log.csv expense-log.csv [subscriptions.csv] [bills.csv] [debt.csv] [savings.csv]")
        print("       python3 freelance_finance_os.py --1099k 1099k-freelance-sample.csv")
        print("       python3 freelance_finance_os.py --bills-debt bills-sample.csv debt-sample.csv")
        print("       python3 freelance_finance_os.py --savings-goals savings-sample.csv")
        print("       python3 freelance_finance_os.py --spreadsheet-system invoice-log.csv expense-log.csv")
        print("       python3 freelance_finance_os.py --six-month-reveal invoice-log.csv expense-log.csv client-hours.csv [subscriptions.csv]")
        print("       python3 freelance_finance_os.py --take-home invoice-log.csv expense-log.csv [reserve_pct]")
        print("       python3 freelance_finance_os.py --dashboard invoice-log.csv expense-log.csv [reserve_pct]")
        print("       python3 freelance_finance_os.py --portable invoice-log.csv expense-log.csv [reserve_pct]")
        print("       python3 freelance_finance_os.py --pricing [net_target tax_divisor annual_expenses margin_pct billable_hours billable_share]")
        sys.exit(1)

    invoices = load_invoices(sys.argv[1])
    expense_path = sys.argv[2]
    expense_total, by_cat = load_expenses(expense_path)
    expense_rows = load_expense_rows(expense_path)

    invoiced = sum(r["amount"] for r in invoices)
    collected = sum(r["amount"] for r in invoices if r["status"] == "paid")
    awaiting = sum(r["amount"] for r in invoices if r["status"] == "sent")
    overdue_amt = sum(r["amount"] for r in invoices if r["overdue"])
    overdue_cnt = sum(1 for r in invoices if r["overdue"])

    net_profit = collected - expense_total
    tax_buffer = max(net_profit, 0) * TAX_BUFFER_PCT / 100
    safe_to_spend = max(net_profit - tax_buffer, 0)
    quarterly = max(net_profit, 0) * ESTIMATED_TAX_PCT / 100 / 4

    inv_rows = len(invoices)
    exp_rows = sum(1 for _ in open(sys.argv[2], encoding="utf-8")) - 1  # header

    print("=== BEGINNER-FRIENDLY (faisalmq/2fj6 — no formulas required) ===")
    print("  You only type into shaded cells. In this kit that's your CSV rows.")
    print("  Type here:     invoice + expense CSV columns (see templates)")
    print("  Auto-calculated: collected, net profit, tax buffer, safe-to-spend, quarterly")
    print(f"  Invoice log: {inv_rows} rows · Expense log: {exp_rows} rows (expandable — duplicate templates)")
    print()
    print("=== FREELANCE FINANCE OS (By the Loop clone) ===")
    print(f"  Invoices logged:     {len(invoices)}")
    print(f"  Total invoiced:      ${invoiced:,.2f}")
    print(f"  Collected (paid):    ${collected:,.2f}")
    print(f"  Awaiting payment:    ${awaiting:,.2f}")
    print(f"  Overdue (sent+late): {overdue_cnt} invoices · ${overdue_amt:,.2f}")
    summarize_accounts_receivable(invoices)
    print()
    print("=== EXPENSE + TAX BUFFER ===")
    print(f"  Expenses YTD:        ${expense_total:,.2f}")
    for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1]):
        print(f"    {cat:12} ${amt:,.2f}")
    print(f"  Net profit (paid):   ${net_profit:,.2f}")
    print(f"  Tax buffer ({TAX_BUFFER_PCT:.0f}%):   ${tax_buffer:,.2f}")
    print(f"  Safe to spend:       ${safe_to_spend:,.2f}")
    print_category_breakdown(expense_rows)
    print()
    margin_pct = (net_profit / collected * 100) if collected > 0 else 0.0
    print("=== PROFIT MARGINS AT A GLANCE (faisalmq/3cpo shape) ===")
    print(f"  Collected (paid):    ${collected:,.2f}")
    print(f"  Expenses YTD:        ${expense_total:,.2f}")
    print(f"  Net profit:          ${net_profit:,.2f}")
    print(f"  Profit margin:       {margin_pct:.1f}%")
    print("  Categorized breakdown (tax preparedness):")
    for cat, amt in sorted(by_cat.items(), key=lambda x: -x[1]):
        pct_rev = (amt / collected * 100) if collected > 0 else 0.0
        print(f"    {cat:12} ${amt:,.2f}  ({pct_rev:.1f}% of revenue)")
    by_client = defaultdict(float)
    for r in invoices:
        if r["status"] == "paid":
            by_client[r["client"]] += r["amount"]
    if by_client:
        print("  Per-client collected (pricing decisions):")
        for client, amt in sorted(by_client.items(), key=lambda x: -x[1]):
            print(f"    {client:20} ${amt:,.2f}")
    print()
    print("=== QUARTERLY TAX ESTIMATOR (1040-ES shape) ===")
    print(f"  Estimated annual tax ({ESTIMATED_TAX_PCT:.0f}% planning rate): ${max(net_profit,0)*ESTIMATED_TAX_PCT/100:,.2f}")
    print(f"  Suggested per deadline: ${quarterly:,.2f}")
    for q, deadline, period in QUARTERLY_DEADLINES:
        print(f"    {q} due {deadline:16} ({period})")
    print()
    print("=== COMPLETE WORKBOOK (hemantdev/1iae — no Notion, offline file) ===")
    print("  Dashboard view:      collected, net profit, safe-to-spend (this stdout)")
    print("  Income log:          invoice-log.csv — one row per payment")
    print("  Expense log:         expense-log.csv — categorized, tax-deductible flags")
    print("  Clients view:        per-client collected totals (from invoice log)")
    print("  Invoices view:       draft/sent/paid/overdue from same log")
    print("  Tax estimator:       quarterly deadlines + suggested set-aside")
    print("  Zero onboarding:     open CSV, type shaded columns, run CLI — no account")
    print()
    print("=== FOUR TOOLS IN ONE BUNDLE ===")
    print("  1. Invoice tracker     [this run]")
    print("  2. Expense + buffer    [this run]")
    print("  3. Rate calculator     [open rate-calculator.html]")
    print("  4. Quarterly estimator [this run]")
    print_command_center(len(invoices), collected, overdue_cnt, overdue_amt, expense_total, net_profit)
    print_bundle_strategy()
    extra = sys.argv[3:]
    subs_path = extra[0] if len(extra) >= 1 and extra[0] else None
    bills_path = extra[1] if len(extra) >= 2 and extra[1] else None
    debt_path = extra[2] if len(extra) >= 3 and extra[2] else None
    savings_path = extra[3] if len(extra) >= 4 and extra[3] else None
    if subs_path:
        summarize_subscription_audit(subs_path)
    if bills_path:
        summarize_bills(bills_path)
    if debt_path:
        summarize_debt(debt_path, ytd_net=net_profit)
    if savings_path:
        summarize_savings(savings_path)
    summarize_spreadsheet_system(sys.argv[1], sys.argv[2])
    summarize_cash_runway(invoices, expense_rows, bills_path, debt_path)


def _parse_iso_date(s):
    s = (s or "").strip()
    if not s:
        return None
    try:
        return datetime.strptime(s, "%Y-%m-%d").date()
    except ValueError:
        return None


def _subscription_status(renewal_date, cancel_by, today):
    """agentchip/52g8 four-state judgment from renewal + cancel-by dates."""
    if renewal_date and today > renewal_date:
        return "EXPIRED"
    if cancel_by and today >= cancel_by:
        return "RENEW NOW"
    if cancel_by:
        days_to_cancel = (cancel_by - today).days
        if 0 <= days_to_cancel <= 30:
            return "Renew soon"
    return "Active"


def summarize_subscription_audit(path):
    """agentchip/52g8: freelance SaaS auto-renewal creep — track cancel-by, not renewal."""
    rows = []
    today = date.today()
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                monthly = float(row.get("monthly_usd", row.get("amount", 0)))
            except (KeyError, ValueError):
                continue
            renewal = _parse_iso_date(row.get("renewal_date", ""))
            cancel_by = _parse_iso_date(row.get("cancel_by", ""))
            status = (row.get("status") or "").strip() or _subscription_status(
                renewal, cancel_by, today
            )
            rows.append({
                "contract": row.get("contract", "").strip(),
                "vendor": row.get("vendor", row.get("bill", "")).strip(),
                "monthly": monthly,
                "cancel_by": cancel_by,
                "status": status,
            })
    if not rows:
        return
    monthly_load = sum(r["monthly"] for r in rows)
    urgent = [r for r in rows if r["status"] in ("RENEW NOW", "Renew soon", "EXPIRED")]
    zombie = [r for r in rows if r["monthly"] >= 50 and r["status"] == "RENEW NOW"]
    print("\n=== SUBSCRIPTION AUTO-RENEWAL AUDIT (agentchip/52g8 shape) ===")
    print("  Track cancel-by deadlines — calendar renewal reminders arrive too late.")
    print(f"  Contracts tracked: {len(rows)} · est. monthly load: ${monthly_load:,.2f}")
    print("  contract   vendor          monthly  cancel_by    status")
    for r in rows:
        cancel = r["cancel_by"].isoformat() if r["cancel_by"] else "—"
        print(
            f"  {r['contract'] or '—':10} {r['vendor'][:14]:14} "
            f"${r['monthly']:>6.2f}  {cancel:10}  {r['status']}"
        )
    if urgent:
        print(f"  Action needed: {len(urgent)} contract(s) in renew/cancel window")
    if zombie:
        wasted = sum(r["monthly"] for r in zombie)
        print(
            f"  Zombie SaaS check: ${wasted:,.2f}/mo flagged RENEW NOW "
            "(unused tools still billing — agentchip/52g8 audit pays for itself)"
        )
    print("  Guide: subscription-audit-guide.md · subscriptions-sample.csv")


def print_bundle_strategy():
    """wedgemethoddev/4hgi: individual template SKUs → one bundle at value gap."""
    tools = (
        ("Invoice tracker", "$12–29/yr", "Did that client pay? Overdue flags"),
        ("Expense + tax buffer", "$9–15/yr", "How much to set aside?"),
        ("Rate calculator", "$5–15", "Am I charging enough?"),
        ("Quarterly tax estimator", "$10–20", "What to send each quarter?"),
    )
    print()
    print("=== BUNDLE STRATEGY (wedgemethoddev/4hgi + By the Loop $5 OS) ===")
    print("  Four freelancer pains → one download instead of four subscriptions:")
    for name, ala_carte, pain in tools:
        print(f"    {name:24} {ala_carte:12} — {pain}")
    print("  À la carte floor:      ~$36–79/yr across separate tools + blank-page setup")
    print("  By the Loop bundle:    $5 one-time (4 xlsx + PDF) — freelance-finance-os")
    print("  Our clone:             EUR 9 one-time (CSV + CLI + rate calculator HTML)")
    print("  Bundle math:           perceived value gap — one OS beats four logins")
    print("  Guide: bundle-strategy-guide.md · wedgemethoddev/4hgi buyer channel clone")


def print_command_center(inv_count, collected, overdue_cnt, overdue_amt, expense_total, net_profit):
    """timmothybuilder/4e81: five-template stack ending in unified command center."""
    active = inv_count > 0 or expense_total > 0
    status = "active" if active else "add rows"
    print()
    print("=== FREELANCER FINANCIAL COMMAND CENTER (timmothybuilder/4e81 shape) ===")
    print("  Five templates every freelancer needs — #5 unifies the rest:")
    print(f"  1. Personal finance tracker → expense log + tax buffer [{status}]")
    print(f"  2. Client / proposal tracker → invoice log + overdue flags [{status}]")
    print("  3. Content calendar → outside kit [use your own calendar]")
    print(f"  4. Weekly money check-in → rate calculator.html [{status}]")
    print(f"  5. Financial command center → full 4-tool By the Loop bundle [{status}]")
    if overdue_cnt > 0:
        print(
            f"  Uncollected overdue invoices: ${overdue_amt:,.2f} ({overdue_cnt}) — "
            "template #5 pays for itself when you find these"
        )
    print(f"  Collected (paid):    ${collected:,.2f}")
    print(f"  Net profit (paid):   ${net_profit:,.2f}")
    print("  Guide: command-center-guide.md · timmothybuilder/4e81 buyer channel clone")


def bills_monthly_load(path):
    monthly_equiv = 0.0
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = float(row["amount"])
            except (KeyError, ValueError):
                continue
            freq = row.get("frequency", "monthly").strip().lower()
            if freq == "monthly":
                monthly_equiv += amt
            elif freq == "quarterly":
                monthly_equiv += amt / 3
            elif freq == "yearly":
                monthly_equiv += amt / 12
            else:
                monthly_equiv += amt
    return monthly_equiv


def debt_monthly_minimum(path):
    total = 0.0
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                total += float(row.get("min_payment", 0) or 0)
            except (KeyError, ValueError):
                continue
    return total


def summarize_cash_runway(invoices, expense_rows, bills_path=None, debt_path=None, months_ahead=12):
    """agentchip/33mm: forward cash forecast — which month balance goes negative."""
    starting_cash = float(os.environ.get("FINANCE_STARTING_CASH", "3000"))
    by_month = defaultdict(lambda: {"income": 0.0, "expense": 0.0})
    for inv in invoices:
        if inv["status"] != "paid" or not inv.get("date"):
            continue
        key = inv["date"].strftime("%Y-%m")
        by_month[key]["income"] += inv["amount"]
    for r in expense_rows:
        key = r["date"].strftime("%Y-%m")
        by_month[key]["expense"] += r["amount"]
    hist_months = sorted(by_month.keys())
    if not hist_months:
        return
    avg_income = sum(m["income"] for m in by_month.values()) / len(hist_months)
    avg_expense = sum(m["expense"] for m in by_month.values()) / len(hist_months)
    bills_monthly = bills_monthly_load(bills_path) if bills_path else 0.0
    debt_min = debt_monthly_minimum(debt_path) if debt_path else 0.0
    fixed_obligations = bills_monthly + debt_min
    tax_reserve_pct = TAX_BUFFER_PCT / 100.0

    def project(income_mult, expense_mult):
        balance = starting_cash
        forecast = []
        lowest = (balance, "start")
        for i in range(months_ahead):
            inc = avg_income * income_mult
            exp = (avg_expense * expense_mult) + fixed_obligations
            tax_set_aside = max(0.0, (inc - exp) * tax_reserve_pct) if inc > exp else 0.0
            net = inc - exp - tax_set_aside
            opening = balance
            balance += net
            label = f"M+{i + 1}"
            forecast.append((label, opening, inc, exp, tax_set_aside, net, balance))
            if balance < lowest[0]:
                lowest = (balance, label)
        return forecast, lowest

    base_fc, base_low = project(1.0, 1.0)
    opt_fc, opt_low = project(1.2, 0.9)
    pes_fc, pes_low = project(0.8, 1.1)

    print("\n=== CASH RUNWAY FORECAST (agentchip/33mm shape) ===")
    print(f"  Starting cash: ${starting_cash:,.2f} (set FINANCE_STARTING_CASH to override)")
    print(f"  Historical avg/mo: income ${avg_income:,.2f} · expenses ${avg_expense:,.2f}")
    if fixed_obligations > 0:
        print(f"  Fixed obligations/mo: ${fixed_obligations:,.2f} (bills + debt minimums)")
    print("  12-month base forecast:")
    for label, opening, inc, exp, tax, net, closing in base_fc[:6]:
        print(
            f"    {label}: open ${opening:,.0f}  in ${inc:,.0f}  out ${exp:,.0f}  "
            f"tax ${tax:,.0f}  close ${closing:,.0f}"
        )
    if len(base_fc) > 6:
        print(f"    … ({len(base_fc) - 6} more months in full output)")
    print(f"  Lowest balance (base): ${base_low[0]:,.2f} at {base_low[1]}")
    if base_low[0] < 0:
        print("  CASH GAP — base scenario goes negative before month ends")
    print(f"  Scenario range: optimistic low ${opt_low[0]:,.2f} · pessimistic low ${pes_low[0]:,.2f}")
    print("  Guide: cash-runway-guide.md · agentchip/33mm buyer channel clone")


if __name__ == "__main__":
    main()
