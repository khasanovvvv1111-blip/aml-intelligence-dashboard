from pathlib import Path
import html

import numpy as np
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
from sklearn.metrics import roc_auc_score

TEAM_ID = "9812BA55"
DATA_DIR = Path(__file__).parent / "data"

st.set_page_config(
    page_title="AML Intelligence | Team 9812BA55",
    page_icon="◈",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ---------------------------- Styles --------------------------------
st.markdown(
    """
    <style>
      .stApp {
        background:
          radial-gradient(circle at 10% 0%, rgba(26, 115, 232, .12), transparent 30%),
          radial-gradient(circle at 90% 10%, rgba(0, 220, 180, .08), transparent 28%),
          #071019;
        color: #eef5fb;
      }
      [data-testid="stSidebar"] {
        background: #0a1520;
        border-right: 1px solid rgba(255,255,255,.08);
      }
      [data-testid="stMetric"] {
        background: linear-gradient(180deg, rgba(255,255,255,.055), rgba(255,255,255,.025));
        border: 1px solid rgba(255,255,255,.08);
        border-radius: 16px;
        padding: 16px;
      }
      .hero {
        padding: 26px 28px;
        border: 1px solid rgba(255,255,255,.08);
        background: linear-gradient(120deg, rgba(19,63,95,.55), rgba(10,26,39,.65));
        border-radius: 22px;
        margin-bottom: 18px;
      }
      .eyebrow {
        color: #7dd3fc; letter-spacing: .16em; font-size: .78rem; font-weight: 700;
      }
      .hero h1 {
        margin: 4px 0 8px 0; font-size: 2.25rem; line-height: 1.04;
      }
      .muted { color: #9bb0c2; }
      .pill {
        display:inline-block; border:1px solid rgba(125,211,252,.35);
        color:#bae6fd; padding:5px 10px; border-radius:999px;
        margin:4px 7px 0 0; font-size:.82rem;
      }
      .info-card {
        border:1px solid rgba(255,255,255,.08);
        background:rgba(255,255,255,.035);
        border-radius:16px; padding:16px 18px;
      }
      .risk-high { color:#ff7b7b; font-weight:800; }
      .risk-medium { color:#ffd166; font-weight:800; }
      .risk-low { color:#58e0b7; font-weight:800; }
      .section-note {
        color:#94a9ba; font-size:.91rem; margin-top:-8px; margin-bottom:12px;
      }
      div[data-testid="stDataFrame"] { border-radius: 14px; overflow:hidden; }
      .block-container { padding-top: 2rem; max-width: 1450px; }
    </style>
    """,
    unsafe_allow_html=True,
)

# ---------------------------- Data ----------------------------------
@st.cache_data(show_spinner=False)
def load_data():
    train = pd.read_csv(DATA_DIR / "dashboard_train.csv", parse_dates=["signal_sanasi"])
    test = pd.read_csv(DATA_DIR / "dashboard_test.csv", parse_dates=["signal_sanasi"])
    importance = pd.read_csv(DATA_DIR / "v2_feature_importance.csv")
    summary = pd.read_csv(DATA_DIR / "v2_score_summary.csv")
    return train, test, importance, summary

train, test, importance, summary = load_data()

V1_AUC = float(summary.loc[0, "v1_auc"])
V2_AUC = float(summary.loc[0, "v2_best_auc"])
POS_RATE = float(train["eskalatsiya"].mean())

# -------------------------- Helpers ---------------------------------
def hero(title, subtitle):
    st.markdown(
        f"""
        <div class="hero">
          <div class="eyebrow">AML INTELLIGENCE · TEAM {TEAM_ID}</div>
          <h1>{html.escape(title)}</h1>
          <div class="muted">{html.escape(subtitle)}</div>
          <div style="margin-top:12px">
            <span class="pill">Temporal behavior</span>
            <span class="pill">ROC-AUC optimization</span>
            <span class="pill">LightGBM + CatBoost</span>
            <span class="pill">Synthetic AML data</span>
          </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

def risk_band(score):
    if score >= 0.80:
        return "High", "risk-high"
    if score >= 0.50:
        return "Medium", "risk-medium"
    return "Low", "risk-low"

def chart_layout(fig, height=420):
    fig.update_layout(
        template="plotly_dark",
        height=height,
        margin=dict(l=18, r=18, t=55, b=20),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(255,255,255,.02)",
        legend_title_text="",
    )
    return fig

# -------------------------- Sidebar ---------------------------------
st.sidebar.markdown("## ◈ AML Intelligence")
st.sidebar.caption(f"Team {TEAM_ID}")

page = st.sidebar.radio(
    "Navigation",
    [
        "Overview",
        "Exploratory Analysis",
        "Risk Explorer",
        "Model Intelligence",
        "Methodology",
    ],
)

st.sidebar.markdown("---")
st.sidebar.caption(
    "Hackathon analytics dashboard. Data is synthetic/transformed and this is not a production AML decision system."
)

# -------------------------- Overview --------------------------------
if page == "Overview":
    hero(
        "Alert Escalation Intelligence",
        "Behavioral risk analytics for prioritizing AML alerts using temporal transaction patterns.",
    )

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Train alerts", f"{len(train):,}")
    c2.metric("Escalation rate", f"{POS_RATE:.2%}")
    c3.metric("Test alerts", f"{len(test):,}")
    c4.metric("Best validated ROC-AUC", f"{V2_AUC:.4f}", f"+{V2_AUC - V1_AUC:.4f} vs V1")

    st.markdown("### What the system does")
    st.markdown(
        """
        Instead of treating every alert equally, the pipeline creates a **temporal behavioral fingerprint**
        for each signal and ranks alerts by escalation risk. The modeling strategy focuses on changes in
        transaction behavior — recent vs historical activity, amount patterns, direction, transaction type,
        timing and switching behavior.
        """
    )

    left, right = st.columns([1.1, 1])

    with left:
        monthly = (
            train.groupby("year_month", as_index=False)
            .agg(alerts=("signal_id", "count"), escalation_rate=("eskalatsiya", "mean"))
        )
        fig = px.bar(
            monthly,
            x="year_month",
            y="alerts",
            title="Alert volume over time",
            labels={"year_month": "Signal month", "alerts": "Alerts"},
        )
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    with right:
        risk_counts = (
            test.assign(
                risk_band=pd.cut(
                    test["ehtimollik"],
                    bins=[-np.inf, 0.50, 0.80, np.inf],
                    labels=["Low", "Medium", "High"],
                )
            )
            .groupby("risk_band", observed=False)
            .size()
            .reset_index(name="alerts")
        )
        fig = px.pie(
            risk_counts,
            names="risk_band",
            values="alerts",
            title="Hidden-test risk-score distribution",
            hole=0.62,
        )
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    st.markdown("### Competition progress")
    perf = pd.DataFrame(
        {
            "Model": ["V1 Ensemble", "V2 LightGBM Full", "V2 LightGBM Behavior", "V2 CatBoost", "V2 Ensemble"],
            "ROC-AUC": [
                summary.loc[0, "v1_auc"],
                summary.loc[0, "v2_lgb_full_auc"],
                summary.loc[0, "v2_lgb_behavior_auc"],
                summary.loc[0, "v2_cat_auc"],
                summary.loc[0, "v2_best_auc"],
            ],
        }
    )
    fig = px.bar(perf, x="Model", y="ROC-AUC", text="ROC-AUC", title="OOF model comparison")
    fig.update_traces(texttemplate="%{text:.4f}", textposition="outside")
    fig.update_yaxes(range=[max(0.5, perf["ROC-AUC"].min() - 0.03), perf["ROC-AUC"].max() + 0.02])
    st.plotly_chart(chart_layout(fig), use_container_width=True)

# ---------------------------- EDA -----------------------------------
elif page == "Exploratory Analysis":
    hero(
        "Exploratory Data Analysis",
        "Understand alert class balance, seasonality and how escalation rates move across the signal timeline.",
    )

    c1, c2 = st.columns(2)

    with c1:
        cls = (
            train["eskalatsiya"]
            .map({0: "Not escalated", 1: "Escalated"})
            .value_counts()
            .rename_axis("class")
            .reset_index(name="alerts")
        )
        fig = px.bar(cls, x="class", y="alerts", text="alerts", title="Target class distribution")
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    with c2:
        monthly_rate = (
            train.groupby("year_month", as_index=False)
            .agg(escalation_rate=("eskalatsiya", "mean"), alerts=("signal_id", "count"))
        )
        fig = px.line(
            monthly_rate,
            x="year_month",
            y="escalation_rate",
            markers=True,
            title="Monthly escalation rate",
        )
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    c3, c4 = st.columns(2)

    with c3:
        dow_order = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        dow = (
            train.groupby("day_of_week", as_index=False)
            .agg(escalation_rate=("eskalatsiya", "mean"), alerts=("signal_id", "count"))
        )
        dow["day_of_week"] = pd.Categorical(dow["day_of_week"], categories=dow_order, ordered=True)
        dow = dow.sort_values("day_of_week")
        fig = px.bar(
            dow,
            x="day_of_week",
            y="escalation_rate",
            text="alerts",
            title="Escalation rate by signal weekday",
        )
        fig.update_yaxes(tickformat=".0%")
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    with c4:
        fig = px.histogram(
            test,
            x="ehtimollik",
            nbins=40,
            title="Final hidden-test score distribution",
            labels={"ehtimollik": "Risk score"},
        )
        st.plotly_chart(chart_layout(fig), use_container_width=True)

    st.markdown("### Risk concentration on labeled OOF data")
    st.caption(
        "The train risk chart below uses the available out-of-fold demo score artifact. "
        "It is used for interpretability only; the V2 validation score shown elsewhere is the stronger benchmark."
    )
    ranked = train.sort_values("demo_risk_score", ascending=False).reset_index(drop=True)
    rows = []
    for pct in [1, 2, 5, 10, 20, 30, 50]:
        n = max(1, int(np.ceil(len(ranked) * pct / 100)))
        top = ranked.head(n)
        rows.append(
            {
                "Top risk segment": f"Top {pct}%",
                "Alerts": n,
                "Escalation rate": top["eskalatsiya"].mean(),
                "Lift vs base": top["eskalatsiya"].mean() / POS_RATE,
            }
        )
    lift = pd.DataFrame(rows)
    st.dataframe(
        lift.style.format({"Escalation rate": "{:.2%}", "Lift vs base": "{:.2f}×"}),
        use_container_width=True,
        hide_index=True,
    )

# ------------------------- Risk Explorer -----------------------------
elif page == "Risk Explorer":
    hero(
        "Risk Explorer",
        "Inspect individual train OOF or hidden-test risk scores without exposing raw customer information.",
    )

    source = st.radio("Dataset", ["Hidden test predictions", "Train OOF demo"], horizontal=True)

    if source == "Hidden test predictions":
        df = test.copy()
        selected = st.selectbox("Select signal_id", df["signal_id"].tolist())
        row = df.loc[df["signal_id"] == selected].iloc[0]
        score = float(row["ehtimollik"])
        band, css = risk_band(score)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Signal ID", selected)
        c2.metric("Risk score", f"{score:.4f}")
        c3.metric("Signal date", str(row["signal_sanasi"].date()))
        c4.markdown(
            f'<div class="info-card">Risk band<br><span class="{css}" style="font-size:1.7rem">{band}</span></div>',
            unsafe_allow_html=True,
        )

        st.markdown("### Position within the hidden-test population")
        percentile = float((df["ehtimollik"] <= score).mean())
        gauge = go.Figure(
            go.Indicator(
                mode="gauge+number",
                value=percentile * 100,
                number={"suffix": "%"},
                title={"text": "Risk-score percentile"},
                gauge={"axis": {"range": [0, 100]}},
            )
        )
        st.plotly_chart(chart_layout(gauge, height=330), use_container_width=True)

        nearby = df.iloc[(df["ehtimollik"] - score).abs().argsort()[:10]][
            ["signal_id", "signal_sanasi", "ehtimollik"]
        ].sort_values("ehtimollik", ascending=False)
        st.markdown("### Similar-scored alerts")
        st.dataframe(nearby, use_container_width=True, hide_index=True)

    else:
        df = train.copy()
        selected = st.selectbox("Select signal_id", df["signal_id"].tolist())
        row = df.loc[df["signal_id"] == selected].iloc[0]
        score = float(row["demo_risk_score"])
        band, css = risk_band(score)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Signal ID", selected)
        c2.metric("OOF demo score", f"{score:.4f}")
        c3.metric("Actual target", "Escalated" if int(row["eskalatsiya"]) == 1 else "Not escalated")
        c4.markdown(
            f'<div class="info-card">Risk band<br><span class="{css}" style="font-size:1.7rem">{band}</span></div>',
            unsafe_allow_html=True,
        )

        compare = pd.DataFrame(
            {
                "Model": ["LightGBM OOF", "CatBoost OOF", "Rank-blend demo"],
                "Score": [row["oof_lightgbm"], row["oof_catboost"], row["demo_risk_score"]],
            }
        )
        fig = px.bar(compare, x="Model", y="Score", text="Score", title="Available OOF model scores")
        fig.update_traces(texttemplate="%{text:.4f}")
        st.plotly_chart(chart_layout(fig), use_container_width=True)

# ---------------------- Model Intelligence ---------------------------
elif page == "Model Intelligence":
    hero(
        "Model Intelligence",
        "See the validated model stack, feature importance and the behavioral concepts driving the ranking.",
    )

    c1, c2, c3 = st.columns(3)
    c1.metric("V1 ROC-AUC", f"{V1_AUC:.4f}")
    c2.metric("V2 ROC-AUC", f"{V2_AUC:.4f}", f"+{V2_AUC - V1_AUC:.4f}")
    c3.metric("Blend", "Rank ensemble", "50% LGB Full · 30% LGB Behavior · 20% CatBoost")

    perf = pd.DataFrame(
        {
            "Model": ["V1 Ensemble", "LGB Full", "LGB Behavior", "CatBoost", "V2 Ensemble"],
            "ROC-AUC": [
                summary.loc[0, "v1_auc"],
                summary.loc[0, "v2_lgb_full_auc"],
                summary.loc[0, "v2_lgb_behavior_auc"],
                summary.loc[0, "v2_cat_auc"],
                summary.loc[0, "v2_best_auc"],
            ],
        }
    )
    fig = px.bar(perf, x="ROC-AUC", y="Model", orientation="h", text="ROC-AUC", title="Out-of-fold validation")
    fig.update_traces(texttemplate="%{text:.5f}", textposition="outside")
    st.plotly_chart(chart_layout(fig, height=390), use_container_width=True)

    st.markdown("### Top behavioral features")
    top_n = st.slider("Number of features", 10, 50, 25, 5)
    top = importance.head(top_n).sort_values("importance")
    fig = px.bar(
        top,
        x="importance",
        y="feature",
        orientation="h",
        title=f"Top {top_n} LightGBM feature importances",
    )
    st.plotly_chart(chart_layout(fig, height=max(500, 22 * top_n)), use_container_width=True)

    st.markdown("### What the strongest features are telling us")
    st.markdown(
        """
        The strongest signals are not only total transaction counts. The model places meaningful weight on
        **direction × transaction type × amount**, **recent-vs-historical distribution shifts**,
        **night/evening behavior**, and **transaction-type switching**. This supports the core hypothesis:
        escalation risk is partly expressed through **behavioral change**, not just absolute activity.
        """
    )

# -------------------------- Methodology -------------------------------
else:
    hero(
        "Methodology & Reproducibility",
        "How the solution turns raw alert-linked transactions into a stable ROC-AUC ranking pipeline.",
    )

    st.markdown("### Modeling pipeline")
    st.code(
        """
Raw transactions
    ↓
Signal-date cutoff
    ↓
Temporal behavioral features
    ├─ 1h / 3h / 6h / 12h / 24h / 48h / 72h windows
    ├─ 1d / 3d / 7d / 14d / 30d / 90d / 180d / 365d windows
    ├─ recent vs previous non-overlapping shifts
    ├─ transaction type × direction × amount
    ├─ burst / rapid-gap behavior
    ├─ daily trends and switching
    └─ distribution-shift features
    ↓
LightGBM Full + LightGBM Behavior + CatBoost
    ↓
5-fold OOF validation
    ↓
ROC-AUC optimized rank ensemble
    ↓
Continuous hidden-test risk scores
        """.strip(),
        language="text",
    )

    left, right = st.columns(2)
    with left:
        st.markdown("### Data schema")
        st.dataframe(
            pd.DataFrame(
                [
                    ["train_signals.csv", "signal_id, signal_sanasi, eskalatsiya"],
                    ["train_transactions.parquet", "signal_id, tranzaksiya_vaqti, kirim_chiqim, tranzaksiya_turi, miqdor_indeksi"],
                    ["test_signals.csv", "signal_id, signal_sanasi"],
                    ["test_transactions.parquet", "same transaction schema, no target"],
                    ["submission", "signal_id, ehtimollik"],
                ],
                columns=["Artifact", "Fields / role"],
            ),
            use_container_width=True,
            hide_index=True,
        )
    with right:
        st.markdown("### Validation principles")
        st.markdown(
            """
            - Primary metric: **ROC-AUC**
            - Continuous scores, not hard labels
            - Out-of-fold evaluation for model comparison
            - Behavior-only model retained to reduce metadata dependence
            - Rank blending used because ROC-AUC is a ranking metric
            - Strict ID / missing / duplicate / range checks before submission
            """
        )

    st.markdown("### Important interpretation note")
    st.info(
        "The competition output is optimized for ranking under ROC-AUC. "
        "A risk score should not automatically be interpreted as a calibrated real-world probability."
    )

    st.markdown("### Data-use note")
    st.caption(
        "The hackathon data is synthetic/transformed. This dashboard is an analytical competition artifact, "
        "not a production AML compliance decision system and not a substitute for investigator review."
    )
