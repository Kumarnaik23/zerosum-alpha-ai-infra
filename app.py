# =============================================================
# ZEROSUM ALPHA — Streamlit Dashboard v3
# Includes: Rankings, Universe, Options, Earnings, Weekly Report, Company Detail
# =============================================================

import streamlit as st
import json
import pandas as pd

st.set_page_config(
    page_title="ZeroSum Alpha · AI Infra",
    page_icon="⚡",
    layout="wide"
)

st.markdown("""
<style>
    .block-container { padding-top: 1.5rem; padding-bottom: 2rem; }
    div[data-testid="stMetric"] { background: #f8f9fa; border-radius: 8px; padding: 12px; }
    .tier-1 { background:#dbeafe;color:#1e40af;padding:2px 10px;border-radius:99px;font-size:12px;font-weight:600; }
    .tier-2 { background:#dcfce7;color:#166534;padding:2px 10px;border-radius:99px;font-size:12px;font-weight:600; }
    .tier-3 { background:#fef9c3;color:#854d0e;padding:2px 10px;border-radius:99px;font-size:12px;font-weight:600; }
    .risk-flag { background:#fee2e2;color:#991b1b;padding:2px 10px;border-radius:99px;font-size:11px; }
    .iv-high { background:#fee2e2;color:#991b1b;padding:2px 10px;border-radius:99px;font-size:11px; }
    .iv-low  { background:#dcfce7;color:#166534;padding:2px 10px;border-radius:99px;font-size:11px; }
    .iv-norm { background:#f8f9fa;color:#374151;padding:2px 10px;border-radius:99px;font-size:11px; }
    .regime-on  { color:#166534;font-weight:600; }
    .regime-off { color:#991b1b;font-weight:600; }
    .regime-neu { color:#92400e;font-weight:600; }
</style>
""", unsafe_allow_html=True)

# =============================================================
# PASSWORD
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

data     = load_data()
df       = pd.DataFrame(data["stocks"])
movers   = data.get("movers", [])
macro    = data.get("macro", {})
earnings = data.get("earnings_calendar", [])
regime   = data.get("regime", "Risk-on")

# =============================================================
# HEADER
# =============================================================
h1, h2, h3 = st.columns([3, 2, 2])
with h1:
    st.markdown("## ⚡ ZEROSUM ALPHA")
    st.caption("AI Infrastructure Intelligence · Quantitative Research Engine")
with h2:
    rc = "regime-on" if regime == "Risk-on" else ("regime-off" if regime == "Risk-off" else "regime-neu")
    st.markdown("**Market Regime**")
    st.markdown(f'<span class="{rc}">{regime}</span>', unsafe_allow_html=True)
with h3:
    st.markdown("**Last Updated**")
    st.markdown(f"`{data.get('generated','N/A')}`")

st.divider()

# =============================================================
# TABS
# =============================================================
tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "📊 Rankings",
    "🌐 Universe",
    "📈 Options",
    "📅 Earnings",
    "📰 Weekly Report",
    "🔍 Company Detail"
])

# ---------------------------------------------------------------
# TAB 1: RANKINGS
# ---------------------------------------------------------------
with tab1:
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Universe",      f"{data.get('universe_count', len(df))} stocks")
    m2.metric("Tier 1",        f"{data.get('tier1_count', 0)} stocks")
    m3.metric("Avg Score",     f"{data.get('avg_score', 0)}")
    m4.metric("Top Subsector", data.get("top_subsector", "—"))

    st.markdown("### All Ranked Stocks")
    fc1, fc2 = st.columns(2)
    with fc1:
        tier_filter = st.multiselect("Tier", [1,2,3], default=[1,2,3])
    with fc2:
        subs = sorted(df["subsector"].unique().tolist())
        sub_filter = st.multiselect("Subsector", subs, default=subs)

    fdf = df[df["tier"].isin(tier_filter) & df["subsector"].isin(sub_filter)].copy()

    cols_map = {
        "rank":"Rank","ticker":"Ticker","name":"Company","subsector":"Subsector",
        "tier":"Tier","score":"Score","rev_growth_pct":"Rev Growth %",
        "rel_strength_pct":"3M Return %","rsi":"RSI","fwd_pe":"Fwd PE","risk_flags":"Risk Flag"
    }
    show = fdf[[c for c in cols_map if c in fdf.columns]].rename(columns=cols_map)
    st.dataframe(
        show,
        column_config={
            "Score": st.column_config.ProgressColumn("Score", min_value=0, max_value=100, format="%d"),
            "Rev Growth %": st.column_config.NumberColumn(format="%.1f%%"),
            "3M Return %":  st.column_config.NumberColumn(format="%.1f%%"),
        },
        use_container_width=True, hide_index=True, height=450
    )

    st.markdown("### This Week")
    wc1, wc2 = st.columns(2)
    with wc1:
        st.markdown("**Score Movers**")
        if movers:
            for m in sorted(movers, key=lambda x: x.get("score_change",0), reverse=True):
                chg = m.get("score_change", 0)
                arrow = "▲" if chg >= 0 else "▼"
                color = "green" if chg >= 0 else "red"
                st.markdown(f"**{m['ticker']}** — <span style='color:{color}'>{arrow} {abs(chg):.0f} pts</span>", unsafe_allow_html=True)
        else:
            st.caption("First run — no prior week to compare.")

    with wc2:
        st.markdown("**Risk Flags**")
        rdf = df[df["risk_flags"] != "None"][["ticker","name","risk_flags"]]
        if not rdf.empty:
            for _, row in rdf.iterrows():
                st.markdown(f"**{row['ticker']}** · <span class='risk-flag'>{row['risk_flags']}</span>", unsafe_allow_html=True)
        else:
            st.success("✅ No material risk flags this week.")


# ---------------------------------------------------------------
# TAB 2: UNIVERSE
# ---------------------------------------------------------------
with tab2:
    st.markdown("### AI Infrastructure Universe — 12 Subsectors")

    subsector_colors = {
        "AI Silicon":"#dbeafe", "Semiconductor Equipment":"#ede9fe",
        "Memory & Storage":"#dcfce7", "Foundry":"#fef9c3",
        "Networking":"#ffedd5", "AI Server Systems":"#fce7f3",
        "Power & Cooling":"#d1fae5", "Energy & Power":"#ecfdf5",
        "Cloud Hyperscaler":"#e0f2fe", "Specialized AI Cloud":"#f0fdf4",
        "Optical Connectivity":"#fef3c7", "AI Observability":"#f5f3ff",
    }

    sub_avg = data.get("subsector_avg", {})
    for sub in subsector_colors.keys():
        sdf = df[df["subsector"] == sub].sort_values("score", ascending=False)
        if sdf.empty:
            continue
        avg = sub_avg.get(sub, 0)
        color = subsector_colors.get(sub, "#f8f9fa")
        st.markdown(f"#### {sub} — Avg Score: {avg}")
        cols = st.columns(min(len(sdf), 5))
        for i, (_, row) in enumerate(sdf.iterrows()):
            with cols[i % 5]:
                st.markdown(
                    f"""<div style='background:{color};border-radius:8px;padding:10px 12px;margin-bottom:8px;'>
                    <div style='font-weight:600;font-size:15px;'>{row['ticker']}</div>
                    <div style='font-size:11px;color:#555;'>{row['name']}</div>
                    <div style='font-size:13px;font-weight:600;margin-top:4px;'>{row['score']}/100</div>
                    <div style='font-size:11px;color:#777;'>T{row['tier']} · {row['rev_growth_pct']}% rev gr</div>
                    </div>""", unsafe_allow_html=True
                )
        st.divider()


# ---------------------------------------------------------------
# TAB 3: OPTIONS
# ---------------------------------------------------------------
with tab3:
    st.markdown("### Options Intelligence — AI Infrastructure Universe")
    st.caption("IV, Put/Call Ratio, and options signals across tracked stocks. Use to size positions and identify when options are cheap vs expensive.")

    # Summary metrics
    iv_df = df[df["iv"] > 0].copy()
    if not iv_df.empty:
        avg_iv    = round(iv_df["iv"].mean(), 1)
        high_iv   = iv_df.nlargest(1, "iv").iloc[0]
        low_iv    = iv_df[iv_df["iv"] > 0].nsmallest(1, "iv").iloc[0]
        cheap_ops = iv_df[iv_df["iv"] < 30]

        oc1, oc2, oc3, oc4 = st.columns(4)
        oc1.metric("Avg IV (Universe)", f"{avg_iv}%")
        oc2.metric("Highest IV", f"{high_iv['ticker']} · {high_iv['iv']}%")
        oc3.metric("Lowest IV",  f"{low_iv['ticker']} · {low_iv['iv']}%")
        oc4.metric("Cheap Options (<30 IV)", f"{len(cheap_ops)} stocks")
    else:
        st.info("Options data loading — run engine with markets open for full IV data.")

    st.divider()

    # Options signal table
    st.markdown("### Options Signal Table")
    st.caption("Tier 1 and Tier 2 stocks with options data available")

    op_cols = ["rank","ticker","name","subsector","tier","score",
               "iv","iv_signal","pc_ratio","pc_signal","rsi","ret_1d_pct"]
    op_df = df[[c for c in op_cols if c in df.columns]].copy()
    op_df = op_df[op_df["tier"].isin([1,2])].sort_values("rank")

    op_rename = {
        "rank":"Rank","ticker":"Ticker","name":"Company","subsector":"Subsector",
        "tier":"Tier","score":"Score","iv":"IV %","iv_signal":"IV Signal",
        "pc_ratio":"P/C Ratio","pc_signal":"P/C Signal","rsi":"RSI","ret_1d_pct":"1D Move %"
    }
    op_show = op_df.rename(columns=op_rename)
    st.dataframe(op_show, use_container_width=True, hide_index=True, height=400)

    st.divider()

    # Best options plays
    st.markdown("### Options Playbook — This Week")

    pc1, pc2, pc3 = st.columns(3)

    with pc1:
        st.markdown("#### 🟢 Buy Calls / Longs")
        st.caption("Tier 1 stocks with low IV — options cheap, bullish setup")
        buy_calls = df[
            (df["tier"] == 1) &
            (df["iv"] > 0) &
            (df["iv"] < 35) &
            (df["pc_ratio"] < 0.8)
        ].sort_values("score", ascending=False)

        if not buy_calls.empty:
            for _, row in buy_calls.head(5).iterrows():
                st.markdown(
                    f"**{row['ticker']}** · Score: {row['score']}  \n"
                    f"IV: {row['iv']}% · P/C: {row['pc_ratio']}  \n"
                    f"*{row.get('iv_signal','')}*"
                )
                st.markdown("")
        else:
            st.caption("No strong buy-call setups this week — IV elevated across Tier 1.")

    with pc2:
        st.markdown("#### 🔴 Sell Premium / Covered Calls")
        st.caption("High IV stocks — options expensive, collect premium")
        sell_prem = df[
            (df["iv"] > 50)
        ].sort_values("iv", ascending=False)

        if not sell_prem.empty:
            for _, row in sell_prem.head(5).iterrows():
                tier_badge = f"T{row['tier']}"
                st.markdown(
                    f"**{row['ticker']}** · {tier_badge}  \n"
                    f"IV: {row['iv']}% · P/C: {row['pc_ratio']}  \n"
                    f"*{row.get('iv_signal','')}*"
                )
                st.markdown("")
        else:
            st.caption("No elevated IV names this week.")

    with pc3:
        st.markdown("#### ⚠️ Bearish Options Flow")
        st.caption("High put/call ratio — smart money buying protection")
        bearish = df[
            (df["pc_ratio"] > 1.3)
        ].sort_values("pc_ratio", ascending=False)

        if not bearish.empty:
            for _, row in bearish.head(5).iterrows():
                st.markdown(
                    f"**{row['ticker']}** · T{row['tier']}  \n"
                    f"P/C: {row['pc_ratio']} · IV: {row['iv']}%  \n"
                    f"*{row.get('pc_signal','')}*"
                )
                st.markdown("")
        else:
            st.caption("No unusual bearish flow detected this week.")

    st.divider()

    # IV vs Score scatter insight
    st.markdown("### IV Ranking — All Stocks with Options Data")
    iv_ranked = df[df["iv"] > 0][["ticker","name","subsector","tier","score","iv","pc_ratio","rsi"]].sort_values("iv", ascending=False)
    iv_rename = {"ticker":"Ticker","name":"Company","subsector":"Subsector",
                 "tier":"Tier","score":"Score","iv":"IV %","pc_ratio":"P/C Ratio","rsi":"RSI"}
    st.dataframe(iv_ranked.rename(columns=iv_rename), use_container_width=True, hide_index=True)


# ---------------------------------------------------------------
# TAB 4: EARNINGS CALENDAR
# ---------------------------------------------------------------
with tab4:
    st.markdown("### Earnings Calendar — Next 14 Days")
    st.caption("Upcoming earnings with AI infrastructure read-through signals")

    if earnings:
        for e in earnings:
            days = e.get("days_away", 0)
            urgency = "🔴" if days <= 3 else ("🟡" if days <= 7 else "🟢")
            with st.expander(f"{urgency} {e['ticker']} — {e['name']} · Reports: {e['date']} ({days} days)"):
                st.markdown(f"**Watch for:** {e.get('watch_for','Standard metrics')}")
                impacts = e.get("impacts", [])
                if impacts:
                    st.markdown(f"**Read-through impacts:** {', '.join(impacts)}")
                    st.markdown(f"**Logic:** {e.get('logic','')}")
    else:
        st.info("No earnings detected in next 14 days via yfinance calendar. Check manually via earnings whispers or Bloomberg.")
        st.markdown("#### Manual Earnings Tracker")
        st.caption("Key AI infrastructure earnings to watch:")

        manual_earnings = [
            {"ticker":"NVDA",  "typical":"Late May / Late Aug / Late Nov / Late Feb", "watch":"Data center revenue, Blackwell shipments, guidance raise"},
            {"ticker":"AVGO",  "typical":"Early Mar / Early Jun / Early Sep / Early Dec", "watch":"AI revenue, custom ASIC wins, networking commentary"},
            {"ticker":"TSM",   "typical":"Mid Jan / Mid Apr / Mid Jul / Mid Oct", "watch":"CoWoS capacity, advanced node utilization, AI chip demand"},
            {"ticker":"MU",    "typical":"Late Mar / Late Jun / Late Sep / Late Dec", "watch":"HBM pricing, capacity ramp, hyperscaler demand"},
            {"ticker":"AMD",   "typical":"Late Jan / Late Apr / Late Jul / Late Oct", "watch":"MI GPU revenue, data center share vs NVDA"},
            {"ticker":"MSFT",  "typical":"Late Jan / Late Apr / Late Jul / Late Oct", "watch":"Azure AI growth rate, capex guidance"},
            {"ticker":"GOOGL", "typical":"Late Jan / Late Apr / Late Jul / Late Oct", "watch":"GCP growth, capex guidance, custom TPU commentary"},
            {"ticker":"META",  "typical":"Late Jan / Late Apr / Late Jul / Late Oct", "watch":"AI capex guidance, Llama training compute"},
            {"ticker":"AMZN",  "typical":"Late Jan / Late Apr / Late Jul / Late Oct", "watch":"AWS revenue, Trainium/Inferentia wins"},
            {"ticker":"DELL",  "typical":"Late Feb / Late May / Late Aug / Late Nov", "watch":"PowerEdge AI server backlog, ISG revenue"},
        ]

        mdf = pd.DataFrame(manual_earnings)
        mdf.columns = ["Ticker", "Typical Schedule", "Watch For"]
        st.dataframe(mdf, use_container_width=True, hide_index=True)

    st.divider()
    st.markdown("### Read-Through Matrix")
    st.caption("When a stock reports, what does it signal for others?")

    rt_stocks = df[df["read_through_signal"] != ""]["ticker"].tolist() if "read_through_signal" in df.columns else []

    matrix_data = [
        {"Reports":"NVDA","Signal":"Data center rev + Blackwell shipments","Impacts":"SMCI, DELL, VRT, ANET, MU, TSM","Direction":"🟢 Bullish for supply chain"},
        {"Reports":"AVGO","Signal":"Custom ASIC revenue + AI networking","Impacts":"ANET, COHR, LITE, TSM","Direction":"🟢 Bullish for optical + networking"},
        {"Reports":"MSFT","Signal":"Azure AI growth + capex guidance","Impacts":"NVDA, AVGO, MRVL, VRT, SMCI","Direction":"🟢 Bullish if capex raised"},
        {"Reports":"GOOGL","Signal":"GCP growth + TPU commentary","Impacts":"NVDA, AVGO, TSM, VRT","Direction":"🟢 Bullish if capex raised"},
        {"Reports":"META","Signal":"AI capex guidance + Llama compute","Impacts":"NVDA, AVGO, ANET, VRT, ETN","Direction":"🟢 Bullish if spending raised"},
        {"Reports":"DELL","Signal":"PowerEdge AI server backlog","Impacts":"NVDA, MU, AVGO, SMCI","Direction":"🟢 Demand signal for AI silicon"},
        {"Reports":"TSM","Signal":"Advanced node utilization + CoWoS","Impacts":"NVDA, AMD, AVGO, ASML, AMAT","Direction":"🟢 Capacity = demand confirmation"},
        {"Reports":"MU", "Signal":"HBM pricing + hyperscaler demand","Impacts":"NVDA, SMCI, DELL, HPE","Direction":"🟢 HBM demand = GPU server rate"},
        {"Reports":"VRT","Signal":"Data centre power orders + backlog","Impacts":"ETN, PWR, HUBB, CEG, VST","Direction":"🟢 Power infra leads energy demand"},
        {"Reports":"SNOW","Signal":"Data cloud growth + AI workloads","Impacts":"AVGO, ANET, CSCO, COHR","Direction":"🟢 Data movement = networking demand"},
    ]

    rt_df = pd.DataFrame(matrix_data)
    st.dataframe(rt_df, use_container_width=True, hide_index=True)


# ---------------------------------------------------------------
# TAB 5: WEEKLY REPORT
# ---------------------------------------------------------------
with tab5:
    st.markdown(f"### Sunday Executive Briefing — {data.get('generated','')}")
    st.markdown(f"**Regime:** `{regime}` · **Vol:** `{data.get('realised_vol','—')}%`")
    st.divider()

    r1, r2 = st.columns(2)
    with r1:
        st.markdown("#### 🏆 Top 5 This Week")
        for _, row in df.nlargest(5, "score").iterrows():
            thesis = str(row.get("thesis",""))
            short  = thesis[:130] + "..." if len(thesis) > 130 else thesis
            st.markdown(f"**{row['rank']}. {row['ticker']}** · {row['name']} · Score: **{row['score']}**")
            st.caption(short)
            st.markdown("")

    with r2:
        st.markdown("#### ⚠️ Watchlist — Tier 3")
        for _, row in df[df["tier"]==3].nlargest(5,"score").iterrows():
            flag = f" · ⚠️ {row['risk_flags']}" if row["risk_flags"] != "None" else ""
            st.markdown(f"**{row['ticker']}** · Score: {row['score']}{flag}")

    st.divider()

    # Macro
    if macro:
        st.markdown("#### 🌍 Macro Signals")
        mc_rows = []
        for ticker, m in macro.items():
            mc_rows.append({
                "Signal": m.get("name", ticker),
                "Value":  m.get("value", "—"),
                "1W Chg %": m.get("chg_1w", 0),
            })
        mc_df = pd.DataFrame(mc_rows)
        st.dataframe(
            mc_df,
            column_config={"1W Chg %": st.column_config.NumberColumn(format="%.2f%%")},
            use_container_width=True, hide_index=True
        )

    st.divider()
    st.markdown("#### 📊 Subsector Avg Scores")
    sa = pd.DataFrame([
        {"Subsector": k, "Avg Score": v}
        for k, v in sorted(data.get("subsector_avg",{}).items(), key=lambda x: -x[1])
    ])
    if not sa.empty:
        st.dataframe(sa, use_container_width=True, hide_index=True)


# ---------------------------------------------------------------
# TAB 6: COMPANY DETAIL
# ---------------------------------------------------------------
with tab6:
    selected = st.selectbox(
        "Select Stock",
        df.sort_values("rank")["ticker"].tolist(),
        format_func=lambda t: f"{t} — {df[df['ticker']==t].iloc[0]['name']}"
    )
    row = df[df["ticker"] == selected].iloc[0]

    # Header metrics
    d1, d2, d3, d4, d5 = st.columns(5)
    d1.metric("Score",      f"{row['score']}/100")
    d2.metric("Tier",       f"Tier {row['tier']}")
    d3.metric("Rev Growth", f"{row['rev_growth_pct']}%")
    d4.metric("3M Return",  f"{row['rel_strength_pct']}%")
    d5.metric("RSI",        f"{row.get('rsi', '—')}")

    st.divider()

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### Score Breakdown")
        comp = row.get("score_components", {})
        labels = {
            "revenue_growth":    "Revenue Growth (max 20)",
            "earnings_revision": "Earnings Revision (max 10)",
            "relative_strength": "Relative Strength (max 20)",
            "ai_exposure":       "AI Exposure (max 20)",
            "valuation":         "Valuation (max 10)",
            "visibility":        "Visibility (max 10)",
            "risk_penalty":      "Risk Penalty",
        }
        for k, label in labels.items():
            v = comp.get(k, 0)
            st.markdown(f"**{label}:** `{v}`")

    with col2:
        st.markdown("#### Key Metrics")
        st.markdown(f"**Subsector:** {row['subsector']}")
        st.markdown(f"**Market Cap:** ${row.get('mkt_cap_b',0)}B")
        st.markdown(f"**Forward PE:** {row.get('fwd_pe','N/A')}")
        st.markdown(f"**Gross Margin:** {row.get('gross_margin',0)}%")
        st.markdown(f"**1D Move:** {row.get('ret_1d_pct',0)}%")
        st.markdown(f"**1W Move:** {row.get('ret_1w_pct',0)}%")
        st.markdown(f"**% from 52W High:** {row.get('pct_from_high',0)}%")
        st.markdown(f"**Vol Ratio (vs 20D):** {row.get('vol_ratio',1)}x")
        st.markdown(f"**Risk Flag:** {row.get('risk_flags','None')}")
        st.markdown(f"**RS Signal:** {row.get('rs_signal','')}")

    with col3:
        st.markdown("#### Options Data")
        iv = row.get("iv", 0)
        pc = row.get("pc_ratio", 0)
        if iv > 0:
            iv_class = "iv-high" if iv > 50 else ("iv-low" if iv < 30 else "iv-norm")
            st.markdown(f"**Implied Volatility:** <span class='{iv_class}'>{iv}%</span>", unsafe_allow_html=True)
            st.markdown(f"**IV Signal:** {row.get('iv_signal','')}")
            st.markdown(f"**Put/Call Ratio:** {pc}")
            st.markdown(f"**P/C Signal:** {row.get('pc_signal','')}")
            st.markdown(f"**Next Expiry:** {row.get('next_expiry','—')}")

            # Options trade idea
            st.divider()
            st.markdown("**Options Idea:**")
            if iv < 30 and row["tier"] == 1:
                st.success(f"Low IV on Tier 1 name — consider buying calls or call spreads before next catalyst.")
            elif iv > 60:
                st.warning(f"Elevated IV — consider selling covered calls or cash-secured puts to collect premium.")
            elif pc > 1.3:
                st.error(f"Heavy put buying — market pricing in downside risk. Caution on long calls.")
            else:
                st.info(f"IV in normal range — standard options positioning applicable.")
        else:
            st.caption("Options data not available for this ticker.")

    st.divider()

    # Read-through section
    impacts_from = row.get("impacted_by", [])
    rt_signal    = row.get("read_through_signal", "")

    if impacts_from or rt_signal:
        st.markdown("#### 🔗 Earnings Read-Through")
        if rt_signal:
            st.markdown(f"**When {selected} reports, watch for:** {rt_signal}")
            impacts = row.get("read_through_impacts", [])
            if impacts:
                st.markdown(f"**Signals for:** {', '.join(impacts)}")

        if impacts_from:
            st.markdown("**Impacted by these upcoming earnings:**")
            for imp in impacts_from:
                st.markdown(f"→ **{imp['ticker']}** · {imp.get('logic','')}")

    st.divider()
    st.markdown("#### Investment Thesis")
    st.info(row.get("thesis", "No thesis available."))
    st.caption("⚠️ ZeroSum Alpha provides quantitative research for informational purposes only. Not personalized investment advice.")

