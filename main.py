import os

os.environ["OTEL_SDK_DISABLED"] = "true"
os.environ["LITELLM_LOCAL_MODEL_COST_MAP"] = "True"

from crewai import Agent, Task, Crew, Process, LLM
from dotenv import load_dotenv

load_dotenv()

# Configure LLM
llm = LLM(
    model="groq/llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY")
)

# =========================
# AGENTS
# =========================

# Professor Agent
professor = Agent(
    role="Professor",
    goal="Provide detailed and accurate conceptual explanations",
    backstory=(
        "You are an experienced university professor "
        "specialized in computer science subjects."
    ),
    verbose=True,
    llm=llm
)

# Tutor Agent
tutor = Agent(
    role="Tutor",
    goal="Simplify difficult concepts for students",
    backstory=(
        "You are a friendly tutor who explains topics "
        "using simple language and practical examples."
    ),
    verbose=True,
    llm=llm
)

# Question Generator Agent
question_generator = Agent(
    role="Question Generator",
    goal="Generate useful practice questions for students",
    backstory=(
        "You are an academic evaluator who creates "
        "MCQs and descriptive questions for learning."
    ),
    verbose=True,
    llm=llm
)

# =========================
# USER INPUT
# =========================

topic = input("Enter topic: ")

# =========================
# TASKS
# =========================

# Task 1 - Professor explains
professor_task = Task(
    description=(
        f"Explain the topic '{topic}' in detail "
        "with proper concepts and technical depth."
    ),
    expected_output="Detailed conceptual explanation.",
    agent=professor
)

# Task 2 - Tutor simplifies
tutor_task = Task(
    description=(
        f"Simplify the explanation of '{topic}' "
        "using easy language and examples."
    ),
    expected_output="Simple student-friendly explanation.",
    agent=tutor
)

# Task 3 - Generate questions
question_task = Task(
    description=(
        f"Generate 5 MCQs and 3 descriptive questions "
        f"for the topic '{topic}'."
    ),
    expected_output="List of practice questions.",
    agent=question_generator
)

# =========================
# CREW
# =========================

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
    verbose=True
)

# =========================
# RUN CREW
# =========================

result = crew.kickoff()

print("\n\n================ FINAL OUTPUT ================\n")
print(result)