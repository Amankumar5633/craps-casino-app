import streamlit as st
import random
import time
import matplotlib.pyplot as plt

# -------- PAGE CONFIG --------
st.set_page_config(page_title="🎲 Craps Casino", layout="centered")

# -------- CUSTOM UI (CASINO STYLE) --------
st.markdown("""
<style>
body {
    background-color: #0e1117;
    color: white;
}
h1 {
    text-align: center;
    color: #00ffcc;
}
.stButton>button {
    border-radius: 10px;
    background: linear-gradient(90deg, #00ffcc, #00ccff);
    color: black;
    font-weight: bold;
    height: 3em;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎲 Craps Casino</h1>", unsafe_allow_html=True)

# -------- SESSION STATE --------
if "balance" not in st.session_state:
    st.session_state.balance = 100
    st.session_state.bet = 10
    st.session_state.point = None
    st.session_state.phase = "comeout"
    st.session_state.history = []

# -------- FUNCTIONS --------
def roll_dice_animation():
    placeholder = st.empty()
    for _ in range(10):
        d1 = random.randint(1,6)
        d2 = random.randint(1,6)
        placeholder.markdown(f"## 🎲 {d1} 🎲 {d2}")
        time.sleep(0.08)
    return d1, d2

def reset_round():
    st.session_state.point = None
    st.session_state.phase = "comeout"

# -------- UI --------
col1, col2 = st.columns(2)
col1.metric("💰 Balance", f"₹{st.session_state.balance}")
col2.metric("🎯 Bet", f"₹{st.session_state.bet}")

st.markdown("---")

# Bet Controls
col3, col4 = st.columns(2)

if col3.button("➕ Increase Bet"):
    st.session_state.bet += 10

if col4.button("➖ Decrease Bet"):
    st.session_state.bet = max(10, st.session_state.bet - 10)

st.markdown("---")

# Roll Dice
if st.button("🎲 Roll Dice"):
    if st.session_state.balance < st.session_state.bet:
        st.error("❌ Not enough balance!")
    else:
        d1, d2 = roll_dice_animation()
        total = d1 + d2

        st.markdown(f"## Result: 🎲 {d1} + {d2} = {total}")

        # COME OUT PHASE
        if st.session_state.phase == "comeout":
            if total in [7, 11]:
                st.success("🎉 You WIN!")
                st.session_state.balance += st.session_state.bet
            elif total in [2, 3, 12]:
                st.error("💀 You LOSE!")
                st.session_state.balance -= st.session_state.bet
            else:
                st.session_state.point = total
                st.session_state.phase = "point"
                st.warning(f"👉 Point set to {total}")

        # POINT PHASE
        else:
            if total == st.session_state.point:
                st.success("🎉 You hit the point → WIN!")
                st.session_state.balance += st.session_state.bet
                reset_round()
            elif total == 7:
                st.error("💀 Rolled 7 → LOSE!")
                st.session_state.balance -= st.session_state.bet
                reset_round()
            else:
                st.info("➡️ Keep rolling...")

        st.session_state.history.append(st.session_state.balance)

# -------- POINT DISPLAY --------
if st.session_state.point:
    st.markdown(f"### 🎯 Current Point: {st.session_state.point}")

# -------- GRAPH --------
st.markdown("---")
st.subheader("📊 Balance Over Time")

if len(st.session_state.history) > 1:
    fig, ax = plt.subplots()
    ax.plot(st.session_state.history)
    ax.set_xlabel("Rounds")
    ax.set_ylabel("Balance")
    ax.set_title("Performance")
    st.pyplot(fig)
else:
    st.info("Play more rounds to see graph!")

# -------- RESET --------
if st.button("🔄 Reset Game"):
    st.session_state.balance = 100
    st.session_state.bet = 10
    st.session_state.point = None
    st.session_state.phase = "comeout"
    st.session_state.history = []