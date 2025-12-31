"""
Shared utility functions for Claude PMS
"""

import os
import uuid
from datetime import datetime
from pathlib import Path
from typing import Optional


def ensure_directory(path: str) -> Path:
    """
    Create directory if it doesn't exist.
    Returns Path object.
    """
    dir_path = Path(path)
    dir_path.mkdir(parents=True, exist_ok=True)
    return dir_path


def get_session_id() -> str:
    """
    Generate or retrieve current session UUID.
    For now, generates a new UUID each time.
    Future enhancement: retrieve from Claude Code session context.
    """
    return str(uuid.uuid4())


def get_timestamp() -> str:
    """
    Get current timestamp in ISO 8601 format.
    Example: "2025-12-31T01:23:45Z"
    """
    return datetime.utcnow().strftime("%Y-%m-%dT%H:%M:%SZ")


def get_project_path() -> str:
    """
    Get current project path.
    Tries environment variables first, falls back to cwd.
    """
    return os.environ.get("PMS_PROJECT_PATH") or \
           os.environ.get("CLAUDE_PROJECT_DIR") or \
           os.getcwd()


def get_git_branch() -> Optional[str]:
    """
    Get current git branch name.
    Returns None if not in git repo.
    """
    try:
        import subprocess
        result = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "HEAD"],
            capture_output=True,
            text=True,
            check=True
        )
        return result.stdout.strip()
    except Exception:
        return None


def parse_jsonl(filepath: str, limit: Optional[int] = None) -> list:
    """
    Parse JSONL file (one JSON object per line).

    Args:
        filepath: Path to JSONL file
        limit: Maximum number of lines to parse (for performance)

    Returns:
        List of parsed JSON objects
    """
    import json

    records = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            for i, line in enumerate(f):
                if limit and i >= limit:
                    break

                line = line.strip()
                if not line:
                    continue

                try:
                    records.append(json.loads(line))
                except json.JSONDecodeError:
                    # Skip malformed lines
                    continue
    except FileNotFoundError:
        return []

    return records


def get_monthly_filename(timestamp: Optional[str] = None) -> str:
    """
    Get monthly filename for episodic records.
    Format: sessions-YYYY-MM.json

    Args:
        timestamp: ISO 8601 timestamp (uses current time if None)

    Returns:
        Filename like "sessions-2025-12.json"
    """
    if timestamp:
        dt = datetime.fromisoformat(timestamp.replace('Z', '+00:00'))
    else:
        dt = datetime.utcnow()

    return f"sessions-{dt.year:04d}-{dt.month:02d}.json"
