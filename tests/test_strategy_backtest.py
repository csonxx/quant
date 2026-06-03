from __future__ import annotations

import unittest
from datetime import date
from pathlib import Path

from quant_learning.backtest import run_long_only_signal_backtest
from quant_learning.data import Bar, group_by_symbol, load_ohlcv_csv
from quant_learning.strategy import (
    Signal,
    moving_average_crossover_signals,
    simple_moving_average,
)


ROOT = Path(__file__).resolve().parents[1]


class StrategyBacktestTest(unittest.TestCase):
    def test_simple_moving_average_warms_up(self) -> None:
        self.assertEqual(simple_moving_average([1, 2, 3, 4], 3), [None, None, 2.0, 3.0])

    def test_backtest_uses_previous_bar_signal(self) -> None:
        bars = group_by_symbol(load_ohlcv_csv(ROOT / "data/samples/ohlcv_demo.csv"))["DEMO"]
        signals = moving_average_crossover_signals(bars, fast_window=3, slow_window=8)
        result = run_long_only_signal_backtest(bars, signals, fee_bps=5.0)

        first_invested_point = next(
            point for point in result.equity_curve if point.position_weight > 0
        )
        first_long_signal = next(signal for signal in signals if signal.target_weight > 0)

        self.assertGreater(first_invested_point.date, first_long_signal.date)
        self.assertGreater(result.final_equity, 0)
        self.assertGreaterEqual(result.total_fees, 0)

    def test_fee_is_charged_before_exposure_is_applied(self) -> None:
        bars = [
            Bar(date(2024, 1, 1), "DEMO", 100, 100, 100, 100, 1000),
            Bar(date(2024, 1, 2), "DEMO", 110, 110, 110, 110, 1000),
        ]
        signals = [Signal(date(2024, 1, 1), "DEMO", 1.0, "test_full_exposure")]

        result = run_long_only_signal_backtest(
            bars,
            signals,
            initial_cash=10_000,
            fee_bps=100,
        )

        self.assertAlmostEqual(result.total_fees, 100)
        self.assertAlmostEqual(result.final_equity, 10_890)


if __name__ == "__main__":
    unittest.main()
