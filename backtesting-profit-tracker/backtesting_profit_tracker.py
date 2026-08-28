#!/usr/bin/env python3
"""Back-testing Profit Tracker — clone of aheadofthetrade.gumroad.com/l/ojdzA ($1.99)."""
import csv
import sys
from collections import defaultdict
from datetime import datetime

DEFAULT_RISK_PCT = 1.0
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
                if "pnl" in row and row["pnl"].strip():
                    pnl = float(row["pnl"])
                else:
                    pnl = round((exit_p - entry) * size * mult, 2)
                dt = datetime.strptime(row["date"].strip(), "%Y-%m-%d")
                risk_pct = float(row.get("risk_pct") or DEFAULT_RISK_PCT)
            except (KeyError, ValueError):
                continue
            rows.append({
                "date": dt,
                "strategy": row.get("strategy", "default").strip(),
                "symbol": row.get("symbol", "").strip(),
                "direction": direction,
                "entry": entry,
                "exit": exit_p,
                "size": size,
                "pnl": pnl,
                "risk_pct": risk_pct,
            })
    return sorted(rows, key=lambda r: r["date"])


def equity_curve(trades, capital=DEFAULT_CAPITAL):
    equity = capital
    curve = [equity]
    peak = equity
    max_dd = 0.0
    for t in trades:
        equity += t["pnl"]
        curve.append(equity)
        peak = max(peak, equity)
        dd = (peak - equity) / peak * 100 if peak else 0
        max_dd = max(max_dd, dd)
    return curve, max_dd, equity


def summarize(trades, capital=DEFAULT_CAPITAL):
    if not trades:
        return None
    wins = [t for t in trades if t["pnl"] > 0]
    losses = [t for t in trades if t["pnl"] < 0]
    total_pnl = sum(t["pnl"] for t in trades)
    gross_win = sum(t["pnl"] for t in wins)
    gross_loss = abs(sum(t["pnl"] for t in losses))
    pf = gross_win / gross_loss if gross_loss else float("inf")
    _, max_dd, final_eq = equity_curve(trades, capital)
    by_strategy = defaultdict(lambda: {"trades": 0, "pnl": 0.0, "wins": 0})
    for t in trades:
        s = by_strategy[t["strategy"]]
        s["trades"] += 1
        s["pnl"] += t["pnl"]
        if t["pnl"] > 0:
            s["wins"] += 1
    return {
        "trades": len(trades),
        "wins": len(wins),
        "losses": len(losses),
        "win_rate": len(wins) / len(trades) * 100,
        "total_pnl": total_pnl,
        "avg_win": gross_win / len(wins) if wins else 0,
        "avg_loss": gross_loss / len(losses) if losses else 0,
        "profit_factor": pf,
        "max_drawdown_pct": max_dd,
        "final_equity": final_eq,
        "return_pct": (final_eq - capital) / capital * 100,
        "by_strategy": dict(by_strategy),
    }


def print_report(trades, capital=DEFAULT_CAPITAL):
    s = summarize(trades, capital)
    if not s:
        print("No valid trades in CSV.")
        return
    print("\n=== BACK-TESTING PROFIT TRACKER (aheadofthetrade ojdzA clone) ===")
    print(f"  Trades:              {s['trades']}")
    print(f"  Wins / Losses:       {s['wins']} / {s['losses']}")
    print(f"  Win rate:            {s['win_rate']:.1f}%")
    print(f"  Total P&L:           ${s['total_pnl']:,.2f}")
    print(f"  Avg win:             ${s['avg_win']:,.2f}")
    print(f"  Avg loss:            ${s['avg_loss']:,.2f}")
    print(f"  Profit factor:       {s['profit_factor']:.2f}")
    print(f"  Max drawdown:        {s['max_drawdown_pct']:.1f}%")
    print(f"  Starting capital:    ${capital:,.2f}")
    print(f"  Final equity:        ${s['final_equity']:,.2f}")
    print(f"  Return:              {s['return_pct']:.1f}%")
    if s["by_strategy"]:
        print("\n  By strategy:")
        for name, data in sorted(s["by_strategy"].items()):
            wr = data["wins"] / data["trades"] * 100 if data["trades"] else 0
            print(f"    {name}: {data['trades']} trades, ${data['pnl']:,.2f} P&L, {wr:.0f}% win rate")
    curve, _, _ = equity_curve(trades, capital)
    print("\n  Equity curve (last 8 points):")
    for eq in curve[-8:]:
        print(f"    ${eq:,.2f}")


def main():
    args = sys.argv[1:]
    if not args or args[0] in ("-h", "--help"):
        print("Usage: backtesting_profit_tracker.py trades.csv [--capital 10000]")
        return
    capital = DEFAULT_CAPITAL
    if "--capital" in args:
        capital = float(args[args.index("--capital") + 1])
    trades = load_trades(args[0])
    print_report(trades, capital)


if __name__ == "__main__":
    main()
