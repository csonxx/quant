from __future__ import annotations

import unittest
from pathlib import Path

from quant_learning.data import group_by_symbol, load_ohlcv_csv


ROOT = Path(__file__).resolve().parents[1]


class DataTest(unittest.TestCase):
    def test_load_sample_data(self) -> None:
        bars = load_ohlcv_csv(ROOT / "data/samples/ohlcv_demo.csv")
        grouped = group_by_symbol(bars)

        self.assertEqual(set(grouped), {"DEMO"})
        self.assertEqual(len(grouped["DEMO"]), 30)
        self.assertLess(grouped["DEMO"][0].date, grouped["DEMO"][-1].date)


if __name__ == "__main__":
    unittest.main()
