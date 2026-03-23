import streamlit as st
import requests

API = "http://127.0.0.1:8000"

st.title("🎰 Craps SaaS Casino")

# -------- LOGIN --------
if "user" not in st.session_state:
    st.session_state.user = None

if not st.session_state.user:
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        res = requests.post(f"{API}/login", json={
            "username": username,
            "password": password
        })

        if res.status_code == 200:
            st.session_state.user = username
            st.success("Logged in!")
        else:
            st.error("Login failed")

    if st.button("Register"):
        requests.post(f"{API}/register", json={
            "username": username,
            "password": password
        })
        st.success("Registered!")

    st.stop()

# -------- GAME --------
st.subheader(f"Welcome {st.session_state.user}")

if st.button("🎲 Roll Dice"):
    res = requests.post(f"{API}/roll/{st.session_state.user}")
    data = res.json()

    st.write(f"Dice: {data['dice']}")
    st.write(f"Result: {data['result']}")
    st.write(f"Balance: ₹{data['balance']}")