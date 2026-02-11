"""Entrypoint for the Python 3.10 project skeleton."""

from datetime import datetime, timezone

from core.models import BarRow


def main() -> None:
    sample = BarRow(
        symbol="DEMO",
        timestamp=datetime.now(timezone.utc),
        open=0.0,
        high=0.0,
        low=0.0,
        close=0.0,
        volume=0.0,
    )
    print("Autotrade v2 skeleton is runnable.")
    print(f"Sample model loaded: {sample}")


if __name__ == "__main__":
    main()
