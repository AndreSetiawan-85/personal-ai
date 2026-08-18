from app.services.ollama import ollama_service
from app.core.config import settings


def detect_search_type(message: str):
    if not message or not message.strip():
        return None

    prompt = f"""
Determine whether the user's message requires current or externally retrieved information.

Return exactly one JSON object:

{{"needs_search": true}}

or

{{"needs_search": false}}

Search is appropriate when the user asks for information that may be current,
changing, externally verifiable, or requires information not contained in the
conversation.

Do not search merely because the message is a question.

USER MESSAGE:
{message.strip()}
"""

    try:
        response = ollama_service.generate_response(prompt)

        normalized = response.strip().lower()

        if '"needs_search": true' in normalized:
            return "general"

        if '"needs_search": false' in normalized:
            return None

    except Exception as e:
        print("Search router error:", e)

    return None