# NX-SOC-001 — Repeated SSH Authentication Failures

- **Purpose:** Identify a source IP generating repeated SSH authentication failures.
- **Severity:** Medium (context-dependent)
- **ATT&CK mapping:** T1110 — Brute Force
- **Logic:** Count failed SSH authentication events by source IP. Alert when the count reaches the configured threshold.
- **Default threshold:** 5 failures in the provided input file.
- **False-positive considerations:** Typing errors, stale automation credentials, misconfigured services, and shared NAT/VPN addresses.
- **Triage:** Confirm time range and source, identify targeted accounts, correlate with VPN/firewall/endpoint logs, and determine whether activity is expected.
- **Caution:** This simple sample parser counts the entire input file, not a rolling time window. A production detection should use normalized timestamps and a defined window.
