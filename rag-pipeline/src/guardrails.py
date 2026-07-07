# ----------------------------
# Guardrail Configuration
# ----------------------------

MAX_QUESTION_LENGTH = 500

BAD_PATTERNS = [
    # Prompt Injection
    "ignore previous instructions",
    "ignore all instructions",
    "forget previous instructions",
    "forget everything",
    "system prompt",
    "developer prompt",
    "developer message",
    "reveal prompt",
    "show prompt",
    "print prompt",
    "repeat your instructions",
    "ignore context",
    "ignore the context",
    "override",
    "bypass",
    "jailbreak",
    "disable safety",
    "disable guardrails",
    "act as",
    "pretend to be",
    "roleplay",

    # HTML / JavaScript Injection
    "<html>",
    "</html>",
    ".bat"
    "<script>",
    "</script>",
    "javascript:",
    "onerror=",
    "onclick=",
    "onload=",
    "<iframe",
    "</iframe>",
    "<img",
    "<svg",
    "<object",
    "<embed",
    "<style",
    "<meta",
    "document.cookie",
    "window.location",
    "eval(",
    "fetch(",
]

# ----------------------------
# Empty Question Check
# ----------------------------
def validate_empty_question(question: str) -> bool:
    return bool(question.strip())

# ----------------------------
# Question Length Check
# ----------------------------
def validate_question_length(question: str) -> bool:
    return len(question) <= MAX_QUESTION_LENGTH

# ----------------------------
# Prompt Injection Check
# ----------------------------
def detect_prompt_injection(question: str) -> bool:
    question = question.lower()
    return any(pattern in question for pattern in BAD_PATTERNS)