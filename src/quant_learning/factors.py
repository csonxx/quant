"""Small factor helpers before moving to pandas or Qlib."""

from __future__ import annotations

from quant_learning.metrics import pct_returns


def trailing_momentum(prices: list[float], lookback: int) -> list[float | None]:
    """Return lookback return at each point, None before enough history exists."""

    if lookback <= 0:
        raise ValueError("lookback must be positive")

    values: list[float | None] = []
    for index, price in enumerate(prices):
        if index < lookback:
            values.append(None)
        else:
            base = prices[index - lookback]
            if base <= 0:
                raise ValueError("price base must be positive")
            values.append(price / base - 1.0)
    return values


def realized_volatility(prices: list[float], lookback: int) -> list[float | None]:
    """Return rolling standard deviation of simple returns."""

    if lookback <= 1:
        raise ValueError("lookback must be greater than 1")

    returns = pct_returns(prices)
    values: list[float | None] = [None]
    for index in range(len(returns)):
        if index + 1 < lookback:
            values.append(None)
            continue
        window = returns[index + 1 - lookback : index + 1]
        mean = sum(window) / len(window)
        variance = sum((item - mean) ** 2 for item in window) / len(window)
        values.append(variance**0.5)
    return values
