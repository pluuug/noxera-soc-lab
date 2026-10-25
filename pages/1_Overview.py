import pandas as pd
import streamlit as st

from noxera_demo import theme
from noxera_demo.engine import REFERENCE_NOW, THRESHOLD
from noxera_demo.state import dataset, status_of

theme.setup("Overview")
events, alerts = dataset()
theme.hero("SECURITY OPERATIONS CENTER / 01", "Command overview",
           "A view of the synthetic 48-hour SSH dataset, detection output, and triage posture.")

failed = sum(e["result"] == "failed" for e in events)
triaged = sum(status_of(a) in ("Benign", "Confirmed") for a in alerts)
new = sum(status_of(a) == "New" for a in alerts)
c = st.columns(4)
c[0].metric("Auth events", len(events), f"{len(events) - failed} success / {failed} failed", delta_color="off")
c[1].metric("Active alerts", len(alerts), f"{new} awaiting triage", delta_color="off")
c[2].metric("High severity", sum(a["severity"] == "high" for a in alerts), "success after failure burst", delta_color="off")
c[3].metric("Triage complete", f"{round(100 * triaged / len(alerts)) if alerts else 0}%", f"{triaged} of {len(alerts)} dispositioned", delta_color="off")

left, right = st.columns([2, 1])
with left:
    st.markdown('<div class="panel-title">Authentication telemetry (hourly, UTC)</div>', unsafe_allow_html=True)
    df = pd.DataFrame(events)
    df["hour"] = df["ts"].dt.floor("h")
    hist = df.pivot_table(index="hour", columns="result", values="ip", aggfunc="count", fill_value=0)
    for col in ("failed", "success"):
        if col not in hist:
            hist[col] = 0
    st.bar_chart(hist[["failed", "success"]], color=["#ff667d", "#71e0b0"])
with right:
    st.markdown('<div class="panel-title">Dispositions</div>', unsafe_allow_html=True)
    counts = pd.Series([status_of(a) for a in alerts]).value_counts()
    for s in ["New", "Investigating", "Benign", "Confirmed"]:
        n = int(counts.get(s, 0))
        st.progress(n / len(alerts) if alerts else 0.0, text=f"{s}: {n}")

st.markdown('<div class="panel-title">Top source IPs (RFC 5737, synthetic)</div>', unsafe_allow_html=True)
g = df.groupby("ip")["result"].agg(Failed=lambda s: (s == "failed").sum(), Success=lambda s: (s == "success").sum())
g["Failure share %"] = (100 * g["Failed"] / (g["Failed"] + g["Success"])).round()
g = g.sort_values(["Failed", "Success"], ascending=False).head(6).reset_index().rename(columns={"ip": "Source IP"})
st.dataframe(g, hide_index=True, width="stretch",
             column_config={"Failure share %": st.column_config.ProgressColumn(min_value=0, max_value=100, format="%d%%")})
st.caption(f"Engine threshold: >= {THRESHOLD} failures / 10 min. Dataset anchored to {REFERENCE_NOW:%Y-%m-%d %H:%M} UTC so the demo never goes stale.")
