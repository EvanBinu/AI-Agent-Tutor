import sqlite3

# =========================
# DATABASE CONNECTION
# =========================

conn = sqlite3.connect(
    "student_memory.db",
    check_same_thread=False
)

cursor = conn.cursor()

# =========================
# STUDENTS TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS students (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT
)
""")

# =========================
# RESULTS TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS results (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT,
    score INTEGER,
    percentage REAL,
    correct_answers TEXT,
    wrong_answers TEXT,
    feedback TEXT,
    suggestions TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# =========================
# WEAK TOPICS TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS weak_topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# =========================
# AGENT MESSAGES TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS agent_messages (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    sender TEXT,
    receiver TEXT,
    content TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# =========================
# LEARNING HISTORY TABLE
# =========================

cursor.execute("""
CREATE TABLE IF NOT EXISTS learning_history (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    topic TEXT,
    activity TEXT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
)
""")

# =========================
# COMMIT CHANGES
# =========================

conn.commit()