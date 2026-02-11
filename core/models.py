"""Core data models for the trading system skeleton."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional


@dataclass(slots=True)
class BarRow:
    symbol: str
    timestamp: datetime
    open: float
    high: float
    low: float
    close: float
    volume: float


@dataclass(slots=True)
class EntrySignal:
    symbol: str
    timestamp: datetime
    reason: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Blocked:
    symbol: str
    timestamp: datetime
    reason: str


@dataclass(slots=True)
class EntryDecision:
    symbol: str
    timestamp: datetime
    should_enter: bool
    blocked: Optional[Blocked] = None
    note: str = ""


@dataclass(slots=True)
class PositionSnapshot:
    symbol: str
    timestamp: datetime
    quantity: float
    average_price: float
    unrealized_pnl: float


@dataclass(slots=True)
class ExitSignal:
    symbol: str
    timestamp: datetime
    reason: str
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass(slots=True)
class Skip:
    symbol: str
    timestamp: datetime
    reason: str


@dataclass(slots=True)
class ExitDecision:
    symbol: str
    timestamp: datetime
    should_exit: bool
    skip: Optional[Skip] = None
    note: str = ""
