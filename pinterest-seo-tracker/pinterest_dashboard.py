#!/usr/bin/env python3
"""Pinterest SEO & Pin Performance Dashboard — clone of AnahitDigitalStudio batvmj ($8.99 Gumroad)."""
import csv
import sys
from collections import defaultdict


def rate(num, denom):
    return (num / denom * 100) if denom else 0.0


def rating(pin_click_rate, outbound_rate, save_rate):
  """Performance rating like Anahit batvmj dashboard."""
  score = pin_click_rate * 0.3 + outbound_rate * 0.5 + save_rate * 0.2
  if score >= 3.0:
    return "Excellent"
  if score >= 1.5:
    return "Good"
  if score >= 0.5:
    return "Average"
  return "Needs work"


def load_csv(path):
    with open(path, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def print_pin_performance(rows):
    total_imp = total_pc = total_ob = total_saves = 0
    ranked = []
    for row in rows:
        try:
            imp = int(float(row["impressions"]))
            pc = int(float(row["pin_clicks"]))
            ob = int(float(row["outbound_clicks"]))
            saves = int(float(row["saves"]))
        except (KeyError, ValueError):
            continue
        pcr = rate(pc, imp)
        obr = rate(ob, imp)
        svr = rate(saves, imp)
        ranked.append({
            "title": row.get("pin_title", "pin").strip(),
            "board": row.get("board", "").strip(),
            "impressions": imp,
            "pin_clicks": pc,
            "outbound_clicks": ob,
            "saves": saves,
            "pin_click_rate": pcr,
            "outbound_rate": obr,
            "save_rate": svr,
            "rating": rating(pcr, obr, svr),
        })
        total_imp += imp
        total_pc += pc
        total_ob += ob
        total_saves += saves
    print("\n=== PIN PERFORMANCE TRACKER (AnahitDigitalStudio batvmj clone) ===")
    print(f"  Pins logged:         {len(ranked)}")
    print(f"  Total impressions:   {total_imp:,}")
    print(f"  Outbound clicks:     {total_ob:,}")
    print(f"  Pin click rate:      {rate(total_pc, total_imp):.2f}%")
    print(f"  Outbound click rate: {rate(total_ob, total_imp):.2f}%")
    print(f"  Save rate:           {rate(total_saves, total_imp):.2f}%")
    print("\n=== TOP PERFORMING PINS (by outbound clicks) ===")
    for i, p in enumerate(sorted(ranked, key=lambda x: x["outbound_clicks"], reverse=True)[:5], 1):
        print(
            f"  #{i} {p['title'][:40]:40s}  ob {p['outbound_clicks']:4d}  "
            f"ob rate {p['outbound_rate']:4.2f}%  rating {p['rating']}"
        )


def print_board_planner(rows):
    print("\n=== PINTEREST BOARD PLANNER ===")
    for row in rows:
        name = row.get("board_name", "").strip()
        if not name:
            continue
        views = int(float(row.get("monthly_views") or 0))
        pins = int(float(row.get("pin_count") or 0))
        kw = row.get("keyword", "").strip()
        print(f"  {name:28s}  pins {pins:3d}  views {views:6,}  kw: {kw}")


def print_ab_tests(rows):
    print("\n=== PIN A/B TEST TRACKER ===")
    for row in rows:
        name = row.get("test_name", "test").strip()
        try:
            ia = int(float(row["impressions_a"]))
            ib = int(float(row["impressions_b"]))
            oa = int(float(row["outbound_a"]))
            ob = int(float(row["outbound_b"]))
        except (KeyError, ValueError):
            continue
        ra = rate(oa, ia)
        rb = rate(ob, ib)
        winner = row.get("winner", "").strip()
        if not winner:
            winner = "A" if ra > rb else ("B" if rb > ra else "tie")
        print(
            f"  {name:30s}  A ob rate {ra:4.2f}%  B ob rate {rb:4.2f}%  "
            f"winner: Pin {winner}"
        )


def print_monthly(rows):
    print("\n=== MONTHLY PINTEREST ANALYTICS ===")
    for row in rows:
        month = row.get("month", "").strip()
        if not month:
            continue
        try:
            imp = int(float(row["impressions"]))
            ob = int(float(row["outbound_clicks"]))
            saves = int(float(row["saves"]))
            goal = int(float(row.get("goal_clicks") or 0))
        except (KeyError, ValueError):
            continue
        pct = (ob / goal * 100) if goal else 0
        kw = row.get("best_keyword", "").strip()
        print(
            f"  {month}  imp {imp:6,}  outbound {ob:4d}  saves {saves:4d}  "
            f"goal {goal:3d} ({pct:5.1f}%)  best: {kw}"
        )


def print_keywords(rows):
    print("\n=== KEYWORD RESEARCH ===")
    active = [r for r in rows if r.get("status", "").strip().lower() in ("active", "testing")]
    for row in sorted(active, key=lambda r: int(float(r.get("search_volume") or 0)), reverse=True):
        kw = row.get("keyword", "").strip()
        vol = int(float(row.get("search_volume") or 0))
        comp = row.get("competition", "").strip()
        board = row.get("board", "").strip()
        print(f"  {kw:32s}  vol {vol:6,}  {comp:8s}  board: {board}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 pinterest_dashboard.py pin-performance.csv [board-planner.csv] [ab-test.csv] [monthly.csv] [keywords.csv]")
        print("Clone target: anahitstudio.gumroad.com/l/batvmj ($8.99)")
        sys.exit(1)
    pins = load_csv(sys.argv[1])
    print_pin_performance(pins)
    if len(sys.argv) > 2:
        print_board_planner(load_csv(sys.argv[2]))
    if len(sys.argv) > 3:
        print_ab_tests(load_csv(sys.argv[3]))
    if len(sys.argv) > 4:
        print_monthly(load_csv(sys.argv[4]))
    if len(sys.argv) > 5:
        print_keywords(load_csv(sys.argv[5]))
    print("\nClone target: anahitstudio.gumroad.com/l/batvmj ($8.99)")


if __name__ == "__main__":
    main()
