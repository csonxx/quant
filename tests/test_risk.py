from __future__ import annotations

import unittest

from quant_learning.risk import (
    TradePlan,
    fixed_fraction_position_size,
    review_trade_plan,
    reward_risk_ratio,
)


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

    def test_reward_risk_ratio_boundaries(self) -> None:
        with self.assertRaisesRegex(ValueError, "stop_price must be below"):
            reward_risk_ratio(entry_price=100, stop_price=100, target_price=110)
        with self.assertRaisesRegex(ValueError, "target_price must be above"):
            reward_risk_ratio(entry_price=100, stop_price=95, target_price=100)


if __name__ == "__main__":
    unittest.main()
