from crewai import Task
from agents import professor, tutor, question_generator

# Create all tasks dynamically
def create_tasks(topic):

    # Professor Task
    professor_task = Task(
        description=(
            f"Explain the topic '{topic}' "
            "in detail with technical depth."
        ),
        expected_output="Detailed explanation.",
        agent=professor
    )

    # Tutor Task
    tutor_task = Task(
        description=(
            f"Simplify the topic '{topic}' "
            "using easy language and examples."
        ),
        expected_output="Simplified explanation.",
        agent=tutor
    )

    # Question Generator Task
    question_task = Task(
        description=(
            f"Generate 5 MCQs and 3 descriptive "
            f"questions for '{topic}'."
        ),
        expected_output="Practice questions.",
        agent=question_generator
    )

    return [
        professor_task,
        tutor_task,
        question_task
    ]