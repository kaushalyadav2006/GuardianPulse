# GuardianPulse

# Hackhthon-02  Project

This is a lightweight hackathon  project with:

- FastAPI backend with emergency escalation simulation APIs
- Frontend dashboard (HTML/CSS/JS + Leaflet map)
- No real provider integrations (everything is simulated)

## Project Structure

- backend: Simulation APIs and in-memory workflow state
- frontend: Browser dashboard with Push/Pull control, timer, map, and timeline

## Quick Start

### 1) Backend setup

```powershell
cd "d:\visual code file\Hackthon\hackhthon-02\backend"
"d:/visual code file/Hackthon/.venv/Scripts/python.exe" -m pip install -r requirements.txt
"d:/visual code file/Hackthon/.venv/Scripts/python.exe" -m uvicorn app:app --host 127.0.0.1 --port 8010 --reload
```

Backend runs at: http://127.0.0.1:8010

### 2) Frontend setup

Open `frontend/index.html` directly in browser, or run a static server:

```powershell
cd "d:\visual code file\Hackthon\hackhthon-02\frontend"
"d:/visual code file/Hackthon/.venv/Scripts/python.exe" -m http.server 5510
```

Frontend runs at: http://127.0.0.1:5510

### 3) Single-command launcher

From project root:

```powershell
d:/hackhthon-02/.venv/Scripts/python.exe d:/hackhthon-02/run-all.py
```

Press Ctrl+C in that terminal to stop both backend and frontend.

## Demo APIs

- GET /health
- GET /api/demo/hospitals
- GET /api/demo/simulation
- POST /api/demo/simulation/start
- POST /api/demo/simulation/stop

## Notes

- This is intentionally non-production and in-memory only.
- Restarting backend resets simulation state.
