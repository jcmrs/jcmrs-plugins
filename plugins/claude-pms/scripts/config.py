"""
Configuration management for Claude PMS
Loads and validates pms.local.md YAML frontmatter
"""

import os
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Dict, List, Optional


@dataclass
class PMSConfig:
    """PMS configuration with typed fields"""

    # Triggers
    trigger_precompact: bool = True
    trigger_session_end: bool = True
    trigger_stop: bool = False

    # Processing
    continuous_mode: bool = True
    auto_synthesize: bool = False

    # Thresholds
    min_sessions: int = 10
    emerging_pattern: int = 2
    strong_pattern: int = 3
    critical_pattern: int = 5

    # Encoding
    prefer_context: bool = True
    fallback_jsonl: bool = True

    # Privacy
    redact_sensitive: bool = True
    custom_redaction_patterns: List[str] = field(default_factory=lambda: [])

    # Timeouts (seconds)
    timeout_encode: int = 30
    timeout_extract: int = 60
    timeout_synthesize: int = 45


def get_default_config() -> PMSConfig:
    """Return default configuration"""
    return PMSConfig()


def load_config(project_path: str) -> PMSConfig:
    """
    Load configuration from project-level pms.local.md
    Falls back to defaults if file missing or invalid

    Args:
        project_path: Path to project root

    Returns:
        PMSConfig object
    """
    config_file = Path(project_path) / ".claude" / "pms.local.md"

    if not config_file.exists():
        return get_default_config()

    try:
        with open(config_file, 'r', encoding='utf-8') as f:
            content = f.read()

        # Extract YAML frontmatter (between --- markers)
        yaml_match = re.search(r'^---\s*\n(.*?)\n---', content, re.DOTALL | re.MULTILINE)
        if not yaml_match:
            return get_default_config()

        yaml_content = yaml_match.group(1)

        # Parse YAML (simple key-value extraction)
        config = get_default_config()

        # Triggers
        config.trigger_precompact = _parse_bool(yaml_content, "precompact", True)
        config.trigger_session_end = _parse_bool(yaml_content, "session_end", True)
        config.trigger_stop = _parse_bool(yaml_content, "stop", False)

        # Processing
        config.continuous_mode = _parse_bool(yaml_content, "continuous_mode", True)
        config.auto_synthesize = _parse_bool(yaml_content, "auto_synthesize", False)

        # Thresholds
        config.min_sessions = _parse_int(yaml_content, "min_sessions", 10, 1, 1000)
        config.emerging_pattern = _parse_int(yaml_content, "emerging_pattern", 2, 1, 100)
        config.strong_pattern = _parse_int(yaml_content, "strong_pattern", 3, 1, 100)
        config.critical_pattern = _parse_int(yaml_content, "critical_pattern", 5, 1, 100)

        # Encoding
        config.prefer_context = _parse_bool(yaml_content, "prefer_context", True)
        config.fallback_jsonl = _parse_bool(yaml_content, "fallback_jsonl", True)

        # Privacy
        config.redact_sensitive = _parse_bool(yaml_content, "redact_sensitive", True)
        # TODO: Parse custom_redaction_patterns list

        # Timeouts
        config.timeout_encode = _parse_int(yaml_content, "encode", 30, 5, 300)
        config.timeout_extract = _parse_int(yaml_content, "extract", 60, 5, 600)
        config.timeout_synthesize = _parse_int(yaml_content, "synthesize", 45, 5, 300)

        return config

    except Exception as e:
        # Any error loading config → fall back to defaults
        print(f"Warning: Error loading config, using defaults: {e}")
        return get_default_config()


def validate_config(config: PMSConfig) -> bool:
    """
    Validate configuration values
    Returns True if valid, False otherwise
    """
    try:
        # Check thresholds are in order
        if not (config.emerging_pattern <= config.strong_pattern <= config.critical_pattern):
            return False

        # Check timeouts are reasonable
        if config.timeout_encode < 5 or config.timeout_encode > 300:
            return False
        if config.timeout_extract < 5 or config.timeout_extract > 600:
            return False
        if config.timeout_synthesize < 5 or config.timeout_synthesize > 300:
            return False

        # Check min_sessions is reasonable
        if config.min_sessions < 1 or config.min_sessions > 1000:
            return False

        return True

    except Exception:
        return False


# Helper functions for parsing YAML
def _parse_bool(yaml_content: str, key: str, default: bool) -> bool:
    """Parse boolean value from YAML content"""
    pattern = rf'^\s*{key}:\s*(\w+)'
    match = re.search(pattern, yaml_content, re.MULTILINE)
    if match:
        value = match.group(1).lower()
        if value in ('true', 'yes', 'on', '1'):
            return True
        if value in ('false', 'no', 'off', '0'):
            return False
    return default


def _parse_int(yaml_content: str, key: str, default: int, min_val: int, max_val: int) -> int:
    """Parse integer value from YAML content with clamping"""
    pattern = rf'^\s*{key}:\s*(\d+)'
    match = re.search(pattern, yaml_content, re.MULTILINE)
    if match:
        try:
            value = int(match.group(1))
            # Clamp to valid range
            return max(min_val, min(value, max_val))
        except ValueError:
            pass
    return default
