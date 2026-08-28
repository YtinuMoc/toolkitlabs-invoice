#!/usr/bin/env python3
"""Freelancer Invoice & Client Tracker — clone of Productive Club productiveclub.gumroad.com/l/gnohas ($19+)."""
import csv
import os
import sys
from collections import defaultdict
from datetime import date, datetime, timedelta

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


FOLLOW_UP_CADENCE_DAYS = (1, 3, 7, 14, 30)


def summarize_payment_follow_up(invoices_path, payments_path=None):
    """agentchip/11n6: overdue invoice follow-up cadence preview — no email send."""
    invoices = load_invoices(invoices_path)
    payments = load_payments(payments_path) if payments_path else {}
    today = date.today()
    cadence = []
    for inv in invoices:
        if inv["status"] == "paid":
            continue
        due = inv.get("due_date", "").strip()
        if not due:
            continue
        try:
            due_d = datetime.strptime(due, "%Y-%m-%d").date()
        except ValueError:
            continue
        if due_d >= today:
            continue
        balance = max(inv["total"] - payments.get(inv["invoice_id"], 0.0), 0.0)
        if balance <= 0:
            continue
        days_late = (today - due_d).days
        touchpoints = []
        for day in FOLLOW_UP_CADENCE_DAYS:
            touch_date = due_d + timedelta(days=day)
            if touch_date <= today:
                touchpoints.append((day, touch_date, "DUE" if touch_date == today else "OVERDUE"))
            elif touch_date == today + timedelta(days=1):
                touchpoints.append((day, touch_date, "TOMORROW"))
        next_due = None
        for day in FOLLOW_UP_CADENCE_DAYS:
            touch_date = due_d + timedelta(days=day)
            if touch_date >= today:
                next_due = (day, touch_date)
                break
        cadence.append({
            "invoice_id": inv["invoice_id"],
            "client": inv["client"],
            "balance": balance,
            "days_late": days_late,
            "due_date": due,
            "touchpoints": touchpoints,
            "next_due": next_due,
        })

    print("\n=== PAYMENT FOLLOW-UP CADENCE (agentchip/11n6 shape) ===")
    print("  Preview only — no emails sent. Fixed 1/3/7/14/30-day rhythm after due date.")
    print(f"  Overdue unpaid invoices: {len(cadence)}")
    if not cadence:
        print("  No overdue balances — cadence idle.")
        return
    for row in sorted(cadence, key=lambda x: -x["days_late"]):
        print(f"\n  {row['invoice_id']} · {row['client']} · ${row['balance']:,.2f} · {row['days_late']}d late (due {row['due_date']})")
        if row["touchpoints"]:
            due_now = [t for t in row["touchpoints"] if t[2] in ("DUE", "OVERDUE")]
            if due_now:
                latest = max(due_now, key=lambda t: t[0])
                print(f"    → Follow up NOW (touch #{FOLLOW_UP_CADENCE_DAYS.index(latest[0]) + 1} · day +{latest[0]})")
            for day, touch_date, status in row["touchpoints"]:
                flag = "← action" if status in ("DUE", "OVERDUE") else status.lower()
                print(f"    touch +{day}d ({touch_date}): {flag}")
        if row["next_due"]:
            day, touch_date = row["next_due"]
            print(f"    next touch: +{day}d on {touch_date}")
    print("\n  Template (copy/paste — you send, not this script):")
    print('    "Hi {{client}} — checking in on invoice {{invoice_id}} (${{balance}}). Let me know if you need anything from my side."')
    print("  Guide: payment-follow-up-guide.md · agentchip/11n6 buyer channel clone")


STALE_OPEN_DAYS = 90


def load_inventory(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sku = row.get("sku", "").strip()
            if not sku:
                continue
            try:
                unit_cost = float(row.get("unit_cost", "0") or 0)
                unit_price = float(row.get("unit_price", "0") or 0)
                reorder = int(float(row.get("reorder_point", "0") or 0))
            except ValueError:
                continue
            rows.append({
                "sku": sku,
                "name": row.get("name", "").strip(),
                "category": row.get("category", "").strip(),
                "unit_cost": unit_cost,
                "unit_price": unit_price,
                "reorder_point": reorder,
            })
    return rows


def load_stock_log(path):
    by_sku = defaultdict(float)
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            sku = row.get("sku", "").strip()
            if not sku:
                continue
            try:
                qty = float(row.get("qty", "0") or 0)
            except ValueError:
                continue
            by_sku[sku] += qty
    return by_sku


def _trial_status(trial_end, cancel_by, converted, today):
    """agentchip/4hc1: trial stack audit — cancel before auto-convert."""
    if converted:
        return "CONVERTED"
    if trial_end and today > trial_end:
        return "EXPIRED"
    if cancel_by and today >= cancel_by:
        return "CANCEL NOW"
    if trial_end:
        days_left = (trial_end - today).days
        if 0 <= days_left <= 7:
            return "CONVERTING SOON"
    return "ACTIVE TRIAL"


def summarize_trial_stack(path):
    """agentchip/4hc1 adapted: freelance SaaS trial stack — track cancel-by before auto-convert."""
    rows = []
    today = date.today()
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            trial_end = _parse_iso_date(row.get("trial_end", ""))
            cancel_by = _parse_iso_date(row.get("cancel_by", ""))
            converted = (row.get("converted") or "").strip().lower() in ("yes", "true", "1", "y")
            try:
                post_trial = float(row.get("post_trial_monthly", row.get("monthly_usd", 0)))
            except (KeyError, ValueError):
                post_trial = 0.0
            status = (row.get("status") or "").strip() or _trial_status(
                trial_end, cancel_by, converted, today
            )
            rows.append({
                "trial_id": row.get("trial_id", "").strip(),
                "tool": row.get("tool", row.get("vendor", "")).strip(),
                "trial_end": trial_end,
                "cancel_by": cancel_by,
                "post_trial": post_trial,
                "status": status,
            })
    if not rows:
        return
    active = [r for r in rows if r["status"] not in ("CONVERTED", "EXPIRED")]
    stack_load = sum(r["post_trial"] for r in active)
    urgent = [r for r in rows if r["status"] in ("CANCEL NOW", "CONVERTING SOON")]
    print("\n=== FREELANCE TRIAL STACK AUDIT (agentchip/4hc1 shape) ===")
    print("  Track cancel-by before trial_end — one-time reminders miss auto-converts.")
    print(f"  Trials tracked: {len(rows)} · active: {len(active)} · stack load if all convert: ${stack_load:,.2f}/mo")
    print("  trial_id   tool            trial_end   cancel_by   post_trial  status")
    for r in rows:
        end = r["trial_end"].isoformat() if r["trial_end"] else "—"
        cancel = r["cancel_by"].isoformat() if r["cancel_by"] else "—"
        print(
            f"  {r['trial_id'] or '—':10} {r['tool'][:14]:14} "
            f"{end:10}  {cancel:10}  ${r['post_trial']:>6.2f}  {r['status']}"
        )
    if urgent:
        at_risk = sum(r["post_trial"] for r in urgent)
        print(f"  Action needed: {len(urgent)} trial(s) in cancel/convert window · ${at_risk:,.2f}/mo at risk")
    print("  Guide: trial-abuse-guide.md · trials-sample.csv · agentchip/4hc1 buyer channel clone")


def summarize_inventory(inventory_path, stock_log_path):
    """agentchip/5fca: derived stock levels, LOW alerts, movement-log audit trail."""
    inventory = load_inventory(inventory_path)
    stock = load_stock_log(stock_log_path)
    print("\n=== DELIVERABLE INVENTORY TRACKER (agentchip/5fca shape) ===")
    print("  Stock derived from movement log — never typed by hand (SUMIF shape).")
    print("  LOW = current stock ≤ reorder point (conditional-format red-row clone).")
    if not inventory:
        print("  No SKU rows — inventory idle.")
        return

    total_units = 0.0
    value_cost = 0.0
    value_price = 0.0
    low_count = 0
    for item in inventory:
        sku = item["sku"]
        current = stock.get(sku, 0.0)
        reorder = item["reorder_point"]
        status = "LOW" if current <= reorder else "OK"
        if status == "LOW":
            low_count += 1
        total_units += max(current, 0.0)
        value_cost += max(current, 0.0) * item["unit_cost"]
        value_price += max(current, 0.0) * item["unit_price"]
        print(
            f"  {sku} · {item['name']} · stock {current:g} · reorder {reorder} · "
            f"{status} · cost ${item['unit_cost']:,.2f} · price ${item['unit_price']:,.2f}"
        )

    print(f"\n  Dashboard: {len(inventory)} SKUs · {total_units:g} units on hand")
    print(f"  Stock value at cost: ${value_cost:,.2f} · potential revenue: ${value_price:,.2f}")
    print(f"  LOW stock lines: {low_count} (reorder today)")
    print("  Guide: inventory-tracker-guide.md · inventory-sample.csv · stock-log-sample.csv")


def summarize_payout_settlement(clients_path, invoices_path, payments_path, stale_days=STALE_OPEN_DAYS):
    """agentchip/52c0: per-client settlement rollup + stale open invoice flags."""
    clients = load_clients(clients_path)
    invoices = load_invoices(invoices_path)
    payments = load_payments(payments_path)
    today = date.today()
    by_client = defaultdict(lambda: {"invoiced": 0.0, "received": 0.0, "open": [], "stale": []})

    for inv in invoices:
        client = inv["client"]
        paid_amt = payments.get(inv["invoice_id"], 0.0)
        balance = max(inv["total"] - paid_amt, 0.0)
        by_client[client]["invoiced"] += inv["total"]
        by_client[client]["received"] += paid_amt
        if balance <= 0:
            continue
        inv_date = inv.get("invoice_date", "").strip()
        days_open = None
        if inv_date:
            try:
                days_open = (today - datetime.strptime(inv_date, "%Y-%m-%d").date()).days
            except ValueError:
                pass
        row = {
            "invoice_id": inv["invoice_id"],
            "balance": balance,
            "status": inv["status"],
            "days_open": days_open,
        }
        by_client[client]["open"].append(row)
        if days_open is not None and days_open >= stale_days:
            by_client[client]["stale"].append(row)

    print("\n=== CLIENT PAYOUT SETTLEMENT (agentchip/52c0 shape) ===")
    print(f"  Per-client rollup — commission math without the afternoon reconciliation.")
    print(f"  Stale open threshold: {stale_days} days (flag before write-off, like consignment 90-day rule).")
    if not by_client:
        print("  No invoice rows — settlement idle.")
        return

    total_owed = 0.0
    stale_count = 0
    for client in sorted(by_client):
        nums = by_client[client]
        owed = nums["invoiced"] - nums["received"]
        total_owed += max(owed, 0.0)
        stale_count += len(nums["stale"])
        terms = clients.get(client, {}).get("payment_terms_days", 30)
        print(f"\n  {client} · terms {terms}d")
        print(f"    Invoiced: ${nums['invoiced']:,.2f} · Received: ${nums['received']:,.2f} · Balance: ${owed:,.2f}")
        if nums["open"]:
            print("    Open invoices:")
            for row in nums["open"]:
                age = f"{row['days_open']}d open" if row["days_open"] is not None else "age unknown"
                flag = " · STALE" if row in nums["stale"] else ""
                print(f"      {row['invoice_id']} · ${row['balance']:,.2f} · {row['status']} · {age}{flag}")
        else:
            print("    Open invoices: none — settled")
        if nums["stale"]:
            print(f"    → {len(nums['stale'])} stale open invoice(s) past {stale_days}d — escalate or write off")

    print(f"\n  Portfolio balance due: ${total_owed:,.2f} · stale open lines: {stale_count}")
    print("  Guide: payout-settlement-guide.md · agentchip/52c0 buyer channel clone")


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
        ("Payment follow-up cadence", "agentchip/11n6", 10),
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
    print("=== FREELANCER INVOICE & CLIENT TRACKER (Productive Club clone) ===")
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
    if len(sys.argv) >= 3 and sys.argv[1] == "--follow-up":
        payments_path = sys.argv[3] if len(sys.argv) >= 4 else None
        summarize_payment_follow_up(sys.argv[2], payments_path)
        return
    if len(sys.argv) >= 5 and sys.argv[1] == "--settlement":
        summarize_payout_settlement(sys.argv[2], sys.argv[3], sys.argv[4])
        return
    if len(sys.argv) >= 4 and sys.argv[1] == "--inventory":
        summarize_inventory(sys.argv[2], sys.argv[3])
        return
    if len(sys.argv) >= 3 and sys.argv[1] == "--trial-audit":
        summarize_trial_stack(sys.argv[2])
        return
    if len(sys.argv) < 4:
        print(
            "Usage: productiveclub_invoice_tracker.py clients.csv invoices.csv payments.csv "
            "[subscriptions.csv] [bills.csv] [debt.csv]\n"
            "       productiveclub_invoice_tracker.py --reconcile dirty-invoices.csv\n"
            "       productiveclub_invoice_tracker.py --follow-up invoices.csv [payments.csv]\n"
            "       productiveclub_invoice_tracker.py --settlement clients.csv invoices.csv payments.csv\n"
            "       productiveclub_invoice_tracker.py --inventory inventory.csv stock-log.csv\n"
            "       productiveclub_invoice_tracker.py --trial-audit trials.csv",
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
