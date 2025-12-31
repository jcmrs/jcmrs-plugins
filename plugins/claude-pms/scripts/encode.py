#!/usr/bin/env python3
"""
Episodic Encoding Engine for Claude PMS
Captures session experiences using context-first strategy with JSONL fallback
"""

import argparse
import json
import os
import signal
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, Optional

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import load_config
from json_handler import merge_monthly, safe_save, update_index
from redaction import detect_and_redact, get_all_patterns
from utils import (
    ensure_directory,
    get_git_branch,
    get_monthly_filename,
    get_project_path,
    get_session_id,
    get_timestamp,
    parse_jsonl,
)


# Timeout handling
class TimeoutError(Exception):
    """Raised when encoding exceeds timeout"""
    pass


def timeout_handler(signum, frame):
    """Signal handler for timeout"""
    raise TimeoutError("Encoding exceeded timeout limit")


def encode_session(project_path: str, trigger: str, session_id: str = None, timeout: int = 30) -> bool:
    """
    Encode current session as episodic memory record.

    Args:
        project_path: Path to project root
        trigger: Trigger event (precompact, session-end, stop)
        session_id: Optional session ID (generates new if None)
        timeout: Maximum encoding time in seconds (default: 30)

    Returns:
        True if successful, False otherwise
    """
    # Set up timeout handler (Unix-like systems only)
    if hasattr(signal, 'SIGALRM'):
        signal.signal(signal.SIGALRM, timeout_handler)
        signal.alarm(timeout)

    try:
        # Load configuration
        config = load_config(project_path)

        # Generate session ID if not provided
        if not session_id:
            session_id = get_session_id()

        # Determine encoding mode based on config with fallback chain
        episodic_record = None
        encoding_errors = []

        if config.prefer_context:
            try:
                # Context-first encoding
                episodic_record = encode_from_context(
                    project_path, session_id, trigger
                )
            except Exception as e:
                encoding_errors.append(f"Context encoding failed: {e}")
                print(f"Warning: Context encoding failed, trying fallback: {e}", file=sys.stderr)

        # Fallback to JSONL if context failed or not preferred
        if not episodic_record and config.fallback_jsonl:
            try:
                episodic_record = encode_from_jsonl(
                    project_path, session_id, trigger
                )
            except Exception as e:
                encoding_errors.append(f"JSONL encoding failed: {e}")
                print(f"Warning: JSONL encoding failed: {e}", file=sys.stderr)

        if not episodic_record:
            print("Error: All encoding methods failed", file=sys.stderr)
            for error in encoding_errors:
                print(f"  - {error}", file=sys.stderr)
            return False

        # Document encoding limitations if context was incomplete
        if episodic_record.get("encoding_mode") == "context" and not episodic_record.get("task_summary"):
            episodic_record["limitations"] = [
                "Context incomplete - best-effort record created",
                "Some session details may be missing"
            ]
            print("Warning: Context incomplete - created best-effort record", file=sys.stderr)

        # Apply privacy redaction with comprehensive error handling
        if config.redact_sensitive:
            try:
                redaction_patterns = get_all_patterns(
                    config.custom_redaction_patterns
                )
                episodic_record, redaction_count = detect_and_redact(
                    episodic_record, redaction_patterns
                )
                if redaction_count > 0:
                    print(f"Redacted {redaction_count} sensitive items")
            except Exception as e:
                # Over-redact on failure: remove potentially sensitive fields
                print(f"Warning: Redaction failed, applying conservative over-redaction: {e}", file=sys.stderr)
                sensitive_fields = ["work_summary", "challenges", "solutions"]
                redacted_count = 0
                for field in sensitive_fields:
                    if field in episodic_record and isinstance(episodic_record[field], str):
                        episodic_record[field] = "[REDACTED - redaction error]"
                        redacted_count += 1
                    elif field in episodic_record and isinstance(episodic_record[field], list):
                        episodic_record[field] = ["[REDACTED - redaction error]"] * len(episodic_record[field])
                        redacted_count += 1
                print(f"Applied conservative redaction to {redacted_count} fields")

        # Save episodic record
        pms_dir = Path(project_path) / ".claude" / "pms"
        episodic_dir = pms_dir / "episodic"
        ensure_directory(episodic_dir)

        # Determine monthly filename
        monthly_filename = get_monthly_filename(episodic_record["timestamp"])
        monthly_filepath = episodic_dir / monthly_filename

        # Merge into monthly file
        success = merge_monthly(episodic_record, str(monthly_filepath))
        if not success:
            print("Error: Failed to save episodic record", file=sys.stderr)
            return False

        # Update index
        index_filepath = episodic_dir / "index.json"
        update_index(
            str(index_filepath),
            episodic_record["session_id"],
            monthly_filename
        )

        print(f"✓ Episodic record saved: {monthly_filename}")

        # Trigger semantic extraction if continuous mode enabled
        if config.continuous_mode:
            # TODO: Call extract.py asynchronously (non-blocking)
            # For now, just log
            print("Continuous mode: Semantic extraction will be triggered")

        # Cancel timeout alarm
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)

        return True

    except TimeoutError as e:
        print(f"Error: Encoding timeout ({timeout}s exceeded)", file=sys.stderr)
        print(f"Attempting to save partial record...", file=sys.stderr)

        # Try to save a minimal partial record
        try:
            partial_record = {
                "session_id": session_id or get_session_id(),
                "timestamp": get_timestamp(),
                "project_path": project_path,
                "trigger": trigger,
                "encoding_mode": "partial_timeout",
                "task_summary": f"[TIMEOUT] Encoding exceeded {timeout}s",
                "limitations": [f"Encoding timeout at {timeout}s", "Partial record only"]
            }

            pms_dir = Path(project_path) / ".claude" / "pms"
            episodic_dir = pms_dir / "episodic"
            ensure_directory(episodic_dir)

            monthly_filename = get_monthly_filename(partial_record["timestamp"])
            monthly_filepath = episodic_dir / monthly_filename

            merge_monthly(partial_record, str(monthly_filepath))
            print(f"Saved partial record due to timeout: {monthly_filename}", file=sys.stderr)
        except Exception as save_error:
            print(f"Failed to save partial record: {save_error}", file=sys.stderr)

        # Cancel timeout alarm
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)

        return False

    except Exception as e:
        print(f"Error encoding session: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

        # Cancel timeout alarm
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)

        return False


def encode_from_context(project_path: str, session_id: str, trigger: str) -> dict:
    """
    Encode session from conversation context.
    This is the preferred method - uses conversation history directly.

    Args:
        project_path: Path to project root
        session_id: Session UUID
        trigger: Trigger event

    Returns:
        Episodic record dictionary
    """
    # TODO: Implement prompt-based analysis using prompts/analyze-session.txt
    # For now, create a basic record structure

    episodic_record = {
        "session_id": session_id,
        "timestamp": get_timestamp(),
        "project_path": project_path,
        "git_branch": get_git_branch(),
        "trigger": trigger,
        "encoding_mode": "context",

        # Core fields (to be filled by prompt analysis)
        "task_summary": "Session work summary (context-first encoding)",
        "work_summary": "Detailed work performed",
        "design_decisions": [],
        "challenges": [],
        "solutions": [],
        "user_preferences": [],
        "code_patterns": [],
        "anti_patterns": [],

        # Context metadata
        "context": {
            "technologies": [],
            "files_modified": [],
            "tools_used": []
        }
    }

    return episodic_record


def encode_from_jsonl(project_path: str, session_id: str, trigger: str) -> Optional[Dict]:
    """
    Encode session from JSONL transcript (fallback method).
    Used when conversation context is unavailable.

    Args:
        project_path: Path to project root
        session_id: Session UUID
        trigger: Trigger event

    Returns:
        Episodic record dictionary or None if JSONL not found
    """
    # Locate JSONL transcript
    # Pattern: ~/.claude/projects/{project}/transcripts/{session-id}.jsonl
    home = Path.home()
    claude_dir = home / ".claude" / "projects"

    # Try to find transcript (this is a best-effort search)
    transcript_records = []
    transcript_path = None
    malformed_lines = 0
    valid_lines = 0

    # Search for recent transcripts
    if not claude_dir.exists():
        print(f"Warning: JSONL directory not found: {claude_dir}", file=sys.stderr)
        print("Falling back to context-only encoding", file=sys.stderr)
        return None

    transcript_found = False
    for transcript_file in claude_dir.rglob("*.jsonl"):
        try:
            transcript_found = True
            # Read with malformed JSONL handling
            with open(transcript_file, 'r', encoding='utf-8') as f:
                for line_num, line in enumerate(f, 1):
                    line = line.strip()
                    if not line:
                        continue

                    try:
                        record = json.loads(line)
                        transcript_records.append(record)
                        valid_lines += 1
                    except json.JSONDecodeError as e:
                        malformed_lines += 1
                        # Log but continue processing
                        if malformed_lines <= 5:  # Only log first 5 errors
                            print(f"Warning: Malformed JSONL at {transcript_file}:{line_num}: {e}", file=sys.stderr)

                    # Limit total records for performance
                    if valid_lines >= 1000:
                        break

            if transcript_records:
                transcript_path = str(transcript_file)
                break

        except Exception as e:
            print(f"Warning: Error reading transcript {transcript_file}: {e}", file=sys.stderr)
            continue

    # Report malformed line handling
    if malformed_lines > 0:
        print(f"Skipped {malformed_lines} malformed JSONL lines, processed {valid_lines} valid lines", file=sys.stderr)

    # If no transcript found
    if not transcript_found or not transcript_records:
        print("Warning: No JSONL transcript records found", file=sys.stderr)
        print("This may be expected if context-first encoding is preferred", file=sys.stderr)
        return None

    # Extract metadata from transcript
    tool_counts = {}
    file_operations = []
    error_messages = []

    for record in transcript_records:
        try:
            # Count tool uses
            if "tool_name" in record:
                tool_name = record["tool_name"]
                tool_counts[tool_name] = tool_counts.get(tool_name, 0) + 1

            # Extract file operations
            if "tool_input" in record and isinstance(record["tool_input"], dict):
                if "file_path" in record["tool_input"]:
                    file_operations.append(record["tool_input"]["file_path"])

            # Extract error messages
            if "error" in record:
                error_messages.append(str(record["error"]))
        except Exception as e:
            # Skip records we can't process
            continue

    episodic_record = {
        "session_id": session_id,
        "timestamp": get_timestamp(),
        "project_path": project_path,
        "git_branch": get_git_branch(),
        "trigger": trigger,
        "encoding_mode": "jsonl_fallback",

        # Core fields (best-effort from transcript)
        "task_summary": f"Session with {valid_lines} transcript records",
        "work_summary": f"Used tools: {', '.join(tool_counts.keys()) if tool_counts else 'none detected'}",
        "design_decisions": [],
        "challenges": error_messages[:5] if error_messages else [],
        "solutions": [],
        "user_preferences": [],
        "code_patterns": [],
        "anti_patterns": [],

        # Context metadata from transcript
        "context": {
            "technologies": [],
            "files_modified": list(set(file_operations))[:20] if file_operations else [],
            "tools_used": list(tool_counts.keys()),
            "tool_counts": tool_counts
        },

        # Transcript metadata
        "transcript": {
            "path": transcript_path,
            "record_count": valid_lines,
            "malformed_lines": malformed_lines
        }
    }

    # Add limitations note if data incomplete
    if malformed_lines > 0 or valid_lines < 10:
        episodic_record["limitations"] = []
        if malformed_lines > 0:
            episodic_record["limitations"].append(f"Skipped {malformed_lines} malformed JSONL lines")
        if valid_lines < 10:
            episodic_record["limitations"].append(f"Limited data: only {valid_lines} valid records")

    return episodic_record


def main():
    """Main entry point for encode.py"""
    parser = argparse.ArgumentParser(
        description="Encode session experience as episodic memory"
    )
    parser.add_argument(
        "--project-path",
        type=str,
        default=None,
        help="Path to project root (uses $CLAUDE_PROJECT_DIR if not specified)"
    )
    parser.add_argument(
        "--trigger",
        type=str,
        required=True,
        choices=["precompact", "session-end", "stop", "manual"],
        help="Trigger event"
    )
    parser.add_argument(
        "--session-id",
        type=str,
        default=None,
        help="Session ID (generates new if not specified)"
    )

    args = parser.parse_args()

    # Determine project path
    project_path = args.project_path or get_project_path()

    # Encode session
    success = encode_session(project_path, args.trigger, args.session_id)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
