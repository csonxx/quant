from __future__ import annotations

import unittest

from quant_learning.portfolio import (
    equal_weights,
    portfolio_return,
    score_to_topk_equal_weights,
)


class PortfolioTest(unittest.TestCase):
    def test_equal_weights(self) -> None:
        self.assertEqual(equal_weights(["AAA", "BBB"]), {"AAA": 0.5, "BBB": 0.5})

    def test_score_to_topk_equal_weights_is_deterministic(self) -> None:
        self.assertEqual(
            score_to_topk_equal_weights({"BBB": 1.0, "AAA": 1.0, "CCC": 0.5}, top_k=2),
            {"AAA": 0.5, "BBB": 0.5},
        )

    def test_portfolio_return(self) -> None:
        self.assertAlmostEqual(
            portfolio_return({"AAA": 0.5, "BBB": 0.5}, {"AAA": 0.02, "BBB": -0.01}),
            0.005,
        )

    def test_portfolio_return_rejects_missing_returns(self) -> None:
        with self.assertRaisesRegex(ValueError, "missing returns"):
            portfolio_return({"AAA": 1.0}, {})


if __name__ == "__main__":
    unittest.main()
