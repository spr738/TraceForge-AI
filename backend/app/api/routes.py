import json
from fastapi import APIRouter, HTTPException, Query
from app.db.database import connect
from app.detection.anomaly import detect_anomaly
from app.schemas import TelemetryCreate, IncidentStatusUpdate, utc_now
from app.services.incident_service import create_incident

router = APIRouter(prefix="/api/v1")


@router.post("/telemetry", status_code=201)
def ingest_telemetry(payload: TelemetryCreate):
    with connect() as connection:
        rows = connection.execute(
            """SELECT value FROM telemetry
            WHERE service = ? AND metric = ?
            ORDER BY id DESC LIMIT 100""",
            (payload.service, payload.metric),
        ).fetchall()
        history = [float(row["value"]) for row in reversed(rows)]

    result = detect_anomaly(history, payload.value)
    created_at = utc_now()
    with connect() as connection:
        cursor = connection.execute(
            """INSERT INTO telemetry(service, metric, value, unit, tags, created_at)
            VALUES (?, ?, ?, ?, ?, ?)""",
            (payload.service, payload.metric, payload.value, payload.unit,
             json.dumps(payload.tags), created_at),
        )
        telemetry_id = int(cursor.lastrowid)

    incident_id = None
    if result.is_anomaly:
        incident_id = create_incident(
            payload.service, payload.metric, payload.value,
            result.baseline, result.z_score
        )

    return {
        "id": telemetry_id,
        "created_at": created_at,
        "anomaly": result.is_anomaly,
        "baseline": result.baseline,
        "z_score": result.z_score,
        "incident_id": incident_id,
    }


@router.get("/telemetry")
def list_telemetry(limit: int = Query(default=100, ge=1, le=500)):
    with connect() as connection:
        rows = connection.execute(
            "SELECT * FROM telemetry ORDER BY id DESC LIMIT ?", (limit,)
        ).fetchall()
    return [{**dict(row), "tags": json.loads(row["tags"])} for row in rows]


@router.get("/services")
def list_services():
    with connect() as connection:
        rows = connection.execute("""
            SELECT service, COUNT(*) AS event_count,
                   MAX(created_at) AS last_seen,
                   SUM(CASE WHEN metric LIKE '%error%' THEN 1 ELSE 0 END) AS error_events
            FROM telemetry GROUP BY service ORDER BY last_seen DESC
        """).fetchall()
    return [dict(row) for row in rows]


@router.get("/incidents")
def list_incidents(status: str | None = None):
    with connect() as connection:
        if status:
            rows = connection.execute(
                "SELECT * FROM incidents WHERE status = ? ORDER BY id DESC",
                (status,),
            ).fetchall()
        else:
            rows = connection.execute(
                "SELECT * FROM incidents ORDER BY id DESC"
            ).fetchall()
    return [dict(row) for row in rows]


@router.patch("/incidents/{incident_id}")
def update_incident(incident_id: int, payload: IncidentStatusUpdate):
    with connect() as connection:
        cursor = connection.execute(
            "UPDATE incidents SET status = ?, updated_at = ? WHERE id = ?",
            (payload.status, utc_now(), incident_id),
        )
        if cursor.rowcount == 0:
            raise HTTPException(status_code=404, detail="Incident not found")
        row = connection.execute(
            "SELECT * FROM incidents WHERE id = ?", (incident_id,)
        ).fetchone()
    return dict(row)
