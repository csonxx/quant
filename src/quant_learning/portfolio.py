"""Small portfolio helpers for score-to-weight teaching examples."""

from __future__ import annotations


def equal_weights(symbols: list[str]) -> dict[str, float]:
    """Return equal weights for a non-empty symbol list."""

    if not symbols:
        raise ValueError("symbols cannot be empty")
    weight = 1.0 / len(symbols)
    return {symbol: weight for symbol in symbols}


def score_to_topk_equal_weights(scores: dict[str, float], top_k: int) -> dict[str, float]:
    """Turn model/factor scores into equal weights for the top-k symbols.

    This is intentionally simple: scores are sorted descending and ties are broken by
    symbol for deterministic teaching output.
    """

    if not scores:
        raise ValueError("scores cannot be empty")
    if top_k <= 0:
        raise ValueError("top_k must be positive")

    selected = sorted(scores, key=lambda symbol: (-scores[symbol], symbol))[:top_k]
    return equal_weights(selected)


def portfolio_return(weights: dict[str, float], returns: dict[str, float]) -> float:
    """Calculate a one-period weighted portfolio return."""

    if not weights:
        raise ValueError("weights cannot be empty")

    missing_returns = sorted(set(weights) - set(returns))
    if missing_returns:
        missing = ", ".join(missing_returns)
        raise ValueError(f"missing returns for: {missing}")

    weight_sum = sum(weights.values())
    if abs(weight_sum - 1.0) > 1e-9:
        raise ValueError("weights must sum to 1")
    if any(weight < 0 for weight in weights.values()):
        raise ValueError("long-only teaching portfolios cannot have negative weights")

    return sum(weights[symbol] * returns[symbol] for symbol in weights)
