# NX-SOC-002 — Successful Login from a Source with Repeated Failures

- **Purpose:** Prioritize a successful SSH login from an IP that also generated repeated failed attempts in the same input file.
- **Severity:** High (investigate; not proof of compromise)
- **ATT&CK mapping:** T1110 — Brute Force; T1078 — Valid Accounts (hypothesis to investigate)
- **Logic:** If a source IP reaches the repeated-failure threshold and also has a successful SSH login, create a second alert.
- **Triage:** Validate the account owner, check whether the login was expected, review surrounding logs, and look for suspicious follow-on activity.
- **Caution:** The sample logic does not prove the success occurred after the failures. A production implementation should parse full timestamps and enforce event ordering and a time window.
