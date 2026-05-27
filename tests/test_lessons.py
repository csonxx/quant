from __future__ import annotations

import unittest

from quant_learning.lessons import (
    TradeOutcome,
    buy_and_hold_equity,
    expected_value,
    summarize_trades,
)


class LessonsTest(unittest.TestCase):
    def test_expected_value_can_punish_high_win_rate(self) -> None:
        self.assertAlmostEqual(
            expected_value(
                win_rate=0.8,
                average_win=100,
                average_loss=600,
                cost_per_trade=10,
            ),
            -50,
        )

    def test_summarize_trades(self) -> None:
        summary = summarize_trades([TradeOutcome(100), TradeOutcome(-50)], cost_per_trade=5)

        self.assertAlmostEqual(summary["win_rate"], 0.5)
        self.assertAlmostEqual(summary["expected_value"], 20)
        self.assertAlmostEqual(summary["total_pnl"], 40)

    def test_buy_and_hold_equity(self) -> None:
        self.assertEqual(buy_and_hold_equity([100, 110, 90], 1000), [1000, 1100, 900])


if __name__ == "__main__":
    unittest.main()
