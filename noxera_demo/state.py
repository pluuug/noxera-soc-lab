"""Triage state: session-based, with best-effort local JSON persistence."""
import json
from datetime import datetime, timezone
from pathlib import Path

import streamlit as st

from .engine import generate_events, run_detections

STORE = Path(__file__).resolve().parent.parent / "reports" / "triage_demo.json"


@st.cache_data
def dataset():
    events = generate_events()
    return events, run_detections(events)


def _load():
    try:
        return json.loads(STORE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def triage():
    if "triage" not in st.session_state:
        st.session_state["triage"] = _load()
    return st.session_state["triage"]


def _save():
    try:
        STORE.parent.mkdir(exist_ok=True)
        STORE.write_text(json.dumps(st.session_state["triage"], indent=2), encoding="utf-8")
    except OSError:
        pass  # read-only host: state stays in this session only


def status_of(alert):
    return triage().get(alert["key"], {}).get("status", "New")


def notes_of(alert):
    return triage().get(alert["key"], {}).get("log", [])


def _entry(alert):
    return triage().setdefault(alert["key"], {"status": "New", "log": []})


def set_status(alert, new):
    old = status_of(alert)
    if old == new:
        return
    e = _entry(alert)
    e["status"] = new
    e["log"].append({"kind": "status", "author": "analyst", "body": f"Disposition changed: {old} -> {new}", "ts": _now()})
    _save()


def add_note(alert, body):
    _entry(alert)["log"].append({"kind": "note", "author": "analyst", "body": body.strip()[:4000], "ts": _now()})
    _save()


def reset():
    st.session_state["triage"] = {}
    _save()


def _now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")
