# NØXERA SOC Lab

A defensive security portfolio project demonstrating entry-level SOC workflows: log review, alert triage, detection logic, and incident documentation.

> **Lab only:** The included logs are synthetic examples. This project does not scan networks, access accounts, or perform offensive actions.

## What it does

- Parses Linux-style SSH authentication log entries.
- Flags source IPs with repeated failed SSH logins.
- Highlights a successful login from an IP that also had repeated failures in the same log window.
- Writes findings to a JSON report for review.
- Documents detection logic and a repeatable analyst workflow.

## Requirements

- Python 3.10+
- No third-party packages required

## Run it

From this folder:

```bash
python src/analyze_auth_logs.py --input data/auth.log --output reports/alerts.json --threshold 5
```

Then open `reports/alerts.json` to review the alerts.

## Example investigation workflow

1. **Validate the alert:** Check the time range, source IP, and event counts.
2. **Establish scope:** Determine which account(s) and host(s) appear in the logs.
3. **Correlate events:** Look for a successful login following repeated failures.
4. **Assess severity:** Consider whether the account is privileged and whether activity is expected.
5. **Recommend response:** Follow the organization's process; examples include validating with the user, reviewing related logs, and resetting credentials if compromise is confirmed.
6. **Document:** Record evidence, confidence, impact, and next steps.

## Portfolio roadmap

- [x] Synthetic authentication log dataset
- [x] Python detection script
- [x] JSON alert output
- [x] Detection rule documentation
- [x] Incident report template
- [ ] Add unit tests
- [ ] Add Windows Event Log sample parser
- [ ] Add a small dashboard
- [ ] Test detections against additional synthetic scenarios

## Limitations

This is a learning project, not a production SIEM. It analyzes a small sample file and does not establish that an event is malicious by itself. Thresholds should be tuned to the environment, and alerts require human investigation.

## Skills demonstrated

Python · Log Analysis · Detection Engineering · Alert Triage · Incident Documentation · MITRE ATT&CK mapping
