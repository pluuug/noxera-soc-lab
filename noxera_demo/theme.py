"""Shared NOXERA styling, matching the arena.ai demo design."""
import streamlit as st

NAME = "N\u00d8XERA"

CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
:root{--bg:#080b10;--panel:#10151e;--panel2:#131a25;--line:#263142;--line2:#2b394c;--muted:#8997aa;--ink:#edf2f8;--silver:#c7d0dc;--cyan:#6ce5f2;--red:#ff667d;--amber:#f4bd63;--mint:#71e0b0}
.stApp{background:radial-gradient(ellipse at 82% -12%,rgba(61,105,142,.16),transparent 38%),radial-gradient(ellipse at 4% 0%,rgba(108,229,242,.055),transparent 28%),var(--bg);color:var(--ink);font-family:'Manrope',sans-serif}
.stApp:before{content:"";position:fixed;inset:0;pointer-events:none;z-index:0;
 background-image:linear-gradient(rgba(108,229,242,.022) 1px,transparent 1px),linear-gradient(90deg,rgba(108,229,242,.022) 1px,transparent 1px);
 background-size:44px 44px;-webkit-mask-image:radial-gradient(ellipse at 50% 0%,black 20%,transparent 75%);mask-image:radial-gradient(ellipse at 50% 0%,black 20%,transparent 75%)}
[data-testid="stHeader"]{background:rgba(8,11,16,.84)}
[data-testid="stSidebar"]{background:linear-gradient(180deg,#0d121a,#090c12);border-right:1px solid var(--line)}
.block-container{padding-top:1.6rem;max-width:1500px}
h1,h2,h3,h4{color:var(--ink)!important;letter-spacing:-.03em}
p,label,[data-testid="stMarkdownContainer"]{color:#bdc7d5}
code,pre{font-family:'DM Mono',monospace!important}
[data-testid="stMetric"]{background:linear-gradient(145deg,rgba(20,28,40,.98),rgba(13,18,27,.98));border:1px solid #293548;border-radius:14px;padding:16px 18px}
[data-testid="stMetricLabel"] p{color:#9aa9bc!important;font-size:.68rem!important;text-transform:uppercase;letter-spacing:.13em;font-weight:800}
[data-testid="stMetricValue"]{color:#f4f7fb!important;font-weight:800}
.eyebrow{color:var(--cyan);font-family:'DM Mono',monospace;font-size:.68rem;letter-spacing:.17em;text-transform:uppercase}
.hero{border:1px solid var(--line2);border-radius:18px;padding:22px 26px;margin-bottom:18px;position:relative;overflow:hidden;background:linear-gradient(115deg,rgba(18,26,38,.98),rgba(10,15,23,.95))}
.hero:after{content:"";position:absolute;width:240px;height:240px;right:-70px;top:-125px;border:1px solid rgba(108,229,242,.15);border-radius:50%;box-shadow:0 0 0 28px rgba(108,229,242,.025),0 0 0 58px rgba(108,229,242,.02);pointer-events:none}
.hero-title{color:#f2f6fb;font-size:2.3rem;line-height:1.1;font-weight:800;letter-spacing:-.05em;margin:.3rem 0}
.hero-sub{color:#93a1b5;font-size:.92rem;max-width:720px;line-height:1.6}
.panel{border:1px solid var(--line);border-radius:14px;padding:16px 18px;margin-bottom:12px;background:linear-gradient(145deg,rgba(20,28,40,.92),rgba(13,18,27,.96))}
.panel-title{color:var(--silver);font-size:.74rem;font-weight:800;letter-spacing:.1em;text-transform:uppercase;margin-bottom:8px}
.badge{display:inline-block;border-radius:6px;border:1px solid;padding:2px 8px;font:500 .62rem 'DM Mono',monospace;letter-spacing:.12em;text-transform:uppercase;margin-right:6px}
.chip{display:inline-block;background:rgba(38,49,66,.7);color:var(--silver);border-radius:4px;padding:2px 7px;margin:2px 4px 2px 0;font:400 .72rem 'DM Mono',monospace}
.mono{font-family:'DM Mono',monospace}
.muted{color:var(--muted);font-size:.78rem}
.step{display:flex;gap:12px;border:1px solid var(--line);background:var(--panel2);border-radius:10px;padding:12px 14px;margin-bottom:10px}
.step-n{flex:0 0 28px;height:28px;border-radius:8px;border:1px solid rgba(108,229,242,.4);background:rgba(108,229,242,.1);color:var(--cyan);font:500 .72rem 'DM Mono',monospace;display:flex;align-items:center;justify-content:center}
.step-t{color:var(--ink);font-weight:700;font-size:.86rem}
.rail{position:relative;margin-left:10px;padding-left:26px;border-left:1px solid var(--line2)}
.ev{position:relative;border:1px solid var(--line);border-radius:12px;padding:10px 14px;margin:0 0 10px;background:linear-gradient(145deg,rgba(20,28,40,.92),rgba(13,18,27,.96))}
.ev:before{content:"";position:absolute;left:-34px;top:14px;width:14px;height:14px;border-radius:50%;background:#0b1017;border:2px solid var(--c)}
.ev-raw{display:block;margin-top:6px;background:rgba(0,0,0,.4);color:#9db0c6;border-radius:5px;padding:5px 9px;font:400 .68rem 'DM Mono',monospace;overflow-x:auto;white-space:nowrap}
.live{display:inline-flex;align-items:center;gap:8px;border:1px solid #2c6558;background:rgba(27,93,73,.18);color:#8ce9c4;border-radius:99px;padding:6px 11px;font:500 .66rem 'DM Mono',monospace;letter-spacing:.08em}
.live i{width:7px;height:7px;border-radius:50%;background:#71e0b0;box-shadow:0 0 10px rgba(113,224,176,.6)}
.stButton button,.stDownloadButton button{border:1px solid #35445a;border-radius:9px;background:#151e2b;color:#edf4fc}
.stButton button:hover{border-color:var(--cyan);color:#fff;background:#1a2938}
[data-testid="stDataFrame"]{border:1px solid #293548;border-radius:12px;overflow:hidden}
div[data-testid="stExpander"]{border:1px solid #283447;border-radius:12px;background:rgba(15,21,31,.8)}
footer,#MainMenu{visibility:hidden}
</style>
"""


def setup(title):
    st.set_page_config(page_title=f"{NAME} SOC | {title}", page_icon="\U0001F6E1", layout="wide")
    st.markdown(CSS, unsafe_allow_html=True)
    with st.sidebar:
        st.markdown(f'<div style="display:flex;align-items:center;gap:12px;padding:6px 0 14px"><div style="width:43px;height:43px;border:1px solid #526276;border-radius:13px;display:flex;align-items:center;justify-content:center;color:#eaf5ff;font-size:21px;font-weight:800;background:linear-gradient(145deg,#202c3d,#101620)">N</div><div><div style="color:#f3f6fb;font-weight:800;letter-spacing:.12em">{NAME}</div><div style="color:#7f8da1;font-size:.6rem;letter-spacing:.16em">SECURITY OPERATIONS</div></div></div>', unsafe_allow_html=True)
        st.divider()


def hero(eyebrow, title, sub, pill="SYNTHETIC DATA"):
    st.markdown(f'<div class="hero"><div style="display:flex;justify-content:space-between;align-items:start"><div class="eyebrow">{eyebrow}</div><span class="live"><i></i>{pill}</span></div><div class="hero-title">{title}</div><div class="hero-sub">{sub}</div></div>', unsafe_allow_html=True)


def badge(text, color):
    return f'<span class="badge" style="color:{color};border-color:{color}55;background:{color}14">{text}</span>'


def panel_open(title):
    st.markdown(f'<div class="panel"><div class="panel-title">{title}</div>', unsafe_allow_html=True)
