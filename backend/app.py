from __future__ import annotations

from datetime import datetime, timezone
from typing import TypedDict
from uuid import uuid4

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

app = FastAPI(title="GuardianPulse Demo API", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class Hospital(BaseModel):
    id: str
    name: str
    phone: str
    lat: float
    lng: float
    distance_km: float


class SimulationLog(BaseModel):
    at_second: int
    title: str
    detail: str
    occurred_at: datetime


class SimulationState(BaseModel):
    simulation_id: str
    active: bool
    started_at: datetime | None
    stopped_at: datetime | None
    elapsed_seconds: int
    log: list[SimulationLog]


class SimulationActionResponse(BaseModel):
    message: str
    state: SimulationState


class SimulationStore(TypedDict):
    simulation_id: str
    active: bool
    started_at: datetime | None
    stopped_at: datetime | None
    log: list[SimulationLog]


HOSPITALS: list[Hospital] = [
    Hospital(
        id="hosp_001",
        name="CityCare Emergency Center",
        phone="+91-120-401-1102",
        lat=28.6282,
        lng=77.3731,
        distance_km=1.8,
    ),
    Hospital(
        id="hosp_002",
        name="Metro Lifeline Hospital",
        phone="+91-120-402-9988",
        lat=28.6321,
        lng=77.3652,
        distance_km=2.7,
    ),
    Hospital(
        id="hosp_003",
        name="Guardian Trauma Unit",
        phone="+91-120-403-2200",
        lat=28.6239,
        lng=77.3584,
        distance_km=4.1,
    ),
    Hospital(
        id="hosp_004",
        name="RapidAid Medical Point",
        phone="+91-120-404-7711",
        lat=28.6184,
        lng=77.3798,
        distance_km=4.6,
    ),
]


SIMULATION_SCHEDULE: list[tuple[int, str, str]] = [
    (
        0,
        "Simulation started",
        "Emergency mode activated from the panic button.",
    ),
    (
        5,
        "Alert sent",
        "Primary alert sent over SMS, WhatsApp, and email.",
    ),
    (
        10,
        "Photo shared with family",
        "Latest location photo was shared with registered family contacts.",
    ),
    (
        15,
        "Audio clip shared with family",
        "Emergency audio clip was sent to family contacts.",
    ),
    (
        20,
        "Video clip shared with family",
        "Short incident video was sent to family contacts.",
    ),
    (
        30,
        "Nearby hospitals contacted",
        "System searched nearby hospitals and placed escalation calls.",
    ),
    (
        60,
        "Escalated to 102",
        "No hospital acknowledged in 1 minute; emergency line 102 was contacted.",
    ),
]


SIMULATION: SimulationStore = {
    "simulation_id": f"sim_{uuid4().hex[:8]}",
    "active": False,
    "started_at": None,
    "stopped_at": None,
    "log": [],
}


def _now_utc() -> datetime:
    return datetime.now(timezone.utc)


def _elapsed_seconds(started_at: datetime | None) -> int:
    if started_at is None:
        return 0
    return max(0, int((_now_utc() - started_at).total_seconds()))


def _append_log(offset: int, title: str, detail: str) -> None:
    SIMULATION["log"].append(
        SimulationLog(
            at_second=offset,
            title=title,
            detail=detail,
            occurred_at=_now_utc(),
        )
    )


def _advance_simulation() -> None:
    if not SIMULATION["active"]:
        return

    started_at = SIMULATION["started_at"]
    elapsed = _elapsed_seconds(started_at)
    logged_offsets = {entry.at_second for entry in SIMULATION["log"]}

    for offset, title, detail in SIMULATION_SCHEDULE:
        if elapsed >= offset and offset not in logged_offsets:
            _append_log(offset, title, detail)


def _simulation_state() -> SimulationState:
    _advance_simulation()
    started_at = SIMULATION["started_at"]
    return SimulationState(
        simulation_id=SIMULATION["simulation_id"],
        active=SIMULATION["active"],
        started_at=started_at,
        stopped_at=SIMULATION["stopped_at"],
        elapsed_seconds=_elapsed_seconds(started_at) if SIMULATION["active"] else 0,
        log=SIMULATION["log"],
    )


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok", "mode": "demo"}


@app.get("/api/demo/hospitals")
def get_hospitals() -> dict[str, list[Hospital]]:
    ordered = sorted(HOSPITALS, key=lambda item: item.distance_km)
    return {"items": ordered}


@app.get("/api/demo/simulation", response_model=SimulationState)
def get_simulation() -> SimulationState:
    return _simulation_state()


@app.post("/api/demo/simulation/start", response_model=SimulationActionResponse)
def start_simulation() -> SimulationActionResponse:
    if SIMULATION["active"]:
        return SimulationActionResponse(message="Simulation already active", state=_simulation_state())

    SIMULATION["simulation_id"] = f"sim_{uuid4().hex[:8]}"
    SIMULATION["active"] = True
    SIMULATION["started_at"] = _now_utc()
    SIMULATION["stopped_at"] = None
    SIMULATION["log"] = []

    return SimulationActionResponse(message="Simulation started", state=_simulation_state())


@app.post("/api/demo/simulation/stop", response_model=SimulationActionResponse)
def stop_simulation() -> SimulationActionResponse:
    if not SIMULATION["active"]:
        return SimulationActionResponse(message="Simulation already stopped", state=_simulation_state())

    SIMULATION["active"] = False
    SIMULATION["stopped_at"] = _now_utc()
    _append_log(
        _elapsed_seconds(SIMULATION["started_at"]),
        "User marked safe",
        "Pull button pressed. User confirmed safe. Family, hospitals, and responders were notified that the user is fine.",
    )

    return SimulationActionResponse(message="Simulation stopped", state=_simulation_state())
