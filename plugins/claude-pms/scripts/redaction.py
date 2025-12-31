"""
Privacy redaction for Claude PMS
Automatically redacts sensitive data before storage
"""

import re
from typing import Any, Dict, List, Tuple


# Default redaction patterns (compiled for performance)
DEFAULT_PATTERNS = [
    # API keys and tokens
    (re.compile(r'\b[A-Za-z0-9_-]{20,}\b'), '[REDACTED_TOKEN]'),
    (re.compile(r'api[_-]?key[\'"\s:=]+[\w-]+', re.IGNORECASE), 'api_key=[REDACTED]'),
    (re.compile(r'access[_-]?token[\'"\s:=]+[\w-]+', re.IGNORECASE), 'access_token=[REDACTED]'),
    (re.compile(r'secret[_-]?key[\'"\s:=]+[\w-]+', re.IGNORECASE), 'secret_key=[REDACTED]'),
    (re.compile(r'auth[_-]?token[\'"\s:=]+[\w-]+', re.IGNORECASE), 'auth_token=[REDACTED]'),

    # Passwords
    (re.compile(r'password[\'"\s:=]+[^\s\'",}]+', re.IGNORECASE), 'password=[REDACTED]'),
    (re.compile(r'passwd[\'"\s:=]+[^\s\'",}]+', re.IGNORECASE), 'passwd=[REDACTED]'),

    # Credentials
    (re.compile(r'credentials?[\'"\s:=]+[^\s\'",}]+', re.IGNORECASE), 'credentials=[REDACTED]'),

    # Bearer tokens
    (re.compile(r'Bearer\s+[\w-]+', re.IGNORECASE), 'Bearer [REDACTED]'),

    # Private keys (PEM format)
    (re.compile(r'-----BEGIN\s+(?:RSA\s+)?PRIVATE\s+KEY-----.*?-----END\s+(?:RSA\s+)?PRIVATE\s+KEY-----', re.DOTALL), '[REDACTED_PRIVATE_KEY]'),
]


def redact_sensitive(text: str, patterns: List[Tuple[re.Pattern, str]] = None) -> Tuple[str, int]:
    """
    Redact sensitive data from text using regex patterns.

    Args:
        text: Text to redact
        patterns: List of (regex_pattern, replacement) tuples
                  Uses DEFAULT_PATTERNS if None

    Returns:
        Tuple of (redacted_text, redaction_count)
    """
    if patterns is None:
        patterns = DEFAULT_PATTERNS

    redaction_count = 0
    redacted_text = text

    for pattern, replacement in patterns:
        matches = pattern.findall(redacted_text)
        if matches:
            redaction_count += len(matches)
            redacted_text = pattern.sub(replacement, redacted_text)

    return redacted_text, redaction_count


def detect_and_redact(data: Any, patterns: List[Tuple[re.Pattern, str]] = None) -> Tuple[Any, int]:
    """
    Recursively redact sensitive data in nested structures.

    Args:
        data: Data to redact (str, dict, list, or primitive)
        patterns: Redaction patterns (uses defaults if None)

    Returns:
        Tuple of (redacted_data, total_redaction_count)
    """
    total_count = 0

    if isinstance(data, str):
        redacted, count = redact_sensitive(data, patterns)
        return redacted, count

    elif isinstance(data, dict):
        redacted_dict = {}
        for key, value in data.items():
            redacted_value, count = detect_and_redact(value, patterns)
            redacted_dict[key] = redacted_value
            total_count += count
        return redacted_dict, total_count

    elif isinstance(data, list):
        redacted_list = []
        for item in data:
            redacted_item, count = detect_and_redact(item, patterns)
            redacted_list.append(redacted_item)
            total_count += count
        return redacted_list, total_count

    else:
        # Primitives (int, float, bool, None) - no redaction needed
        return data, 0


def compile_custom_patterns(pattern_strings: List[str]) -> List[Tuple[re.Pattern, str]]:
    """
    Compile custom redaction patterns from strings.

    Args:
        pattern_strings: List of regex pattern strings

    Returns:
        List of (compiled_pattern, replacement) tuples
    """
    compiled = []
    for pattern_str in pattern_strings:
        try:
            compiled.append((re.compile(pattern_str, re.IGNORECASE), '[REDACTED]'))
        except re.error:
            # Skip invalid patterns
            continue
    return compiled


def get_all_patterns(custom_patterns: List[str] = None) -> List[Tuple[re.Pattern, str]]:
    """
    Get combined default + custom redaction patterns.

    Args:
        custom_patterns: List of custom regex pattern strings

    Returns:
        Combined list of (pattern, replacement) tuples
    """
    patterns = DEFAULT_PATTERNS.copy()
    if custom_patterns:
        patterns.extend(compile_custom_patterns(custom_patterns))
    return patterns
