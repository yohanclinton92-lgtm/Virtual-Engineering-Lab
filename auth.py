import streamlit as st

USERS = {
    "student1": {"password": "1234", "role": "student"},
    "faculty1": {"password": "1234", "role": "faculty"},
    "admin1": {"password": "1234", "role": "admin"}
}

def login():
    st.title("🔐 Login")

    u = st.text_input("Username")
    p = st.text_input("Password", type="password")

    if st.button("Login"):
        if u in USERS and USERS[u]["password"] == p:
            st.session_state.logged_in = True
            st.session_state.username = u
            st.session_state.role = USERS[u]["role"]
            st.experimental_rerun()
        else:
            st.error("Invalid credentials")

def logout():
    st.session_state.clear()
    st.experimental_rerun()
