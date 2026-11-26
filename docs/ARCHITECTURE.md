# Architecture

## MVP request flow

1. An application posts a metric event to `POST /api/v1/telemetry`.
2. Pydantic validates the service name, metric name, value, unit, and tags.
3. The API loads recent values for the same service and metric.
4. The detection module compares the new value with the historical baseline.
5. The telemetry event is persisted. If it is anomalous, an incident is created.
6. The dashboard reads service summaries and incidents from the API.

## Detection model

The MVP uses a rolling z-score baseline. It requires a minimum history before classifying a value as anomalous. The detector returns the baseline, standard deviation, and score so that a future investigation workflow can cite measurable evidence.

This is a lightweight starting point, not a replacement for seasonality-aware production monitoring. Production evolution should evaluate robust statistics, per-service thresholds, missing data, cardinality limits, and model drift.

## Production evolution

- Replace SQLite with PostgreSQL migrations and connection pooling.
- Move ingestion to a durable queue for backpressure and replay.
- Add Redis for short-lived aggregation and deduplication.
- Instrument services with OpenTelemetry SDKs and collectors.
- Add tenant-aware authorization and audit events.
- Store incident evidence and investigation traces.
- Ground LLM explanations in telemetry and runbook retrieval.
