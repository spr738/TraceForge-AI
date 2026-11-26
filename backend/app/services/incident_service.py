from app.db.database import connect
from app.schemas import utc_now


def create_incident(
    service: str,
    metric: str,
    observed_value: float,
    baseline: float,
    z_score: float,
) -> int:
    now = utc_now()
    severity = "critical" if z_score >= 5 else "warning"
    title = f"Unusual {metric} detected for {service}"
    description = (
        f"Observed {observed_value:g}; historical baseline {baseline:g}. "
        "Review recent deployments, dependency health, and traffic changes."
    )
    with connect() as connection:
        cursor = connection.execute(
            """INSERT INTO incidents
            (service, metric, severity, title, description, status,
             observed_value, baseline, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, 'open', ?, ?, ?, ?)""",
            (service, metric, severity, title, description,
             observed_value, baseline, now, now),
        )
        return int(cursor.lastrowid)
