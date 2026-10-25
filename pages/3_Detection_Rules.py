import streamlit as st

from noxera_demo import theme
from noxera_demo.reference import RULES, SEVERITY_COLOR

theme.setup("Detection rules")
theme.hero("SECURITY OPERATIONS CENTER / 03", "Detection rules", "Rule logic, MITRE ATT&CK mappings, rationale, and false-positive guidance.", "ATT&CK REFERENCE")
for rid, r in RULES.items():
    with st.expander(f"{rid} | {r['name']}", expanded=(rid == "NX-SOC-002")):
        st.markdown(theme.badge(r["severity"], SEVERITY_COLOR[r["severity"]]), unsafe_allow_html=True)
        st.markdown(f"**Logic:** {r['logic']}")
        st.write(r["description"])
        st.markdown("**ATT&CK techniques**")
        for t in r["techniques"]:
            st.markdown(f"- [{t['id']} {t['name']}]({t['url']}) ({t['tactic']}): {t['why']}" + (f" *{t['caveat']}*" if t["caveat"] else ""))
        c1, c2 = st.columns(2)
        c1.markdown("**False positives**\n" + "\n".join(f"- {x}" for x in r["false_positives"]))
        c2.markdown("**Recommended triage**\n" + "\n".join(f"{i}. {x}" for i, x in enumerate(r["triage"], 1)))
