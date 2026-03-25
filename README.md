# GuardianPulse Emergency Escalation Simulator

GuardianPulse is a hackathon prototype that simulates a real emergency escalation workflow.

It includes:

- FastAPI backend with timed simulation APIs
- Frontend dashboard (HTML/CSS/JS + Leaflet map)
- One-command Python launcher for local run

This is simulation-first and does not call real SMS, call, or emergency providers yet.

## What It Simulates

When PUSH is pressed, a timed chain runs:

1. T+5s: SMS, WhatsApp, Email alert
2. T+10s: Photo shared with family
3. T+15s: Audio shared with family
4. T+20s: Video shared with family
5. T+30s: Nearby hospitals contacted
6. T+60s: Escalation to 102

When PULL is pressed, simulation stops and user-safe notification is broadcast.

## Project Structure

- backend: FastAPI simulation state and endpoints
- frontend: Dashboard UI (Push/Pull, timer, timeline, map)
- run-all.py: Starts and stops backend + frontend together

## Local Setup

### 1) Create and activate virtual environment

From project root:

```powershell
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install -r backend/requirements.txt
```

### 2) Run both services with one command

```powershell
.\.venv\Scripts\python.exe .\run-all.py
```

Open:

- Frontend: http://127.0.0.1:5510
- Backend health: http://127.0.0.1:8010/health

Press Ctrl+C in the same terminal to stop both services.

## APIs

- GET /health
- GET /api/demo/hospitals
- GET /api/demo/simulation
- POST /api/demo/simulation/start
- POST /api/demo/simulation/stop
