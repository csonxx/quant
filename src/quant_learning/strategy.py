"""Toy strategies used to teach signal discipline."""

from __future__ import annotations

from dataclasses import dataclass
from datetime import date

from quant_learning.data import Bar, closes


@dataclass(frozen=True)
class Signal:
    """Target weight produced at the end of `date`.

    A backtest should apply this no earlier than the next bar, otherwise it is
    silently stealing information from the close.
    """

    date: date
    symbol: str
    target_weight: float
    reason: str


def simple_moving_average(values: list[float], window: int) -> list[float | None]:
    """Return a rolling simple moving average with None before the window is full."""

    if window <= 0:
        raise ValueError("window must be positive")

    averages: list[float | None] = []
    rolling_sum = 0.0
    for index, value in enumerate(values):
        rolling_sum += value
        if index >= window:
            rolling_sum -= values[index - window]
        if index + 1 < window:
            averages.append(None)
        else:
            averages.append(rolling_sum / window)
    return averages


def moving_average_crossover_signals(
    bars: list[Bar],
    fast_window: int = 5,
    slow_window: int = 20,
) -> list[Signal]:
    """Generate long-only target weights from a moving-average crossover."""

    if fast_window >= slow_window:
        raise ValueError("fast_window must be smaller than slow_window")
    if not bars:
        return []

    symbol = bars[0].symbol
    if any(bar.symbol != symbol for bar in bars):
        raise ValueError("moving_average_crossover_signals expects one symbol at a time")

    price = closes(bars)
    fast = simple_moving_average(price, fast_window)
    slow = simple_moving_average(price, slow_window)

    signals: list[Signal] = []
    for bar, fast_value, slow_value in zip(bars, fast, slow, strict=True):
        if fast_value is None or slow_value is None:
            signals.append(Signal(bar.date, bar.symbol, 0.0, "warming_up"))
        elif fast_value > slow_value:
            signals.append(Signal(bar.date, bar.symbol, 1.0, "fast_ma_above_slow_ma"))
        else:
            signals.append(Signal(bar.date, bar.symbol, 0.0, "fast_ma_not_above_slow_ma"))
    return signals
