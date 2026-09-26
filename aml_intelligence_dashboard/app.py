from pathlib import Path
import json, html
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

TEAM_ID = "9812BA55"
DATA = Path(__file__).parent / "data"

st.set_page_config(
    page_title="AML Intelligence | Team 9812BA55",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ============================================================
# PREMIUM FINTECH / AML UI
# ============================================================
st.markdown("""
<style>
:root{
  --bg:#071019;
  --panel:#0b1722;
  --panel2:#0e1d2a;
  --line:rgba(255,255,255,.085);
  --line2:rgba(125,211,252,.18);
  --text:#eef6fb;
  --muted:#9bb0bf;
  --cyan:#7dd3fc;
  --emerald:#58e0b7;
  --amber:#ffd166;
  --red:#ff8585;
}
html, body, [class*="css"] { font-family: Inter, ui-sans-serif, system-ui, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif; }

.stApp {
  background:
    radial-gradient(circle at 4% 0%, rgba(56,189,248,.10), transparent 26%),
    radial-gradient(circle at 95% 4%, rgba(16,185,129,.065), transparent 24%),
    linear-gradient(180deg,#071019 0%,#071019 72%,#08121a 100%) !important;
  color:var(--text) !important;
}
[data-stale="true"], [data-stale="true"] * { opacity:1 !important; filter:none !important; }

[data-testid="stSidebar"] {
  background:linear-gradient(180deg,#091520,#08121b) !important;
  border-right:1px solid var(--line) !important;
}
[data-testid="stSidebar"] * { color:#dce9f5 !important; opacity:1 !important; }
[data-testid="stSidebar"] [role="radiogroup"] > label {
  border-radius:10px !important;
  padding:.38rem .55rem !important;
  margin:.05rem 0 !important;
}
[data-testid="stSidebar"] [role="radiogroup"] > label:hover {
  background:rgba(125,211,252,.07) !important;
}
[data-testid="stSidebar"] [role="radiogroup"] label:has(input:checked) {
  background:linear-gradient(90deg,rgba(125,211,252,.12),rgba(88,224,183,.06)) !important;
  border:1px solid rgba(125,211,252,.16) !important;
}
[data-testid="stMarkdownContainer"] p,
[data-testid="stMarkdownContainer"] li { color:#d6e2eb; }
.block-container { padding-top:1.35rem; padding-bottom:3rem; max-width:1480px; }

.brand {
  display:flex;align-items:center;gap:10px;margin:2px 0 2px;
}
.brandmark {
  width:32px;height:32px;border-radius:9px;display:flex;align-items:center;justify-content:center;
  background:linear-gradient(135deg,rgba(125,211,252,.18),rgba(88,224,183,.14));
  border:1px solid rgba(125,211,252,.22);font-weight:800;color:#bdeaff;
}
.brandtitle { font-size:1.02rem;font-weight:800;color:#f5fbff;line-height:1; }
.brandsub { font-size:.72rem;color:#8298a9;margin-top:4px; }

.hero {
  position:relative;overflow:hidden;
  padding:25px 28px 23px;
  border:1px solid var(--line);
  background:
    linear-gradient(115deg,rgba(17,54,79,.74),rgba(8,26,39,.77) 55%,rgba(8,35,36,.68));
  border-radius:20px;margin-bottom:14px;
  box-shadow:0 18px 55px rgba(0,0,0,.18);
}
.hero:after {
  content:"";position:absolute;width:280px;height:280px;border-radius:50%;
  right:-120px;top:-155px;background:rgba(88,224,183,.08);filter:blur(2px);
}
.eyebrow { color:#8bdcff;font-size:.73rem;font-weight:800;letter-spacing:.17em;text-transform:uppercase; }
.hero h1 { margin:5px 0 7px;font-size:2.12rem;color:#f7fbfe;line-height:1.06;letter-spacing:-.025em; }
.hero p { color:#aac0cf !important;margin:0;max-width:900px;font-size:.97rem; }
.hero-meta { margin-top:12px;display:flex;gap:8px;flex-wrap:wrap; }
.badge {
  display:inline-flex;align-items:center;gap:6px;border:1px solid rgba(125,211,252,.24);
  color:#c8efff;background:rgba(8,20,31,.28);border-radius:999px;padding:5px 9px;font-size:.76rem;
}
.dot { width:6px;height:6px;border-radius:50%;background:var(--emerald);box-shadow:0 0 10px rgba(88,224,183,.55); }

.kpi-grid { display:grid;grid-template-columns:repeat(4,1fr);gap:11px;margin:10px 0 19px; }
.kpi {
  position:relative;overflow:hidden;
  background:linear-gradient(180deg,rgba(255,255,255,.050),rgba(255,255,255,.022));
  border:1px solid var(--line);border-radius:15px;padding:16px 17px;
}
.kpi:before { content:"";position:absolute;left:0;top:0;bottom:0;width:2px;background:rgba(125,211,252,.36); }
.kpi .label { color:#9cb0bf;font-size:.78rem;font-weight:700;text-transform:uppercase;letter-spacing:.05em; }
.kpi .value { color:#f8fcff;font-size:1.72rem;font-weight:820;margin-top:7px;line-height:1;letter-spacing:-.025em; }
.kpi .delta { color:var(--emerald);font-size:.77rem;margin-top:8px; }

.cap-grid { display:grid;grid-template-columns:repeat(3,1fr);gap:11px;margin:9px 0 22px; }
.cap {
  background:rgba(255,255,255,.025);border:1px solid var(--line);border-radius:14px;padding:15px 16px;
}
.cap-num {
  width:27px;height:27px;border-radius:8px;background:rgba(125,211,252,.09);
  border:1px solid rgba(125,211,252,.18);color:#9be4ff;display:flex;align-items:center;justify-content:center;
  font-size:.75rem;font-weight:800;margin-bottom:10px;
}
.cap-title { color:#f0f7fb;font-weight:760;font-size:.95rem; }
.cap-text { color:#94a9b8;font-size:.83rem;margin-top:5px;line-height:1.45; }

.section-head {
  display:flex;align-items:flex-end;justify-content:space-between;gap:12px;margin:22px 0 10px;
}
.section-title { color:#f3f8fc;font-size:1.16rem;font-weight:800;letter-spacing:-.01em; }
.section-sub { color:#8fa3b2;font-size:.82rem; }

.note {
  border:1px solid var(--line);background:rgba(255,255,255,.028);
  border-radius:13px;padding:13px 15px;color:#b5c6d2;margin-bottom:14px;font-size:.88rem;
}
.info-row {
  display:grid;grid-template-columns:1.2fr 1fr;gap:11px;margin:8px 0 17px;
}
.info-card {
  background:rgba(255,255,255,.025);border:1px solid var(--line);border-radius:14px;padding:15px 16px;
}
.info-card h4 { margin:0 0 7px;color:#f0f7fb;font-size:.92rem; }
.info-card p { margin:0;color:#95aaba !important;font-size:.83rem;line-height:1.48; }

.alert-head {
  display:flex;justify-content:space-between;align-items:center;gap:15px;padding:17px 18px;
  background:linear-gradient(110deg,rgba(255,255,255,.04),rgba(255,255,255,.018));
  border:1px solid var(--line);border-radius:14px;margin:10px 0 13px;
}
.alert-id { color:#f5fbff;font-size:1.05rem;font-weight:800; }
.alert-meta { color:#8fa4b4;font-size:.79rem;margin-top:3px; }
.risk-chip { padding:7px 10px;border-radius:999px;font-size:.76rem;font-weight:850;letter-spacing:.05em; }
.risk-high { background:rgba(255,133,133,.10);border:1px solid rgba(255,133,133,.24);color:#ff9a9a; }
.risk-medium { background:rgba(255,209,102,.10);border:1px solid rgba(255,209,102,.24);color:#ffda7b; }
.risk-low { background:rgba(88,224,183,.10);border:1px solid rgba(88,224,183,.24);color:#6be9c1; }

.pipeline { display:grid;grid-template-columns:repeat(5,1fr);gap:9px;margin:12px 0 19px; }
.pipe {
  position:relative;background:rgba(255,255,255,.025);border:1px solid var(--line);
  border-radius:13px;padding:14px 13px;min-height:112px;
}
.pipe-step { color:#7dd3fc;font-size:.68rem;font-weight:850;letter-spacing:.09em; }
.pipe-title { color:#f2f8fc;font-size:.88rem;font-weight:760;margin-top:8px; }
.pipe-text { color:#8fa4b4;font-size:.76rem;line-height:1.4;margin-top:5px; }

.table-label { color:#8fa5b4;font-size:.78rem;margin-bottom:6px; }
.good { color:var(--emerald);font-weight:800; }
.warn { color:var(--amber);font-weight:800; }
.high { color:var(--red);font-weight:800; }

div[data-testid="stDataFrame"] { border:1px solid var(--line);border-radius:13px;overflow:hidden; }
[data-testid="stMetricLabel"],[data-testid="stMetricValue"],[data-testid="stMetricDelta"] {
  color:#eef5fb !important;opacity:1 !important;
}
.stTextInput input {
  background:#0b1722 !important;color:#eef5fb !important;border:1px solid rgba(255,255,255,.10) !important;
}

@media (max-width:980px) {
  .kpi-grid{grid-template-columns:repeat(2,1fr)} .cap-grid{grid-template-columns:1fr}
  .pipeline{grid-template-columns:1fr 1fr}.info-row{grid-template-columns:1fr}
}
@media (max-width:620px) {
  .kpi-grid{grid-template-columns:1fr}.pipeline{grid-template-columns:1fr}
  .hero h1{font-size:1.72rem}.hero{padding:20px 18px}
}
</style>
""", unsafe_allow_html=True)

PLOT = dict(
    template="plotly_dark",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(255,255,255,.012)",
    font=dict(color="#d8e5ee", size=12),
    margin=dict(l=20,r=20,t=50,b=28),
    hoverlabel=dict(bgcolor="#10202d", font_color="#f3f8fc"),
)
PLOT_CONFIG = {"displayModeBar": False, "responsive": True, "scrollZoom": False}

@st.cache_data(show_spinner=False)
def jload(name):
    return json.loads((DATA/name).read_text(encoding="utf-8"))

@st.cache_data(show_spinner=False)
def csv(name, **kwargs):
    return pd.read_csv(DATA/name, **kwargs)

S = jload("summary.json")

def hero(title, subtitle):
    st.markdown(f"""
    <div class="hero">
      <div class="eyebrow">AML ALERT ESCALATION · TEAM {TEAM_ID}</div>
      <h1>{html.escape(title)}</h1>
      <p>{html.escape(subtitle)}</p>
      <div class="hero-meta">
        <span class="badge"><span class="dot"></span>System online</span>
        <span class="badge">ROC-AUC optimized</span>
        <span class="badge">Behavior-driven ranking</span>
        <span class="badge">Synthetic AML data</span>
      </div>
    </div>""", unsafe_allow_html=True)

def kpis(items):
    cards=[]
    for label,value,delta in items:
        d=f'<div class="delta">{html.escape(delta)}</div>' if delta else ""
        cards.append(f'<div class="kpi"><div class="label">{html.escape(label)}</div>'
                     f'<div class="value">{html.escape(value)}</div>{d}</div>')
    st.markdown('<div class="kpi-grid">'+''.join(cards)+'</div>',unsafe_allow_html=True)

def section(title, sub=""):
    st.markdown(
        f'<div class="section-head"><div class="section-title">{html.escape(title)}</div>'
        f'<div class="section-sub">{html.escape(sub)}</div></div>',
        unsafe_allow_html=True
    )

def style_fig(fig, height=390):
    fig.update_layout(**PLOT,height=height,legend_title_text="")
    fig.update_xaxes(gridcolor="rgba(255,255,255,.065)",zeroline=False)
    fig.update_yaxes(gridcolor="rgba(255,255,255,.065)",zeroline=False)
    return fig

def plot(fig):
    st.plotly_chart(fig,use_container_width=True,config=PLOT_CONFIG)

def risk_band(v):
    if v>=.80:return "HIGH RISK","risk-high"
    if v>=.50:return "MEDIUM RISK","risk-medium"
    return "LOW RISK","risk-low"

st.sidebar.markdown("""
<div class="brand">
  <div class="brandmark">◈</div>
  <div><div class="brandtitle">AML Intelligence</div><div class="brandsub">Behavioral risk analytics</div></div>
</div>
""", unsafe_allow_html=True)
st.sidebar.markdown("<div style='height:12px'></div>",unsafe_allow_html=True)
page=st.sidebar.radio(
    "Workspace",
    ["Executive Summary","Exploratory Analysis","Behavior Intelligence",
     "Risk Explorer","Model Intelligence","Methodology & Integrity"],
    label_visibility="collapsed"
)
st.sidebar.markdown("---")
st.sidebar.markdown(f"<div style='font-size:.73rem;color:#8499a8'>TEAM</div><div style='font-weight:800'>9812BA55</div>",unsafe_allow_html=True)
st.sidebar.markdown("<div style='margin-top:9px;font-size:.76rem;color:#58e0b7'>● System online</div>",unsafe_allow_html=True)
st.sidebar.caption("Synthetic/transformed hackathon data. Analytical artifact — not a production AML decision system.")

if page=="Executive Summary":
    hero("Alert Escalation Intelligence",
         "Behavior-driven prioritization for AML alerts — built to help investigators focus attention where escalation risk is highest.")
    kpis([
      ("Train alerts",f'{S["train_alerts"]:,}',"labeled signals"),
      ("Escalation rate",f'{S["escalation_rate"]:.2%}',f'{S["positive_alerts"]:,} escalated'),
      ("Validated ROC-AUC",f'{S["v2_best_auc"]:.4f}',f'+{S["delta_vs_v1"]:.4f} vs V1'),
      ("Hidden-test alerts",f'{S["test_alerts"]:,}',"continuous risk scores"),
    ])

    st.markdown("""
    <div class="cap-grid">
      <div class="cap"><div class="cap-num">01</div><div class="cap-title">Detect behavioral change</div>
      <div class="cap-text">Compare recent alert-linked activity with its historical transaction pattern.</div></div>
      <div class="cap"><div class="cap-num">02</div><div class="cap-title">Rank suspicious alerts</div>
      <div class="cap-text">Use ensemble risk scores to prioritize alerts instead of treating every signal equally.</div></div>
      <div class="cap"><div class="cap-num">03</div><div class="cap-title">Support investigator review</div>
      <div class="cap-text">Surface interpretable behavioral evidence while keeping human review in the loop.</div></div>
    </div>
    """,unsafe_allow_html=True)

    monthly=csv("monthly.csv");bands=csv("risk_bands.csv")
    section("Portfolio snapshot","volume and hidden-test ranking structure")
    c1,c2=st.columns([1.15,1])
    with c1:
        fig=px.bar(monthly,x="year_month",y="alerts",title="Alert volume by signal month",
                   labels={"year_month":"Signal month","alerts":"Alerts"})
        plot(style_fig(fig,380))
    with c2:
        fig=px.pie(bands,names="risk_band",values="alerts",hole=.68,title="Hidden-test risk bands")
        fig.update_traces(textinfo="percent+label")
        plot(style_fig(fig,380))

    section("Model progress","OOF validation")
    perf=csv("model_perf.csv")
    fig=px.bar(perf,x="model",y="auc",text="auc",title="Validated ROC-AUC by model")
    fig.update_traces(texttemplate="%{text:.4f}",textposition="outside")
    fig.update_yaxes(range=[max(.50,perf["auc"].min()-.025),perf["auc"].max()+.012])
    plot(style_fig(fig,390))

elif page=="Exploratory Analysis":
    hero("Exploratory Analysis","Class balance, seasonality and score structure — pre-aggregated for a fast public dashboard.")
    cls=csv("class_distribution.csv");monthly=csv("monthly.csv");weekday=csv("weekday.csv");hist=csv("risk_hist.csv")

    section("Target structure","what the labeled data looks like")
    c1,c2=st.columns(2)
    with c1:
        fig=px.bar(cls,x="class",y="alerts",text="alerts",title="Target class distribution")
        plot(style_fig(fig))
    with c2:
        fig=px.line(monthly,x="year_month",y="escalation_rate",markers=True,title="Monthly escalation rate")
        fig.update_yaxes(tickformat=".0%")
        plot(style_fig(fig))

    section("Timing & score shape","calendar patterns and hidden-test ranking")
    c3,c4=st.columns(2)
    with c3:
        fig=px.bar(weekday,x="day_of_week",y="escalation_rate",text="alerts",title="Escalation rate by weekday")
        fig.update_yaxes(tickformat=".0%")
        plot(style_fig(fig))
    with c4:
        fig=px.bar(hist,x="bin_mid",y="count",title="Hidden-test risk-score distribution",
                   labels={"bin_mid":"Risk score","count":"Alerts"})
        plot(style_fig(fig))

    section("Risk concentration","how much escalation is concentrated near the top")
    lift=csv("lift.csv")
    lift["Escalation rate"]=lift["escalation_rate"].map(lambda x:f"{x:.2%}")
    lift["Lift vs base"]=lift["lift_vs_base"].map(lambda x:f"{x:.2f}×")
    st.dataframe(lift[["segment","alerts","Escalation rate","Lift vs base"]]
                 .rename(columns={"segment":"Top risk segment","alerts":"Alerts"}),use_container_width=True,hide_index=True)
    st.caption("Interpretability table uses the OOF demo artifact currently available; the headline V2 ROC-AUC remains the stronger validated benchmark.")

elif page=="Behavior Intelligence":
    hero("Behavior Intelligence","Translate model evidence into investigator-friendly behavioral themes without serving millions of raw transactions.")
    st.markdown("""
    <div class="info-row">
      <div class="info-card"><h4>Why behavior matters</h4><p>AML escalation may emerge as a change in timing,
      direction, transaction type or amount distribution — not only as a large absolute value.</p></div>
      <div class="info-card"><h4>Why the public app stays fast</h4><p>Heavy transaction feature engineering runs offline.
      This site loads only compact, precomputed evidence and model diagnostics.</p></div>
    </div>""",unsafe_allow_html=True)

    fam=csv("feature_family_importance.csv")
    section("Behavioral evidence map","importance aggregated by feature family")
    fig=px.bar(fam.sort_values("importance"),x="importance",y="family",orientation="h",title="Feature importance by behavioral family")
    plot(style_fig(fig,430))

    top=csv("top_features.csv").head(18).sort_values("importance")
    section("Top evidence","human-readable labels with technical feature names retained")
    fig=px.bar(top,x="importance",y="human_label",orientation="h",color="family",
               hover_data={"feature":True,"human_label":False,"importance":":.2f"},
               title="Top behavioral signals")
    plot(style_fig(fig,610))

    st.markdown("""
    <div class="note"><b>Interpretation:</b> strong features include direction × amount behavior,
    transaction-type statistics and recent-vs-historical distribution shifts. This supports the core hypothesis:
    escalation risk is partly expressed through <b>behavioral change</b>, not just total activity.</div>
    """,unsafe_allow_html=True)

elif page=="Risk Explorer":
    hero("Risk Explorer","Inspect an alert's score context with a lightweight investigator-style view.")
    source=st.radio("Dataset",["Hidden test predictions","Train OOF demo"],horizontal=True)

    if source=="Hidden test predictions":
        df=csv("risk_test.csv",dtype={"signal_id":"string"})
        default=str(df.sort_values("ehtimollik",ascending=False).iloc[0]["signal_id"])
        sid=st.text_input("Signal ID",value=default,help="Paste a signal_id from the test set.")
        m=df[df["signal_id"].astype(str)==sid.strip()]
        if m.empty:
            st.warning("Signal ID not found. Example: "+default)
        else:
            r=m.iloc[0];score=float(r["ehtimollik"]);band,css=risk_band(score)
            percentile=float((df["ehtimollik"]<=score).mean())
            st.markdown(f"""
            <div class="alert-head">
              <div><div class="alert-id">{html.escape(str(r["signal_id"]))}</div>
              <div class="alert-meta">Signal date · {pd.to_datetime(r["signal_sanasi"]).date()} · Hidden test</div></div>
              <div class="risk-chip {css}">{band}</div>
            </div>""",unsafe_allow_html=True)
            kpis([
              ("Risk score",f"{score:.4f}","continuous ranking score"),
              ("Risk percentile",f"{percentile:.1%}","within hidden test"),
              ("Risk band",band.replace(" RISK",""),"dashboard interpretation"),
              ("Dataset","Hidden test","unlabeled"),
            ])
            c1,c2=st.columns([.8,1.2])
            with c1:
                fig=go.Figure(go.Indicator(mode="gauge+number",value=percentile*100,number={"suffix":"%"},
                  title={"text":"Score percentile"},gauge={"axis":{"range":[0,100]}}))
                plot(style_fig(fig,300))
            with c2:
                nearby=df.iloc[(df["ehtimollik"]-score).abs().argsort()[:8]][["signal_id","signal_sanasi","ehtimollik"]].sort_values("ehtimollik",ascending=False)
                st.markdown("#### Similar-scored alerts")
                st.dataframe(nearby,use_container_width=True,hide_index=True)
    else:
        df=csv("risk_train.csv",dtype={"signal_id":"string"})
        default=str(df.sort_values("demo_risk_score",ascending=False).iloc[0]["signal_id"])
        sid=st.text_input("Signal ID",value=default)
        m=df[df["signal_id"].astype(str)==sid.strip()]
        if m.empty:
            st.warning("Signal ID not found. Example: "+default)
        else:
            r=m.iloc[0];score=float(r["demo_risk_score"]);band,css=risk_band(score)
            st.markdown(f"""
            <div class="alert-head">
              <div><div class="alert-id">{html.escape(str(r["signal_id"]))}</div>
              <div class="alert-meta">Signal date · {pd.to_datetime(r["signal_sanasi"]).date()} · Labeled train OOF demo</div></div>
              <div class="risk-chip {css}">{band}</div>
            </div>""",unsafe_allow_html=True)
            kpis([
              ("OOF demo score",f"{score:.4f}","interpretability only"),
              ("Actual target","Escalated" if int(r["eskalatsiya"]) else "Not escalated","ground truth"),
              ("LightGBM OOF",f'{float(r["oof_lightgbm"]):.4f}',"base model"),
              ("CatBoost OOF",f'{float(r["oof_catboost"]):.4f}',"base model"),
            ])
            comp=pd.DataFrame({"Model":["LightGBM OOF","CatBoost OOF","Rank-blend demo"],
                               "Score":[r["oof_lightgbm"],r["oof_catboost"],r["demo_risk_score"]]})
            fig=px.bar(comp,x="Model",y="Score",text="Score",title="Available OOF model scores")
            fig.update_traces(texttemplate="%{text:.4f}")
            plot(style_fig(fig,370))
            st.caption("Train explorer is explicitly a demo using the available OOF artifact and is not presented as the V2 ensemble probability.")

elif page=="Model Intelligence":
    hero("Model Intelligence","Validated model stack, ensemble design and feature evidence behind the final ranking.")
    kpis([
      ("V1 ROC-AUC",f'{S["v1_auc"]:.4f}',"baseline ensemble"),
      ("V2 ROC-AUC",f'{S["v2_best_auc"]:.4f}',f'+{S["delta_vs_v1"]:.4f} vs V1'),
      ("Validation","5-fold OOF","out-of-fold"),
      ("Blend","Rank ensemble",f'{S["w_lgb_full"]:.0%} / {S["w_lgb_behavior"]:.0%} / {S["w_cat"]:.0%}'),
    ])

    st.markdown("""
    <div class="cap-grid">
      <div class="cap"><div class="cap-num">L</div><div class="cap-title">LightGBM Full</div><div class="cap-text">Broad feature set including behavioral and metadata signals.</div></div>
      <div class="cap"><div class="cap-num">B</div><div class="cap-title">LightGBM Behavior</div><div class="cap-text">Behavior-only view retained to reduce metadata dependence.</div></div>
      <div class="cap"><div class="cap-num">C</div><div class="cap-title">CatBoost</div><div class="cap-text">Different boosting family contributes ensemble diversity.</div></div>
    </div>""",unsafe_allow_html=True)

    perf=csv("model_perf.csv")
    section("Validation leaderboard","same OOF framework across model candidates")
    fig=px.bar(perf,x="auc",y="model",orientation="h",text="auc",title="Out-of-fold ROC-AUC")
    fig.update_traces(texttemplate="%{text:.5f}",textposition="outside")
    fig.update_xaxes(range=[max(.50,perf["auc"].min()-.02),perf["auc"].max()+.012])
    plot(style_fig(fig,390))

    top=csv("top_features.csv").head(25).sort_values("importance")
    section("Feature evidence","human-readable labels + technical hover detail")
    fig=px.bar(top,x="importance",y="human_label",orientation="h",color="family",
               hover_data={"feature":True,"human_label":False,"importance":":.2f"},
               title="Top 25 LightGBM feature importances")
    plot(style_fig(fig,690))

else:
    hero("Methodology & Integrity","A compact audit trail from raw alert-linked transactions to a validated submission.")
    st.markdown("""
    <div class="pipeline">
      <div class="pipe"><div class="pipe-step">STEP 01</div><div class="pipe-title">Cutoff</div><div class="pipe-text">Keep transaction history available before the signal cutoff.</div></div>
      <div class="pipe"><div class="pipe-step">STEP 02</div><div class="pipe-title">Behavior</div><div class="pipe-text">Build recent, historical, timing, type, direction and amount features.</div></div>
      <div class="pipe"><div class="pipe-step">STEP 03</div><div class="pipe-title">OOF models</div><div class="pipe-text">Evaluate LightGBM and CatBoost with 5-fold out-of-fold validation.</div></div>
      <div class="pipe"><div class="pipe-step">STEP 04</div><div class="pipe-title">Rank ensemble</div><div class="pipe-text">Blend complementary models for the ROC-AUC ranking objective.</div></div>
      <div class="pipe"><div class="pipe-step">STEP 05</div><div class="pipe-title">Integrity</div><div class="pipe-text">Validate IDs, missing values, duplicates and score range before export.</div></div>
    </div>""",unsafe_allow_html=True)

    c1,c2=st.columns(2)
    with c1:
        section("Data boundaries")
        st.write(f"Train signal period: **{S['train_date_min']} → {S['train_date_max']}**")
        st.write(f"Test signal period: **{S['test_date_min']} → {S['test_date_max']}**")
        st.write("Public dashboard serves compact derived artifacts instead of millions of raw transaction rows.")
    with c2:
        section("Validation principles")
        st.markdown("- **ROC-AUC** is the primary metric\n- Continuous scores, not hard labels\n- 5-fold OOF model comparison\n- Behavior-only model retained\n- Rank blending for ranking quality\n- Strict final CSV checks")

    section("Submission integrity","automated checks on the current competition file")
    I=jload("submission_integrity.json")
    kpis([
      ("Rows",f'{I["rows"]:,}',"expected test count"),
      ("Duplicate IDs",f'{I["duplicate_ids"]}',"must be 0"),
      ("Missing scores",f'{I["missing_scores"]}',"must be 0"),
      ("Score range",f'{I["min_score"]:.4f}–{I["max_score"]:.4f}',"must stay inside [0,1]"),
    ])
    if I["test_ids_match"] and I["all_scores_0_1"] and I["duplicate_ids"]==0 and I["missing_scores"]==0:
        st.success("Submission integrity checks passed.")
    else:
        st.error("Submission integrity check failed.")

    st.info("ROC-AUC evaluates ranking. The competition score should not automatically be interpreted as a calibrated real-world probability.")
    st.caption("Synthetic/transformed hackathon data. This is an analytical competition artifact, not a production AML compliance decision system or a substitute for investigator review.")
