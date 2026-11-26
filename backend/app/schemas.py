from datetime import datetime, timezone
from typing import Any, Literal
from pydantic import BaseModel, Field


class TelemetryCreate(BaseModel):
    service: str = Field(min_length=1, max_length=120)
    metric: str = Field(min_length=1, max_length=160)
    value: float
    unit: str | None = Field(default=None, max_length=24)
    tags: dict[str, Any] = Field(default_factory=dict)


class TelemetryRead(TelemetryCreate):
    id: int
    created_at: datetime


class IncidentRead(BaseModel):
    id: int
    service: str
    metric: str
    severity: str
    title: str
    description: str
    status: str
    observed_value: float
    baseline: float
    created_at: datetime
    updated_at: datetime


class IncidentStatusUpdate(BaseModel):
    status: Literal["open", "investigating", "resolved"]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()
