#!/usr/bin/env python3
"""Profit After Fees — clone of sundayscope.gumroad.com/l/jmqyil ($27)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime

LISTING_FEE = 0.20
TRANSACTION_PCT = 0.065
PROCESSING_PCT = 0.03
PROCESSING_FLAT = 0.25
OFFSITE_ADS_PCT = 0.15
OFFSITE_ADS_HV_PCT = 0.12
DEFAULT_TAX_SET_ASIDE_PCT = 0.28


def calc_etsy_fees(gross, qty, offsite=False, high_volume=False):
    listing = LISTING_FEE * qty
    transaction = gross * TRANSACTION_PCT
    processing = gross * PROCESSING_PCT + PROCESSING_FLAT
    offsite_fee = 0.0
    if offsite:
        rate = OFFSITE_ADS_HV_PCT if high_volume else OFFSITE_ADS_PCT
        offsite_fee = gross * rate
    total = listing + transaction + processing + offsite_fee
    return {
        "listing_fee": round(listing, 2),
        "transaction_fee": round(transaction, 2),
        "processing_fee": round(processing, 2),
        "offsite_fee": round(offsite_fee, 2),
        "total_fees": round(total, 2),
        "net": round(gross - total, 2),
    }


def load_sales(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                gross = float(row.get("gross") or row.get("sale_price", 0))
                qty = int(float(row.get("quantity", "1") or "1"))
                if "sale_price" in row and "gross" not in row:
                    gross = float(row["sale_price"]) * qty
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            offsite = row.get("offsite_ad", "").strip().lower() in ("yes", "true", "1", "y")
            hv = row.get("high_volume_shop", "").strip().lower() in ("yes", "true", "1", "y")
            fees = calc_etsy_fees(gross, qty, offsite, hv)
            rows.append({
                "date": dt,
                "product": row.get("product", row.get("listing", "product")).strip(),
                "gross": gross,
                "qty": qty,
                **fees,
            })
    return rows


def load_expenses(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                amt = float(row["amount"])
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            rows.append({
                "date": dt,
                "category": row.get("category", "other").strip().lower(),
                "amount": amt,
            })
    return rows


def load_ads(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                spend = float(row["ad_spend"])
                attributed = float(row.get("attributed_revenue", 0) or 0)
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            rows.append({
                "date": dt,
                "listing": row.get("listing", "unknown").strip(),
                "ad_spend": spend,
                "attributed_revenue": attributed,
            })
    return rows


def print_profit_after_fees(sales, expenses):
    gross = sum(r["gross"] for r in sales)
    fees = sum(r["total_fees"] for r in sales)
    net_after_fees = sum(r["net"] for r in sales)
    expense_total = sum(r["amount"] for r in expenses)
    real_profit = net_after_fees - expense_total
    margin = (real_profit / gross * 100) if gross else 0.0
    print("\n=== PROFIT AFTER FEES (sundayscope jmqyil clone) ===")
    print(f"  Gross sales:         ${gross:,.2f}")
    print(f"  Etsy fees:           ${fees:,.2f}")
    print(f"  Net after fees:      ${net_after_fees:,.2f}")
    print(f"  Expenses:            ${expense_total:,.2f}")
    print(f"  Real profit:         ${real_profit:,.2f}")
    print(f"  Margin:              {margin:.1f}%")


def print_tax_set_aside(net_profit, rate=DEFAULT_TAX_SET_ASIDE_PCT):
    set_aside = net_profit * rate
    print("\n=== TAX SET-ASIDE ESTIMATOR (sundayscope tab) ===")
    print(f"  Net profit:          ${net_profit:,.2f}")
    print(f"  Set-aside rate:      {rate*100:.0f}% (planning only — confirm with a pro)")
    print(f"  Park this quarter:   ${set_aside:,.2f}")


def print_pay_yourself(net_profit, tax_set_aside, expenses_total):
    safe = net_profit - tax_set_aside
    print("\n=== PAY YOURSELF CALCULATOR (sundayscope tab) ===")
    print(f"  Net profit:          ${net_profit:,.2f}")
    print(f"  Tax set-aside:       ${tax_set_aside:,.2f}")
    print(f"  Safe to spend:       ${safe:,.2f}")


def print_product_profitability(sales):
    perf = defaultdict(lambda: {"units": 0, "gross": 0.0, "fees": 0.0, "net": 0.0})
    for r in sales:
        p = perf[r["product"]]
        p["units"] += r["qty"]
        p["gross"] += r["gross"]
        p["fees"] += r["total_fees"]
        p["net"] += r["net"]
    ranked = sorted(perf, key=lambda k: perf[k]["net"], reverse=True)
    print("\n=== PRODUCT PROFITABILITY (sundayscope tab) ===")
    for rank, product in enumerate(ranked, 1):
        p = perf[product]
        margin = (p["net"] / p["gross"] * 100) if p["gross"] else 0.0
        print(
            f"  #{rank} {product[:28]:28s}  units {p['units']:3d}  "
            f"gross ${p['gross']:7,.2f}  net ${p['net']:7,.2f}  margin {margin:5.1f}%"
        )


def print_monthly_tracker(sales, expenses):
    monthly = defaultdict(lambda: {"gross": 0.0, "fees": 0.0, "net": 0.0, "expenses": 0.0})
    for r in sales:
        mk = r["date"].strftime("%Y-%m")
        m = monthly[mk]
        m["gross"] += r["gross"]
        m["fees"] += r["total_fees"]
        m["net"] += r["net"]
    for r in expenses:
        mk = r["date"].strftime("%Y-%m")
        monthly[mk]["expenses"] += r["amount"]
    print("\n=== FULL-YEAR MONTHLY TRACKER (sundayscope tab) ===")
    for mk in sorted(monthly):
        m = monthly[mk]
        profit = m["net"] - m["expenses"]
        print(
            f"  {mk}  gross ${m['gross']:8,.2f}  fees ${m['fees']:7,.2f}  "
            f"exp ${m['expenses']:6,.2f}  profit ${profit:8,.2f}"
        )


def print_ads_roi(ads_rows, sales):
    spend = sum(r["ad_spend"] for r in ads_rows)
    attributed = sum(r["attributed_revenue"] for r in ads_rows)
    roas = (attributed / spend) if spend else 0.0
    gross = sum(r["gross"] for r in sales)
    fees = sum(r["total_fees"] for r in sales)
    fee_rate = (fees / gross) if gross else 0.0
    net_after_fees = attributed * (1 - fee_rate) if attributed else 0.0
    net_after_ads = net_after_fees - spend
    print("\n=== ADS SPEND & ROI (jartan/207j buyer-channel shape) ===")
    print(f"  Ad spend:            ${spend:,.2f}")
    print(f"  Attributed revenue:  ${attributed:,.2f}")
    print(f"  ROAS (revenue):      {roas:.2f}x  ← Etsy dashboard stops here")
    print(f"  Est. net after fees: ${net_after_fees:,.2f}")
    print(f"  NET PROFIT AFTER ADS:${net_after_ads:,.2f}  ← bank-account number")


def print_ceo_weekly_checkin(sales, expenses):
    gross = sum(r["gross"] for r in sales)
    fees = sum(r["total_fees"] for r in sales)
    net = sum(r["net"] for r in sales) - sum(r["amount"] for r in expenses)
    print("\n=== CEO WEEKLY CHECK-IN (10-minute template) ===")
    print(f"  1. Gross this period:     ${gross:,.2f}")
    print(f"  2. Fees paid to Etsy:     ${fees:,.2f}")
    print(f"  3. Real profit:           ${net:,.2f}")
    print(f"  4. Tax set-aside ({DEFAULT_TAX_SET_ASIDE_PCT*100:.0f}%):  ${net * DEFAULT_TAX_SET_ASIDE_PCT:,.2f}")
    print(f"  5. Decision: scale / hold / cut ads based on NET, not ROAS")


def main():
    sales_path = sys.argv[1] if len(sys.argv) > 1 else "sales-sample.csv"
    expense_path = sys.argv[2] if len(sys.argv) > 2 else "expense-sample.csv"
    ads_path = sys.argv[3] if len(sys.argv) > 3 else "ads-sample.csv"
    sales = load_sales(sales_path)
    expenses = load_expenses(expense_path)
    ads_rows = load_ads(ads_path)
    if not sales:
        print("No sales rows loaded.", file=sys.stderr)
        sys.exit(1)
    print(f"Loaded {len(sales)} sales, {len(expenses)} expenses, {len(ads_rows)} ad rows")
    print_profit_after_fees(sales, expenses)
    net_profit = sum(r["net"] for r in sales) - sum(r["amount"] for r in expenses)
    print_tax_set_aside(net_profit)
    print_pay_yourself(net_profit, net_profit * DEFAULT_TAX_SET_ASIDE_PCT, sum(r["amount"] for r in expenses))
    print_product_profitability(sales)
    print_monthly_tracker(sales, expenses)
    if ads_rows:
        print_ads_roi(ads_rows, sales)
    print_ceo_weekly_checkin(sales, expenses)
    print("\nClone target: sundayscope.gumroad.com/l/jmqyil ($27)")


if __name__ == "__main__":
    main()
