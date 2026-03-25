from __future__ import annotations

import atexit
import os
import signal
import subprocess
import sys
import time
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parent
PYTHON_EXE = ROOT / ".venv" / "Scripts" / "python.exe"
BACKEND_PORT = 8010
FRONTEND_PORT = 5510


def _require_python() -> None:
    if not PYTHON_EXE.exists():
        raise SystemExit(
            f"Python environment not found at {PYTHON_EXE}. "
            "Create it first using: py -m venv .venv"
        )


def _listening_pid(port: int) -> int | None:
    cmd = ["netstat", "-ano", "-p", "tcp"]
    output = subprocess.check_output(cmd, text=True, errors="ignore")

    for line in output.splitlines():
        line = line.strip()
        if f":{port}" not in line:
            continue
        if "LISTENING" not in line:
            continue

        parts = line.split()
        if not parts:
            continue

        pid_str = parts[-1]
        if pid_str.isdigit():
            return int(pid_str)

    return None


def _kill_pid(pid: int) -> None:
    subprocess.run(["taskkill", "/PID", str(pid), "/F"], check=False, capture_output=True, text=True)


def _clear_port(port: int) -> None:
    pid = _listening_pid(port)
    if pid is None:
        return

    if pid == 0:
        return

    if pid == os.getpid():
        raise SystemExit(f"Launcher itself is bound to port {port}.")

    print(f"[warn] Port {port} already in use by PID {pid}. Stopping it before launch...")
    _kill_pid(pid)
    time.sleep(0.3)


class ProcessGroup:
    def __init__(self) -> None:
        self.backend: subprocess.Popen[Any] | None = None
        self.frontend: subprocess.Popen[Any] | None = None
        self._stopping = False

    def start(self) -> None:
        backend_cmd = [
            str(PYTHON_EXE),
            "-m",
            "uvicorn",
            "app:app",
            "--app-dir",
            str(ROOT / "backend"),
            "--host",
            "127.0.0.1",
            "--port",
            str(BACKEND_PORT),
            "--reload",
        ]

        frontend_cmd = [
            str(PYTHON_EXE),
            "-m",
            "http.server",
            str(FRONTEND_PORT),
            "--directory",
            str(ROOT / "frontend"),
        ]

        self.backend = subprocess.Popen(backend_cmd)
        self.frontend = subprocess.Popen(frontend_cmd)

        assert self.backend is not None
        assert self.frontend is not None

        time.sleep(1.0)

        if self.backend.poll() is not None:
            raise RuntimeError("Backend failed to start. Check port 8010 permissions/availability.")

        if self.frontend.poll() is not None:
            raise RuntimeError("Frontend failed to start. Check port 5510 availability.")

        print(f"Started backend PID: {self.backend.pid}")
        print(f"Started frontend PID: {self.frontend.pid}")
        print("UI: http://127.0.0.1:5510")
        print("API: http://127.0.0.1:8010/health")
        print("Press Ctrl+C to stop both services.")

    def stop(self) -> None:
        if self._stopping:
            return
        self._stopping = True

        for proc in (self.backend, self.frontend):
            if proc is None:
                continue
            if proc.poll() is not None:
                continue
            proc.terminate()

        deadline = time.time() + 2.0
        for proc in (self.backend, self.frontend):
            if proc is None:
                continue
            while proc.poll() is None and time.time() < deadline:
                time.sleep(0.1)

        for proc in (self.backend, self.frontend):
            if proc is None:
                continue
            if proc.poll() is None:
                proc.kill()

        print("All services stopped.")

    def watch(self) -> None:
        while True:
            time.sleep(1.0)
            backend_done = self.backend is not None and self.backend.poll() is not None
            frontend_done = self.frontend is not None and self.frontend.poll() is not None

            if backend_done or frontend_done:
                print("[warn] One service exited unexpectedly. Stopping remaining services...")
                break


def main() -> int:
    _require_python()
    _clear_port(BACKEND_PORT)
    _clear_port(FRONTEND_PORT)

    group = ProcessGroup()
    atexit.register(group.stop)

    def _handle_signal(_sig: int, _frame: object) -> None:
        group.stop()
        raise SystemExit(0)

    signal.signal(signal.SIGINT, _handle_signal)
    signal.signal(signal.SIGTERM, _handle_signal)

    try:
        group.start()
        group.watch()
    except KeyboardInterrupt:
        pass
    except Exception as exc:
        print(f"[error] {exc}")
        return 1
    finally:
        group.stop()

    return 0


if __name__ == "__main__":
    sys.exit(main())
