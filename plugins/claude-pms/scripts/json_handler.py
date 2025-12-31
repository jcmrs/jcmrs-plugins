"""
Safe JSON handling for Claude PMS
Atomic writes, corruption handling, and schema validation
"""

import json
import os
import shutil
from pathlib import Path
from typing import Any, Dict, List, Optional


def safe_load(filepath: str, default: Any = None) -> Any:
    """
    Safely load JSON file with error handling.
    Returns default value if file doesn't exist or is corrupted.

    Args:
        filepath: Path to JSON file
        default: Default value if load fails (usually {} or [])

    Returns:
        Loaded JSON data or default value
    """
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        return default if default is not None else {}
    except json.JSONDecodeError as e:
        print(f"Warning: Corrupted JSON in {filepath}: {e}")
        # Attempt repair (remove incomplete lines)
        try:
            return _attempt_repair(filepath)
        except Exception:
            # Repair failed - return default
            return default if default is not None else {}
    except Exception as e:
        print(f"Warning: Error loading {filepath}: {e}")
        return default if default is not None else {}


def safe_save(filepath: str, data: Any, indent: int = 2, max_retries: int = 3) -> bool:
    """
    Safely save JSON file using atomic write (temp file + rename) with retry logic.

    Args:
        filepath: Path to JSON file
        data: Data to save
        indent: JSON indentation (default: 2 spaces)
        max_retries: Maximum retry attempts (default: 3)

    Returns:
        True if successful, False otherwise
    """
    import time

    for attempt in range(max_retries):
        try:
            # Ensure directory exists
            Path(filepath).parent.mkdir(parents=True, exist_ok=True)

            # Write to temporary file first
            temp_filepath = f"{filepath}.tmp"
            with open(temp_filepath, 'w', encoding='utf-8') as f:
                json.dump(data, f, indent=indent, ensure_ascii=False)
                f.flush()
                os.fsync(f.fileno())

            # Verify temp file was written successfully
            if not os.path.exists(temp_filepath):
                raise Exception("Temp file creation failed")

            # Verify temp file is readable and valid JSON
            try:
                with open(temp_filepath, 'r', encoding='utf-8') as f:
                    json.load(f)
            except json.JSONDecodeError as e:
                raise Exception(f"Generated invalid JSON: {e}")

            # Atomic rename
            shutil.move(temp_filepath, filepath)

            # Verify final file exists
            if not os.path.exists(filepath):
                raise Exception("Final file not created after rename")

            return True

        except Exception as e:
            if attempt < max_retries - 1:
                # Retry after brief delay
                print(f"Warning: Save attempt {attempt + 1} failed, retrying: {e}")
                time.sleep(0.1 * (attempt + 1))  # Exponential backoff

                # Clean up temp file if it exists
                try:
                    if os.path.exists(f"{filepath}.tmp"):
                        os.remove(f"{filepath}.tmp")
                except Exception:
                    pass
            else:
                # Final attempt failed
                print(f"Error saving {filepath} after {max_retries} attempts: {e}")

                # Clean up temp file if it exists
                try:
                    if os.path.exists(f"{filepath}.tmp"):
                        os.remove(f"{filepath}.tmp")
                except Exception:
                    pass

                return False

    return False


def merge_monthly(session_record: Dict, monthly_filepath: str) -> bool:
    """
    Append session record to monthly episodic file.
    Loads existing file, appends new record, saves atomically.

    Args:
        session_record: New session record to append
        monthly_filepath: Path to monthly sessions file

    Returns:
        True if successful, False otherwise
    """
    try:
        # Load existing records (default to empty list)
        existing_data = safe_load(monthly_filepath, default={"sessions": []})

        # Ensure structure
        if not isinstance(existing_data, dict):
            existing_data = {"sessions": []}
        if "sessions" not in existing_data:
            existing_data["sessions"] = []

        # Append new record
        existing_data["sessions"].append(session_record)

        # Update metadata
        existing_data["count"] = len(existing_data["sessions"])
        existing_data["last_updated"] = session_record.get("timestamp")

        # Save atomically
        return safe_save(monthly_filepath, existing_data)

    except Exception as e:
        print(f"Error merging to monthly file: {e}")
        return False


def update_index(index_filepath: str, session_id: str, monthly_filename: str) -> bool:
    """
    Update index.json with session ID → monthly file mapping.

    Args:
        index_filepath: Path to index.json
        session_id: Session UUID
        monthly_filename: Monthly file name (e.g., "sessions-2025-12.json")

    Returns:
        True if successful, False otherwise
    """
    try:
        # Load existing index
        index = safe_load(index_filepath, default={})

        # Add mapping
        index[session_id] = monthly_filename

        # Save atomically
        return safe_save(index_filepath, index)

    except Exception as e:
        print(f"Error updating index: {e}")
        return False


def _attempt_repair(filepath: str) -> Any:
    """
    Attempt to repair corrupted JSON by stripping incomplete lines.
    This is a best-effort recovery.

    Args:
        filepath: Path to corrupted JSON file

    Returns:
        Repaired JSON data

    Raises:
        Exception if repair fails
    """
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    # Try to find last complete JSON structure
    # Look for closing } or ]
    for i in range(len(content) - 1, -1, -1):
        if content[i] in ('}', ']'):
            try:
                return json.loads(content[:i+1])
            except json.JSONDecodeError:
                continue

    # Repair failed
    raise Exception("Unable to repair JSON")


def validate_episodic_record(record: Dict) -> bool:
    """
    Validate episodic record schema.

    Required fields:
    - session_id
    - timestamp
    - project_path
    - task_summary

    Args:
        record: Episodic record to validate

    Returns:
        True if valid, False otherwise
    """
    required_fields = ["session_id", "timestamp", "project_path", "task_summary"]
    return all(field in record for field in required_fields)


def validate_semantic_pattern(pattern: Dict) -> bool:
    """
    Validate semantic pattern schema.

    Required fields:
    - pattern_id
    - description
    - occurrences
    - evidence

    Args:
        pattern: Semantic pattern to validate

    Returns:
        True if valid, False otherwise
    """
    required_fields = ["pattern_id", "description", "occurrences", "evidence"]
    return all(field in pattern for field in required_fields)
