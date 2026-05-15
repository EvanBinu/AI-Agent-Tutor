from crewai import Task
from agents import professor, tutor, question_generator

# Create tasks dynamically
def create_tasks(topic):

    # =========================
    # PROFESSOR TASK
    # =========================

    professor_task = Task(
        description=(
            f"""
            Explain the topic '{topic}' briefly.

            RULES:
            - Maximum 120 words
            - Keep concise
            - Focus only on key concepts
            """
        ),
        expected_output="Short conceptual explanation.",
        agent=professor
    )

    # =========================
    # TUTOR TASK
    # =========================

    tutor_task = Task(
        description=(
            f"""
            Simplify the topic '{topic}'.

            RULES:
            - Maximum 80 words
            - Use very simple language
            - Give only 1 small example
            """
        ),
        expected_output="Short simplified explanation.",
        agent=tutor
    )

    # =========================
    # QUESTION GENERATOR TASK
    # =========================

    question_task = Task(
        description=(
            f"""
            Generate questions for '{topic}'.

            RULES:
            - Generate ONLY 3 MCQs
            - Generate ONLY 1 descriptive question
            - DO NOT provide answers
            - Keep questions concise
            - Keep options short
            """
        ),
        expected_output="Questions only without answers.",
        agent=question_generator
    )

    return [
        professor_task,
        tutor_task,
        question_task
    ]