import streamlit as st
import json, os
import numpy as np
import matplotlib.pyplot as plt

from engine import run_experiment
from auth import login, logout
from db import log_experiment

# ---------- LOGIN ----------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if not st.session_state.logged_in:
    login()
    st.stop()

if st.session_state.role != "student":
    st.error("Student access only")
    st.stop()

st.sidebar.write(f"User: {st.session_state.username}")
if st.sidebar.button("Logout"):
    logout()

st.title("🧪 Virtual Engineering Laboratory")

# ---------- LOAD EXPERIMENT ----------
BASE = "experiments"
dept = st.sidebar.selectbox("Select Department", os.listdir(BASE))
dept_path = os.path.join(BASE, dept)

exp_files = [f for f in os.listdir(dept_path) if f.endswith(".json")]
exp_map = {f.replace(".json","").replace("_"," ").title(): f for f in exp_files}

exp_name = st.sidebar.selectbox("Select Experiment", exp_map.keys())
exp_path = os.path.join(dept_path, exp_map[exp_name])

with open(exp_path, "r", encoding="utf-8") as f:
    experiment = json.load(f)

st.subheader(experiment["meta"]["name"])

# ---------- THEORY ----------
with st.expander("📘 About the Experiment", expanded=True):
    st.markdown("### Aim")
    st.write(experiment["theory"]["aim"])
    st.markdown("### Theory")
    st.write(experiment["theory"]["description"])
    st.markdown("### Procedure")
    for p in experiment["theory"]["procedure"]:
        st.write("•", p)
    st.markdown("### Applications")
    for a in experiment["theory"]["applications"]:
        st.write("•", a)

# ---------- INPUTS ----------
st.sidebar.markdown("### Inputs")
inputs = {}

for i in experiment["inputs"]:
    if i.get("type") == "choice":
        inputs[i["key"]] = st.sidebar.selectbox(i["label"], i["options"])
    else:
        inputs[i["key"]] = st.sidebar.number_input(
            i["label"],
            float(i.get("min", 0)),
            float(i.get("max", 100)),
            float(i.get("min", 0))
        )

# ---------- RUN ----------
if st.sidebar.button("▶ Run Experiment"):
    result = run_experiment(experiment, inputs)

    st.subheader("📊 Results")
    for k, v in result["results"].items():
        st.write(f"{k} = {v}")

    if result["feedback"]:
        st.subheader("🧠 Feedback")
        for f in result["feedback"]:
            st.write("•", f)

    # ---------- CALCULATIONS ----------
    if experiment.get("calculation_steps"):
        st.subheader("🧮 Calculations")
        for step in experiment["calculation_steps"]:
            st.markdown(f"### {step['title']}")
            st.write(step["explanation"])
            st.code(step["formula"])

    eff = result["results"].get("effectiveness")
    if eff:
        log_experiment(st.session_state.username, experiment["meta"]["name"], eff)

    # ---------- HEAT EXCHANGER PLOT ----------
    if experiment["meta"]["name"] == "Heat Exchanger":
        x = np.linspace(0, 1, 10)
        Th = np.linspace(inputs["Th_in"], result["results"]["Th_out"], 10)
        Tc = np.linspace(inputs["Tc_in"], result["results"]["Tc_out"], 10)

        fig, ax = plt.subplots()
        ax.plot(x, Th, label="Hot Fluid")
        ax.plot(x, Tc, label="Cold Fluid")
        ax.legend()
        st.pyplot(fig)
