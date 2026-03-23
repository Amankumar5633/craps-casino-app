import streamlit as st
import random
import time
import matplotlib.pyplot as plt

st.set_page_config(page_title="🎰 Vegas Craps", layout="wide")

# ---------- NEON CASINO UI ----------
st.markdown("""
<style>
body {
    background: radial-gradient(circle, #0b0f1a, #000000);
    color: white;
}
h1 {
    text-align: center;
    color: #00ffcc;
    text-shadow: 0 0 20px #00ffcc;
}
.chip {
    font-size: 22px;
    padding: 8px;
    border-radius: 50%;
    background: gold;
    color: black;
    text-align: center;
}
.result {
    text-align: center;
    font-size: 32px;
    margin-top: 10px;
}
</style>
""", unsafe_allow_html=True)

st.markdown("<h1>🎰 VEGAS CRAPS TABLE</h1>", unsafe_allow_html=True)

# ---------- STATE ----------
if "balance" not in st.session_state:
    st.session_state.balance = 1000
    st.session_state.bet = 100
    st.session_state.point = None
    st.session_state.phase = "comeout"
    st.session_state.history = []
    st.session_state.result = ""
    st.session_state.bet_type = "Pass Line"

# ---------- SIDEBAR ----------
st.sidebar.title("🎲 Casino Controls")

st.session_state.bet = st.sidebar.slider("🪙 Chips", 50, 500, st.session_state.bet, step=50)

st.session_state.bet_type = st.sidebar.radio(
    "🎯 Bet Type",
    ["Pass Line", "Don't Pass"]
)

# ---------- TOP DASHBOARD ----------
c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Balance", f"₹{st.session_state.balance}")
c2.metric("🪙 Bet", f"₹{st.session_state.bet}")
c3.metric("🎯 Point", st.session_state.point if st.session_state.point else "-")
c4.metric("🎲 Phase", st.session_state.phase.upper())

st.markdown("---")

# ---------- SOUND ----------
def play_sound():
    st.audio("https://www.soundjay.com/misc/sounds/dice-roll-1.mp3")

# ---------- DICE ----------
dice_images = {
    1: "https://upload.wikimedia.org/wikipedia/commons/1/1b/Dice-1-b.svg",
    2: "https://upload.wikimedia.org/wikipedia/commons/5/5f/Dice-2-b.svg",
    3: "https://upload.wikimedia.org/wikipedia/commons/b/b1/Dice-3-b.svg",
    4: "https://upload.wikimedia.org/wikipedia/commons/f/fd/Dice-4-b.svg",
    5: "https://upload.wikimedia.org/wikipedia/commons/0/08/Dice-5-b.svg",
    6: "https://upload.wikimedia.org/wikipedia/commons/2/26/Dice-6-b.svg"
}

dice_area = st.empty()

def roll_animation():
    play_sound()
    for _ in range(10):
        d1 = random.randint(1,6)
        d2 = random.randint(1,6)
        dice_area.image([dice_images[d1], dice_images[d2]], width=120)
        time.sleep(0.08)
    return d1, d2

def reset_round():
    st.session_state.point = None
    st.session_state.phase = "comeout"

# ---------- GAME LOGIC ----------
def play_round(total):
    bet_type = st.session_state.bet_type

    if st.session_state.phase == "comeout":
        if total in [7,11]:
            win = (bet_type == "Pass Line")
        elif total in [2,3,12]:
            win = (bet_type == "Don't Pass")
        else:
            st.session_state.point = total
            st.session_state.phase = "point"
            st.session_state.result = f"🎯 Point is {total}"
            return
    else:
        if total == st.session_state.point:
            win = (bet_type == "Pass Line")
            reset_round()
        elif total == 7:
            win = (bet_type == "Don't Pass")
            reset_round()
        else:
            st.session_state.result = f"➡️ Rolling... ({total})"
            return

    if win:
        st.session_state.balance += st.session_state.bet
        st.session_state.result = f"🎉 WIN ({bet_type})"
    else:
        st.session_state.balance -= st.session_state.bet
        st.session_state.result = f"💀 LOSE ({bet_type})"

    st.session_state.history.append(st.session_state.balance)

# ---------- CENTER TABLE ----------
st.markdown("## 🎲 Roll Area")

if st.button("🎲 ROLL DICE", use_container_width=True):
    if st.session_state.balance < st.session_state.bet:
        st.error("❌ Not enough chips!")
    else:
        d1, d2 = roll_animation()
        total = d1 + d2
        play_round(total)

# ---------- RESULT ----------
st.markdown(f"<div class='result'>{st.session_state.result}</div>", unsafe_allow_html=True)

# ---------- STATS ----------
st.markdown("---")
colA, colB = st.columns(2)

with colA:
    st.subheader("📊 Balance Trend")
    if len(st.session_state.history) > 1:
        fig, ax = plt.subplots()
        ax.plot(st.session_state.history)
        ax.set_xlabel("Rounds")
        ax.set_ylabel("Balance")
        st.pyplot(fig)

with colB:
    st.subheader("📈 Game Stats")
    st.write(f"Total Rounds: {len(st.session_state.history)}")
    if st.session_state.history:
        st.write(f"Max Balance: ₹{max(st.session_state.history)}")
        st.write(f"Min Balance: ₹{min(st.session_state.history)}")

# ---------- RESET ----------
st.markdown("---")
if st.button("🔄 RESET TABLE", use_container_width=True):
    st.session_state.balance = 1000
    st.session_state.bet = 100
    st.session_state.point = None
    st.session_state.phase = "comeout"
    st.session_state.history = []
    st.session_state.result = ""