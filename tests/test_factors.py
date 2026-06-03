from __future__ import annotations

import unittest

from quant_learning.factors import realized_volatility, trailing_momentum


class FactorsTest(unittest.TestCase):
    def test_trailing_momentum(self) -> None:
        values = trailing_momentum([100, 110, 121], lookback=2)

        self.assertEqual(values[:2], [None, None])
        self.assertAlmostEqual(values[2], 0.21)

    def test_realized_volatility_uses_sample_standard_deviation(self) -> None:
        values = realized_volatility([100, 110, 99], lookback=2)

        self.assertEqual(values[:2], [None, None])
        self.assertAlmostEqual(values[2], 0.14142135623730956)


if __name__ == "__main__":
    unittest.main()
