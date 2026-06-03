"""Data contracts for small OHLCV research examples."""

from __future__ import annotations

import csv
from collections import defaultdict
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path


REQUIRED_OHLCV_COLUMNS = {"date", "symbol", "open", "high", "low", "close", "volume"}


@dataclass(frozen=True)
class Bar:
    """One daily OHLCV bar.

    This intentionally stays tiny. If this object is confusing, a large dataframe will
    only hide the confusion.
    """

    date: date
    symbol: str
    open: float
    high: float
    low: float
    close: float
    volume: int


def load_ohlcv_csv(path: str | Path) -> list[Bar]:
    """Load and validate a CSV with date,symbol,open,high,low,close,volume columns."""

    csv_path = Path(path)
    with csv_path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle)
        columns = set(reader.fieldnames or [])
        missing = REQUIRED_OHLCV_COLUMNS - columns
        if missing:
            missing_columns = ", ".join(sorted(missing))
            raise ValueError(f"{csv_path} missing required columns: {missing_columns}")

        bars = [_parse_bar(row, row_number=index + 2) for index, row in enumerate(reader)]

    if not bars:
        raise ValueError(f"{csv_path} contains no bars")

    return sorted(bars, key=lambda bar: (bar.symbol, bar.date))


def group_by_symbol(bars: list[Bar]) -> dict[str, list[Bar]]:
    """Group bars by symbol and enforce strictly increasing dates per symbol."""

    grouped: dict[str, list[Bar]] = defaultdict(list)
    for bar in bars:
        grouped[bar.symbol].append(bar)

    for symbol, symbol_bars in grouped.items():
        previous_date: date | None = None
        for bar in symbol_bars:
            if previous_date is not None and bar.date <= previous_date:
                raise ValueError(f"{symbol} dates must be strictly increasing")
            previous_date = bar.date

    return dict(grouped)


def closes(bars: list[Bar]) -> list[float]:
    """Return close prices from a sorted bar list."""

    return [bar.close for bar in bars]


def _parse_bar(row: dict[str, str], row_number: int) -> Bar:
    try:
        parsed_date = datetime.strptime(row["date"], "%Y-%m-%d").date()
        symbol = row["symbol"].strip()
        open_price = float(row["open"])
        high = float(row["high"])
        low = float(row["low"])
        close = float(row["close"])
        volume = int(row["volume"])
    except Exception as exc:  # noqa: BLE001 - convert parser detail into row context.
        raise ValueError(f"invalid OHLCV row {row_number}: {row}") from exc

    if not symbol:
        raise ValueError(f"row {row_number} has empty symbol")
    if min(open_price, high, low, close) <= 0:
        raise ValueError(f"row {row_number} has non-positive price")
    if low > high:
        raise ValueError(f"row {row_number} has low above high")
    if not (low <= open_price <= high and low <= close <= high):
        raise ValueError(f"row {row_number} has inconsistent OHLC range")
    if volume < 0:
        raise ValueError(f"row {row_number} has negative volume")

    return Bar(
        date=parsed_date,
        symbol=symbol,
        open=open_price,
        high=high,
        low=low,
        close=close,
        volume=volume,
    )
