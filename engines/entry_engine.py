from __future__ import annotations

from datetime import datetime
from zoneinfo import ZoneInfo

from core.models import BarRow, EntryDecision


class EntryEngine:
    def evaluate(self, bar: BarRow) -> EntryDecision:
        """Evaluate whether to open an entry position for the given bar."""
        # TODO: implement entry condition logic
        # TODO: add additional signal scoring
        # Stub: no strategy logic yet
        return None


if __name__ == "__main__":
    # sample test (interface only)
    ts_ny = datetime.now(ZoneInfo("America/New_York"))
    minute_key = ts_ny.strftime("%Y%m%d-%H%M")

    dummy = BarRow(
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
        bar_count=3,
        is_rth=True,
        src="REPLAY",
    )

    engine = EntryEngine()
    print(engine.evaluate(dummy))
