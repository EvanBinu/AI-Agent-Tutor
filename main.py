from crewai import Crew, Process

from agents import (
    professor,
    tutor,
    question_generator
)

from tasks import create_tasks

# User input
topic = input("Enter topic: ")

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

# Run crew
result = crew.kickoff()

print("\n========== FINAL OUTPUT ==========\n")
print(result)