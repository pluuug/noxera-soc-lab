#!/usr/bin/env python3
"""Analyze synthetic Linux SSH authentication logs for basic SOC detections."""
from __future__ import annotations

import argparse
import json
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path

FAILED_RE = re.compile(
    r"(?P<timestamp>\w{3}\s+\d{1,2}\s[\d:]+).*Failed password for "
    r"(?:invalid user )?(?P<user>\S+) from (?P<ip>\d{1,3}(?:\.\d{1,3}){3})"
)
SUCCESS_RE = re.compile(
    r"(?P<timestamp>\w{3}\s+\d{1,2}\s[\d:]+).*Accepted \S+ for "
    r"(?P<user>\S+) from (?P<ip>\d{1,3}(?:\.\d{1,3}){3})"
)

def parse_timestamp(value: str) -> str:
    """Return a best-effort timestamp string; year is intentionally not inferred."""
    return value.strip()

def analyze(lines: list[str], threshold: int) -> dict:
    failures = Counter()
    failure_users = defaultdict(set)
    successes = []
    events = []

    for line_number, line in enumerate(lines, start=1):
        failed = FAILED_RE.search(line)
        if failed:
            ip, user = failed.group("ip"), failed.group("user")
            failures[ip] += 1
            failure_users[ip].add(user)
            events.append({
                "line": line_number,
                "event": "failed_login",
                "timestamp": parse_timestamp(failed.group("timestamp")),
                "user": user,
                "source_ip": ip,
            })
            continue

        success = SUCCESS_RE.search(line)
        if success:
            item = {
                "line": line_number,
                "event": "successful_login",
                "timestamp": parse_timestamp(success.group("timestamp")),
                "user": success.group("user"),
                "source_ip": success.group("ip"),
            }
            successes.append(item)
            events.append(item)

    alerts = []
    for ip, count in sorted(failures.items()):
        if count >= threshold:
            alerts.append({
                "rule_id": "NX-SOC-001",
                "title": "Repeated SSH authentication failures",
                "severity": "medium",
                "source_ip": ip,
                "failed_attempts": count,
                "targeted_users": sorted(failure_users[ip]),
                "mitre_attack": ["T1110 - Brute Force"],
                "evidence": "Source IP reached the configured failed-login threshold.",
                "recommended_triage": [
                    "Confirm the source IP and time window in the original logs.",
                    "Check whether targeted accounts are privileged or valid.",
                    "Review firewall, VPN, and endpoint logs for related activity.",
                    "Escalate according to the organization's incident-response process.",
                ],
            })

    suspicious_ips = {a["source_ip"] for a in alerts}
    for success in successes:
        if success["source_ip"] in suspicious_ips:
            alerts.append({
                "rule_id": "NX-SOC-002",
                "title": "Successful SSH login from an IP with repeated failures",
                "severity": "high",
                "source_ip": success["source_ip"],
                "account": success["user"],
                "timestamp": success["timestamp"],
                "evidence": "The same source IP had repeated failures and at least one successful login in this input file.",
                "mitre_attack": [
                    "T1110 - Brute Force",
                    "T1078 - Valid Accounts (investigate; not confirmed)",
                ],
                "recommended_triage": [
                    "Verify the login with the account owner and check whether it was expected.",
                    "Review surrounding authentication and endpoint events.",
                    "Check for privilege changes, new keys, and unusual follow-on activity.",
                    "Escalate and contain only according to approved procedures and evidence.",
                ],
            })

    return {
        "tool": "NØXERA SOC Lab - Authentication Log Analyzer",
        "generated_at_utc": datetime.now(timezone.utc).isoformat(),
        "input_event_count": len(events),
        "threshold": threshold,
        "failed_attempts_by_ip": dict(sorted(failures.items())),
        "alerts": alerts,
        "analyst_note": "Alerts are leads for investigation, not proof of compromise.",
    }

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, help="Path to a Linux-style auth log file")
    parser.add_argument("--output", required=True, help="Path for JSON alert report")
    parser.add_argument("--threshold", type=int, default=5, help="Failed-login threshold per source IP")
    args = parser.parse_args()

    if args.threshold < 1:
        parser.error("--threshold must be at least 1")

    input_path = Path(args.input)
    if not input_path.is_file():
        parser.error(f"Input file does not exist: {input_path}")

    result = analyze(input_path.read_text(encoding="utf-8", errors="replace").splitlines(), args.threshold)
    output_path = Path(args.output)
    output_path.parent.mkdir(parents=True, exist_ok=True)
    output_path.write_text(json.dumps(result, indent=2), encoding="utf-8")

    print(f"Analyzed {result['input_event_count']} authentication events.")
    print(f"Found {len(result['alerts'])} alert(s).")
    print(f"Report written to: {output_path}")

if __name__ == "__main__":
    main()
