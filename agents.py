from crewai import Agent
from config import llm

# Professor Agent
professor = Agent(
    role="Professor",
    goal="Provide detailed conceptual explanations",
    backstory=(
        "Experienced university professor "
        "specialized in academic subjects."
    ),
    verbose=False,
    llm=llm
)

# Tutor Agent
tutor = Agent(
    role="Tutor",
    goal="Simplify concepts with examples",
    backstory=(
        "Friendly tutor helping students "
        "understand difficult concepts."
    ),
    verbose=False,
    llm=llm
)

# Question Generator Agent
question_generator = Agent(
    role="Question Generator",
    goal="Generate practice questions",
    backstory=(
        "Academic evaluator creating "
        "MCQs and descriptive questions."
    ),
    verbose=False,
    llm=llm
)
# Evaluator Agent
evaluator = Agent(
    role="Evaluator",
    goal="Evaluate student answers and provide feedback",
    backstory=(
        "Experienced academic evaluator "
        "who checks answers and gives scores."
    ),
    verbose=False,
    llm=llm
)