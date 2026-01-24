import streamlit as st
import json
import os
import numpy as np
import matplotlib.pyplot as plt

from engine import run_experiment
from db import log_experiment
from auth import login, logout


# ===============================
# LOGIN
# ===============================

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

if st.session_state.role != "student":
    st.error("Access denied")
    st.stop()


# ===============================
# PAGE SETUP
# ===============================

st.set_page_config(page_title="Virtual Engineering Lab", layout="wide")
st.title("🧪 Virtual Engineering Laboratory")

st.sidebar.write(f"User: {st.session_state.username}")
if st.sidebar.button("Logout"):
    logout()


# ===============================
# DEPARTMENT SELECTION
# ===============================

BASE_DIR = "experiments"

departments = [
    d for d in os.listdir(BASE_DIR)
    if os.path.isdir(os.path.join(BASE_DIR, d))
]

department = st.sidebar.selectbox("Select Department", sorted(departments))


# ===============================
# EXPERIMENT SELECTION
# ===============================

dept_path = os.path.join(BASE_DIR, department)

exp_files = [f for f in os.listdir(dept_path) if f.endswith(".json")]

exp_map = {
    f.replace(".json", "").replace("_", " ").title(): f
    for f in exp_files
}

exp_name = st.sidebar.selectbox("Select Experiment", sorted(exp_map.keys()))
exp_path = os.path.join(dept_path, exp_map[exp_name])


# ===============================
# LOAD JSON (UTF-8 SAFE)
# ===============================

with open(exp_path, "r", encoding="utf-8") as f:
    experiment = json.load(f)

st.subheader(f"{experiment['meta']['name']} | {experiment['meta']['subject']}")


# ===============================
# THEORY SECTION
# ===============================

if "theory" in experiment:
    with st.expander("📘 About the Experiment", expanded=True):
        st.markdown("### 🎯 Aim")
        st.write(experiment["theory"].get("aim", ""))

        st.markdown("### 📖 Theory")
        st.write(experiment["theory"].get("description", ""))

        st.markdown("### 🔬 Procedure")
        for p in experiment["theory"].get("procedure", []):
            st.write("•", p)

        st.markdown("### 🏭 Applications")
        for a in experiment["theory"].get("applications", []):
            st.write("•", a)


# ===============================
# INPUTS (ABSOLUTELY SAFE)
# ===============================

st.sidebar.markdown("### 🔢 Enter Inputs")
user_inputs = {}

for inp in experiment.get("inputs", []):

    key = inp.get("key")
    label = inp.get("label", key)
    input_type = inp.get("type", "number")

    if input_type == "choice":
        user_inputs[key] = st.sidebar.selectbox(
            label,
            inp.get("options", [])
        )
    else:
        min_val = float(inp.get("min", 0))
        max_val = float(inp.get("max", min_val + 100))
        default = float(inp.get("default", min_val))

        user_inputs[key] = st.sidebar.number_input(
            label,
            min_value=min_val,
            max_value=max_val,
            value=default
        )


# ===============================
# RUN EXPERIMENT
# ===============================

if st.sidebar.button("▶ Run Experiment"):

    result = run_experiment(experiment, user_inputs)

    if result["status"] != "success":
        st.error(result["message"])
        st.stop()

    st.success("Experiment completed")

    st.subheader("📊 Results")
    for k, v in result["results"].items():
        st.write(f"{k} : {v}")

    if result["feedback"]:
        st.subheader("🧠 Feedback")
        for f in result["feedback"]:
            st.write("•", f)

    eff = result["results"].get("effectiveness")
    if eff is not None:
        log_experiment(
            student=st.session_state.username,
            experiment=experiment["meta"]["name"],
            effectiveness=float(eff)
        )

    if experiment["meta"]["name"] == "Heat Exchanger":
        st.subheader("📈 Temperature Profile")
        x = np.linspace(0, 1, 10)
        Th = np.linspace(user_inputs["Th_in"], result["results"]["Th_out"], 10)
        Tc = np.linspace(user_inputs["Tc_in"], result["results"]["Tc_out"], 10)

        fig, ax = plt.subplots()
        ax.plot(x, Th, label="Hot Fluid")
        ax.plot(x, Tc, label="Cold Fluid")
        ax.legend()
        st.pyplot(fig)
