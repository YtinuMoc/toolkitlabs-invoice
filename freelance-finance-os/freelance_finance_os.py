#!/usr/bin/env python3
"""Freelance Finance OS — clone of By the Loop freelance-finance-os ($5 Gumroad)."""
import csv
import sys
from collections import defaultdict
from datetime import date, datetime

TAX_BUFFER_PCT = 25.0
ESTIMATED_TAX_PCT = 28.0  # planning default; not tax advice

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
            rows.append({
                "client": row.get("client", "unknown").strip() or "unknown",
                "amount": amt,
                "status": status,
                "overdue": overdue,
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


def main():
    if len(sys.argv) < 3:
        print("Usage: python3 freelance_finance_os.py invoice-log.csv expense-log.csv [subscriptions.csv]")
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
    if len(sys.argv) >= 4 and sys.argv[3]:
        summarize_subscription_audit(sys.argv[3])


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


if __name__ == "__main__":
    main()
