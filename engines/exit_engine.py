from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from core.models import BarRow, ExitDecision, PositionSnapshot


class ExitEngine:
    def evaluate(self, bar: BarRow, pos: PositionSnapshot | None) -> ExitDecision:
        """Evaluate whether to exit the current position for the given bar.

        Stub only: no strategy logic yet.
        """
        return None


if __name__ == "__main__":
    ts_ny = datetime.now(ZoneInfo("America/New_York"))
    minute_key = ts_ny.strftime("%Y%m%d-%H%M")

    bar = BarRow(
        ts_ny=ts_ny,
        minute_key=minute_key,
        symbol="TQQQ",
        o=0.0,
        h=0.0,
        l=0.0,
        c=0.0,
        v=0,
        ema5=0.0,
        ema10=0.0,
        dif=0.0,
        dea=0.0,
        macd_hist=0.0,
        bar_count=1,
        is_rth=True,
        src="REPLAY",
    )

    pos = PositionSnapshot(
        ts_ny=ts_ny,
        symbol="TQQQ",
        qty=1,
        avg_entry_px=100.0,
        entry_ts_ny=ts_ny,
        unrealized_pl_pct=0.0,
        highest_pl_pct=0.0,
        step_tp_floor_pl_pct=0.0,
        step_tp_armed=False,
    )

    engine = ExitEngine()
    print(engine.evaluate(bar, pos))
