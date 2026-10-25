"""Rule + MITRE ATT&CK reference (ported from the NOXERA demo)."""

STATUSES = ["New", "Investigating", "Benign", "Confirmed"]
STATUS_COLOR = {"New": "#6ce5f2", "Investigating": "#f4bd63", "Benign": "#71e0b0", "Confirmed": "#ff667d"}
SEVERITY_COLOR = {"critical": "#ff667d", "high": "#ff8b70", "medium": "#f4bd63", "low": "#71e0b0"}

RULES = {
    "NX-SOC-001": {
        "name": "Repeated SSH authentication failures", "severity": "medium",
        "logic": "\u2265 5 failed SSH logins from one source IP within a 10-minute window.",
        "description": "A single source generates a burst of failed SSH authentication attempts. This is the classic signature of automated credential guessing against an exposed service.",
        "techniques": [
            {"id": "T1110", "name": "Brute Force", "tactic": "Credential Access", "url": "https://attack.mitre.org/techniques/T1110/",
             "why": "Repeated authentication failures from one source in a short window match adversaries attempting to obtain valid credentials by systematically guessing passwords.", "caveat": ""},
            {"id": "T1110.001", "name": "Password Guessing", "tactic": "Credential Access", "url": "https://attack.mitre.org/techniques/T1110/001/",
             "why": "Targeting common account names (admin, root, oracle, test) suggests guessing likely username/password combinations rather than spraying one known password.",
             "caveat": "Sub-technique inferred from account selection; confirm with full log context."},
        ],
        "false_positives": [
            "Misconfigured automation (cron jobs, CI runners, backup agents) retrying with expired credentials.",
            "A legitimate user with a stale password saved in an SSH client or key manager.",
            "Monitoring or vulnerability scanners performing authenticated checks.",
            "NAT: many benign users behind one egress IP can aggregate failures.",
        ],
        "triage": [
            "Confirm the source IP and time window in the original logs.",
            "Check whether targeted accounts are privileged or valid.",
            "Review firewall, VPN, and endpoint logs for related activity.",
            "Escalate according to the organization's incident-response process.",
        ],
    },
    "NX-SOC-002": {
        "name": "Successful SSH login after repeated failures", "severity": "high",
        "logic": "\u2265 5 failures from one source IP, followed by a successful SSH login from the same IP within 10 minutes.",
        "description": "A success immediately following a failure burst is the highest-signal pattern in this lab: the guessing may have worked. Prioritize this alert above standalone failure bursts.",
        "techniques": [
            {"id": "T1110", "name": "Brute Force", "tactic": "Credential Access", "url": "https://attack.mitre.org/techniques/T1110/",
             "why": "The preceding failure burst indicates a credential-guessing attempt; the subsequent success is consistent with the attempt succeeding.", "caveat": ""},
            {"id": "T1078", "name": "Valid Accounts", "tactic": "Initial Access / Persistence / Privilege Escalation / Defense Evasion", "url": "https://attack.mitre.org/techniques/T1078/",
             "why": "If the guessed credential was correct, the adversary now authenticates as a valid account, blending in with normal traffic.",
             "caveat": "Investigate, not confirmed. A success alone never proves compromise."},
            {"id": "T1021.004", "name": "Remote Services: SSH", "tactic": "Lateral Movement", "url": "https://attack.mitre.org/techniques/T1021/004/",
             "why": "SSH sessions established with compromised credentials are a common lateral-movement path; review follow-on activity from the session.",
             "caveat": "Only relevant if follow-on activity to other hosts is observed."},
        ],
        "false_positives": [
            "User fat-fingers a password several times, then logs in successfully.",
            "Automation retrying during a credential rotation, then succeeding with the new secret.",
            "A developer switching between machines or keys before the right one is used.",
        ],
        "triage": [
            "Verify the login with the account owner and check whether it was expected.",
            "Review surrounding authentication and endpoint events.",
            "Check for privilege changes, new keys, and unusual follow-on activity.",
            "Escalate and contain only according to approved procedures and evidence.",
        ],
    },
    "NX-SOC-003": {
        "name": "Possible SSH password spraying across multiple accounts", "severity": "medium",
        "logic": "Failed SSH logins targeting \u2265 5 distinct accounts from one source IP within 10 minutes.",
        "description": "One source touching many distinct accounts suggests a low-and-slow spray: try one common password across many users to stay under per-account lockout thresholds.",
        "techniques": [
            {"id": "T1110.003", "name": "Password Spraying", "tactic": "Credential Access", "url": "https://attack.mitre.org/techniques/T1110/003/",
             "why": "Many distinct usernames failed from a single source in a short window matches the spray pattern: breadth over depth to evade lockout policies.", "caveat": ""},
            {"id": "T1087", "name": "Account Discovery", "tactic": "Discovery", "url": "https://attack.mitre.org/techniques/T1087/",
             "why": "Attackers often probe which account names exist before spraying; a list of common service accounts may reflect prior enumeration.",
             "caveat": "Secondary hypothesis. SSH failure messages alone rarely confirm enumeration."},
        ],
        "false_positives": [
            "Shared jump host or bastion where several users mistype credentials around the same time.",
            "Orchestration tools iterating over service accounts with an expired shared secret.",
            "Penetration tests or purple-team exercises. Always check the change calendar.",
        ],
        "triage": [
            "Confirm whether the source IP is expected or belongs to approved infrastructure.",
            "Review authentication results for each targeted account and related hosts.",
            "Check for successful logins from the source IP and for activity across other systems.",
            "Escalate per the IR process; do not block solely on this alert.",
        ],
    },
}
