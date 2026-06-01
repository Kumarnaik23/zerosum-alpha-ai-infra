import streamlit as st
import json
import pandas as pd

st.set_page_config(page_title="ZeroSum Alpha - AI Infra", layout="wide")

# 1. SECURE GATEWAY FOR PARTNER ACCESS
if st.text_input("Enter Access Token", type="password") != "zerosumAlpha26":
    st.info("Please enter your security token to view the AI Infrastructure Control Room.")
    st.stop()

# 2. LOAD DATA SCRIPT
@st.cache_data
def load_weekly_data():
    with open('scores.json', 'r') as f:
        return json.load(f)

data = load_weekly_data()
df = pd.DataFrame(data['stocks'])

# 3. HEADER RENDERING
st.title("🎛️ ZEROSUM ALPHA")
st.caption("AI Infrastructure Intelligence • Quantitative Analysis Engine")

col1, col2 = st.columns([8, 2])
with col1:
    st.markdown(f"**Market Regime Indicator:** `{data['regime']}`")
with col2:
    st.markdown(f"**Last Update:** `{data['generated']}`")

st.markdown("---")

# 4. TABBED NAVIGATION PLATFORM
tab1, tab2, tab3, tab4 = st.tabs(["📊 Rankings", "🌌 Universe", "📰 Weekly Report", "🔍 Company Detail"])

with tab1:
    st.subheader("Rankings — All Tracked Stocks")
    
    # Summary Metrics Rows
    m1, m2, m3 = st.columns(3)
    m1.metric("Universe Size", f"{len(df)} Stocks")
    m2.metric("Tier 1 (High Conviction)", f"{len(df[df['tier'] == 1])} Stocks")
    m3.metric("Average System Score", f"{round(df['score'].mean(), 1)}")
    
    # Display Score Table Match
    display_df = df[['ticker', 'name', 'subsector', 'tier', 'score', 'rev_growth_pct', 'risk_flags']]
    st.dataframe(
        display_df, 
        column_config={
            "score": st.column_config.ProgressColumn("Quant Score", min_value=0, max_value=100, format="%d"),
            "rev_growth_pct": "Revenue Growth YoY (%)",
            "rel_strength_pct": "Relative Strength vs SPY (%)"
        },
        use_container_width=True,
        hide_index=True
    )
    
    # Side-by-side Risk & Mover Panels
    st.markdown("### Risk Analysis & Operational Flags")
    risk_df = df[df['risk_flags'] != "None"][['ticker', 'risk_flags']]
    if not risk_df.empty:
        st.table(risk_df)
    else:
        st.success("No critical infrastructure risk flags triggered this week.")

with tab2:
    st.subheader("AI Infrastructure Asset Matrix")
    for subsector, group in df.groupby('subsector'):
        st.markdown(f"#### {subsector}")
        st.write(", ".join([f"**{row['ticker']}** ({row['name']})" for _, row in group.iterrows()]))
        st.markdown("---")

with tab3:
    st.subheader("Sunday Executive Macro Briefing")
    st.markdown(f"### Core Narrative: System Environment is in `{data['regime']}`")
    st.write("Current computing clusters are exhibiting highly efficient capital deployment. Growth scoring remains concentrated across primary Silicon and specialized layer infrastructure architectures.")

with tab4:
    st.subheader("Granular Asset Analysis")
    selected_ticker = st.selectbox("Select Equity Blueprint", df['ticker'].unique())
    stock_row = df[df['ticker'] == selected_ticker].iloc[0]
    
    st.markdown(f"## {stock_row['name']} ({stock_row['ticker']})")
    st.markdown(f"**Subsector:** {stock_row['subsector']} | **Assigned Priority:** Tier {stock_row['tier']}")
    st.info(f"**System Thesis:** {stock_row['thesis']}")
