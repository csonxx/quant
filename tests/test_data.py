from __future__ import annotations

import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

from quant_learning.data import group_by_symbol, load_ohlcv_csv


ROOT = Path(__file__).resolve().parents[1]


class DataTest(unittest.TestCase):
    def test_load_sample_data(self) -> None:
        bars = load_ohlcv_csv(ROOT / "data/samples/ohlcv_demo.csv")
        grouped = group_by_symbol(bars)

        self.assertEqual(set(grouped), {"DEMO"})
        self.assertEqual(len(grouped["DEMO"]), 30)
        self.assertLess(grouped["DEMO"][0].date, grouped["DEMO"][-1].date)

    def test_rejects_missing_required_column(self) -> None:
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "bad.csv"
            path.write_text("date,symbol,open,high,low,volume\n", encoding="utf-8")

            with self.assertRaisesRegex(ValueError, "missing required columns: close"):
                load_ohlcv_csv(path)

    def test_rejects_invalid_ohlc_range(self) -> None:
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "bad.csv"
            _write_csv_row(path, "2024-01-01,DEMO,100,98,95,97,1000\n")

            with self.assertRaisesRegex(ValueError, "inconsistent OHLC range"):
                load_ohlcv_csv(path)

    def test_rejects_non_positive_price_negative_volume_and_empty_symbol(self) -> None:
        invalid_rows = [
            ("2024-01-01,DEMO,0,100,95,97,1000\n", "non-positive price"),
            ("2024-01-01,DEMO,100,100,95,97,-1\n", "negative volume"),
            ("2024-01-01,,100,100,95,97,1000\n", "empty symbol"),
        ]

        for row, message in invalid_rows:
            with self.subTest(message=message), TemporaryDirectory() as tmpdir:
                path = Path(tmpdir) / "bad.csv"
                _write_csv_row(path, row)

                with self.assertRaisesRegex(ValueError, message):
                    load_ohlcv_csv(path)

    def test_group_by_symbol_rejects_duplicate_dates(self) -> None:
        with TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "bad.csv"
            path.write_text(
                "date,symbol,open,high,low,close,volume\n"
                "2024-01-01,DEMO,100,101,99,100,1000\n"
                "2024-01-01,DEMO,100,101,99,100,1000\n",
                encoding="utf-8",
            )

            with self.assertRaisesRegex(ValueError, "dates must be strictly increasing"):
                group_by_symbol(load_ohlcv_csv(path))


def _write_csv_row(path: Path, row: str) -> None:
    path.write_text(
        "date,symbol,open,high,low,close,volume\n" + row,
        encoding="utf-8",
    )


if __name__ == "__main__":
    unittest.main()
