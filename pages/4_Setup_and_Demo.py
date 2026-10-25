import streamlit as st

from noxera_demo import state, theme

theme.setup("Setup and demo")
theme.hero("SECURITY OPERATIONS CENTER / 04", "Setup and live demo", "Synthetic-data policy, local setup, and a recruiter-ready walkthrough.", "PORTFOLIO")
st.success("This demo runs on synthetic authentication logs only. Every IP is from RFC 5737 documentation ranges "
           "(192.0.2.0/24, 198.51.100.0/24, 203.0.113.0/24). No real credentials, hostnames, or infrastructure data.")
steps = [
    ("Open the Alert explorer", "NX-SOC-002 (high) sits above the medium failure bursts. Severity drives the queue order."),
    ("Investigate 203.0.113.42", "Open the NX-SOC-002 alert. Walk the Event timeline: failures across admin/deploy/oracle/root/test, then a success as 'deploy'. Set Investigating and add a note."),
    ("Show the ATT&CK mapping", "T1110 Brute Force, T1078 Valid Accounts (investigate, not confirmed), T1021.004 SSH. Read one false-positive consideration aloud."),
    ("Triage the false positive", "Open NX-SOC-002 from 192.0.2.50 (svc-backup). A single service account retrying steadily suggests stale cron credentials. Mark Benign with a note."),
    ("Confirm the incident", "Mark the 203.0.113.42 alert Confirmed, then return to Overview. The dispositions and triage-complete metric update."),
    ("Explain the engineering", "Thresholds, sliding windows, spray detection across >= 5 accounts. 198.51.100.230 (typo then success) correctly produced no alert."),
]
st.subheader("5-minute recruiter demo script")
for i, (t, d) in enumerate(steps, 1):
    st.markdown(f'<div class="step"><div class="step-n">{i}</div><div><div class="step-t">{t}</div><div class="muted">{d}</div></div></div>', unsafe_allow_html=True)
st.subheader("Run locally")
st.code("git clone https://github.com/pluuug/noxera-soc-lab\ncd noxera-soc-lab\npip install -r requirements.txt\nstreamlit run app.py", language="bash")
st.caption("Triage is stored per browser session and, where the host allows, in reports/triage_demo.json. Hosted demos reset on restart.")
if st.button("Reset demo triage state"):
    state.reset()
    st.rerun()
