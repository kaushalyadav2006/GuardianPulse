# GuardianPulse Emergency Escalation Simulator

GuardianPulse is a hackathon prototype that simulates a real emergency escalation workflow.

It includes:

- FastAPI backend with timed simulation APIs
- Frontend dashboard (HTML/CSS/JS + Leaflet map)
- One-command Python launcher for local run

This is simulation-first and does not call real SMS, call, or emergency providers yet.

---

## Problem Statement

In real medical or safety emergencies, every second matters, but there is often no structured and automated way to alert family members, nearby hospitals, and emergency services in a coordinated sequence. Victims may be alone, panicked, or unconscious, and families frequently receive information late or not at all. This delay in communication and escalation can result in slower ambulance dispatch, slower hospital preparation, and, in the worst cases, preventable loss of life.

There is a clear need for a system that can, with a single action, trigger a reliable, time-bound escalation chain: from notifying close contacts to reaching hospitals and finally the official emergency helpline (102), while also allowing the user to cancel the alert if they become safe again.

---

## Proposed Solution

GuardianPulse is a simulation-first emergency escalation system that demonstrates how a real-world solution could automate the full alert pipeline within 60 seconds.

- The **PUSH** action starts an emergency escalation workflow.
- The system sends staged notifications (SMS / WhatsApp / Email), then shares media (photo, audio, video) with family, then contacts nearby hospitals, and finally escalates to **102** in the final step.
- The **PULL** action immediately stops the simulation and broadcasts a “user is safe” notification to close the incident.

The project is implemented as:

- A **FastAPI backend** that maintains simulation state and exposes APIs for starting, stopping, and monitoring the escalation.
- A **frontend dashboard** that shows the current simulation timeline, PUSH/PULL controls, and a map of nearby hospitals.
- A **one-command runner script** (`run-all.py`) that starts both backend and frontend together for easy demo during evaluation.

This prototype focuses on workflow correctness, timing, and user experience. It does not send real messages or integrate with real emergency providers yet, making it safe for demonstration but realistic in behavior.

---

## Dataset Used

GuardianPulse does **not** rely on any external real-world dataset.

- All data used in the simulation (hospital list, alerts, media events, and timelines) is **synthetic/mock data** defined within the project.
- No organizer-provided datasets are used; all configuration and simulation data are created by the team for this prototype.

This aligns with the requirement that teams are responsible for collecting or generating their own data.

---

## Tech Stack

**Backend**

- Python
- FastAPI
- Uvicorn

**Frontend**

- HTML
- CSS
- JavaScript
- Leaflet.js (for interactive map and nearby hospitals visualization)

**Tooling & Environment**

- Virtual environment using `venv`
- One-command launcher script (`run-all.py`) for combined backend + frontend startup

---

## Team

- **Team Name:** GuardianPulse  

- **Member 1 (Leader):**  
  - Name: **Manichand Gupta**  
  - Email: `manichand.gupta.contact@gmail.com`  
  - GitHub: https://github.com/EclipseManic

- **Member 2:**  
  - Name: **Kaushal Yadav**  
  - Email: `yadavkaushal2023@gmail.com`  
  - GitHub: https://github.com/kaushalyadav2006  

- **Member 3:**  
  - Name: **Ansh Sharma**  
  - Email: `as7793557@gmail.com`  
  - GitHub: N/A

---

## What It Simulates

When PUSH is pressed, a timed chain runs:

1. T+5s: SMS, WhatsApp, Email alert  
2. T+10s: Photo shared with family  
3. T+15s: Audio shared with family  
4. T+20s: Video shared with family  
5. T+30s: Nearby hospitals contacted  
6. T+60s: Escalation to 102  

When PULL is pressed, simulation stops and user-safe notification is broadcast.

---

## Project Structure

- `backend`: FastAPI simulation state and endpoints  
- `frontend`: Dashboard UI (Push/Pull, timer, timeline, map)  
- `run-all.py`: Starts and stops backend + frontend together  

---

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

Press `Ctrl + C` in the same terminal to stop both services.

---

## APIs

- `GET /health`
- `GET /api/demo/hospitals`
- `GET /api/demo/simulation`
- `POST /api/demo/simulation/start`
- `POST /api/demo/simulation/stop`
