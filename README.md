# TraceForge AI

**AI-powered application monitoring, anomaly detection, and incident intelligence.**

TraceForge AI is a full-stack observability platform for collecting application telemetry, detecting unusual behavior, investigating incidents, and helping engineers move from noisy signals to actionable diagnoses.

## What it does

- Accepts structured application logs and metric events through a REST ingestion API.
- Tracks service health, request latency, error rates, and event volume.
- Detects unusual metric behavior with a rolling statistical baseline.
- Creates incidents with severity, evidence, and investigation status.
- Produces explainable incident summaries and recommended next steps.
- Exposes a dashboard-ready API and interactive API documentation.

> The current repository delivers a runnable MVP foundation. AI provider integration, persistent production storage, authentication, alert delivery, and distributed deployment are staged for subsequent milestones.

## Architecture

```text
Application / Demo Generator
          |
          v
    FastAPI Ingestion API
          |
          +------> Event validation
          |
          +------> Rolling anomaly detector
          |
          +------> Incident engine
          |
          v
   SQLite (local MVP storage)
          |
          v
    Dashboard API / UI
```

## Technology

| Layer | Technology |
|---|---|
| API | Python 3.12, FastAPI, Pydantic |
| Detection | NumPy, rolling z-score baseline |
| MVP storage | SQLite |
| Frontend | Next.js, React, TypeScript |
| Local environment | Docker Compose |
| API documentation | OpenAPI / Swagger UI |

## Quick start (Windows)

### 1. Requirements

- Python 3.12+
- Node.js 20+
- npm
- Git
- Docker Desktop (optional)

### 2. Start the backend

Open PowerShell in the repository:

```powershell
cd backend
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
pip install -r requirements.txt
uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

API: http://127.0.0.1:8000  
Swagger UI: http://127.0.0.1:8000/docs  
Health: http://127.0.0.1:8000/health

### 3. Start the frontend

In a second PowerShell window:

```powershell
cd frontend
npm install
npm run dev
```

Dashboard: http://localhost:3000

### 4. Send a test metric

```powershell
$body = @{
  service = "checkout-api"
  metric = "http.request.duration_ms"
  value = 850
  unit = "ms"
  tags = @{ environment = "development"; route = "/checkout" }
} | ConvertTo-Json -Depth 5

Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:8000/api/v1/telemetry" -ContentType "application/json" -Body $body
```

## API endpoints

| Method | Endpoint | Purpose |
|---|---|---|
| GET | `/health` | Service health |
| POST | `/api/v1/telemetry` | Ingest a metric event |
| GET | `/api/v1/telemetry` | List recent telemetry |
| GET | `/api/v1/services` | Service summary |
| GET | `/api/v1/incidents` | List detected incidents |
| PATCH | `/api/v1/incidents/{id}` | Update incident status |

## Repository layout

```text
backend/
  app/
    api/             # HTTP routes
    core/            # Configuration
    db/              # SQLite persistence
    detection/       # Anomaly detection
    services/        # Incident processing
    main.py
frontend/
  app/               # Next.js application
  components/        # Dashboard components
  lib/               # API client
docs/                # Architecture and roadmap
infrastructure/      # Local deployment assets
docker-compose.yml
```

## Engineering roadmap

- [x] API service and health endpoint
- [x] Telemetry ingestion and local persistence
- [x] Rolling statistical anomaly detection
- [x] Incident lifecycle API
- [x] Dashboard starter UI
- [ ] User authentication and organization isolation
- [ ] PostgreSQL and Redis-backed processing
- [ ] OpenTelemetry collector integration
- [ ] LLM-based evidence-grounded incident investigation
- [ ] Alert routing, notification policies, and runbooks
- [ ] Automated tests, CI pipeline, and deployment hardening

## Development principles

- Validate incoming telemetry at the API boundary.
- Keep anomaly results explainable and tied to observed measurements.
- Treat AI-generated investigation notes as recommendations, not facts.
- Keep secrets in environment variables; never commit API keys.
- Add tests and operational safeguards before production use.

## License

This project is distributed under the MIT License. See [LICENSE](LICENSE).
