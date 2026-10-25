# NX-SOC-003 — Possible SSH Password Spraying

- **Severity:** Medium
- **Purpose:** Identify failed SSH authentication attempts from one source IP against multiple distinct account names in a rolling time window.
- **Default window:** 10 minutes
- **Minimum distinct accounts:** `max(3, --threshold)`
- **MITRE ATT&CK:** T1110.003 — Password Spraying

## Detection logic

The analyzer groups failed SSH authentication events by source IP, examines rolling windows, and counts distinct targeted usernames. It raises an alert when the number of distinct usernames reaches the configured minimum. Repeated failures against only one account do not trigger this rule by themselves.

## Triage guidance

1. Validate the source IP and event window against original logs.
2. Review each targeted account and determine whether the attempts are expected.
3. Correlate successful logins and authentication events across other systems.
4. Escalate through the organization's incident-response process. Do not block an IP or disable accounts solely because this alert fired.

## Limitations

This is a heuristic for lab use. Legitimate scanners, misconfigured clients, shared NAT addresses, and incomplete logs can create misleading patterns. The alert is not proof of compromise.
