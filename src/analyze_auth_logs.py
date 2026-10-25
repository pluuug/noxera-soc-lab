#!/usr/bin/env python3
"""Analyze synthetic Linux SSH authentication logs for basic SOC detections."""
from __future__ import annotations
import argparse, json, re
from collections import defaultdict
from datetime import datetime, timedelta, timezone
from pathlib import Path

FAILED_RE = re.compile(r"(?P<timestamp>\w{3}\s+\d{1,2}\s[\d:]+).*Failed password for (?:invalid user )?(?P<user>\S+) from (?P<ip>\d{1,3}(?:\.\d{1,3}){3})")
SUCCESS_RE = re.compile(r"(?P<timestamp>\w{3}\s+\d{1,2}\s[\d:]+).*Accepted \S+ for (?P<user>\S+) from (?P<ip>\d{1,3}(?:\.\d{1,3}){3})")

def parse_timestamp(value: str, year: int) -> datetime:
    return datetime.strptime(f"{year} {value.strip()}", "%Y %b %d %H:%M:%S").replace(tzinfo=timezone.utc)

def analyze(lines: list[str], threshold: int, window_minutes: int = 10) -> dict:
    if threshold < 1 or window_minutes < 1:
        raise ValueError("threshold and window_minutes must be at least 1")
    year = datetime.now(timezone.utc).year
    events, failures_by_ip = [], defaultdict(list)
    for line_number, line in enumerate(lines, 1):
        match = FAILED_RE.search(line)
        kind = "failed_login"
        if match is None:
            match = SUCCESS_RE.search(line)
            kind = "successful_login"
        if match is None:
            continue
        stamp = match.group("timestamp").strip()
        try:
            parsed = parse_timestamp(stamp, year)
        except ValueError:
            continue
        event = {"line": line_number, "event": kind, "timestamp": stamp,
                 "_dt": parsed, "user": match.group("user"), "source_ip": match.group("ip")}
        events.append(event)
        if kind == "failed_login":
            failures_by_ip[event["source_ip"]].append(event)

    window = timedelta(minutes=window_minutes)
    alerts = []
    totals = {ip: len(items) for ip, items in sorted(failures_by_ip.items())}
    suspicious = set()

    for ip, items in sorted(failures_by_ip.items()):
        ordered = sorted(items, key=lambda e: e["_dt"])
        left, best = 0, []
        for right, current in enumerate(ordered):
            while left <= right and current["_dt"] - ordered[left]["_dt"] > window:
                left += 1
            candidate = ordered[left:right + 1]
            if len(candidate) > len(best):
                best = candidate
        if len(best) >= threshold:
            suspicious.add(ip)
            alerts.append({
                "rule_id": "NX-SOC-001", "title": "Repeated SSH authentication failures",
                "severity": "medium", "source_ip": ip, "failed_attempts": len(best),
                "window_minutes": window_minutes,
                "first_failure": min(e["_dt"] for e in best).isoformat(),
                "last_failure": max(e["_dt"] for e in best).isoformat(),
                "targeted_users": sorted({e["user"] for e in best}),
                "mitre_attack": ["T1110 - Brute Force"],
                "evidence": f"{len(best)} failed SSH logins from this IP occurred within {window_minutes} minutes.",
                "recommended_triage": [
                    "Confirm the source IP and time window in the original logs.",
                    "Check whether targeted accounts are privileged or valid.",
                    "Review firewall, VPN, and endpoint logs for related activity.",
                    "Escalate according to the organization's incident-response process."
                ]})

    for success in sorted((e for e in events if e["event"] == "successful_login"), key=lambda e: e["_dt"]):
        prior = [f for f in failures_by_ip.get(success["source_ip"], [])
                 if timedelta(0) <= success["_dt"] - f["_dt"] <= window]
        if len(prior) < threshold:
            continue
        alerts.append({
            "rule_id": "NX-SOC-002", "title": "Successful SSH login after repeated failures",
            "severity": "high", "source_ip": success["source_ip"], "account": success["user"],
            "timestamp": success["_dt"].isoformat(), "failed_attempts_before_success": len(prior),
            "window_minutes": window_minutes,
            "evidence": f"A successful SSH login followed {len(prior)} failed login(s) from the same IP within {window_minutes} minutes.",
            "mitre_attack": ["T1110 - Brute Force", "T1078 - Valid Accounts (investigate; not confirmed)"],
            "recommended_triage": [
                "Verify the login with the account owner and check whether it was expected.",
                "Review surrounding authentication and endpoint events.",
                "Check for privilege changes, new keys, and unusual follow-on activity.",
                "Escalate and contain only according to approved procedures and evidence."
            ]})

    return {
        "tool": "NØXERA SOC Lab - Authentication Log Analyzer",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_event_count": len(events), "threshold": threshold,
        "window_minutes": window_minutes, "failed_attempts_by_ip": totals,
        "alerts": alerts,
        "analyst_note": "Alerts are leads for investigation, not proof of compromise. Traditional syslog timestamps omit the year; this lab assigns the current UTC year."
    }

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to a Linux-style auth log file")
    parser.add_argument("--output", required=True, help="Path for JSON alert report")
    parser.add_argument("--threshold", type=int, default=5, help="Failed-login threshold per source IP")
    parser.add_argument("--window-minutes", type=int, default=10, help="Rolling detection window in minutes")
    args = parser.parse_args()
    if args.threshold < 1: parser.error("--threshold must be at least 1")
    if args.window_minutes < 1: parser.error("--window-minutes must be at least 1")
    input_path = Path(args.input)
    if not input_path.is_file(): parser.error(f"Input file does not exist: {input_path}")
    result = analyze(input_path.read_text(encoding="utf-8", errors="replace").splitlines(), args.threshold, args.window_minutes)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"Analyzed {result['input_event_count']} authentication events.")
    print(f"Found {len(result['alerts'])} alert(s).")
    print(f"Report written to: {output_path}")

if __name__ == "__main__":
    main()
