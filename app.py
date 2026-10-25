import json
from pathlib import Path

import pandas as pd
import streamlit as st

BASE_DIR = Path(__file__).resolve().parent
REPORT_PATH = BASE_DIR / "reports" / "alerts.json"

st.set_page_config(
    page_title="N\u00d8XERA SOC | Command Center",
    page_icon="\U0001F6E1",
    layout="wide",
    initial_sidebar_state="expanded",
)

# N\u00d8XERA dark command-center styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');

:root {
  --bg: #080b10;
  --panel: #10151e;
  --panel-2: #131a25;
  --line: #263142;
  --muted: #8997aa;
  --text: #edf2f8;
  --silver: #c7d0dc;
  --cyan: #6ce5f2;
  --red: #ff667d;
  --amber: #f4bd63;
  --green: #71e0b0;
}
.stApp {
  background:
    radial-gradient(ellipse at 82% -12%, rgba(61, 105, 142, .16), transparent 38%),
    radial-gradient(ellipse at 4% 0%, rgba(108, 229, 242, .055), transparent 28%),
    var(--bg);
  color: var(--text);
  font-family: 'Manrope', sans-serif;
}
[data-testid="stHeader"] { background: rgba(8,11,16,.84); }
[data-testid="stSidebar"] {
  background: linear-gradient(180deg, #0d121a 0%, #090c12 100%);
  border-right: 1px solid var(--line);
}
[data-testid="stSidebar"] > div { padding-top: 1.25rem; }
.block-container { padding-top: 1.6rem; padding-bottom: 2.5rem; max-width: 1600px; }
h1,h2,h3,h4 { color: var(--text) !important; letter-spacing: -.035em; }
p, label, [data-testid="stMarkdownContainer"] { color: #bdc7d5; }
code, pre, .mono { font-family: 'DM Mono', monospace !important; }
hr { border-color: var(--line); }
[data-testid="stMetric"] {
  background: linear-gradient(145deg, rgba(20,28,40,.98), rgba(13,18,27,.98));
  border: 1px solid #293548;
  border-radius: 14px;
  padding: 18px 20px;
  box-shadow: 0 12px 30px rgba(0,0,0,.12);
}
[data-testid="stMetricLabel"] p {
  color: #9aa9bc !important; font-size: .72rem !important;
  text-transform: uppercase; letter-spacing: .13em; font-weight: 800;
}
[data-testid="stMetricValue"] { color: #f4f7fb !important; font-weight: 800; }
[data-testid="stMetricDelta"] { font-size: .78rem; }
.soc-brand {
  display:flex; align-items:center; gap:12px; padding: 8px 0 18px;
}
.soc-mark {
  display:flex; align-items:center; justify-content:center;
  width:43px; height:43px; border:1px solid #526276; border-radius:13px;
  color:#eaf5ff; font-size:21px; font-weight:800;
  background:linear-gradient(145deg,#202c3d,#101620);
  box-shadow:inset 0 1px rgba(255,255,255,.06), 0 8px 24px rgba(0,0,0,.2);
}
.soc-brand-name { color:#f3f6fb; font-size:1.1rem; font-weight:800; letter-spacing:.12em; }
.soc-brand-sub { color:#7f8da1; font-size:.62rem; letter-spacing:.16em; margin-top:3px; }
.eyebrow { color:var(--cyan); font-family:'DM Mono',monospace; font-size:.68rem; letter-spacing:.17em; text-transform:uppercase; }
.hero-title { color:#f2f6fb; font-size:clamp(2rem,4vw,3.1rem); line-height:1.08; font-weight:800; letter-spacing:-.06em; margin:.35rem 0 .5rem; }
.hero-sub { color:#93a1b5; font-size:.94rem; max-width:700px; line-height:1.65; }
.hero-panel {
  border:1px solid #2b394c; border-radius:18px; padding:24px 26px;
  background:linear-gradient(115deg,rgba(18,26,38,.98),rgba(10,15,23,.95));
  position:relative; overflow:hidden; margin-bottom:20px;
}
.hero-panel:after {
  content:""; position:absolute; width:240px; height:240px; right:-70px; top:-125px;
  border:1px solid rgba(108,229,242,.15); border-radius:50%;
  box-shadow:0 0 0 28px rgba(108,229,242,.025),0 0 0 58px rgba(108,229,242,.02);
  pointer-events:none;
}
.live-pill {
  display:inline-flex; align-items:center; gap:8px; border:1px solid #2c6558;
  background:rgba(27,93,73,.18); color:#8ce9c4; border-radius:99px;
  padding:7px 11px; font:500 .68rem 'DM Mono',monospace; letter-spacing:.08em;
}
.live-dot { width:7px; height:7px; border-radius:50%; background:#71e0b0; box-shadow:0 0 10px rgba(113,224,176,.6); }
.section-head { display:flex; align-items:center; gap:10px; margin:24px 0 12px; }
.section-index { color:var(--cyan); font:500 .7rem 'DM Mono',monospace; }
.section-title { color:#e7edf5; font-size:.92rem; font-weight:800; letter-spacing:.07em; text-transform:uppercase; }
.section-note { color:#8290a4; font-size:.78rem; margin:0 0 14px; }
div[data-testid="stExpander"] {
  border:1px solid #283447; border-radius:12px; background:rgba(15,21,31,.8);
}
div[data-testid="stExpander"] summary { color:#eaf0f8; }
.stButton button, .stDownloadButton button {
  border:1px solid #35445a; border-radius:9px; background:#151e2b;
  color:#edf4fc; transition:all .15s ease;
}
.stButton button:hover, .stDownloadButton button:hover {
  border-color:var(--cyan); color:#fff; background:#1a2938;
}
div[data-testid="stMultiSelect"] [data-baseweb="tag"] {
  background:#1b3340; border:1px solid #2f6270;
}
input, textarea { color:#edf2f8 !important; }
[data-testid="stDataFrame"] { border:1px solid #293548; border-radius:12px; overflow:hidden; }
div[data-testid="stAlert"] { border-radius:10px; }
footer { visibility:hidden; }
#MainMenu { visibility:hidden; }
@media (max-width: 800px) {
  .block-container { padding-top:1rem; }
  .hero-panel { padding:19px; }
  .hero-title { font-size:2rem; }
}
</style>
""", unsafe_allow_html=True)


def load_report():
    if not REPORT_PATH.exists():
        return {}, (
            f"Report not found: {REPORT_PATH}. "
            "Run the analyzer first to generate it."
        )
    try:
        with REPORT_PATH.open("r", encoding="utf-8-sig") as file:
            data = json.load(file)
        if isinstance(data, list):
            return {"alerts": data}, None
        if not isinstance(data, dict):
            return {}, "The report must contain a JSON object or alert list."
        alerts = data.get("alerts", [])
        if not isinstance(alerts, list):
            return {}, "The report's 'alerts' field must be a list."
        return data, None
    except (OSError, json.JSONDecodeError) as exc:
        return {}, f"Could not read report: {exc}"


def text_value(value):
    if value is None:
        return "\u2014"
    if isinstance(value, (list, tuple, set)):
        return ", ".join(str(item) for item in value) or "\u2014"
    if isinstance(value, dict):
        return json.dumps(value, ensure_ascii=False)
    return str(value)


def alert_value(alert, *keys, default="\u2014"):
    for key in keys:
        value = alert.get(key)
        if value is not None and value != "":
            return value
    return default


def severity_of(alert):
    return str(alert_value(alert, "severity", "level", "priority", default="Unknown")).strip()


def rule_of(alert):
    return str(alert_value(alert, "rule_id", "detection_rule", "rule", "id", default="Unspecified"))


def source_of(alert):
    return str(alert_value(alert, "source_ip", "src_ip", "source", "src", default="Unknown"))


def title_of(alert):
    return str(alert_value(alert, "title", "name", "alert_name", "description", default="Detection alert"))


def evidence_of(alert):
    return alert_value(alert, "evidence", "details", "matched_events")


def rule_name(rule_id):
    names = {
        "NX-SOC-001": "Repeated SSH failures",
        "NX-SOC-002": "Failure then success",
        "NX-SOC-003": "Password spraying",
    }
    return names.get(rule_id, "Other detection")


def severity_color(severity):
    level = severity.lower()
    if level in {"critical", "severe"}:
        return "#ff667d"
    if level == "high":
        return "#ff8b70"
    if level in {"medium", "moderate"}:
        return "#f4bd63"
    if level == "low":
        return "#71e0b0"
    return "#aab6c7"


def section_heading(index, title, note=None):
    st.markdown(
        f'<div class="section-head"><span class="section-index">{index}</span>'
        f'<span class="section-title">{title}</span></div>',
        unsafe_allow_html=True,
    )
    if note:
        st.markdown(f'<div class="section-note">{note}</div>', unsafe_allow_html=True)


report, load_error = load_report()
alerts = [item for item in report.get("alerts", []) if isinstance(item, dict)]

with st.sidebar:
    st.markdown(
        '<div class="soc-brand"><div class="soc-mark">N</div><div>'
        '<div class="soc-brand-name">N\u00d8XERA</div>'
        '<div class="soc-brand-sub">SECURITY OPERATIONS</div></div></div>',
        unsafe_allow_html=True,
    )
    st.divider()
    st.markdown('<div class="eyebrow">WORKSPACE</div>', unsafe_allow_html=True)
    st.markdown("**\u25c8  Command overview**")
    st.markdown("**\u2315  Alert explorer**")
    st.markdown("**\u25ce  Investigation queue**")
    st.markdown("**\u2318  Detection rules**")
    st.divider()
    st.markdown('<div class="eyebrow">DATA PIPELINE</div>', unsafe_allow_html=True)
    st.caption("LOCAL REPORT")
    st.code("reports/alerts.json", language="text")
    if st.button("\u21bb  Refresh report", width="stretch"):
        st.rerun()
    st.caption("Environment")
    st.markdown("`LOCAL / SYNTHETIC DATA`")
    st.divider()
    st.caption("N\u00d8XERA SOC LAB \u00b7 BUILD 01")

st.markdown(
    '<div class="hero-panel"><div class="eyebrow">SECURITY OPERATIONS CENTER / 001</div>'
    '<div class="hero-title">Threat visibility.<br>Without the noise.</div>'
    '<div class="hero-sub">Authentication telemetry, detection signals, and investigation context '
    'in one focused command center.</div></div>',
    unsafe_allow_html=True,
)

head_left, head_right = st.columns([3, 1])
with head_left:
    section_heading("01", "Command overview", "A live view of the most recently generated local report.")
with head_right:
    st.markdown(
        '<div style="text-align:right;padding-top:16px"><span class="live-pill">'
        '<span class="live-dot"></span> REPORT LOADED</span></div>',
        unsafe_allow_html=True,
    )

if load_error:
    st.error(load_error)
    st.info("Run the authentication log analyzer from your project folder, then refresh this dashboard.")
    st.stop()

high_alerts = sum(severity_of(a).lower() in {"high", "critical", "severe"} for a in alerts)
critical_alerts = sum(severity_of(a).lower() in {"critical", "severe"} for a in alerts)
source_ips = {source_of(a) for a in alerts if source_of(a) != "Unknown"}
event_count = report.get("input_event_count", report.get("total_events", report.get("event_count")))
if event_count is None:
    summary = report.get("summary", {})
    event_count = summary.get("input_event_count", "\u2014") if isinstance(summary, dict) else "\u2014"

m1, m2, m3, m4 = st.columns(4)
m1.metric("Total detections", len(alerts), help="Total alerts in the current report")
m2.metric("High / critical", high_alerts, delta=f"{critical_alerts} critical", delta_color="inverse")
m3.metric("Unique source IPs", len(source_ips))
m4.metric("Events analyzed", text_value(event_count))

section_heading("02", "Detection telemetry", "Breakdown of findings by severity and analytic rule.")
if not alerts:
    st.success("No alerts in the current report. Run the analyzer to inspect your sample logs.")
    st.stop()

chart_left, chart_right = st.columns([1, 1], gap="large")
with chart_left:
    with st.container(border=True):
        st.markdown("#### Severity distribution")
        severity_order = ["Critical", "High", "Medium", "Low", "Unknown"]
        severity_counts = {}
        for alert in alerts:
            label = severity_of(alert).title()
            severity_counts[label] = severity_counts.get(label, 0) + 1
        ordered = [{"Severity": s, "Alerts": severity_counts[s]} for s in severity_order if severity_counts.get(s)]
        ordered += [{"Severity": s, "Alerts": n} for s, n in severity_counts.items() if s not in severity_order]
        st.bar_chart(pd.DataFrame(ordered).set_index("Severity"), height=245)
        st.caption("Prioritize critical and high-severity findings first.")
with chart_right:
    with st.container(border=True):
        st.markdown("#### Detection rule activity")
        rule_counts = {}
        for alert in alerts:
            rule_id = rule_of(alert)
            label = f"{rule_id} \u00b7 {rule_name(rule_id)}"
            rule_counts[label] = rule_counts.get(label, 0) + 1
        rule_df = pd.DataFrame([{"Detection rule": k, "Alerts": v} for k, v in rule_counts.items()])
        st.bar_chart(rule_df.set_index("Detection rule"), height=245)
        st.caption("Counts reflect alerts in the generated JSON report.")

section_heading("03", "Alert explorer", "Filter, search, and open an alert to review evidence and triage context.")
with st.container(border=True):
    f1, f2, f3 = st.columns(3)
    severities = sorted({severity_of(a) for a in alerts})
    rules = sorted({rule_of(a) for a in alerts})
    sources = sorted({source_of(a) for a in alerts})
    with f1:
        selected_severities = st.multiselect("Severity", severities, default=severities, key="severity_filter")
    with f2:
        selected_rules = st.multiselect("Detection rule", rules, default=rules, key="rule_filter")
    with f3:
        selected_sources = st.multiselect("Source IP", sources, default=sources, key="source_filter")
    search = st.text_input("Search findings", placeholder="Search title, IP, account, evidence, or rule ID...").strip().lower()

filtered = []
for alert in alerts:
    if severity_of(alert) not in selected_severities:
        continue
    if rule_of(alert) not in selected_rules:
        continue
    if source_of(alert) not in selected_sources:
        continue
    if search and search not in json.dumps(alert, ensure_ascii=False, default=str).lower():
        continue
    filtered.append(alert)

count_left, count_right = st.columns([3, 1])
with count_left:
    st.markdown(f"**{len(filtered)}** findings shown <span style='color:#8190a4'>/ {len(alerts)} total</span>", unsafe_allow_html=True)
with count_right:
    st.download_button(
        "Export filtered JSON",
        data=json.dumps(filtered, indent=2, ensure_ascii=False, default=str),
        file_name="noxera-filtered-alerts.json",
        mime="application/json",
        width="stretch",
    )

if filtered:
    table_rows = []
    for index, alert in enumerate(filtered, start=1):
        table_rows.append({
            "Severity": severity_of(alert).upper(),
            "Rule": rule_of(alert),
            "Detection": title_of(alert),
            "Source IP": source_of(alert),
            "Account": text_value(alert_value(alert, "account", "username", "user", default="\u2014")),
            "Timestamp": text_value(alert_value(alert, "timestamp", "time", "first_seen")),
        })
    st.dataframe(pd.DataFrame(table_rows), width="stretch", hide_index=True)

    section_heading("04", "Investigation queue", "Expand a finding to inspect evidence, targets, and available triage notes.")
    for index, alert in enumerate(filtered, start=1):
        sev = severity_of(alert)
        color = severity_color(sev)
        heading = f"{sev.upper()}  \u00b7  {rule_of(alert)}  \u00b7  {title_of(alert)}"
        with st.expander(heading, expanded=(len(filtered) == 1)):
            st.markdown(
                f'<div style="display:inline-block;border:1px solid {color};color:{color};'
                f'background:{color}12;border-radius:6px;padding:5px 9px;'
                f'font:500 .7rem DM Mono,monospace;letter-spacing:.08em">'
                f'{sev.upper()} SEVERITY</div>',
                unsafe_allow_html=True,
            )
            d1, d2 = st.columns(2)
            with d1:
                st.markdown("##### Finding details")
                st.write("**Timestamp:**", text_value(alert_value(alert, "timestamp", "time", "first_seen")))
                st.write("**Source IP:**", source_of(alert))
                st.write("**Detection rule:**", f"{rule_of(alert)} \u00b7 {rule_name(rule_of(alert))}")
                st.write("**Severity:**", sev.title())
            with d2:
                st.markdown("##### Accounts and targets")
                found_target = False
                for key in ("targeted_users", "targeted_accounts", "account", "username",
                            "distinct_accounts_targeted", "user"):
                    if key in alert:
                        st.write(f"**{key.replace('_', ' ').title()}:**", text_value(alert[key]))
                        found_target = True
                if not found_target:
                    st.caption("No account or target fields were included in this alert.")
            st.markdown("##### Evidence")
            evidence = evidence_of(alert)
            if isinstance(evidence, (dict, list)):
                st.json(evidence)
            else:
                st.write(text_value(evidence))
            for key in ("mitre_attack", "mitre", "recommended_triage", "recommendations", "related_events"):
                if key in alert:
                    st.markdown(f"##### {key.replace('_', ' ').title()}")
                    value = alert[key]
                    if isinstance(value, list):
                        for item in value:
                            st.markdown(f"- {text_value(item)}")
                    elif isinstance(value, dict):
                        st.json(value)
                    else:
                        st.write(text_value(value))
            with st.expander("Raw alert JSON"):
                st.json(alert)
else:
    st.warning("No alerts match these filters. Try widening your selection.")

section_heading("05", "Detection rule reference", "The three analytics currently included in this lab.")
rule_reference = [
    {"Rule ID": "NX-SOC-001", "Detection": "Repeated SSH failures", "Purpose": "Identify repeated authentication failures in a time window."},
    {"Rule ID": "NX-SOC-002", "Detection": "Failure then success", "Purpose": "Flag a successful SSH login after repeated failures."},
    {"Rule ID": "NX-SOC-003", "Detection": "Password spraying", "Purpose": "Identify failures across multiple distinct accounts."},
]
st.dataframe(pd.DataFrame(rule_reference), width="stretch", hide_index=True)

st.divider()
st.markdown(
    '<div style="display:flex;justify-content:space-between;gap:12px;flex-wrap:wrap;'
    'color:#718096;font: .68rem DM Mono,monospace;letter-spacing:.06em">'
    '<span>N\u00d8XERA SOC LAB \u00b7 LOCAL ANALYSIS ONLY</span>'
    '<span>USE SYNTHETIC OR AUTHORIZED SECURITY LOGS</span></div>',
    unsafe_allow_html=True,
)
st.caption("Alerts are investigation leads, not proof of compromise. This dashboard displays findings; it does not block traffic.")
