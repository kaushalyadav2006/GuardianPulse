const API_BASE = "http://127.0.0.1:8010";

const apiStatus = document.getElementById("apiStatus");
const timerBadge = document.getElementById("timerBadge");
const simStateText = document.getElementById("simStateText");
const controlButton = document.getElementById("controlButton");
const timelineList = document.getElementById("timelineList");

let map;
let markersLayer;
let timerTicker;
let elapsedSeconds = 0;
let simulationActive = false;

function eventTag(title) {
  const lower = title.toLowerCase();
  if (lower.includes("alert")) return { label: "Alert", cls: "tag-alert" };
  if (lower.includes("photo")) return { label: "Photo", cls: "tag-photo" };
  if (lower.includes("audio")) return { label: "Audio", cls: "tag-audio" };
  if (lower.includes("video")) return { label: "Video", cls: "tag-video" };
  if (lower.includes("hospital")) return { label: "Hospital", cls: "tag-hospital" };
  if (lower.includes("102")) return { label: "Emergency", cls: "tag-emergency" };
  if (lower.includes("safe")) return { label: "Safe", cls: "tag-safe" };
  return { label: "Event", cls: "tag-default" };
}

function toMMSS(totalSeconds) {
  const safe = Math.max(0, Math.floor(totalSeconds));
  const mm = String(Math.floor(safe / 60)).padStart(2, "0");
  const ss = String(safe % 60).padStart(2, "0");
  return `${mm}:${ss}`;
}

function renderTimer() {
  timerBadge.textContent = toMMSS(elapsedSeconds);
}

function stopTimerTicker() {
  if (timerTicker) {
    clearInterval(timerTicker);
    timerTicker = null;
  }
}

function startTimerTicker() {
  stopTimerTicker();
  timerTicker = setInterval(() => {
    if (!simulationActive) {
      return;
    }
    elapsedSeconds += 1;
    renderTimer();
  }, 1000);
}

function setControlMode(isActive) {
  simulationActive = isActive;
  controlButton.textContent = isActive ? "PULL" : "PUSH";
  controlButton.classList.toggle("is-pull", isActive);

  if (!isActive) {
    stopTimerTicker();
  }
}

function timelineRow(entry) {
  const stamp = new Date(entry.occurred_at).toLocaleTimeString();
  const tag = eventTag(entry.title);
  return `
    <article class="timeline-item">
      <div class="time">T+${entry.at_second}s</div>
      <div>
        <span class="event-tag ${tag.cls}">${tag.label}</span>
        <strong>${entry.title}</strong>
        <p>${entry.detail}</p>
      </div>
      <div class="stamp">${stamp}</div>
    </article>
  `;
}

function renderTimeline(items) {
  if (!items.length) {
    timelineList.innerHTML = '<p class="empty">No simulation events yet.</p>';
    return;
  }

  timelineList.innerHTML = items.map(timelineRow).join("");
}

async function ensureMap() {
  if (!map) {
    map = L.map("hospitalMap", { zoomControl: true }).setView([28.626, 77.37], 13);
    L.tileLayer("https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png", {
      attribution: '&copy; <a href="https://www.openstreetmap.org/copyright">OpenStreetMap</a>',
    }).addTo(map);
    markersLayer = L.layerGroup().addTo(map);
  }

  const res = await fetch(`${API_BASE}/api/demo/hospitals`);
  const data = await res.json();

  markersLayer.clearLayers();

  data.items.forEach((hospital) => {
    const marker = L.marker([hospital.lat, hospital.lng]);
    marker.bindPopup(`
      <strong>${hospital.name}</strong><br/>
      Phone: ${hospital.phone}<br/>
      Distance: ${hospital.distance_km} km
    `);
    marker.addTo(markersLayer);
  });
}

async function checkHealth() {
  try {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) {
      throw new Error("Health check failed");
    }
    apiStatus.textContent = "API Online";
  } catch (error) {
    apiStatus.textContent = "API Offline";
  }
}

async function loadSimulationState() {
  const res = await fetch(`${API_BASE}/api/demo/simulation`);
  const data = await res.json();

  setControlMode(data.active);
  elapsedSeconds = data.elapsed_seconds;
  renderTimer();
  renderTimeline(data.log);

  if (data.active) {
    simStateText.textContent = "Simulation in progress. Escalation flow is running.";
    document.body.classList.add("sim-live");
    if (!timerTicker) {
      startTimerTicker();
    }
  } else {
    simStateText.textContent = "System idle. Press PUSH to start simulation.";
    document.body.classList.remove("sim-live");
  }
}

async function refreshAll() {
  await checkHealth();
  await loadSimulationState();
}

controlButton.addEventListener("click", async () => {
  controlButton.disabled = true;
  const route = simulationActive ? "stop" : "start";

  try {
    const res = await fetch(`${API_BASE}/api/demo/simulation/${route}`, { method: "POST" });
    const data = await res.json();
    setControlMode(data.state.active);
    elapsedSeconds = data.state.elapsed_seconds;
    renderTimer();
    renderTimeline(data.state.log);

    if (data.state.active) {
      simStateText.textContent = "Simulation in progress. Escalation flow is running.";
      document.body.classList.add("sim-live");
      startTimerTicker();
    } else {
      simStateText.textContent = "User marked safe. Escalation flow stopped.";
      document.body.classList.remove("sim-live");
      stopTimerTicker();
    }
  } finally {
    controlButton.disabled = false;
  }
});

(async () => {
  await ensureMap();
  await refreshAll();
  setInterval(refreshAll, 1000);
})();
