import re

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

    # File / Command Injection
    ".bat",
    ".cmd",
    ".exe",
    ".sh",
    "powershell",
    "cmd.exe",
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
    return len(question.strip()) <= MAX_QUESTION_LENGTH


# ----------------------------
# Repeated Character Check
# ----------------------------
def validate_repeated_characters(question: str) -> bool:
    """
    Reject inputs like:
    aaaaaaaaaaaaaaaaaaaaa
    !!!!!!!!
    1111111111111111
    """
    return re.search(r"(.)\1{20,}", question) is None


# ----------------------------
# Prompt Injection Check
# ----------------------------
def detect_prompt_injection(question: str) -> bool:
    question = question.lower()
    return any(pattern in question for pattern in BAD_PATTERNS)