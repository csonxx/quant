"""Performance metrics with explicit assumptions."""

from __future__ import annotations

import math
from statistics import fmean, pstdev


def pct_returns(values: list[float]) -> list[float]:
    """Convert a price or equity series into simple percentage returns."""

    if len(values) < 2:
        return []

    returns: list[float] = []
    for previous, current in zip(values, values[1:]):
        if previous <= 0:
            raise ValueError("return base must be positive")
        returns.append(current / previous - 1.0)
    return returns


def cumulative_return(returns: list[float]) -> float:
    """Compound a return series."""

    wealth = 1.0
    for item in returns:
        wealth *= 1.0 + item
    return wealth - 1.0


def annualized_return(returns: list[float], periods_per_year: int = 252) -> float:
    """Annualize compounded returns using the observed number of periods."""

    if not returns:
        return 0.0

    total = cumulative_return(returns)
    years = len(returns) / periods_per_year
    if years <= 0:
        return 0.0
    return (1.0 + total) ** (1.0 / years) - 1.0


def annualized_volatility(returns: list[float], periods_per_year: int = 252) -> float:
    """Population volatility annualized by sqrt(periods)."""

    if len(returns) < 2:
        return 0.0
    return pstdev(returns) * math.sqrt(periods_per_year)


def sharpe_ratio(
    returns: list[float],
    risk_free_rate: float = 0.0,
    periods_per_year: int = 252,
) -> float:
    """Annualized Sharpe ratio.

    `risk_free_rate` is annualized. For a learning repo this is enough; production
    work should use a dated risk-free curve.
    """

    if len(returns) < 2:
        return 0.0

    period_risk_free = (1.0 + risk_free_rate) ** (1.0 / periods_per_year) - 1.0
    excess = [item - period_risk_free for item in returns]
    vol = pstdev(excess)
    if vol == 0:
        return 0.0
    return fmean(excess) / vol * math.sqrt(periods_per_year)


def max_drawdown(equity_curve: list[float]) -> float:
    """Return the worst peak-to-trough drawdown as a negative number."""

    if not equity_curve:
        return 0.0

    peak = equity_curve[0]
    worst = 0.0
    for equity in equity_curve:
        if equity <= 0:
            raise ValueError("equity must stay positive for drawdown calculation")
        peak = max(peak, equity)
        drawdown = equity / peak - 1.0
        worst = min(worst, drawdown)
    return worst


def summarize_returns(returns: list[float], equity_curve: list[float]) -> dict[str, float]:
    """Return a compact metric dictionary for demos and tests."""

    return {
        "total_return": cumulative_return(returns),
        "annualized_return": annualized_return(returns),
        "annualized_volatility": annualized_volatility(returns),
        "sharpe_ratio": sharpe_ratio(returns),
        "max_drawdown": max_drawdown(equity_curve),
    }
