#!/usr/bin/env python3
"""Trading Journal Tracker — clone of jordisquare.gumroad.com/l/tradingjournal ($48)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime

DEFAULT_CAPITAL = 10000.0


def load_trades(path):
    rows = []
    with open(path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            try:
                entry = float(row.get("entry_price") or row.get("entry", 0))
                exit_p = float(row.get("exit_price") or row.get("exit", 0))
                size = float(row.get("position_size") or row.get("size", 1))
                direction = row.get("direction", "long").strip().lower()
                mult = -1 if direction in ("short", "sell", "s") else 1
                if row.get("pnl", "").strip():
                    pnl = float(row["pnl"])
                else:
                    pnl = round((exit_p - entry) * size * mult, 2)
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
            except (KeyError, ValueError):
                continue
            rows.append({
                "date": dt,
                "market": row.get("market", row.get("symbol", "")).strip(),
                "setup": row.get("setup", row.get("strategy", "default")).strip(),
                "direction": direction,
                "entry": entry,
                "exit": exit_p,
                "size": size,
                "pnl": pnl,
                "reflection": row.get("reflection", "").strip(),
            })
    return sorted(rows, key=lambda r: r["date"])


def equity_curve(trades, capital=DEFAULT_CAPITAL):
    equity = capital
    peak = equity
    max_dd = 0.0
    for t in trades:
        equity += t["pnl"]
        peak = max(peak, equity)
        dd = (peak - equity) / peak * 100 if peak else 0
        max_dd = max(max_dd, dd)
    return max_dd, equity


def calendar_summary(trades):
    by_day = defaultdict(lambda: {"trades": 0, "pnl": 0.0, "wins": 0})
    for t in trades:
        key = t["date"].strftime("%Y-%m-%d")
        by_day[key]["trades"] += 1
        by_day[key]["pnl"] += t["pnl"]
        if t["pnl"] > 0:
            by_day[key]["wins"] += 1
    return dict(sorted(by_day.items()))


def period_summary(trades, fmt):
    buckets = defaultdict(lambda: {"trades": 0, "pnl": 0.0, "wins": 0})
    for t in trades:
        key = t["date"].strftime(fmt)
        buckets[key]["trades"] += 1
        buckets[key]["pnl"] += t["pnl"]
        if t["pnl"] > 0:
            buckets[key]["wins"] += 1
    return dict(sorted(buckets.items()))


def summarize(trades, capital=DEFAULT_CAPITAL):
    if not trades:
        return None
    wins = [t for t in trades if t["pnl"] > 0]
    losses = [t for t in trades if t["pnl"] < 0]
    total_pnl = sum(t["pnl"] for t in trades)
    gross_win = sum(t["pnl"] for t in wins)
    gross_loss = abs(sum(t["pnl"] for t in losses))
    pf = gross_win / gross_loss if gross_loss else float("inf")
    max_dd, final_eq = equity_curve(trades, capital)
    by_market = defaultdict(lambda: {"trades": 0, "pnl": 0.0})
    for t in trades:
        by_market[t["market"]]["trades"] += 1
        by_market[t["market"]]["pnl"] += t["pnl"]
    return {
        "trades": len(trades),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": len(wins) / len(trades) * 100,
        "total_pnl": total_pnl,
        "profit_factor": pf,
        "max_drawdown": max_dd,
        "return_pct": total_pnl / capital * 100,
        "final_equity": final_eq,
        "by_market": dict(by_market),
    }


def print_report(trades, capital=DEFAULT_CAPITAL):
    s = summarize(trades, capital)
    if not s:
        print("No valid trades found.")
        return
    print("=== TRADING JOURNAL TRACKER (jordisquare tradingjournal clone) ===")
    print(f"  Trades:              {s['trades']}")
    print(f"  Wins / Losses:       {s['wins']} / {s['losses']}")
    print(f"  Win rate:            {s['win_rate']:.1f}%")
    print(f"  Total P&L:           ${s['total_pnl']:,.2f}")
    print(f"  Profit factor:       {s['profit_factor']:.2f}")
    print(f"  Max drawdown:        {s['max_drawdown']:.1f}%")
    print(f"  Return:              {s['return_pct']:.1f}%")
    print(f"  Final equity:        ${s['final_equity']:,.2f}")
    print()
    print("--- Calendar (daily P&L) ---")
    for day, d in calendar_summary(trades).items():
        wr = d["wins"] / d["trades"] * 100 if d["trades"] else 0
        print(f"  {day}: {d['trades']} trades · ${d['pnl']:,.2f} · {wr:.0f}% wins")
    print()
    print("--- Monthly ---")
    for period, d in period_summary(trades, "%Y-%m").items():
        print(f"  {period}: {d['trades']} trades · ${d['pnl']:,.2f}")
    print()
    print("--- By market ---")
    for market, d in sorted(s["by_market"].items(), key=lambda x: -x[1]["pnl"]):
        if market:
            print(f"  {market}: {d['trades']} trades · ${d['pnl']:,.2f}")
    reflections = [t for t in trades if t["reflection"]]
    if reflections:
        print()
        print("--- Journal reflections ---")
        for t in reflections[-3:]:
            print(f"  {t['date'].strftime('%Y-%m-%d')} ({t['market']}): {t['reflection'][:80]}")


def main():
    if len(sys.argv) < 2:
        print("Usage: trading_journal_tracker.py trades.csv [--capital 10000]")
        sys.exit(1)
    path = sys.argv[1]
    capital = DEFAULT_CAPITAL
    if "--capital" in sys.argv:
        idx = sys.argv.index("--capital")
        capital = float(sys.argv[idx + 1])
    trades = load_trades(path)
    print_report(trades, capital)


if __name__ == "__main__":
    main()
