from __future__ import annotations

import unittest

from quant_learning.metrics import (
    annualized_volatility,
    cumulative_return,
    max_drawdown,
    pct_returns,
    sharpe_ratio,
)


class MetricsTest(unittest.TestCase):
    def test_pct_returns_and_compounding(self) -> None:
        returns = pct_returns([100.0, 110.0, 99.0])

        self.assertAlmostEqual(returns[0], 0.1)
        self.assertAlmostEqual(returns[1], -0.1)
        self.assertAlmostEqual(cumulative_return(returns), -0.01)

    def test_max_drawdown(self) -> None:
        self.assertAlmostEqual(max_drawdown([100.0, 120.0, 90.0, 110.0]), -0.25)

    def test_annualized_volatility_uses_sample_standard_deviation(self) -> None:
        self.assertAlmostEqual(
            annualized_volatility([0.01, 0.03], periods_per_year=1),
            0.01414213562373095,
        )

    def test_sharpe_zero_for_flat_returns(self) -> None:
        self.assertEqual(sharpe_ratio([0.01, 0.01, 0.01]), 0.0)


if __name__ == "__main__":
    unittest.main()
