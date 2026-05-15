# 📘 AI Academic Assistant Team

An advanced multi-agent AI tutoring platform built using CrewAI, Streamlit, SQLite, and Agent-to-Agent (A2A) communication.

---

# 🚀 Project Overview

AI Academic Assistant Team is an Agentic AI educational platform designed to simulate a collaborative academic tutoring environment.

The system uses multiple AI agents that work together to:

* explain academic concepts,
* simplify difficult topics,
* generate practice questions,
* evaluate student answers,
* identify weak areas,
* provide personalized remediation,
* maintain persistent learning memory.

The project demonstrates:

* Multi-Agent AI Systems
* Agent-to-Agent (A2A) Communication
* Persistent AI Memory
* Structured JSON Workflows
* Adaptive Learning Systems
* Streamlit-based Interactive UI
* SQLite-based Long-Term Memory

---

# 🧠 Core Features

## ✅ Multi-Agent Collaboration

The application uses specialized AI agents:

| Agent                    | Responsibility                          |
| ------------------------ | --------------------------------------- |
| Professor Agent          | Provides conceptual explanations        |
| Tutor Agent              | Simplifies concepts with examples       |
| Question Generator Agent | Creates MCQs and descriptive questions  |
| Evaluator Agent          | Evaluates answers and provides feedback |

---

# 🔄 Agent-to-Agent (A2A) Communication

The system supports inter-agent collaboration.

Example workflow:

```text
Evaluator detects weak topic
        ↓
Sends message to Tutor Agent
        ↓
Tutor generates remedial lesson
```

This enables adaptive tutoring behavior.

---

# 🧠 Persistent AI Memory

The platform stores:

* quiz results
* weak topics
* learning history
* A2A messages
* evaluation summaries

using SQLite.

This allows:

* long-term personalization,
* adaptive remediation,
* learning analytics.

---

# 📊 Structured Evaluation System

The Evaluator Agent returns structured JSON.

Example:

```json
{
  "score": 2,
  "percentage": 66.7,
  "correct_answers": [],
  "wrong_answers": [],
  "feedback": "Good understanding",
  "suggestions": []
}
```

This enables:

* deterministic parsing,
* structured UI rendering,
* analytics generation,
* database storage.

---

# 🖥️ Interactive Streamlit UI

The project includes:

* topic input interface,
* AI-generated explanations,
* question display,
* answer submission,
* evaluation dashboard,
* remediation section.

---

# 🏗️ System Architecture

```text
Frontend (Streamlit)
        ↓
CrewAI Orchestrator
        ↓
Professor Agent
Tutor Agent
Question Generator Agent
Evaluator Agent
        ↓
A2A Messaging Layer
        ↓
SQLite Persistent Memory
```

---

# 📁 Project Structure

```text
AI-Agent-Tutor/
│
├── app.py
├── agents.py
├── tasks.py
├── config.py
├── memory.py
├── a2a_workflow.py
├── database.py
├── view_db.py
├── requirements.txt
├── .env
├── .gitignore
├── student_memory.db
│
└── README.md
```

---

# ⚙️ Technologies Used

| Technology | Purpose                   |
| ---------- | ------------------------- |
| CrewAI     | Multi-agent orchestration |
| Streamlit  | Web UI                    |
| SQLite     | Persistent memory         |
| Python     | Backend logic             |
| Groq API   | LLM inference             |
| JSON       | Structured AI outputs     |

---

# 🧩 Agent Descriptions

---

## 👨‍🏫 Professor Agent

### Responsibilities

* Explain concepts deeply
* Provide technical understanding
* Teach theoretical foundations

### Example

```text
Explain Operating Systems in under 120 words.
```

---

## 🧑‍🎓 Tutor Agent

### Responsibilities

* Simplify explanations
* Use beginner-friendly language
* Provide examples
* Generate remedial lessons

### Example

```text
Simplify deadlocks using simple examples.
```

---

## ❓ Question Generator Agent

### Responsibilities

* Generate MCQs
* Generate descriptive questions
* Create assessment content

### Current Output

* 3 MCQs
* 1 descriptive question

---

## 📝 Evaluator Agent

### Responsibilities

* Evaluate student answers
* Calculate scores
* Generate structured JSON feedback
* Detect weak topics
* Trigger remediation workflows

---

# 🧠 A2A Communication System

The project includes a custom A2A communication layer.

---

# Shared Memory

```python
shared_memory = {
    "weak_topics": [],
    "student_scores": [],
    "agent_messages": []
}
```

---

# Message Passing

Agents communicate using:

```python
send_message(sender, receiver, content)
```

Example:

```python
send_message(
    "Evaluator",
    "Tutor",
    "Student weak in Deadlocks"
)
```

---

# 🗄️ Database Design

The system uses SQLite for persistent memory.

---

# Database Tables

## results

Stores:

* scores
* percentages
* feedback
* structured evaluation data

---

## weak_topics

Stores:

* topics where student performance is poor

---

## agent_messages

Stores:

* A2A communication logs

---

## learning_history

Stores:

* generated learning activities

---

# 📦 Installation Guide

---

# Step 1 — Clone Repository

```bash
git clone <repository-url>
cd AI-Agent-Tutor
```

---

# Step 2 — Create Virtual Environment

## Windows

```bash
python -m venv venv
venv\Scripts\activate
```

## Linux / Mac

```bash
python3 -m venv venv
source venv/bin/activate
```

---

# Step 3 — Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Step 4 — Create .env File

Create:

```text
.env
```

Add:

```env
GROQ_API_KEY=your_api_key_here
```

---

# Step 5 — Run Application

```bash
streamlit run app.py
```

---

# 🌐 Application Workflow

```text
User enters topic
        ↓
Professor Agent explains concept
        ↓
Tutor Agent simplifies concept
        ↓
Question Generator creates questions
        ↓
Student submits answers
        ↓
Evaluator grades answers
        ↓
Weak topics detected
        ↓
Tutor generates remediation
        ↓
Results stored in SQLite
```

---

# 📊 Evaluation Workflow

The Evaluator Agent returns structured JSON.

---

# Example Output

```json
{
  "score": 1,
  "percentage": 33.3,
  "correct_answers": [
    {
      "question": "What is DBMS?",
      "correct_answer": "B"
    }
  ],
  "wrong_answers": [
    {
      "question": "What is schema?",
      "student_answer": "A",
      "correct_answer": "C"
    }
  ],
  "feedback": "Needs improvement",
  "suggestions": [
    "Review DBMS basics"
  ]
}
```

---

# 📈 Adaptive Remediation System

If:

```text
percentage < 50
```

then:

* weak topic stored,
* A2A message sent,
* Tutor Agent creates remedial lesson.

---

# 🧪 Example Use Case

## Topic

```text
Operating Systems
```

## Student Performance

```text
Score: 1/3
```

## System Response

```text
Evaluator → Tutor:
Student weak in Operating Systems
```

Tutor automatically generates:

```text
Simplified remediation lesson
```

---

# 🔒 Error Handling Features

The system includes:

* JSON parsing validation
* Session-state management
* Duplicate A2A prevention
* Structured evaluation parsing
* SQLite persistence checks

---

# 📌 Current Capabilities

✅ Multi-Agent Collaboration

✅ Agent-to-Agent Communication

✅ Persistent SQLite Memory

✅ Adaptive Remediation

✅ Structured JSON Evaluation

✅ Interactive Streamlit UI

✅ Weak Topic Detection

✅ Learning History Tracking

---

# 🚧 Future Enhancements

---

# 1. Structured JSON Question Generation

Convert question generation to:

```json
{
  "question": "...",
  "options": [],
  "correct_answer": "A"
}
```

---

# 2. Interactive Quiz UI

Replace text answers with:

* radio buttons
* selectable MCQs
* automatic grading

---

# 3. RAG (Retrieval-Augmented Generation)

Allow students to upload:

* PDFs
* notes
* textbooks
* PPTs

and answer questions from uploaded material.

---

# 4. Supervisor Agent

Add hierarchical orchestration.

```text
Supervisor Agent
      ↓
Controls all educational agents
```

---

# 5. Tool-Using Agents

Agents will:

* search internet,
* retrieve PDFs,
* use calculators,
* access databases.

---

# 6. Learning Analytics Dashboard

Track:

* weak subjects,
* topic mastery,
* score trends,
* performance history.

---

# 7. Autonomous Study Planner

Generate:

* revision plans,
* study schedules,
* personalized learning paths.

---

# 8. MCP-Style Tool Architecture

Introduce:

* unified tool layer,
* protocol-based AI tooling,
* interoperable AI systems.

---

# 🧠 Key AI Concepts Demonstrated

This project demonstrates:

* Agentic AI
* Multi-Agent Systems
* A2A Communication
* Structured AI Outputs
* Persistent AI Memory
* Adaptive AI Workflows
* Autonomous Remediation
* Context Persistence
* Prompt Engineering
* AI Orchestration

---

# 📚 Learning Outcomes

By building this project, concepts learned include:

* CrewAI orchestration
* Streamlit application development
* SQLite persistence
* JSON parsing
* Agent communication systems
* AI workflow engineering
* adaptive tutoring systems
* structured AI architecture

---

# 👨‍💻 Author

Developed as an advanced Agentic AI educational platform project.

---

# 📄 License

This project is intended for educational and research purposes.
