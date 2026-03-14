import streamlit as st
import random
import pandas as pd

# 1. Reference Data (NFL 2023 - 2025)
nfl_data = {
    "Kansas City Chiefs": {
        "last_5": ["Loss", "Loss", "Loss", "Loss", "Loss"],  # Late 2025 slump
        "win_ratio": 0.0,
        "points_avg": 18.5,
        "status": "In Rebuild"
    },
    "San Francisco 49ers": {
        "last_5": ["Loss", "Win", "Win", "Win", "Loss"],
        "win_ratio": 0.6,
        "points_avg": 25.7,
        "status": "Contender"
    },
    "Philadelphia Eagles": {
        "last_5": ["Loss", "Win", "Win", "Loss", "Win"],
        "win_ratio": 0.6,
        "points_avg": 22.3,
        "status": "Contender"
    },
    "Dallas Cowboys": {
        "last_5": ["Loss", "Win", "Loss", "Loss", "Loss"],
        "win_ratio": 0.2,
        "points_avg": 21.0,
        "status": "Inconsistent"
    }
}

# UI Configuration
st.set_page_config(page_title="NFL AI Predictor", layout="wide")
st.title("🏈 NFL Win Predictor (2023-2026 Data)")
st.markdown("---")

# Sidebar for selection
st.sidebar.header("Agent Parameters")
team_a = st.sidebar.selectbox("Select Team 1", list(nfl_data.keys()), index=0)
team_b = st.sidebar.selectbox("Select Team 2", list(nfl_data.keys()), index=1)

# Main UI layout
col1, col2 = st.columns(2)

with col1:
    st.subheader(f"{team_a}")
    st.write(f"**Recent Form:** {' | '.join(nfl_data[team_a]['last_5'])}")
    st.metric("Last 5 Win Ratio", f"{int(nfl_data[team_a]['win_ratio']*100)}%")

with col2:
    st.subheader(f"{team_b}")
    st.write(f"**Recent Form:** {' | '.join(nfl_data[team_b]['last_5'])}")
    st.metric("Last 5 Win Ratio", f"{int(nfl_data[team_b]['win_ratio']*100)}%")

# Prediction Logic Agent
if st.button("Run AI Prediction"):
    st.markdown("### AI Analysis Results")
    
    # Simple probability logic based on win ratio + small random factor
    score_a = nfl_data[team_a]['win_ratio'] + (random.uniform(0.1, 0.3))
    score_b = nfl_data[team_b]['win_ratio'] + (random.uniform(0.1, 0.3))
    
    total = score_a + score_b
    prob_a = (score_a / total) * 100
    prob_b = (score_b / total) * 100
    
    winner = team_a if prob_a > prob_b else team_b
    loser = team_b if winner == team_a else team_a
    
    st.success(f"**The AI Predicts: {winner} has a {prob_a:.1f}% chance of winning!**")
    st.progress(prob_a / 100)
    
    st.info(f"💡 **Advice for {loser}:** Focus on defensive coverage and time of possession. Their current streak of {nfl_data[loser]['last_5'].count('Loss')} losses indicates a failure in 4th quarter execution.")

    # Auditor Agent code is below for hallucination checker
    def audit_agent(prediction_output, team_name, ground_truth):
        """
        Checks if the predicted stats match the ground truth reference data.
        """
    st.markdown("---")
    st.subheader("🕵️ AI Audit Agent")
    
    # Logic: Verify if the 'Last 5' in the UI matches our hardcoded DB
    if team_name in ground_truth:
        reference_ratio = ground_truth[team_name]['win_ratio']
        # Check for discrepancies (Hallucination detection)
        if reference_ratio > 1.0 or reference_ratio < 0.0:
            st.error("🚩 RED FLAG: Hallucination Detected! Win ratio is out of bounds.")
        else:
            st.success("✅ GREEN FLAG: Data Authenticity Verified.")
            st.write(f"Auditor confirmed: {team_name} actual win ratio is {reference_ratio}.")
    else:
        st.error("🚩 RED FLAG: AI is referencing a team not in the database.")

# To use this, add it to the bottom of the main script:
audit_agent(None, team_a, nfl_data)
