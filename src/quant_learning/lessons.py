"""Runnable lesson drills for beginner quant concepts."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
from pathlib import Path

from quant_learning.data import group_by_symbol, load_ohlcv_csv
from quant_learning.factors import realized_volatility, trailing_momentum
from quant_learning.metrics import max_drawdown, pct_returns
from quant_learning.portfolio import portfolio_return, score_to_topk_equal_weights


@dataclass(frozen=True)
class TradeOutcome:
    gross_pnl: float

    @property
    def won(self) -> bool:
        return self.gross_pnl > 0


def expected_value(
    win_rate: float,
    average_win: float,
    average_loss: float,
    cost_per_trade: float = 0.0,
) -> float:
    """Expected profit per trade.

    `average_loss` should be a positive magnitude. This function subtracts it.
    """

    if not 0 <= win_rate <= 1:
        raise ValueError("win_rate must be in [0, 1]")
    if average_win < 0 or average_loss < 0 or cost_per_trade < 0:
        raise ValueError("win/loss/cost inputs must be non-negative")
    loss_rate = 1.0 - win_rate
    return win_rate * average_win - loss_rate * average_loss - cost_per_trade


def summarize_trades(
    outcomes: list[TradeOutcome],
    cost_per_trade: float = 0.0,
) -> dict[str, float]:
    """Summarize a small list of trade outcomes."""

    if not outcomes:
        raise ValueError("at least one trade outcome is required")
    if cost_per_trade < 0:
        raise ValueError("cost_per_trade cannot be negative")

    wins = [item.gross_pnl for item in outcomes if item.won]
    losses = [-item.gross_pnl for item in outcomes if item.gross_pnl < 0]
    total_cost = len(outcomes) * cost_per_trade
    total_pnl = sum(item.gross_pnl for item in outcomes) - total_cost
    win_rate = len(wins) / len(outcomes)
    average_win = sum(wins) / len(wins) if wins else 0.0
    average_loss = sum(losses) / len(losses) if losses else 0.0

    return {
        "trades": float(len(outcomes)),
        "win_rate": win_rate,
        "average_win": average_win,
        "average_loss": average_loss,
        "cost_per_trade": cost_per_trade,
        "expected_value": expected_value(
            win_rate=win_rate,
            average_win=average_win,
            average_loss=average_loss,
            cost_per_trade=cost_per_trade,
        ),
        "total_pnl": total_pnl,
    }


def buy_and_hold_equity(prices: list[float], initial_cash: float = 10_000.0) -> list[float]:
    """Return buy-and-hold equity for a price series."""

    if not prices:
        raise ValueError("prices cannot be empty")
    if prices[0] <= 0:
        raise ValueError("first price must be positive")
    shares = initial_cash / prices[0]
    return [shares * price for price in prices]


def lesson00() -> None:
    """Print the expected-value lesson."""

    high_win_rate_trades = [TradeOutcome(100.0)] * 8 + [TradeOutcome(-600.0)] * 2
    low_win_rate_trades = [TradeOutcome(500.0)] * 4 + [TradeOutcome(-150.0)] * 6

    print("lesson00: expected value beats win rate")
    print("")
    _print_summary("high_win_rate_but_bad", summarize_trades(high_win_rate_trades, 10.0))
    print("")
    _print_summary("low_win_rate_but_good", summarize_trades(low_win_rate_trades, 10.0))
    print("")
    print("read this as: high win rate can still lose money when average losses are too large.")


def lesson01() -> None:
    """Print the return/drawdown lesson."""

    csv_path = Path(__file__).resolve().parents[2] / "data/samples/ohlcv_demo.csv"
    bars = group_by_symbol(load_ohlcv_csv(csv_path))["DEMO"]
    prices = [bar.close for bar in bars[:6]]
    returns = pct_returns(prices)
    equity = buy_and_hold_equity(prices)

    print("lesson01: returns, equity, drawdown")
    print("")
    print(f"prices: {[round(item, 2) for item in prices]}")
    print(f"returns: {[f'{item:.2%}' for item in returns]}")
    print(f"equity: {[round(item, 2) for item in equity]}")
    print(f"total_return: {prices[-1] / prices[0] - 1:.2%}")
    print(f"max_drawdown: {max_drawdown(equity):.2%}")
    print("")
    print("read this as: price movement becomes account movement only after position sizing.")


def lesson05() -> None:
    """Print a factor scoring lesson."""

    csv_path = Path(__file__).resolve().parents[2] / "data/samples/ohlcv_demo.csv"
    bars = group_by_symbol(load_ohlcv_csv(csv_path))["DEMO"]
    prices = [bar.close for bar in bars[:10]]
    momentum = trailing_momentum(prices, lookback=5)
    volatility = realized_volatility(prices, lookback=5)

    print("lesson05: factor values are scores, not trades")
    print("")
    print(f"prices: {[round(item, 2) for item in prices]}")
    print(f"5_day_momentum: {_format_optional_series(momentum)}")
    print(f"5_return_realized_volatility: {_format_optional_series(volatility)}")
    print("")
    print("read this as: a factor must still pass grouping, turnover, cost, and risk tests.")


def lesson06() -> None:
    """Print a score-to-portfolio lesson."""

    scores = {"AAA": 0.9, "BBB": 0.2, "CCC": 0.9, "DDD": -0.1}
    next_returns = {"AAA": 0.02, "BBB": -0.01, "CCC": 0.005, "DDD": 0.03}
    weights = score_to_topk_equal_weights(scores, top_k=2)
    one_period_return = portfolio_return(weights, next_returns)

    print("lesson06: scores become weights before they become returns")
    print("")
    print(f"scores: {scores}")
    print(f"top2_equal_weights: {weights}")
    print(f"next_returns: {next_returns}")
    print(f"portfolio_return: {one_period_return:.2%}")
    print("")
    print("read this as: model/factor scores are not trades until position rules define weights.")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description="Run beginner quant lesson drills.")
    parser.add_argument("lesson", choices=["00", "01", "05", "06"], help="Lesson number to run.")
    args = parser.parse_args(argv)

    if args.lesson == "00":
        lesson00()
    elif args.lesson == "01":
        lesson01()
    elif args.lesson == "05":
        lesson05()
    elif args.lesson == "06":
        lesson06()
    return 0


def _print_summary(name: str, summary: dict[str, float]) -> None:
    print(name)
    print(f"  trades: {summary['trades']:.0f}")
    print(f"  win_rate: {summary['win_rate']:.2%}")
    print(f"  average_win: {summary['average_win']:.2f}")
    print(f"  average_loss: {summary['average_loss']:.2f}")
    print(f"  cost_per_trade: {summary['cost_per_trade']:.2f}")
    print(f"  expected_value: {summary['expected_value']:.2f}")
    print(f"  total_pnl: {summary['total_pnl']:.2f}")


def _format_optional_series(values: list[float | None]) -> list[str]:
    return ["None" if item is None else f"{item:.4f}" for item in values]


if __name__ == "__main__":
    raise SystemExit(main())
