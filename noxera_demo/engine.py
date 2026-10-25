"""Synthetic SSH auth data + NX-SOC-001/002/003 detections (port of the demo engine).

All IPs are RFC 5737 documentation addresses. Timestamps are anchored to a FIXED
reference time so the public demo never goes stale or changes between visits.
"""
from datetime import datetime, timedelta, timezone

from .reference import RULES

THRESHOLD = 5
WINDOW = timedelta(minutes=10)
MIN_DISTINCT_ACCOUNTS = 5
REFERENCE_NOW = datetime(2026, 10, 25, 12, 0, 0, tzinfo=timezone.utc)
_MONTHS = ["Jan", "Feb", "Mar", "Apr", "May", "Jun", "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]


def syslog_line(e):
    d = e["ts"]
    stamp = f"{_MONTHS[d.month - 1]} {d.day:2d} {d:%H:%M:%S}"
    port = 40000 + int(d.timestamp()) % 20000
    pid = 1200 + port % 800
    verb = "Failed" if e["result"] == "failed" else "Accepted"
    return f"{stamp} {e['host']} sshd[{pid}]: {verb} password for {e['user']} from {e['ip']} port {port} ssh2"


def generate_events(now=REFERENCE_NOW):
    H, M, S = timedelta(hours=1), timedelta(minutes=1), timedelta(seconds=1)
    ev = []

    def push(offset, ip, user, result, host="nx-edge-01"):
        ev.append({"ts": now - offset, "host": host, "ip": ip, "user": user, "result": result})

    routine = [("192.0.2.10", "svc-backup"), ("192.0.2.11", "m.okafor"),
               ("192.0.2.12", "deploy"), ("192.0.2.13", "j.reyes")]
    for h in range(47, -1, -3):
        ip, user = routine[h % len(routine)]
        push(h * H + 7 * M, ip, user, "success", "nx-edge-01" if h % 2 else "nx-app-02")

    # Below threshold: must NOT alert
    push(31 * H, "198.51.100.17", "root", "failed")
    push(9 * H + 22 * M, "198.51.100.230", "admin", "failed")
    push(9 * H + 19 * M, "198.51.100.230", "admin", "failed")
    push(9 * H + 15 * M, "198.51.100.230", "admin", "success")

    # Incident A (~26h ago): brute force then success
    a = 26 * H
    for i, u in enumerate(["admin", "deploy", "oracle", "root", "test"]):
        push(a - i * 3 * S, "203.0.113.42", u, "failed")
    push(a - 15 * S, "203.0.113.42", "test", "failed")
    push(a - 18 * S, "203.0.113.42", "deploy", "success")

    # Incident B (~5h ago): pure password spray
    b = 5 * H
    for i, u in enumerate(["admin", "oracle", "postgres", "test", "ubuntu", "guest", "deploy"]):
        push(b - i * 9 * S, "203.0.113.77", u, "failed", "nx-app-02")

    # Incident C (~40min ago): stale cron credentials (benign false positive)
    c = 40 * M
    for i in range(6):
        push(c - i * 20 * S, "192.0.2.50", "svc-backup", "failed", "nx-app-02")
    push(c - 130 * S, "192.0.2.50", "svc-backup", "success", "nx-app-02")

    ev.sort(key=lambda e: e["ts"])
    for e in ev:
        e["raw"] = syslog_line(e)
    return ev


def _bursts(failures):
    """Greedy 10-minute windows; a burst only consumes events that start it."""
    out, i = [], 0
    while i < len(failures):
        start = failures[i]["ts"]
        burst = [f for f in failures if start <= f["ts"] <= start + WINDOW]
        if len(burst) >= THRESHOLD:
            out.append(burst)
            i += len(burst)
        else:
            i += 1  # fixed: do not skip past a too-small window
    return out


def run_detections(events):
    by_ip = {}
    for e in sorted(events, key=lambda x: x["ts"]):
        by_ip.setdefault(e["ip"], []).append(e)
    results = []
    for ip, lst in by_ip.items():
        fails = [e for e in lst if e["result"] == "failed"]
        succ = [e for e in lst if e["result"] == "success"]
        for burst in _bursts(fails):
            users = sorted({b["user"] for b in burst})
            first, last = burst[0]["ts"], burst[-1]["ts"]
            n = len(burst)
            results.append(dict(
                rule_id="NX-SOC-001", title=RULES["NX-SOC-001"]["name"], severity="medium", ip=ip,
                first_seen=first, last_seen=last, failed_attempts=n, targeted_users=users,
                mitre=["T1110 - Brute Force"],
                evidence=f"{n} failed SSH logins from this IP occurred within 10 minutes."))
            if len(users) >= MIN_DISTINCT_ACCOUNTS:
                results.append(dict(
                    rule_id="NX-SOC-003", title=RULES["NX-SOC-003"]["name"], severity="medium", ip=ip,
                    first_seen=first, last_seen=last, failed_attempts=n, targeted_users=users,
                    distinct_accounts=len(users), mitre=["T1110.003 - Password Spraying"],
                    evidence=f"Failed SSH logins targeted {len(users)} distinct accounts from one IP within 10 minutes."))
        for s in succ:
            prior = [f for f in fails if f["ts"] < s["ts"] and s["ts"] - f["ts"] <= WINDOW]
            if len(prior) >= THRESHOLD:
                results.append(dict(
                    rule_id="NX-SOC-002", title=RULES["NX-SOC-002"]["name"], severity="high", ip=ip,
                    first_seen=prior[0]["ts"], last_seen=s["ts"], failed_attempts=len(prior),
                    account=s["user"],
                    mitre=["T1110 - Brute Force", "T1078 - Valid Accounts (investigate; not confirmed)"],
                    evidence=f"A successful SSH login followed {len(prior)} failed login(s) from the same IP within 10 minutes."))
    rank = {"critical": 0, "high": 1, "medium": 2, "low": 3}
    results.sort(key=lambda r: (rank.get(r["severity"], 9), -r["last_seen"].timestamp()))
    for r in results:
        r["key"] = f"{r['rule_id']}|{r['ip']}|{r['first_seen'].isoformat()}"
    return results
