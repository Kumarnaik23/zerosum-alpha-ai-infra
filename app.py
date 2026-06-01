# =============================================================
# ZEROSUM ALPHA — Streamlit Dashboard v2
# app.py — deploy to Streamlit Cloud via GitHub
# =============================================================

import streamlit as st
import json
import pandas as pd

st.set_page_config(
    page_title="ZeroSum Alpha · AI Infra",
    page_icon="⚡",
    layout="wide"
)

# --- Custom CSS ---
st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    .metric-container { background: #f8f9fa; border-radius: 8px; padding: 12px 16px; }
    .tier-1 { background-color: #dbeafe; color: #1e40af; padding: 2px 10px; border-radius: 99px; font-size: 12px; font-weight: 600; }
    .tier-2 { background-color: #dcfce7; color: #166534; padding: 2px 10px; border-radius: 99px; font-size: 12px; font-weight: 600; }
    .tier-3 { background-color: #fef9c3; color: #854d0e; padding: 2px 10px; border-radius: 99px; font-size: 12px; font-weight: 600; }
    .risk-flag { background-color: #fee2e2; color: #991b1b; padding: 2px 10px; border-radius: 99px; font-size: 11px; }
    .regime-on  { color: #166534; font-weight: 600; }
    .regime-off { color: #991b1b; font-weight: 600; }
    .regime-neu { color: #92400e; font-weight: 600; }
    div[data-testid="stMetric"] { background: #f8f9fa; border-radius: 8px; padding: 12px; }
</style>
""", unsafe_allow_html=True)

# =============================================================
# PASSWORD GATE
# =============================================================
pwd = st.text_input("Enter Access Token", type="password")
if pwd != "zerosumAlpha26":
    st.info("🔐 Enter your access token to open the ZeroSum Alpha AI Infrastructure Control Room.")
    st.stop()

# =============================================================
# LOAD DATA
# =============================================================
@st.cache_data(ttl=3600)
def load_data():
    try:
        with open("scores.json", "r") as f:
            return json.load(f)
    except:
        st.error("scores.json not found. Run the Sunday engine first.")
        st.stop()

data = load_data()
df = pd.DataFrame(data["stocks"])
movers_data = data.get("movers", [])

# =============================================================
# HEADER
# =============================================================
col_logo, col_regime, col_date = st.columns([3, 2, 2])
with col_logo:
    st.markdown("## ⚡ ZEROSUM ALPHA")
    st.caption("AI Infrastructure Intelligence · Quantitative Research Engine")
with col_regime:
    regime = data.get("regime", "Unknown")
    regime_class = "regime-on" if regime == "Risk-on" else ("regime-off" if regime == "Risk-off" else "regime-neu")
    st.markdown(f"**Market Regime**")
    st.markdown(f'<span class="{regime_class}">{regime}</span>', unsafe_allow_html=True)
with col_date:
    st.markdown(f"**Last Updated**")
    st.markdown(f"`{data.get('generated', 'N/A')}`")

st.divider()

# =============================================================
# TABS
# =============================================================
tab1, tab2, tab3, tab4 = st.tabs(["📊 Rankings", "🌐 Universe", "📰 Weekly Report", "🔍 Company Detail"])

# ---------------------------------------------------------------
# TAB 1: RANKINGS
# ---------------------------------------------------------------
with tab1:
    # Summary metrics
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Universe", f"{data.get('universe_count', len(df))} stocks")
    m2.metric("Tier 1 (80+)", f"{data.get('tier1_count', len(df[df['tier']==1]))} stocks")
    m3.metric("Avg Score", f"{data.get('avg_score', round(df['score'].mean(),1))}")
    m4.metric("Top Subsector", data.get("top_subsector", "—"))

    st.markdown("### All Ranked Stocks")

    # Filter controls
    fc1, fc2 = st.columns([2, 2])
    with fc1:
        tier_filter = st.multiselect("Filter by Tier", [1, 2, 3], default=[1, 2, 3])
    with fc2:
        subsectors = sorted(df["subsector"].unique().tolist())
        sub_filter = st.multiselect("Filter by Subsector", subsectors, default=subsectors)

    filtered = df[df["tier"].isin(tier_filter) & df["subsector"].isin(sub_filter)].copy()

    # Display table
    display_cols = {
        "rank": "Rank",
        "ticker": "Ticker",
        "name": "Company",
        "subsector": "Subsector",
        "tier": "Tier",
        "score": "Score",
        "rev_growth_pct": "Rev Growth %",
        "rel_strength_pct": "3M Return %",
        "fwd_pe": "Fwd PE",
        "risk_flags": "Risk Flag"
    }

    show_df = filtered[[c for c in display_cols.keys() if c in filtered.columns]].rename(columns=display_cols)

    st.dataframe(
        show_df,
        column_config={
            "Score": st.column_config.ProgressColumn(
                "Score", min_value=0, max_value=100, format="%d"
            ),
            "Rev Growth %": st.column_config.NumberColumn("Rev Growth %", format="%.1f%%"),
            "3M Return %": st.column_config.NumberColumn("3M Return %", format="%.1f%%"),
        },
        use_container_width=True,
        hide_index=True,
        height=420
    )

    # Movers + Risk flags side by side
    st.markdown("### This Week")
    mc1, mc2 = st.columns(2)

    with mc1:
        st.markdown("**Score Movers**")
        movers_df = pd.DataFrame(movers_data) if movers_data else pd.DataFrame()
        if not movers_df.empty and "score_change" in movers_df.columns:
            movers_df = movers_df.sort_values("score_change", ascending=False)
            for _, row in movers_df.iterrows():
                chg = row["score_change"]
                arrow = "▲" if chg >= 0 else "▼"
                color = "green" if chg >= 0 else "red"
                st.markdown(
                    f"**{row['ticker']}** — "
                    f"<span style='color:{color}'>{arrow} {abs(chg):.0f} pts</span>",
                    unsafe_allow_html=True
                )
        else:
            st.caption("First run — no prior week to compare.")

    with mc2:
        st.markdown("**Risk Flags**")
        risk_df = df[df["risk_flags"] != "None"][["ticker", "name", "risk_flags"]]
        if not risk_df.empty:
            for _, row in risk_df.iterrows():
                st.markdown(
                    f"**{row['ticker']}** · "
                    f"<span class='risk-flag'>{row['risk_flags']}</span>",
                    unsafe_allow_html=True
                )
        else:
            st.success("✅ No material risk flags this week.")


# ---------------------------------------------------------------
# TAB 2: UNIVERSE
# ---------------------------------------------------------------
with tab2:
    st.markdown("### AI Infrastructure Universe — 7 Subsectors")

    subsector_order = [
        "AI Silicon", "Semiconductor Equipment", "Memory & Storage",
        "Foundry", "Networking", "AI Server Systems",
        "Power & Cooling", "Cloud Hyperscaler", "Specialized AI Cloud",
        "Optical Connectivity"
    ]

    subsector_colors = {
        "AI Silicon":             "#dbeafe",
        "Semiconductor Equipment":"#ede9fe",
        "Memory & Storage":       "#dcfce7",
        "Foundry":                "#fef9c3",
        "Networking":             "#ffedd5",
        "AI Server Systems":      "#fce7f3",
        "Power & Cooling":        "#d1fae5",
        "Cloud Hyperscaler":      "#e0f2fe",
        "Specialized AI Cloud":   "#f0fdf4",
        "Optical Connectivity":   "#fef3c7",
    }

    for sub in subsector_order:
        sub_df = df[df["subsector"] == sub].sort_values("score", ascending=False)
        if sub_df.empty:
            continue
        color = subsector_colors.get(sub, "#f8f9fa")
        st.markdown(f"#### {sub}")
        cols = st.columns(min(len(sub_df), 5))
        for i, (_, row) in enumerate(sub_df.iterrows()):
            with cols[i % 5]:
                tier_label = f"T{row['tier']}"
                st.markdown(
                    f"""<div style='background:{color};border-radius:8px;padding:10px 12px;margin-bottom:8px;'>
                    <div style='font-weight:600;font-size:15px;'>{row['ticker']}</div>
                    <div style='font-size:12px;color:#555;'>{row['name']}</div>
                    <div style='font-size:13px;font-weight:600;margin-top:4px;'>{row['score']}/100</div>
                    <div style='font-size:11px;color:#777;'>{tier_label}</div>
                    </div>""",
                    unsafe_allow_html=True
                )
        st.divider()


# ---------------------------------------------------------------
# TAB 3: WEEKLY REPORT
# ---------------------------------------------------------------
with tab3:
    st.markdown(f"### Sunday Executive Briefing — {data.get('generated', '')}")
    st.markdown(f"**Market Regime:** `{regime}` · **Realised Vol (SPY):** `{data.get('realised_vol', '—')}%`")
    st.divider()

    r1, r2 = st.columns(2)

    with r1:
        st.markdown("#### 🏆 Top 5 This Week")
        top5 = df.nlargest(5, "score")
        for _, row in top5.iterrows():
            st.markdown(
                f"**{row['rank']}. {row['ticker']}** · {row['name']} · Score: **{row['score']}**  \n"
                f"*{row['thesis'][:120]}...*" if len(str(row.get("thesis",""))) > 120
                else f"**{row['rank']}. {row['ticker']}** · {row['name']} · Score: **{row['score']}**  \n*{row.get('thesis','')}*"
            )
            st.markdown("")

    with r2:
        st.markdown("#### ⚠️ Watchlist")
        tier3 = df[df["tier"] == 3].nlargest(5, "score")
        for _, row in tier3.iterrows():
            flag = f" · ⚠️ {row['risk_flags']}" if row["risk_flags"] != "None" else ""
            st.markdown(f"**{row['ticker']}** · Score: {row['score']}{flag}")

    st.divider()
    st.markdown("#### 📊 Subsector Avg Scores")
    sub_avg = df.groupby("subsector")["score"].mean().round(1).sort_values(ascending=False).reset_index()
    sub_avg.columns = ["Subsector", "Avg Score"]
    st.dataframe(sub_avg, use_container_width=True, hide_index=True, height=300)


# ---------------------------------------------------------------
# TAB 4: COMPANY DETAIL
# ---------------------------------------------------------------
with tab4:
    selected = st.selectbox(
        "Select Stock",
        df.sort_values("rank")["ticker"].tolist(),
        format_func=lambda t: f"{t} — {df[df['ticker']==t].iloc[0]['name']}"
    )

    row = df[df["ticker"] == selected].iloc[0]

    d1, d2, d3, d4 = st.columns(4)
    d1.metric("Score", f"{row['score']}/100")
    d2.metric("Tier", f"Tier {row['tier']}")
    d3.metric("Rev Growth", f"{row['rev_growth_pct']}%")
    d4.metric("3M Return", f"{row['rel_strength_pct']}%")

    st.divider()

    sc1, sc2 = st.columns(2)
    with sc1:
        st.markdown("#### Score Breakdown")
        components = row.get("score_components", {})
        comp_labels = {
            "revenue_growth": "Revenue Growth (max 20)",
            "earnings_revision": "Earnings Revision (max 10)",
            "relative_strength": "Relative Strength (max 20)",
            "ai_exposure": "AI Exposure (max 20)",
            "valuation": "Valuation (max 10)",
            "visibility": "Visibility (max 10)",
            "risk_penalty": "Risk Penalty"
        }
        for key, label in comp_labels.items():
            val = components.get(key, 0)
            st.markdown(f"**{label}:** `{val}`")

    with sc2:
        st.markdown("#### Key Metrics")
        st.markdown(f"**Subsector:** {row['subsector']}")
        st.markdown(f"**Market Cap:** ${row.get('mkt_cap_b', 0)}B")
        st.markdown(f"**Forward PE:** {row.get('fwd_pe', 'N/A')}")
        st.markdown(f"**Risk Flag:** {row.get('risk_flags', 'None')}")
        st.markdown(f"**Rank:** #{row['rank']} of {len(df)}")

    st.divider()
    st.markdown("#### Investment Thesis")
    st.info(row.get("thesis", "No thesis available."))

    st.caption("⚠️ ZeroSum Alpha provides quantitative research for informational purposes only. Not personalized investment advice.")

