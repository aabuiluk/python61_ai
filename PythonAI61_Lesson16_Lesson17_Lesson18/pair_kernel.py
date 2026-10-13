#!/usr/bin/env python3
"""Local Python kernel for pair presentations.

Two modes:
  python pair_kernel.py              HTTP on 127.0.0.1:8765 (student/teacher venv)
  python pair_kernel.py --stdio      JSON lines on stdin/stdout (journal worker)

Bind is localhost only. CORS is open so file:// presentations can reach the kernel.
"""

from __future__ import annotations

import argparse
import ast
import base64
import io
import json
import os
import sys
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock
from typing import Any

INPUT_BLOCKED = "інтерактивне введення в цій версії недоступне"
HOST = "127.0.0.1"
PORT = 8765

_SESSIONS: dict[str, dict[str, Any]] = {}
_LOCK = Lock()


def _blocked_input(*_args: Any, **_kwargs: Any) -> str:
    raise RuntimeError(INPUT_BLOCKED)


def _namespace(session_id: str, cwd: Path) -> dict[str, Any]:
    ns = _SESSIONS.get(session_id)
    if ns is None:
        ns = {"__name__": "__main__"}
        _SESSIONS[session_id] = ns
    ns["__file__"] = str(cwd / "_notebook_cell.py")
    return ns


def run_cell(source: str, *, cwd: Path, session_id: str = "default") -> dict[str, Any]:
    """Execute one cell in a persistent namespace. Shared by HTTP and stdio."""
    cwd = cwd.resolve()
    cwd.mkdir(parents=True, exist_ok=True)
    previous = os.getcwd()
    os.chdir(cwd)
    ns = _namespace(session_id, cwd)
    ns["input"] = _blocked_input
    try:
        import builtins

        builtins.input = _blocked_input
    except Exception:
        pass

    stdout = io.StringIO()
    stderr = io.StringIO()
    oldout, olderr = sys.stdout, sys.stderr
    sys.stdout, sys.stderr = stdout, stderr
    result_repr = None
    error = None
    try:
        tree = ast.parse(source)
        if tree.body:
            last = tree.body[-1]
            if isinstance(last, ast.Expr):
                body = tree.body[:-1]
                if body:
                    exec(compile(ast.Module(body, type_ignores=[]), "<cell>", "exec"), ns)
                value = eval(compile(ast.Expression(last.value), "<cell>", "eval"), ns)
                if value is not None:
                    result_repr = repr(value)
            else:
                exec(compile(tree, "<cell>", "exec"), ns)
    except Exception:
        error = traceback.format_exc()
    finally:
        sys.stdout, sys.stderr = oldout, olderr
        try:
            os.chdir(previous)
        except OSError:
            pass

    images: list[str] = []
    try:
        import matplotlib

        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        for num in list(plt.get_fignums()):
            fig = plt.figure(num)
            buf = io.BytesIO()
            fig.savefig(buf, format="png", bbox_inches="tight")
            images.append(base64.b64encode(buf.getvalue()).decode("ascii"))
        plt.close("all")
    except Exception:
        pass

    return {
        "stdout": stdout.getvalue(),
        "stderr": stderr.getvalue(),
        "result": result_repr,
        "error": error,
        "images": images,
    }


def probe_packages() -> dict[str, bool]:
    import importlib.util

    names = (
        "numpy",
        "pandas",
        "matplotlib",
        "sklearn",
        "scipy",
        "seaborn",
        "PIL",
        "torch",
        "nltk",
        "tensorflow",
    )
    return {name: importlib.util.find_spec(name) is not None for name in names}


def stdio_loop() -> None:
    for raw in sys.stdin:
        line = raw.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except json.JSONDecodeError as exc:
            sys.stdout.write(json.dumps({"error": str(exc)}) + "\n")
            sys.stdout.flush()
            continue
        cmd = msg.get("cmd") or "run"
        if cmd == "ping":
            sys.stdout.write(json.dumps({"ok": True, "packages": probe_packages()}) + "\n")
            sys.stdout.flush()
            continue
        cwd = Path(msg.get("cwd") or os.getcwd())
        with _LOCK:
            result = run_cell(
                str(msg.get("source") or ""),
                cwd=cwd,
                session_id=str(msg.get("session_id") or "default"),
            )
        result["id"] = msg.get("id")
        sys.stdout.write(json.dumps(result) + "\n")
        sys.stdout.flush()


class KernelHandler(BaseHTTPRequestHandler):
    cwd: Path = Path(".")

    def log_message(self, format: str, *args: Any) -> None:  # noqa: A003
        return

    def _send(self, code: int, payload: dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_OPTIONS(self) -> None:  # noqa: N802
        self._send(204, {})

    def do_GET(self) -> None:  # noqa: N802
        if self.path.split("?", 1)[0] in {"/status", "/", "/health"}:
            self._send(
                200,
                {
                    "ok": True,
                    "engine": "project-venv",
                    "cwd": str(self.cwd),
                    "packages": probe_packages(),
                },
            )
            return
        self._send(404, {"error": "not found"})

    def do_POST(self) -> None:  # noqa: N802
        if self.path.split("?", 1)[0] not in {"/run", "/"}:
            self._send(404, {"error": "not found"})
            return
        length = int(self.headers.get("Content-Length") or 0)
        raw = self.rfile.read(length) if length else b"{}"
        try:
            msg = json.loads(raw.decode("utf-8"))
        except json.JSONDecodeError:
            self._send(400, {"error": "invalid json"})
            return
        with _LOCK:
            result = run_cell(
                str(msg.get("source") or ""),
                cwd=self.cwd,
                session_id=str(msg.get("session_id") or "default"),
            )
        self._send(200, result)


def serve_http(port: int, cwd: Path) -> None:
    KernelHandler.cwd = cwd.resolve()
    server = ThreadingHTTPServer((HOST, port), KernelHandler)
    print(f"pair-kernel http://{HOST}:{port}  cwd={KernelHandler.cwd}", file=sys.stderr)
    server.serve_forever()


def main() -> int:
    parser = argparse.ArgumentParser(description="Kernel for pair presentation.html")
    parser.add_argument("--stdio", action="store_true", help="JSON lines worker for the journal")
    parser.add_argument("--port", type=int, default=PORT)
    parser.add_argument("--cwd", default=os.getcwd())
    args = parser.parse_args()
    if args.stdio:
        stdio_loop()
        return 0
    serve_http(args.port, Path(args.cwd))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
