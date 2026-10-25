# 🛡️ NØXERA SOC Lab

**Security Operations · Detection Engineering · Incident Response**

A hands-on cybersecurity portfolio project focused on analyzing authentication logs, detecting suspicious login activity, investigating alerts, and documenting incident response workflows.

## 🎯 Project Objectives

- Analyze Linux SSH authentication logs using Python.
- Detect repeated failed login attempts.
- Identify successful logins from sources associated with repeated failures.
- Generate structured JSON alerts for investigation.
- Document detection rules and map them to MITRE ATT&CK.
- Practice SOC alert triage and incident reporting.

## ⚙️ Technologies



\


## 🔍 Detection Rules

| Rule ID    | Detection                                          | Severity           |
| ---------- | -------------------------------------------------- | ------------------ |
| NX-SOC-001 | Repeated SSH authentication failures               | Medium             |
| NX-SOC-002 | Successful login from an IP with repeated failures | High — investigate |

Severity is illustrative and should be validated against the environment and supporting evidence.

## 🚀 Getting Started

### Requirements

- Python 3.10 or newer
- No third-party Python packages required

### Run the analyzer

```bash
python src/analyze_auth_logs.py --input data/auth.log --output reports/alerts.json --threshold 5
```

The analyzer processes the supplied sample log file and writes its findings to `reports/alerts.json`.

## 🧪 Investigation Workflow

1. Validate the alert and examine the supporting log events.
2. Identify the source IP, targeted accounts, and relevant time range.
3. Correlate failed and successful authentication events.
4. Consider benign explanations and assess potential impact.
5. Document findings, confidence, and recommended next steps.
6. Escalate according to the applicable incident-response process.

## 📁 Repository Structure

```text
noxera-soc-lab/
├── data/
│   └── auth.log
├── detections/
│   ├── NX-SOC-001-repeated-ssh-failures.md
│   └── NX-SOC-002-failure-then-success.md
├── reports/
│   ├── incident-report-template.md
│   └── sample-alerts.json
├── src/
│   └── analyze_auth_logs.py
├── .gitignore
└── README.md
```

## 🗺️ Roadmap

- [x] Authentication log analysis
- [x] Basic SSH detection rules
- [x] JSON alert reporting
- [x] Incident report template
- [x] Unit tests and additional synthetic test cases
- [x] Improved timestamp correlation and time-window detection
- [x] Windows event log analysis
- [x] SIEM integration and dashboard

## ⚠️ Scope and Limitations

This project uses synthetic sample logs for defensive learning. An alert is an investigative lead, not proof of compromise. The current analyzer counts events across the supplied file and has limitations in timestamp correlation; it is not a production SIEM.

## 👨‍💻 About

This project is part of my ongoing development in cybersecurity, SOC operations, Python automation, and defensive security analysis.

*Learn. Analyze. Detect. Investigate.*
