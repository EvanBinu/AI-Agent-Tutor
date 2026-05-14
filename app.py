import streamlit as st
from crewai import Crew, Process

from agents import (
    professor,
    tutor,
    question_generator
)

from tasks import create_tasks

# =========================
# PAGE CONFIG
# =========================

st.set_page_config(
    page_title="AI Academic Assistant",
    page_icon="📘",
    layout="wide"
)

# =========================
# CUSTOM CSS
# =========================

st.markdown("""
<style>

.main {
    background-color: #0E1117;
}

h1 {
    color: #FFFFFF;
    text-align: center;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 18px;
}

.agent-box {
    padding: 20px;
    border-radius: 10px;
    background-color: #1E1E1E;
    margin-bottom: 20px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.title("📘 AI Academic Assistant Team")

st.markdown("""
This AI system uses multiple collaborative agents:

- 👨‍🏫 Professor Agent
- 🧑‍🎓 Tutor Agent
- ❓ Question Generator Agent

Enter any academic topic to begin learning.
""")

# =========================
# INPUT
# =========================

topic = st.text_input(
    "Enter Topic",
    placeholder="Example: Operating Systems"
)

# =========================
# BUTTON
# =========================

if st.button("Generate Learning Content"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")
        st.stop()

    # Loading animation
    with st.spinner("AI Agents are collaborating..."):

        # Create tasks
        tasks = create_tasks(topic)

        # Create crew
        crew = Crew(
            agents=[
                professor,
                tutor,
                question_generator
            ],
            tasks=tasks,
            process=Process.sequential,
            verbose=False
        )

        # Execute crew
        crew.kickoff()

    # Success message
    st.success("Content Generated Successfully!")

    # =========================
    # DISPLAY INDIVIDUAL OUTPUTS
    # =========================

    st.markdown("---")

    # Professor Output
    with st.expander("👨‍🏫 Professor Agent", expanded=True):
        st.markdown(tasks[0].output.raw)

    # Tutor Output
    with st.expander("🧑‍🎓 Tutor Agent", expanded=False):
        st.markdown(tasks[1].output.raw)

    # Question Generator Output
    with st.expander("❓ Question Generator Agent", expanded=False):
        st.markdown(tasks[2].output.raw)