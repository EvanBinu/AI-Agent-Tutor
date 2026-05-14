import os

os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"

import streamlit as st
from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Configure page
st.set_page_config(
    page_title="AI Academic Assistant",
    page_icon="📘",
    layout="wide"
)

st.title("📘 AI Academic Assistant Team")

# Topic input
topic = st.text_input("Enter a topic")

# Generate button
if st.button("Generate Learning Content"):

    # Configure LLM
    llm = LLM(
        model="groq/llama-3.3-70b-versatile",
        api_key=os.getenv("GROQ_API_KEY")
    )

    # Professor Agent
    professor = Agent(
        role="Professor",
        goal="Explain concepts in depth",
        backstory="Experienced university professor",
        verbose=False,
        llm=llm
    )

    # Tutor Agent
    tutor = Agent(
        role="Tutor",
        goal="Simplify concepts",
        backstory="Friendly tutor using examples",
        verbose=False,
        llm=llm
    )

    # Question Generator
    question_generator = Agent(
        role="Question Generator",
        goal="Generate practice questions",
        backstory="Academic evaluator",
        verbose=False,
        llm=llm
    )

    # Tasks
    professor_task = Task(
        description=f"Explain {topic} in detail.",
        expected_output="Detailed explanation",
        agent=professor
    )

    tutor_task = Task(
        description=f"Simplify the topic {topic} with examples.",
        expected_output="Simplified explanation",
        agent=tutor
    )

    question_task = Task(
        description=f"Generate 5 MCQs for {topic}.",
        expected_output="Practice questions",
        agent=question_generator
    )

    # Crew
    crew = Crew(
        agents=[
            professor,
            tutor,
            question_generator
        ],
        tasks=[
            professor_task,
            tutor_task,
            question_task
        ],
        process=Process.sequential,
        verbose=False
    )

    # Loading spinner
    with st.spinner("Agents are collaborating..."):

        result = crew.kickoff()

    # Output
    st.success("Content Generated Successfully!")

    st.markdown(result)