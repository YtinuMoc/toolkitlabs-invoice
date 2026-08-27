#!/usr/bin/env python3
"""Etsy Shop Profit + Fees Tracker — clone of PattyBun ejmzqy ($12.99 Gumroad)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime

# Settings tab defaults (PattyBun Settings shape)
LISTING_FEE = 0.20
TRANSACTION_PCT = 0.065
PROCESSING_PCT = 0.03
PROCESSING_FLAT = 0.25
OFFSITE_ADS_PCT = 0.15
OFFSITE_ADS_HV_PCT = 0.12

GOAL_REVENUE = 5000.0
GOAL_PROFIT = 3500.0


def calc_fees(gross, qty, offsite, high_volume):
    listing = LISTING_FEE * qty
    transaction = gross * TRANSACTION_PCT
    processing = gross * PROCESSING_PCT + PROCESSING_FLAT
    offsite_fee = 0.0
    if offsite:
        rate = OFFSITE_ADS_HV_PCT if high_volume else OFFSITE_ADS_PCT
        offsite_fee = gross * rate
    total = listing + transaction + processing + offsite_fee
    return {
        "listing": round(listing, 2),
        "transaction": round(transaction, 2),
        "processing": round(processing, 2),
        "offsite": round(offsite_fee, 2),
        "total": round(total, 2),
        "net": round(gross - total, 2),
    }


def load_sales(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                price = float(row["sale_price"])
                qty = int(float(row.get("quantity", "1") or "1"))
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            gross = price * qty
            offsite = row.get("offsite_ad", "").strip().lower() in ("yes", "true", "1", "y")
            hv = row.get("high_volume_shop", "").strip().lower() in ("yes", "true", "1", "y")
            fees = calc_fees(gross, qty, offsite, hv)
            rows.append({
                "date": dt,
                "listing": row.get("listing", "unknown").strip() or "unknown",
                "gross": gross,
                "qty": qty,
                "offsite": offsite,
                **fees,
            })
    return rows


def print_dashboard(rows):
    gross = sum(r["gross"] for r in rows)
    fees = sum(r["total"] for r in rows)
    net = sum(r["net"] for r in rows)
    margin = (net / gross * 100) if gross else 0.0
    print("\n=== DASHBOARD (PattyBun ejmzqy clone) ===")
    print(f"  Sales logged:   {len(rows)}")
    print(f"  Total revenue:  ${gross:,.2f}")
    print(f"  Total fees:     ${fees:,.2f}")
    print(f"  Net profit:     ${net:,.2f}")
    print(f"  Margin:         {margin:.1f}%")


def print_monthly_summary(rows):
    monthly = defaultdict(lambda: {"gross": 0.0, "fees": 0.0, "net": 0.0, "count": 0})
    for r in rows:
        mk = r["date"].strftime("%Y-%m")
        m = monthly[mk]
        m["gross"] += r["gross"]
        m["fees"] += r["total"]
        m["net"] += r["net"]
        m["count"] += 1
    print("\n=== MONTHLY SUMMARY (PattyBun tab 3 — 24 months) ===")
    for mk in sorted(monthly)[-24:]:
        m = monthly[mk]
        margin = (m["net"] / m["gross"] * 100) if m["gross"] else 0.0
        print(
            f"  {mk}  sales {m['count']:3d}  gross ${m['gross']:8,.2f}  "
            f"fees ${m['fees']:7,.2f}  net ${m['net']:8,.2f}  margin {margin:5.1f}%"
        )


def print_listing_performance(rows):
    perf = defaultdict(lambda: {"units": 0, "gross": 0.0, "fees": 0.0, "net": 0.0})
    for r in rows:
        p = perf[r["listing"]]
        p["units"] += r["qty"]
        p["gross"] += r["gross"]
        p["fees"] += r["total"]
        p["net"] += r["net"]
    ranked = sorted(perf, key=lambda k: perf[k]["net"], reverse=True)
    print("\n=== LISTING PERFORMANCE (PattyBun tab 4) ===")
    for rank, listing in enumerate(ranked, 1):
        p = perf[listing]
        margin = (p["net"] / p["gross"] * 100) if p["gross"] else 0.0
        print(
            f"  #{rank} {listing:24s}  units {p['units']:3d}  gross ${p['gross']:8,.2f}  "
            f"fees ${p['fees']:7,.2f}  net ${p['net']:8,.2f}  margin {margin:5.1f}%"
        )


def print_fee_calculator(price, qty=1, offsite=False, high_volume=False):
    gross = price * qty
    f = calc_fees(gross, qty, offsite, high_volume)
    print("\n=== FEE CALCULATOR (PattyBun tab 5 — what-if) ===")
    print(f"  Sale price ${price:.2f} × qty {qty} = gross ${gross:.2f}")
    print(f"  Listing fee:      ${f['listing']:.2f}")
    print(f"  Transaction (6.5%): ${f['transaction']:.2f}")
    print(f"  Processing (3%+$0.25): ${f['processing']:.2f}")
    print(f"  Offsite ads:      ${f['offsite']:.2f}")
    print(f"  Total fees:       ${f['total']:.2f}")
    print(f"  NET PROFIT:       ${f['net']:.2f}")
    margin = (f["net"] / gross * 100) if gross else 0.0
    print(f"  Margin:           {margin:.1f}%")


def print_goals(rows):
    gross = sum(r["gross"] for r in rows)
    net = sum(r["net"] for r in rows)
    rev_pct = (gross / GOAL_REVENUE * 100) if GOAL_REVENUE else 0.0
    profit_pct = (net / GOAL_PROFIT * 100) if GOAL_PROFIT else 0.0
    rev_status = "✓ hit" if gross >= GOAL_REVENUE else f"{rev_pct:.0f}% of target"
    profit_status = "✓ hit" if net >= GOAL_PROFIT else f"{profit_pct:.0f}% of target"
    print("\n=== GOALS (PattyBun tab 6) ===")
    print(f"  Revenue target ${GOAL_REVENUE:,.0f}  actual ${gross:,.2f}  {rev_status}")
    print(f"  Profit target  ${GOAL_PROFIT:,.0f}  actual ${net:,.2f}  {profit_status}")


def print_sales_log(rows):
    print("\n=== SALES LOG (PattyBun tab 1 — per-row fee breakdown) ===")
    print("  date        listing                  gross    list   txn   proc  offsite  fees    net")
    for r in sorted(rows, key=lambda x: x["date"]):
        print(
            f"  {r['date'].strftime('%Y-%m-%d')}  {r['listing'][:22]:22s}  "
            f"${r['gross']:6.2f}  ${r['listing']:4.2f}  ${r['transaction']:5.2f}  "
            f"${r['processing']:5.2f}  ${r['offsite']:6.2f}  ${r['total']:5.2f}  ${r['net']:6.2f}"
        )


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "sales-sample.csv"
    rows = load_sales(path)
    if not rows:
        print("No rows loaded.", file=sys.stderr)
        sys.exit(1)
    print(f"Loaded {len(rows)} sales from {path}")
    print(f"Settings: listing ${LISTING_FEE} · txn {TRANSACTION_PCT*100:.1f}% · "
          f"proc {PROCESSING_PCT*100:.0f}%+${PROCESSING_FLAT} · offsite {OFFSITE_ADS_PCT*100:.0f}%/{OFFSITE_ADS_HV_PCT*100:.0f}%")
    print_sales_log(rows)
    print_dashboard(rows)
    print_monthly_summary(rows)
    print_listing_performance(rows)
    print_fee_calculator(24.99, qty=1, offsite=True, high_volume=False)
    print_goals(rows)
    print("\nClone target: pattybun.gumroad.com/l/ejmzqy ($12.99)")


if __name__ == "__main__":
    main()
