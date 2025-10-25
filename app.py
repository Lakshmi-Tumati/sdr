import streamlit as st
from main import AISDR
from config import API_KEY

# compute weighted score based on user scoring
def weighted_score(ai_scores: dict, user_weights: dict) -> float:
    total_weight = sum(user_weights.values())
    if total_weight == 0:
        return 0
    weighted_sum = sum(ai_scores[k] * user_weights[k] for k in ai_scores)
    weighted_avg = weighted_sum / total_weight
    return ((weighted_avg - 1) / 4) * 100

def main():
    st.title("AI Sales Development Representative (SDR)")

    if "sdr" not in st.session_state:
        st.session_state.sdr = AISDR()
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = []
    if "ai_scores" not in st.session_state:
        st.session_state.ai_scores = None
    if "user_weights" not in st.session_state:
        # Default equal weights
        st.session_state.user_weights = {
            "budget": 3,
            "company_size": 3,
            "business_needs": 3,
            "industry_fit": 3,
            "urgency": 3,
            "engagement": 3
        }
    
    if "input" not in st.session_state:
        st.session_state.input = ""
    if "clear_input" not in st.session_state:
        st.session_state.clear_input = False

    if st.session_state.clear_input:
        st.session_state.input = ""
        st.session_state.clear_input = False

    # Display chat messages
    for msg in st.session_state.chat_history:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    user_input = st.text_input("Ask something:", key="input")

    if st.button("Send") and user_input:
        reply = st.session_state.sdr.ask(user_input)
        st.session_state.chat_history.append({"role": "user", "content": user_input})
        st.session_state.chat_history.append({"role": "assistant", "content": reply})

        st.session_state.clear_input = True
        st.rerun()

    if st.button("Score Lead"):
        with st.spinner("AI is scoring the lead..."):
            try:
                # AI scoring called but not shown
                scores = st.session_state.sdr.score_lead()
                st.session_state.ai_scores = scores
                st.success("Lead scored internally. Adjust weights below.")
            except Exception as e:
                st.error(f"Error scoring lead: {e}")

    if st.session_state.ai_scores:
        st.markdown("Adjust Importance of Lead Scoring Factors")

        # Sliders for user to set weights (0-10 for example)
        for factor in st.session_state.user_weights:
            st.session_state.user_weights[factor] = st.slider(
                label=factor.replace("_", " ").title(),
                min_value=0,
                max_value=5,
                value=st.session_state.user_weights[factor],
                key=f"weight_{factor}"
            )

        if st.button("Calculate Final Score"):
            final_score = weighted_score(st.session_state.ai_scores, st.session_state.user_weights)
            st.markdown(f"Final Lead Score: **{final_score:.2f}%%** (Weighted)")
            
if __name__ == "__main__":
    main()