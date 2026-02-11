"""
Core data models for AutoTrade v2.0 (schema-aligned, stricter validation).

Notes:
- LONG-only. No short selling. Bear exposure is via long inverse ETFs.
- All timestamps are NY time (America/New_York) and must be tz-aware datetimes.
- minute_key must be "%Y%m%d-%H%M" derived from ts_ny (bar close minute in NY).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Literal, Optional, Union


Source = Literal["IEX", "SIP", "REPLAY"]
Side = Literal["LONG"]


def _require_tzaware(dt: datetime, field_name: str) -> None:
    if dt.tzinfo is None or dt.utcoffset() is None:
        raise ValueError(f"{field_name} must be timezone-aware datetime")


def _derive_minute_key(ts_ny: datetime) -> str:
    return ts_ny.strftime("%Y%m%d-%H%M")


def _require_minute_key(ts_ny: datetime, minute_key: str, field_name: str = "minute_key") -> None:
    expected = _derive_minute_key(ts_ny)
    if minute_key != expected:
        raise ValueError(f"{field_name} must equal ts_ny-derived key: expected {expected}, got {minute_key}")


# =========================
# Market Data Contract
# =========================
@dataclass(slots=True)
class BarRow:
    ts_ny: datetime
    minute_key: str  # "%Y%m%d-%H%M"
    symbol: str

    o: float
    h: float
    l: float
    c: float
    v: int  # volume must be int

    ema5: float
    ema10: float
    dif: float
    dea: float
    macd_hist: float

    bar_count: int  # int >= 1
    is_rth: bool
    src: Source

    def __post_init__(self) -> None:
        _require_tzaware(self.ts_ny, "ts_ny")

        if self.bar_count < 1:
            raise ValueError("bar_count must be >= 1")
        if self.v < 0:
            raise ValueError("v (volume) must be >= 0")

        _require_minute_key(self.ts_ny, self.minute_key)


# =========================
# Entry Contract
# =========================
EntryReason = Literal["MACD_HIST_CROSS_UP__EMA_CONFIRM"]


@dataclass(slots=True)
class EntrySignal:
    ts_ny: datetime
    minute_key: str
    symbol: str
    side: Side  # LONG-only
    score: float  # used for same-minute ranking
    reason: EntryReason
    features: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_tzaware(self.ts_ny, "ts_ny")
        _require_minute_key(self.ts_ny, self.minute_key)


BlockCode = Literal[
    "COLD_START",
    "OPEN_NO_ENTRY",
    "NO_ENTRY_BEFORE_CLOSE",
    "OUTSIDE_RTH",
    "INVERSE_ETF_TIME_BAN",
    "CAPACITY_FULL",
    "ALREADY_IN_POSITION",
    "INSUFFICIENT_CASH",
]


@dataclass(slots=True)
class Blocked:
    ts_ny: datetime
    minute_key: str
    symbol: str
    block_code: BlockCode
    detail: str
    snapshot: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_tzaware(self.ts_ny, "ts_ny")
        _require_minute_key(self.ts_ny, self.minute_key)


EntryDecision = Optional[Union[EntrySignal, Blocked]]


# =========================
# Position Snapshot Contract
# =========================
@dataclass(slots=True)
class PositionSnapshot:
    ts_ny: datetime
    symbol: str
    qty: int
    avg_entry_px: float
    entry_ts_ny: Optional[datetime]

    # P/L fields are percent values, e.g. +0.003 == +0.3%
    unrealized_pl_pct: float
    highest_pl_pct: float

    # StepTP state (persisted via state/positions.json per your rule)
    step_tp_floor_pl_pct: float
    step_tp_armed: bool

    def __post_init__(self) -> None:
        _require_tzaware(self.ts_ny, "ts_ny")
        if self.entry_ts_ny is not None:
            _require_tzaware(self.entry_ts_ny, "entry_ts_ny")


# =========================
# Exit Contract
# =========================
ExitAction = Literal["CLOSE"]

ExitReasonCode = Literal[
    "FORCE_FLAT",
    "STOP_LOSS",
    "STEP_FLOOR_BROKEN",
    "TAKE_PROFIT",
    "TTL_EXPIRED",
]


@dataclass(slots=True)
class ExitSignal:
    ts_ny: datetime
    minute_key: str
    symbol: str
    action: ExitAction
    reason_code: ExitReasonCode
    qty: Optional[int]  # None means "close all"
    meta: dict[str, Any] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_tzaware(self.ts_ny, "ts_ny")
        _require_minute_key(self.ts_ny, self.minute_key)


SkipCode = Literal[
    "NO_POSITION",
    "HOLDING_OK",
    "WAIT_TTL",
    "WAIT_STEP_TP",
    "WAIT_TP",
    "WAIT_SL",
]


@dataclass(slots=True)
class Skip:
    ts_ny: datetime
    minute_key: str
    symbol: str
    skip_code: SkipCode
    detail: str

    def __post_init__(self) -> None:
        _require_tzaware(self.ts_ny, "ts_ny")
        _require_minute_key(self.ts_ny, self.minute_key)


ExitDecision = Optional[Union[ExitSignal, Skip]]
