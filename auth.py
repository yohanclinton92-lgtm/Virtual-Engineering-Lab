import streamlit as st

# -------------------------------
# TEMP USERS (PILOT PHASE)
# -------------------------------
USERS = {
    "student1": {"password": "1234", "role": "student"},
    "faculty1": {"password": "1234", "role": "faculty"},
    "admin1": {"password": "1234", "role": "admin"}
}


def login():
    st.title("🔐 Virtual Lab Login")

    username = st.text_input("Username")
    password = st.text_input("Password", type="password")

    if st.button("Login"):
        if username in USERS and USERS[username]["password"] == password:
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.session_state["role"] = USERS[username]["role"]
            st.success("Login successful")
            st.rerun()
        else:
            st.error("Invalid username or password")


def logout():
    for key in ["logged_in", "username", "role"]:
        if key in st.session_state:
            del st.session_state[key]
    st.rerun()
