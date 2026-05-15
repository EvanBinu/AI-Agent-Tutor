import streamlit as st
from crewai import Crew, Process, Task
import json
# =========================
# IMPORTS
# =========================

import database

from database import conn, cursor

from memory import (
    shared_memory,
    send_message
)

from a2a_workflow import tutor_remediation

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

if "score" not in st.session_state:
    st.session_state.score = 0

if "percentage" not in st.session_state:
    st.session_state.percentage = 0

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
    color: white;
    text-align: center;
}

.stButton > button {
    width: 100%;
    border-radius: 10px;
    height: 3em;
    font-size: 18px;
}

</style>
""", unsafe_allow_html=True)

# =========================
# HEADER
# =========================

st.title("📘 AI Academic Assistant Team")

st.markdown("""
This AI system uses collaborative AI agents:

- 👨‍🏫 Professor Agent
- 🧑‍🎓 Tutor Agent
- ❓ Question Generator Agent
- 📝 Evaluator Agent

Features:
- Multi-Agent Collaboration
- A2A Communication
- Persistent Memory
- Personalized Remediation
""")

# =========================
# TOPIC INPUT
# =========================

topic = st.text_input(
    "Enter Topic",
    placeholder="Example: Operating Systems"
)

# =========================
# GENERATE CONTENT
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

        # Store session data
        st.session_state.tasks = tasks
        st.session_state.questions = tasks[2].output.raw
        st.session_state.content_generated = True

        # Save learning history
        cursor.execute("""
        INSERT INTO learning_history(
            topic,
            activity
        )
        VALUES (?, ?)
        """, (
            topic,
            "Generated learning content"
        ))

        conn.commit()

# =========================
# DISPLAY CONTENT
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

    with st.expander("🧑‍🎓 Tutor Agent"):
        st.markdown(tasks[1].output.raw)

    # =========================
    # QUESTIONS OUTPUT
    # =========================

    with st.expander("❓ Question Generator Agent"):
        st.markdown(tasks[2].output.raw)

    # =========================
    # ANSWER SUBMISSION
    # =========================

    st.markdown("---")
    st.subheader("📝 Submit Your Answers")

    student_answers = st.text_area(
        "Enter your answers",
        height=200,
        placeholder="""
Example:

1. A
2. B
3. C
"""
    )

    # =========================
    # EVALUATE ANSWERS
    # =========================

    if st.button("Evaluate Answers"):

        if student_answers.strip() == "":
            st.warning("Please enter your answers.")
            st.stop()

        with st.spinner("Evaluator Agent is checking answers..."):

# =========================
# EVALUATION TASK
# =========================

            evaluation_task = Task(
                description=f"""
            Evaluate the student's answers.

            QUESTIONS:
            {st.session_state.questions}

            STUDENT ANSWERS:
            {student_answers}

            Return ONLY valid JSON.

            FORMAT:

            {{
                "score": 0,
                "percentage": 0,
                "correct_answers": [
                    {{
                        "question": "Question text",
                        "correct_answer": "A"
                    }}
                ],
                "wrong_answers": [
                    {{
                        "question": "Question text",
                        "student_answer": "B",
                        "correct_answer": "C"
                    }}
                ],
                "feedback": "Short feedback",
                "suggestions": [
                    "Suggestion 1",
                    "Suggestion 2"
                ]
            }}

            RULES:
            - No markdown
            - No explanations outside JSON
            - No extra text
            - Valid JSON only

            SCORING RULES:
            - There are 3 MCQs
            - Each correct answer = 1 mark
            - Wrong answer = 0
            - No partial marks

            CALCULATE:
            percentage = (score / 3) * 100
            """,
                expected_output="Valid JSON evaluation report.",
                agent=evaluator
            )

            # =========================
            # CREATE EVALUATION CREW
            # =========================

            evaluation_crew = Crew(
                agents=[evaluator],
                tasks=[evaluation_task],
                process=Process.sequential,
                verbose=False
            )

            # =========================
            # RUN EVALUATION
            # =========================

            evaluation_result = evaluation_crew.kickoff()

            # =========================
            # PARSE JSON RESPONSE
            # =========================

            try:

                evaluation_data = json.loads(
                    str(evaluation_result)
                )

            except Exception as e:

                st.error("Invalid JSON returned by Evaluator Agent")

                st.code(str(e))

                st.stop()

            # =========================
            # EXTRACT STRUCTURED DATA
            # =========================

            score = evaluation_data["score"]

            percentage = evaluation_data["percentage"]

            correct_answers = evaluation_data["correct_answers"]

            wrong_answers = evaluation_data["wrong_answers"]

            feedback = evaluation_data["feedback"]

            suggestions = evaluation_data["suggestions"]

            # =========================
            # STORE SESSION DATA
            # =========================

            st.session_state.evaluation_result = evaluation_data

            st.session_state.score = score

            st.session_state.percentage = percentage

            # =========================
            # SAVE RESULTS TO DATABASE
            # =========================

            cursor.execute("""
            INSERT INTO results(
                topic,
                score,
                percentage,
                correct_answers,
                wrong_answers,
                feedback,
                suggestions
            )
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                topic,
                score,
                percentage,
                json.dumps(correct_answers),
                json.dumps(wrong_answers),
                feedback,
                json.dumps(suggestions)
            ))

            conn.commit()

            # =========================
            # WEAK TOPIC DETECTION
            # =========================

            if percentage < 50:

                weak_topic = topic

                # Save weak topic
                cursor.execute("""
                INSERT INTO weak_topics(topic)
                VALUES (?)
                """, (weak_topic,))

                conn.commit()

                # Shared memory
                shared_memory["weak_topics"].append(
                    weak_topic
                )

                # A2A message
                existing_messages = shared_memory["agent_messages"]

                message_content = f"Student is weak in {weak_topic}"

                already_exists = any(
                    msg["content"] == message_content
                    for msg in existing_messages
                )

                if not already_exists:

                    send_message(
                        "Evaluator",
                        "Tutor",
                        message_content
                    )

                # Save agent message
                cursor.execute("""
                INSERT INTO agent_messages(
                    sender,
                    receiver,
                    content
                )
                VALUES (?, ?, ?)
                """, (
                    "Evaluator",
                    "Tutor",
                    f"Student is weak in {weak_topic}"
                ))

                conn.commit()

# =========================
# DISPLAY EVALUATION
# =========================

if st.session_state.evaluation_result:

    st.markdown("---")

    st.success("Evaluation Completed!")

    st.markdown("## 📊 Evaluation Report")

    evaluation = st.session_state.evaluation_result

    # =========================
    # EVALUATION SUMMARY
    # =========================

    st.markdown("## 📊 Evaluation Summary")

    # Score
    st.markdown(f"""
    ### ✅ Score

    {evaluation['score']}/3
    """)

    # Percentage
    st.markdown(f"""
    ### 📈 Percentage

    {evaluation['percentage']}%
    """)

    # =========================
    # CORRECT ANSWERS
    # =========================

    st.markdown("## ✔ Correct Answers")

    for item in evaluation["correct_answers"]:

        st.success(f"""
    Question:
    {item['question']}

    Correct Answer:
    {item['correct_answer']}
    """)

    # =========================
    # WRONG ANSWERS
    # =========================

    st.markdown("## ❌ Wrong Answers")

    for item in evaluation["wrong_answers"]:

        st.error(f"""
    Question:
    {item['question']}

    Your Answer:
    {item['student_answer']}

    Correct Answer:
    {item['correct_answer']}
    """)

    # =========================
    # FEEDBACK
    # =========================

    st.markdown("## 💬 Feedback")

    st.info(evaluation["feedback"])

    # =========================
    # SUGGESTIONS
    # =========================

    st.markdown("## 🚀 Suggestions")

    for item in evaluation["suggestions"]:

        st.markdown(f"- {item}")

    for item in evaluation["suggestions"]:
        st.markdown(f"- {item}")

    st.markdown(f"""
### 📈 Performance Summary

- Score: {st.session_state.score}/3
- Percentage: {st.session_state.percentage}%
""")

# =========================
# REMEDIAL LEARNING
# =========================

remediation = tutor_remediation()

if remediation:

    st.markdown("---")
    st.subheader("📘 Personalized Remedial Learning")

    for item in remediation:

        remedial_task = Task(
            description=f"""
Create a short remedial lesson.

MESSAGE:
{item}

RULES:
- Under 100 words
- Simple explanation
- Beginner friendly
""",
            expected_output="Short remedial lesson.",
            agent=tutor
        )

        remedial_crew = Crew(
            agents=[tutor],
            tasks=[remedial_task],
            verbose=False
        )

        remedial_result = remedial_crew.kickoff()

        st.markdown(remedial_result)