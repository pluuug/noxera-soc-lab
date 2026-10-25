import html
from datetime import timedelta

import pandas as pd
import streamlit as st

from noxera_demo import state, theme
from noxera_demo.engine import REFERENCE_NOW
from noxera_demo.reference import RULES, SEVERITY_COLOR, STATUS_COLOR, STATUSES

theme.setup("Alert explorer")
events, alerts = state.dataset()
theme.hero("SECURITY OPERATIONS CENTER / 02", "Alert explorer",
           "Filter by time window, status, severity, and rule. Select an alert to investigate.")

with st.sidebar:
    st.markdown('<div class="eyebrow">FILTERS</div>', unsafe_allow_html=True)
    window = st.selectbox("Time window", ["All (48h)", "Last 24 hours", "Last 6 hours", "Last 1 hour"])
    f_status = st.multiselect("Status", STATUSES, default=STATUSES)
    sevs = sorted({a["severity"] for a in alerts})
    f_sev = st.multiselect("Severity", sevs, default=sevs)
    f_rule = st.multiselect("Rule", sorted(RULES), default=sorted(RULES))
    st.caption(f"Windows are relative to {REFERENCE_NOW:%Y-%m-%d %H:%M} UTC (fixed demo clock).")

hours = {"Last 24 hours": 24, "Last 6 hours": 6, "Last 1 hour": 1}.get(window)
cut = REFERENCE_NOW - timedelta(hours=hours) if hours else None
shown = [a for a in alerts if state.status_of(a) in f_status and a["severity"] in f_sev
         and a["rule_id"] in f_rule and (cut is None or a["last_seen"] >= cut)]

fmt = lambda d: d.strftime("%b %d %H:%M:%S")
st.dataframe(pd.DataFrame([{"Severity": a["severity"], "Status": state.status_of(a), "Rule": a["rule_id"],
                            "Source IP": a["ip"], "First seen": fmt(a["first_seen"]), "Last seen": fmt(a["last_seen"]),
                            "Notes": sum(n["kind"] == "note" for n in state.notes_of(a))} for a in shown]),
             hide_index=True, width="stretch")
if not shown:
    st.info("No alerts match the current filters.")
    st.stop()

labels = {f"[{state.status_of(a)}] {a['rule_id']} | {a['ip']} | {fmt(a['last_seen'])}": a for a in shown}
a = labels[st.selectbox("Open alert", list(labels))]
ref = RULES[a["rule_id"]]
sc, stc = SEVERITY_COLOR.get(a["severity"], "#aab6c7"), STATUS_COLOR[state.status_of(a)]

st.markdown(f'<div class="panel"><span class="mono" style="color:#6ce5f2">{a["rule_id"]}</span> '
            f'{theme.badge(a["severity"], sc)}{theme.badge(state.status_of(a), stc)}'
            f'<h3 style="margin:.4rem 0 .2rem">{html.escape(a["title"])}</h3>'
            f'<span class="mono muted">SRC {a["ip"]} | {fmt(a["first_seen"])} to {a["last_seen"]:%H:%M:%S} UTC</span></div>',
            unsafe_allow_html=True)

st.markdown('<div class="eyebrow">DISPOSITION</div>', unsafe_allow_html=True)
cols = st.columns(len(STATUSES))
for col, s in zip(cols, STATUSES):
    if col.button(s, key=f"st_{a['key']}_{s}", disabled=(s == state.status_of(a)), width="stretch"):
        state.set_status(a, s)
        st.rerun()

t_inv, t_time, t_att = st.tabs(["Investigation", "Event timeline", "ATT&CK mapping"])

with t_inv:
    st.markdown(f'<div class="panel"><div class="panel-title">Evidence</div>{html.escape(a["evidence"])}</div>', unsafe_allow_html=True)
    f = st.columns(4)
    f[0].metric("Failed attempts", a["failed_attempts"])
    f[1].metric("Window", "10 min")
    if "distinct_accounts" in a:
        f[2].metric("Distinct accounts", a["distinct_accounts"])
    if "account" in a:
        f[2].metric("Account", a["account"])
    if a.get("targeted_users"):
        st.markdown("**Targeted users** " + "".join(f'<span class="chip">{html.escape(u)}</span>' for u in a["targeted_users"]), unsafe_allow_html=True)
    st.markdown('<div class="panel-title" style="margin-top:12px">Recommended triage</div>', unsafe_allow_html=True)
    for i, step in enumerate(ref["triage"], 1):
        st.markdown(f"`{i:02d}` {step}")
    st.markdown('<div class="panel-title" style="margin-top:12px">Analyst notes and activity</div>', unsafe_allow_html=True)
    with st.form(f"note_{a['key']}", clear_on_submit=True):
        txt = st.text_area("Note", placeholder="Record your findings...", label_visibility="collapsed")
        if st.form_submit_button("Save note") and txt.strip():
            state.add_note(a, txt)
            st.rerun()
    log = state.notes_of(a)
    if not log:
        st.caption("No activity yet. Notes and disposition changes appear here.")
    for n in reversed(log):
        st.markdown(f'<div class="ev" style="--c:#35445a"><span class="mono muted">{html.escape(n["author"])} | {n["ts"]}</span>'
                    f'<div>{html.escape(n["body"])}</div></div>', unsafe_allow_html=True)

with t_time:
    pad = timedelta(minutes=10)
    evs = [e for e in events if e["ip"] == a["ip"] and a["first_seen"] - pad <= e["ts"] <= a["last_seen"] + pad]
    st.caption(f"Raw synthetic SSH events from {a['ip']}, +/-10 minutes around the detection window ({len(evs)} events). Not every event is itself an alert.")
    out = '<div class="rail">'
    for e in evs:
        ok = e["result"] == "success"
        color = "#71e0b0" if ok else "#ff667d"
        out += (f'<div class="ev" style="--c:{color}"><span class="mono" style="color:{color}">{"SUCCESS" if ok else "FAILED"}</span> '
                f'<span class="mono">{html.escape(e["user"])}</span> <span class="mono muted">@ {e["host"]}</span>'
                f'<span class="mono muted" style="float:right">{fmt(e["ts"])}</span>'
                f'<code class="ev-raw">{html.escape(e["raw"])}</code></div>')
    st.markdown(out + "</div>", unsafe_allow_html=True)

with t_att:
    for t in ref["techniques"]:
        with st.expander(f"{t['id']} | {t['name']}", expanded=True):
            st.markdown(f"**Tactic:** {t['tactic']}  \n**Why it matches:** {t['why']}")
            if t["caveat"]:
                st.warning(t["caveat"])
            st.markdown(f"[View on attack.mitre.org]({t['url']})")
    st.markdown("**False-positive considerations**")
    for fp in ref["false_positives"]:
        st.markdown(f"- {fp}")
    st.caption("An ATT&CK mapping is a hypothesis for investigation, not proof of compromise.")
