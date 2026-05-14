import streamlit as st
from crewai import Crew, Process, Task

from agents import (
    professor,
    tutor,
    question_generator,
    evaluator
)

from tasks import create_tasks

# =========================
# SESSION STATE
# =========================

if "questions" not in st.session_state:
    st.session_state.questions = None

if "tasks" not in st.session_state:
    st.session_state.tasks = None

if "content_generated" not in st.session_state:
    st.session_state.content_generated = False

if "evaluation_result" not in st.session_state:
    st.session_state.evaluation_result = None

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
- 📝 Evaluator Agent

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
# GENERATE CONTENT BUTTON
# =========================

if st.button("Generate Learning Content"):

    if topic.strip() == "":
        st.warning("Please enter a topic.")
        st.stop()

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

        # Store in session state
        st.session_state.tasks = tasks
        st.session_state.questions = tasks[2].output.raw
        st.session_state.content_generated = True

# =========================
# DISPLAY GENERATED CONTENT
# =========================

if st.session_state.content_generated:

    tasks = st.session_state.tasks

    st.success("Content Generated Successfully!")

    st.markdown("---")

    # =========================
    # PROFESSOR OUTPUT
    # =========================

    with st.expander("👨‍🏫 Professor Agent", expanded=True):
        st.markdown(tasks[0].output.raw)

    # =========================
    # TUTOR OUTPUT
    # =========================

    with st.expander("🧑‍🎓 Tutor Agent", expanded=False):
        st.markdown(tasks[1].output.raw)

    # =========================
    # QUESTION GENERATOR OUTPUT
    # =========================

    with st.expander("❓ Question Generator Agent", expanded=False):
        st.markdown(tasks[2].output.raw)

    # =========================
    # STUDENT ANSWERS
    # =========================

    st.markdown("---")
    st.subheader("📝 Submit Your Answers")

    student_answers = st.text_area(
        "Enter your answers here",
        height=200,
        placeholder="""
Example:

1. B
2. C
3. A

Descriptive:
Operating systems manage hardware...
"""
    )

    # =========================
    # EVALUATE BUTTON
    # =========================

    if st.button("Evaluate Answers"):

        if student_answers.strip() == "":
            st.warning("Please enter your answers.")
            st.stop()

        with st.spinner("Evaluator Agent is checking answers..."):

            evaluation_task = Task(
                description=f"""
Evaluate the student's answers.

QUESTIONS:
{st.session_state.questions}

STUDENT ANSWERS:
{student_answers}

Provide:
1. Overall score
2. Correct answers
3. Mistakes
4. Feedback
5. Suggestions for improvement
""",
                expected_output="Detailed evaluation report.",
                agent=evaluator
            )

            evaluation_crew = Crew(
                agents=[evaluator],
                tasks=[evaluation_task],
                process=Process.sequential,
                verbose=False
            )

            evaluation_result = evaluation_crew.kickoff()

            # Save evaluation result
            st.session_state.evaluation_result = evaluation_result

# =========================
# DISPLAY EVALUATION RESULT
# =========================

if st.session_state.evaluation_result:

    st.success("Evaluation Completed!")

    st.markdown("---")
    st.markdown("## 📊 Evaluation Report")

    st.markdown(st.session_state.evaluation_result)