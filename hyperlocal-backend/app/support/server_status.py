from datetime import UTC, datetime


def build_status_payload(db_ok: bool) -> dict:
    return {
        "status": "ok" if db_ok else "degraded",
        "time_utc": datetime.now(UTC).isoformat(),
        "services": {"api": "up", "database": "up" if db_ok else "down"},
    }
