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

## Deployment (Recommended for Hackathon Judges)

Use this setup for a stable public link:

- Backend: Render
- Frontend: Netlify

### A) Deploy backend on Render

1. Push repo to GitHub.
2. In Render: New Web Service -> Connect repo.
3. Set:
	- Root directory: backend
	- Runtime: Python
	- Build command: pip install -r requirements.txt
	- Start command: uvicorn app:app --host 0.0.0.0 --port $PORT
4. Deploy and copy backend URL.
5. Verify in browser: https://YOUR-RENDER-URL/health

### B) Point frontend to live backend

Edit frontend/app.js and set API_BASE to your Render URL, for example:

```js
const API_BASE = "https://YOUR-RENDER-URL";
```

Commit and push.

### C) Deploy frontend on Netlify

1. In Netlify: Add new site -> Import from GitHub.
2. Set:
	- Base directory: frontend
	- Build command: (leave empty)
	- Publish directory: frontend
3. Deploy.
4. Share Netlify URL with judges.

## Judge Demo Notes

Tell judges:

- Press PUSH to start timed escalation.
- Watch timer + timeline + hospital map update live.
- Press PULL to stop escalation and mark user safe.

## Important Security Note

If test.py is pushed publicly, do not keep API keys hardcoded.

- Move secrets to environment variables.
- Rotate any exposed key immediately.

## Limitations

- In-memory simulation state (resets on restart)
- No real provider integrations yet
- Built for workflow validation and demo clarity
