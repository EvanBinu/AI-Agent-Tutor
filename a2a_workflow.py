from memory import get_messages

def tutor_remediation():

    messages = get_messages("Tutor")

    remediation_topics = []

    for msg in messages:
        remediation_topics.append(msg["content"])

    return remediation_topics