#!/usr/bin/env python3
"""Freelancer Invoice & Client Tracker — clone of AgentChip qiliang.gumroad.com/l/ahefab ($15)."""
import csv
import os
import sys
from collections import defaultdict
from datetime import date, datetime

TAX_BUFFER_PCT = 25.0


def load_clients(path):
    clients = {}
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            name = row.get("client_name", "").strip()
            if not name:
                continue
            rate = float(row.get("hourly_rate", "0") or 0)
            clients[name] = {
                "contact": row.get("contact", "").strip(),
                "payment_terms_days": int(row.get("payment_terms_days", "30") or 30),
                "hourly_rate": rate,
                "status": row.get("status", "active").strip().lower(),
            }
    return clients


def load_invoices(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amount = float(row.get("amount", "0") or 0)
                tax = float(row.get("tax", "0") or 0)
            except ValueError:
                continue
            inv_id = row.get("invoice_id", "").strip()
            if not inv_id:
                continue
            due = row.get("due_date", "").strip()
            status = row.get("status", "pending").strip().lower()
            overdue = False
            days_late = 0
            if due and status in ("pending", "sent", "overdue"):
                try:
                    due_d = datetime.strptime(due, "%Y-%m-%d").date()
                    if due_d < date.today():
                        overdue = True
                        days_late = (date.today() - due_d).days
                        status = "overdue"
                except ValueError:
                    pass
            rows.append({
                "invoice_id": inv_id,
                "client": row.get("client", "").strip(),
                "invoice_date": row.get("invoice_date", "").strip(),
                "description": row.get("description", "").strip(),
                "amount": amount,
                "tax": tax,
                "total": amount + tax,
                "status": status,
                "due_date": due,
                "overdue": overdue,
                "days_late": days_late,
            })
    return rows


def load_payments(path):
    paid = defaultdict(float)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            inv_id = row.get("invoice_id", "").strip()
            if not inv_id:
                continue
            try:
                amt = float(row.get("amount", "0") or 0)
            except ValueError:
                continue
            paid[inv_id] += amt
    return dict(paid)


def payments_by_month(path):
    by_month = defaultdict(float)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            pay_date = row.get("payment_date", "").strip()
            if not pay_date:
                continue
            try:
                amt = float(row.get("amount", "0") or 0)
            except ValueError:
                continue
            by_month[pay_date[:7]] += amt
    return dict(by_month)


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


def subscription_monthly_load(path):
    total = 0.0
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                total += float(row.get("monthly_usd", row.get("amount", 0)) or 0)
            except (KeyError, ValueError):
                continue
    return total


def summarize(clients, invoices, payments):
    total_invoiced = sum(i["total"] for i in invoices)
    total_received = sum(payments.values())
    outstanding = 0.0
    overdue_total = 0.0
    overdue_count = 0
    paid_count = 0
    pending_count = 0

    for inv in invoices:
        paid_amt = payments.get(inv["invoice_id"], 0.0)
        balance = max(inv["total"] - paid_amt, 0.0)
        if balance <= 0.01:
            paid_count += 1
            continue
        pending_count += 1
        outstanding += balance
        if inv["overdue"]:
            overdue_count += 1
            overdue_total += balance

    active_clients = sum(1 for c in clients.values() if c["status"] == "active")
    return {
        "total_invoiced": total_invoiced,
        "total_received": total_received,
        "outstanding": outstanding,
        "overdue_total": overdue_total,
        "overdue_count": overdue_count,
        "paid_count": paid_count,
        "pending_count": pending_count,
        "active_clients": active_clients,
    }


def _parse_iso_date(s):
    if not s:
        return None
    try:
        return datetime.strptime(s.strip(), "%Y-%m-%d").date()
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


def summarize_cash_runway(
    payments_path,
    subscriptions_path=None,
    bills_path=None,
    debt_path=None,
    months_ahead=12,
):
    """agentchip/33mm: forward cash forecast — which month balance goes negative."""
    by_month = payments_by_month(payments_path)
    if not by_month:
        return
    starting_cash = float(os.environ.get("FINANCE_STARTING_CASH", "3000"))
    hist_months = sorted(by_month.keys())
    avg_income = sum(by_month.values()) / len(hist_months)
    sub_monthly = subscription_monthly_load(subscriptions_path) if subscriptions_path else 0.0
    bills_monthly = bills_monthly_load(bills_path) if bills_path else 0.0
    debt_min = debt_monthly_minimum(debt_path) if debt_path else 0.0
    fixed_obligations = sub_monthly + bills_monthly + debt_min
    tax_reserve_pct = TAX_BUFFER_PCT / 100.0

    def project(income_mult, expense_mult):
        balance = starting_cash
        forecast = []
        lowest = (balance, "start")
        for i in range(months_ahead):
            inc = avg_income * income_mult
            exp = (fixed_obligations * expense_mult)
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
    print(f"  Historical avg/mo income: ${avg_income:,.2f} ({len(hist_months)} month(s) of payments)")
    if fixed_obligations > 0:
        print(f"  Fixed obligations/mo: ${fixed_obligations:,.2f} (SaaS + bills + debt minimums)")
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


def _normalize_vendor(name):
    n = name.strip().upper()
    for suffix in (" CORPORATION", " CORP", " INC.", " INC", " LTD.", " LTD", " LLC"):
        if n.endswith(suffix):
            n = n[: -len(suffix)].strip()
    return n


def _parse_dirty_amount(raw):
    if raw is None:
        raise ValueError("empty amount")
    s = str(raw).strip().replace("$", "").replace(",", "")
    if not s or s.lower() in ("invalid-amount", "n/a"):
        raise ValueError(f"unparseable amount: {raw}")
    return float(s)


def _parse_dirty_date(raw):
    s = (raw or "").strip()
    if not s:
        raise ValueError("empty date")
    for fmt in ("%Y-%m-%d", "%m/%d/%Y", "%m/%d/%y", "%d/%m/%Y"):
        try:
            return datetime.strptime(s, fmt).date().isoformat()
        except ValueError:
            continue
    raise ValueError(f"unparseable date: {raw}")


def clean_dirty_invoices(path):
    """agentchip/47ag: deterministic CSV cleaning — dedupe, normalize, no AI guesses."""
    rows_in = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            rows_in.append(row)

    clean = []
    errors = []
    seen = set()

    for i, row in enumerate(rows_in, start=2):
        vendor_raw = row.get("vendor", row.get("client", "")).strip()
        if not vendor_raw:
            errors.append({"row": i, "reason": "missing vendor", "raw": row})
            continue
        try:
            amount = _parse_dirty_amount(row.get("amount", ""))
            inv_date = _parse_dirty_date(row.get("invoice_date", row.get("date", "")))
        except ValueError as exc:
            errors.append({"row": i, "reason": str(exc), "raw": row})
            continue
        vendor = _normalize_vendor(vendor_raw)
        desc = row.get("description", "").strip()
        key = (vendor, inv_date, round(amount, 2), desc.lower())
        if key in seen:
            continue
        seen.add(key)
        clean.append({
            "vendor": vendor,
            "invoice_date": inv_date,
            "amount": amount,
            "description": desc,
        })

    return clean, errors, len(rows_in)


def summarize_invoice_reconciliation(path):
    """agentchip/47ag: CSV in, reconciliation out — nightly copy-paste ritual killer."""
    clean, errors, raw_count = clean_dirty_invoices(path)
    dupes_removed = raw_count - len(clean) - len(errors)
    by_vendor = defaultdict(float)
    by_month = defaultdict(float)
    for row in clean:
        by_vendor[row["vendor"]] += row["amount"]
        by_month[row["invoice_date"][:7]] += row["amount"]

    print("\n=== INVOICE CSV RECONCILIATION (agentchip/47ag shape) ===")
    print("  Deterministic parsing — no AI guesses. Unparseable rows go to errors, not invented.")
    print(f"  Rows in: {raw_count} · clean: {len(clean)} · duplicates removed: {max(dupes_removed, 0)} · errors: {len(errors)}")
    if errors:
        print("  Unparsed rows (fix manually — never silently dropped):")
        for e in errors[:5]:
            print(f"    line {e['row']}: {e['reason']}")
        if len(errors) > 5:
            print(f"    … {len(errors) - 5} more")
    if by_vendor:
        print("  Totals by vendor:")
        for vendor, total in sorted(by_vendor.items(), key=lambda x: -x[1]):
            print(f"    {vendor:20} ${total:,.2f}")
    if by_month:
        print("  Totals by month:")
        for month, total in sorted(by_month.items()):
            print(f"    {month}: ${total:,.2f}")
    print(f"  Grand total (clean): ${sum(by_vendor.values()):,.2f}")
    print("  Guide: invoice-reconciliation-guide.md · dirty-invoices-sample.csv")


def print_bundle_stack(manifest_path=None):
    """agentchip/2dgn: separate tools priced individually → one connected workbook stack."""
    modules = [
        ("Invoice + overdue flags", "agentchip/2b11", 15),
        ("Subscription auto-renewal audit", "agentchip/52g8", 12),
        ("Cash runway forecast", "agentchip/33mm", 12),
        ("Client dashboard rollup", "built-in", 0),
    ]
    if manifest_path:
        try:
            with open(manifest_path, newline="") as f:
                rows = list(csv.DictReader(f))
            if rows:
                modules = [
                    (r["name"], r["buyer_channel"], float(r["separate_price_usd"]))
                    for r in rows
                    if r.get("included", "yes").lower() in ("yes", "true", "1")
                ]
        except OSError:
            pass
    separate_total = sum(p for _, _, p in modules)
    kit_price_eur = 9
    savings = max(separate_total - kit_price_eur, 0)
    pct = int(round(100 * savings / separate_total)) if separate_total else 0
    print("\n=== FREELANCER FINANCE STACK (agentchip/2dgn shape) ===")
    for name, channel, price in modules:
        tag = f"separate ~${price:.0f}" if price else "built-in"
        print(f"  Module: {name} ({channel}) — {tag} · included ✓")
    print(f"  Separate stack total: ~${separate_total:.0f} · this kit: EUR {kit_price_eur} one-time")
    if separate_total:
        print(f"  Savings vs buying separately: ~{pct}%")
    print("  Guide: bundle-stack-guide.md · agentchip/2dgn buyer channel clone")


def print_report(clients, invoices, payments):
    s = summarize(clients, invoices, payments)
    print("=== FREELANCER INVOICE & CLIENT TRACKER (AgentChip clone) ===")
    print(f"  Active clients:      {s['active_clients']}")
    print(f"  Total invoiced:      ${s['total_invoiced']:,.2f}")
    print(f"  Total received:      ${s['total_received']:,.2f}")
    print(f"  Outstanding:         ${s['outstanding']:,.2f}")
    print(f"  Overdue invoices:    {s['overdue_count']} · ${s['overdue_total']:,.2f}")
    print(f"  Paid / pending:      {s['paid_count']} paid · {s['pending_count']} open")

    overdue = [i for i in invoices if i["overdue"]]
    if overdue:
        print("\n=== OVERDUE FLAGS ===")
        for inv in sorted(overdue, key=lambda x: -x["days_late"]):
            bal = max(inv["total"] - payments.get(inv["invoice_id"], 0.0), 0.0)
            print(f"  {inv['invoice_id']} · {inv['client']} · {inv['days_late']}d late · ${bal:,.2f}")

    by_client = defaultdict(lambda: {"invoiced": 0.0, "received": 0.0})
    for inv in invoices:
        by_client[inv["client"]]["invoiced"] += inv["total"]
        by_client[inv["client"]]["received"] += payments.get(inv["invoice_id"], 0.0)
    if by_client:
        print("\n=== DASHBOARD BY CLIENT ===")
        for client, nums in sorted(by_client.items()):
            owed = nums["invoiced"] - nums["received"]
            print(f"  {client}: invoiced ${nums['invoiced']:,.2f} · received ${nums['received']:,.2f} · owed ${owed:,.2f}")


def main():
    if len(sys.argv) >= 3 and sys.argv[1] == "--reconcile":
        summarize_invoice_reconciliation(sys.argv[2])
        return
    if len(sys.argv) < 4:
        print(
            "Usage: freelancer_invoice_tracker.py clients.csv invoices.csv payments.csv "
            "[subscriptions.csv] [bills.csv] [debt.csv]\n"
            "       freelancer_invoice_tracker.py --reconcile dirty-invoices.csv",
            file=sys.stderr,
        )
        sys.exit(1)
    clients = load_clients(sys.argv[1])
    invoices = load_invoices(sys.argv[2])
    payments = load_payments(sys.argv[3])
    print_report(clients, invoices, payments)
    subs_path = sys.argv[4] if len(sys.argv) >= 5 else None
    bills_path = sys.argv[5] if len(sys.argv) >= 6 else None
    debt_path = sys.argv[6] if len(sys.argv) >= 7 else None
    if subs_path:
        summarize_subscription_audit(subs_path)
    summarize_cash_runway(
        sys.argv[3],
        subscriptions_path=subs_path,
        bills_path=bills_path,
        debt_path=debt_path,
    )
    manifest = None
    for arg in sys.argv[4:]:
        if arg.endswith("modules-manifest.csv"):
            manifest = arg
            break
    print_bundle_stack(manifest)


if __name__ == "__main__":
    main()
