from __future__ import annotations

import unittest

from quant_learning.risk import TradePlan, fixed_fraction_position_size, review_trade_plan


class RiskTest(unittest.TestCase):
    def test_fixed_fraction_position_size(self) -> None:
        self.assertEqual(
            fixed_fraction_position_size(
                account_equity=10_000,
                risk_fraction=0.01,
                entry_price=100,
                stop_price=95,
            ),
            20,
        )

    def test_high_risk_fraction_warns_but_is_allowed(self) -> None:
        with self.assertWarns(UserWarning):
            shares = fixed_fraction_position_size(
                account_equity=10_000,
                risk_fraction=0.10,
                entry_price=100,
                stop_price=95,
            )

        self.assertEqual(shares, 200)

    def test_review_trade_plan(self) -> None:
        review = review_trade_plan(
            TradePlan(
                entry_price=100,
                stop_price=95,
                target_price=112,
                account_equity=10_000,
                risk_fraction=0.01,
            )
        )

        self.assertTrue(review["passes_minimum_reward_risk"])
        self.assertEqual(review["risk_amount"], 100)


if __name__ == "__main__":
    unittest.main()
