shared_memory = {
    "weak_topics": [],
    "student_scores": [],
    "agent_messages": []
}

# =========================
# SEND MESSAGE
# =========================

def send_message(sender, receiver, content):

    shared_memory["agent_messages"].append({
        "from": sender,
        "to": receiver,
        "content": content
    })

# =========================
# GET MESSAGES
# =========================

def get_messages(receiver):

    return [
        msg
        for msg in shared_memory["agent_messages"]
        if msg["to"] == receiver
    ]