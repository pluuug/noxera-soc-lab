# NØXERA SOC Lab

A defensive cybersecurity portfolio project demonstrating entry-level Security Operations Center (SOC) workflows through authentication log analysis, detection engineering, alert triage, and investigation documentation.

> **Lab only:** The included authentication logs are synthetic examples. This project does not monitor live systems, scan networks, access accounts, or perform offensive actions.

## Project Overview

The analyzer parses Linux-style SSH authentication logs, identifies suspicious authentication patterns, and generates a structured JSON report for analyst review.

### Features

- Parses successful and failed SSH authentication events.
- Detects repeated failed logins within a configurable rolling time window.
- Detects successful logins following repeated failures from the same source IP.
- Generates JSON alerts with evidence, severity, timestamps, and recommended triage steps.
- Maps detections to relevant MITRE ATT&CK techniques.
- Includes automated unit tests for core detection logic.

## Detection Rules

| Rule ID | Detection | Default severity |
|---|---|---|
| NX-SOC-001 | Repeated SSH authentication failures from one source IP within the configured window | Medium |
| NX-SOC-002 | Successful SSH login following repeated failures from the same IP within the configured window | High |

Severity indicates investigation priority, not confirmed compromise. Both detections require analyst review and supporting evidence.

## Requirements

- Python 3.10 or later
- No third-party Python packages required

## Run the Analyzer

From the project root:

```powershell
python src/analyze_auth_logs.py --input data/auth.log --output reports/alerts.json --threshold 5 --window-minutes 10
```

The options configure:

- `--input`: Path to the authentication log file.
- `--output`: Destination for the JSON report.
- `--threshold`: Number of failed logins required to trigger a detection.
- `--window-minutes`: Rolling time window used by the detection rules.

If `python` is unavailable in your Windows terminal, use your installed Python executable or configure Python on your PATH.

### Expected sample result

With the included sample dataset and default values above, the analyzer processes 8 authentication events and generates 2 alerts.

The generated report is saved to `reports/alerts.json`.

## Run the Tests

From the project root:

```powershell
python -m unittest discover -s tests -v
```

The current test suite covers:

1. Repeated failures within the window trigger NX-SOC-001.
2. Failures outside the window do not trigger NX-SOC-001.
3. A successful login after repeated failures triggers NX-SOC-002.
4. A successful login before the failures does not trigger NX-SOC-002.

## Analyst Investigation Workflow

1. **Validate the alert:** Review the source IP, timestamps, threshold, and evidence.
2. **Establish scope:** Identify the accounts and authentication events involved.
3. **Correlate events:** Check whether a successful login followed repeated failures.
4. **Assess severity:** Consider account privileges, expected activity, and additional evidence.
5. **Investigate further:** Review relevant endpoint, firewall, VPN, and authentication records where available.
6. **Recommend response:** Follow the organization's incident-response process; do not assume compromise from this alert alone.
7. **Document findings:** Record evidence, confidence, impact, and recommended next steps.

## MITRE ATT&CK References

- **T1110 — Brute Force:** Relevant to repeated authentication failures.
- **T1078 — Valid Accounts:** A potential investigation lead when a successful login follows repeated failures; this detection alone does not establish account compromise.

## Limitations

- The included dataset is synthetic and intentionally small.
- The analyzer processes a supplied file; it is not a live SIEM or endpoint monitoring agent.
- Traditional syslog timestamps may omit the year. The current parser assigns the current UTC year, which can misdate historical logs.
- Source IP addresses in the sample use documentation-reserved ranges and do not identify real attackers.
- Thresholds and severity should be tuned to the environment.
- Alerts are investigative leads, not proof of malicious activity.

## Project Structure

```text
noxera-soc-lab/
├── data/
│   └── auth.log
├── detections/
├── reports/
│   └── alerts.json
├── src/
│   └── analyze_auth_logs.py
├── tests/
│   └── test_analyze_auth_logs.py
└── README.md
```

## Skills Demonstrated

Python · Authentication Log Analysis · Detection Engineering · Time-Window Correlation · JSON Reporting · Alert Triage · MITRE ATT&CK · Unit Testing · Technical Documentation

## Roadmap

- [x] Synthetic authentication log dataset
- [x] Python detection engine
- [x] JSON alert reporting
- [x] Time-window-based detection rules
- [x] Four unit tests for core detection scenarios
- [x] Investigation recommendations and ATT&CK references
- [ ] Add malformed-input and edge-case tests
- [ ] Improve handling of historical syslog timestamps
- [ ] Add a Windows Event Log sample parser
- [ ] Build a small alert dashboard
- [ ] Expand synthetic test scenarios
