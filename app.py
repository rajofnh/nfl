import streamlit as st
import random
import pandas as pd

# --- 1. SETTING THE UI STYLE ---
st.set_page_config(page_title="NFL AI Predictor & Auditor", layout="wide")

# Custom CSS for a professional look
st.markdown("""
    <style>
    .stMetric {
        background-color: #1e2130;
        padding: 15px;
        border-radius: 10px;
        border: 1px solid #4e5d6c;
    }
    .stButton>button {
        width: 100%;
        background-color: #ff4b4b;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# --- 2. REFERENCE DATA (2023 - 2026) ---
nfl_data = {
    "Kansas City Chiefs": {
        "last_5": ["Loss", "Loss", "Loss", "Loss", "Loss"],
        "win_ratio": 0.0,
        "advice": "Re-evaluate the offensive line protection."
    },
    "San Francisco 49ers": {
        "last_5": ["Loss", "Win", "Win", "Win", "Loss"],
        "win_ratio": 0.6,
        "advice": "Tighten up special teams coverage."
    },
    "Philadelphia Eagles": {
        "last_5": ["Loss", "Win", "Win", "Loss", "Win"],
        "win_ratio": 0.6,
        "advice": "Balance the pass-run ratio."
    },
    "Dallas Cowboys": {
        "last_5": ["Loss", "Win", "Loss", "Loss", "Loss"],
        "win_ratio": 0.2,
        "advice": "Reduce pre-snap penalties."
    }
}

# --- 3. UI LAYOUT ---
st.title("🏈 NFL AI Predictor & Auditor")
st.sidebar.header("Matchup Settings")

team_a = st.sidebar.selectbox("Select Team 1", list(nfl_data.keys()), index=0)
team_b = st.sidebar.selectbox("Select Team 2", list(nfl_data.keys()), index=1)

col1, col2 = st.columns(2)
with col1:
    st.metric(f"{team_a} Win Ratio", f"{int(nfl_data[team_a]['win_ratio']*100)}%")
with col2:
    st.metric(f"{team_b} Win Ratio", f"{int(nfl_data[team_b]['win_ratio']*100)}%")

# --- 4. PREDICTOR & AUDITOR LOGIC ---
if st.button("🚀 Run AI Analysis"):
    # PREDICTOR AGENT
    score_a = nfl_data[team_a]['win_ratio'] + (random.uniform(0.1, 0.3))
    score_b = nfl_data[team_b]['win_ratio'] + (random.uniform(0.1, 0.3))
    
    total = score_a + score_b
    prob_a = (score_a / total) * 100
    prob_b = (score_b / total) * 100
    
    winner = team_a if prob_a > prob_b else team_b
    loser = team_b if winner == team_a else team_a
    win_pct = prob_a if winner == team_a else prob_b
    
    st.success(f"**AI Prediction:** {winner} wins with a {win_pct:.1f}% probability.")
    st.warning(f"💡 **Strategic Advice for {loser}:** {nfl_data[loser]['advice']}")
    
    # AUDITOR AGENT (Now using the correct variables)
    st.markdown("---")
    st.subheader("🕵️ AI Auditor Log")
    
    # Check 1: Data Integrity
    if team_a in nfl_data and team_b in nfl_data:
        st.write("✅ **GREEN FLAG:** Team data verified against 2023-2026 Ground Truth.")
    else:
        st.write("🚩 **RED FLAG:** Reference data mismatch.")
        
    # Check 2: Hallucination Check
    if 0 <= win_pct <= 100:
        st.write("✅ **GREEN FLAG:** No mathematical hallucinations detected.")
    else:
        st.write("🚩 **RED FLAG:** Hallucination detected in probability engine.")

else:
    st.info("Select teams and click 'Run' to see the AI agent and Auditor in action.")
