"""Run the smallest end-to-end quant research loop."""

from __future__ import annotations

import argparse
from pathlib import Path

from quant_learning.backtest import Trade, run_long_only_signal_backtest
from quant_learning.data import Bar, group_by_symbol, load_ohlcv_csv
from quant_learning.risk import TradePlan, review_trade_plan
from quant_learning.strategy import moving_average_crossover_signals


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run the teaching quant demo.")
    parser.add_argument(
        "--csv",
        type=Path,
        default=Path(__file__).resolve().parents[2] / "data/samples/ohlcv_demo.csv",
        help="OHLCV CSV path.",
    )
    parser.add_argument("--fast", type=int, default=3, help="Fast moving average window.")
    parser.add_argument("--slow", type=int, default=8, help="Slow moving average window.")
    parser.add_argument("--fee-bps", type=float, default=5.0, help="One-way fee in basis points.")
    args = parser.parse_args(argv)

    bars = load_ohlcv_csv(args.csv)
    grouped = group_by_symbol(bars)
    symbol, symbol_bars = next(iter(grouped.items()))
    signals = moving_average_crossover_signals(
        symbol_bars,
        fast_window=args.fast,
        slow_window=args.slow,
    )
    result = run_long_only_signal_backtest(symbol_bars, signals, fee_bps=args.fee_bps)
    summary = result.summary()

    print(f"symbol: {symbol}")
    print(f"bars: {len(symbol_bars)}")
    print(f"trades: {int(summary['trades'])}")
    print(f"final_equity: {summary['final_equity']:.2f}")
    print(f"total_return: {summary['total_return']:.2%}")
    print(f"max_drawdown: {summary['max_drawdown']:.2%}")
    print(f"sharpe_ratio: {summary['sharpe_ratio']:.2f}")
    print(f"total_fees: {summary['total_fees']:.2f}")

    plan = _first_long_trade_plan(symbol_bars, result.trades)
    risk_review = review_trade_plan(plan)
    print("risk_review_for_first_long_trade:")
    print(f"  entry_price: {plan.entry_price:.2f}")
    print(f"  stop_price: {plan.stop_price:.2f}")
    print(f"  target_price: {plan.target_price:.2f}")
    print(f"  shares: {risk_review['shares']:.0f}")
    print(f"  risk_amount: {risk_review['risk_amount']:.2f}")
    print(f"  reward_risk_ratio: {risk_review['reward_risk_ratio']:.2f}")
    print(f"  passes_minimum_reward_risk: {risk_review['passes_minimum_reward_risk']}")
    return 0


def _first_long_trade_plan(bars: list[Bar], trades: list[Trade]) -> TradePlan:
    first_long_trade = next(
        (trade for trade in trades if trade.to_weight > trade.from_weight),
        None,
    )
    if first_long_trade is None:
        entry_bar = bars[0]
    else:
        entry_bar = next(bar for bar in bars if bar.date == first_long_trade.date)

    entry_price = entry_bar.close
    return TradePlan(
        entry_price=entry_price,
        stop_price=entry_price * 0.95,
        target_price=entry_price * 1.12,
        account_equity=10_000.0,
        risk_fraction=0.01,
    )


if __name__ == "__main__":
    raise SystemExit(main())
