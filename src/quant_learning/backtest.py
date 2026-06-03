"""A tiny, explicit backtester for long-only target-weight signals."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from quant_learning.data import Bar
from quant_learning.metrics import pct_returns, summarize_returns
from quant_learning.strategy import Signal


@dataclass(frozen=True)
class EquityPoint:
    date: date
    equity: float
    position_weight: float
    daily_return: float
    fee_paid: float


@dataclass(frozen=True)
class Trade:
    date: date
    from_weight: float
    to_weight: float
    fee_paid: float
    reason: str


@dataclass(frozen=True)
class BacktestResult:
    symbol: str
    initial_cash: float
    final_equity: float
    equity_curve: list[EquityPoint]
    trades: list[Trade]

    @property
    def returns(self) -> list[float]:
        return pct_returns([point.equity for point in self.equity_curve])

    @property
    def total_fees(self) -> float:
        return sum(point.fee_paid for point in self.equity_curve)

    def summary(self) -> dict[str, float]:
        equity_values = [point.equity for point in self.equity_curve]
        returns = pct_returns(equity_values)
        total_fees = sum(point.fee_paid for point in self.equity_curve)

        metrics = summarize_returns(returns, equity_values)
        metrics["final_equity"] = self.final_equity
        metrics["total_fees"] = total_fees
        metrics["trades"] = float(len(self.trades))
        return metrics


def run_long_only_signal_backtest(
    bars: list[Bar],
    signals: list[Signal],
    initial_cash: float = 10_000.0,
    fee_bps: float = 5.0,
) -> BacktestResult:
    """Run a simple close-to-close backtest.

    Signal timing is deliberately conservative: the signal generated on bar `t-1`
    controls exposure from close `t-1` to close `t`.
    """

    if initial_cash <= 0:
        raise ValueError("initial_cash must be positive")
    if fee_bps < 0:
        raise ValueError("fee_bps cannot be negative")
    if len(bars) < 2:
        raise ValueError("at least two bars are required")

    symbol = bars[0].symbol
    if any(bar.symbol != symbol for bar in bars):
        raise ValueError("backtest expects one symbol at a time")

    signal_by_date = {signal.date: signal for signal in signals}
    equity = initial_cash
    previous_weight = 0.0
    equity_curve = [
        EquityPoint(
            date=bars[0].date,
            equity=initial_cash,
            position_weight=0.0,
            daily_return=0.0,
            fee_paid=0.0,
        )
    ]
    trades: list[Trade] = []

    for previous_bar, current_bar in zip(bars, bars[1:]):
        signal = signal_by_date.get(previous_bar.date)
        target_weight = _clamp_weight(signal.target_weight if signal else 0.0)
        # Teaching assumption: fees are charged on pre-trade equity turnover, then
        # exposure is applied to the remaining equity. This slightly reduces the
        # invested notional after fees and keeps the cash ledger explicit.
        fee_paid = equity * abs(target_weight - previous_weight) * fee_bps / 10_000.0

        if target_weight != previous_weight:
            trades.append(
                Trade(
                    date=previous_bar.date,
                    from_weight=previous_weight,
                    to_weight=target_weight,
                    fee_paid=fee_paid,
                    reason=signal.reason if signal else "missing_signal",
                )
            )

        equity_after_fee = equity - fee_paid
        asset_return = current_bar.close / previous_bar.close - 1.0
        strategy_return = target_weight * asset_return
        equity = equity_after_fee * (1.0 + strategy_return)

        equity_curve.append(
            EquityPoint(
                date=current_bar.date,
                equity=equity,
                position_weight=target_weight,
                daily_return=strategy_return,
                fee_paid=fee_paid,
            )
        )
        previous_weight = target_weight

    return BacktestResult(
        symbol=symbol,
        initial_cash=initial_cash,
        final_equity=equity,
        equity_curve=equity_curve,
        trades=trades,
    )


def _clamp_weight(weight: float) -> float:
    if weight < 0.0 or weight > 1.0:
        raise ValueError("this teaching backtester only supports weights in [0, 1]")
    return weight
