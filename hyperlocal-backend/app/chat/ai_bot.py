HUMAN_KEYWORDS = ("human", "agent", "complain", "help me", "talk to someone")


def build_reply(user_text: str) -> tuple[str, bool]:
    lower = user_text.lower()
    if any(k in lower for k in HUMAN_KEYWORDS):
        return (
            "I understand you may want a person to help. Use the handoff card from the API response.",
            True,
        )
    return (
        f"(Demo bot) You said: {user_text[:500]}. "
        "Delivery in Pune is typically same-day for nearby stores. "
        "Ask about fees, returns, or shop onboarding.",
        False,
    )
