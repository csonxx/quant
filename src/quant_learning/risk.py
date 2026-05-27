"""Risk helpers for turning opinions into survivable position sizes."""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class TradePlan:
    entry_price: float
    stop_price: float
    target_price: float
    account_equity: float
    risk_fraction: float


def reward_risk_ratio(entry_price: float, stop_price: float, target_price: float) -> float:
    """Return upside divided by downside for a long trade."""

    downside = entry_price - stop_price
    upside = target_price - entry_price
    if downside <= 0:
        raise ValueError("stop_price must be below entry_price for a long trade")
    if upside <= 0:
        raise ValueError("target_price must be above entry_price for a long trade")
    return upside / downside


def fixed_fraction_position_size(
    account_equity: float,
    risk_fraction: float,
    entry_price: float,
    stop_price: float,
) -> int:
    """Size a long position by maximum account loss if the stop is hit."""

    if account_equity <= 0:
        raise ValueError("account_equity must be positive")
    if not 0 < risk_fraction <= 0.05:
        raise ValueError("risk_fraction should be in (0, 0.05] for this learning helper")
    per_share_risk = entry_price - stop_price
    if per_share_risk <= 0:
        raise ValueError("stop_price must be below entry_price")

    risk_budget = account_equity * risk_fraction
    return int(risk_budget // per_share_risk)


def review_trade_plan(plan: TradePlan) -> dict[str, float | bool]:
    """Return a compact pre-trade risk review."""

    shares = fixed_fraction_position_size(
        account_equity=plan.account_equity,
        risk_fraction=plan.risk_fraction,
        entry_price=plan.entry_price,
        stop_price=plan.stop_price,
    )
    notional = shares * plan.entry_price
    risk_amount = shares * (plan.entry_price - plan.stop_price)
    ratio = reward_risk_ratio(plan.entry_price, plan.stop_price, plan.target_price)
    return {
        "shares": float(shares),
        "notional": notional,
        "risk_amount": risk_amount,
        "reward_risk_ratio": ratio,
        "passes_minimum_reward_risk": ratio >= 2.0,
    }
