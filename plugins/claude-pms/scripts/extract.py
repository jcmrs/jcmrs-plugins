#!/usr/bin/env python3
"""
Semantic Extraction Engine for Claude PMS
Analyzes episodic records to detect patterns, preferences, and anti-patterns
"""

import argparse
import json
import signal
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Dict, List, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import load_config
from json_handler import safe_load, safe_save
from utils import ensure_directory, get_project_path, get_timestamp


# Timeout handling
class ExtractionTimeoutError(Exception):
    """Raised when extraction exceeds timeout"""
    pass


def extraction_timeout_handler(signum, frame):
    """Signal handler for extraction timeout"""
    raise ExtractionTimeoutError("Semantic extraction exceeded timeout limit")


def extract_patterns(project_path: str, min_sessions: int = None, timeout: int = 60) -> bool:
    """
    Extract semantic patterns from episodic records.

    Args:
        project_path: Path to project root
        min_sessions: Minimum sessions before extraction (uses config if None)
        timeout: Maximum extraction time in seconds (default: 60)

    Returns:
        True if successful, False otherwise
    """
    # Set up timeout handler (Unix-like systems only)
    if hasattr(signal, 'SIGALRM'):
        signal.signal(signal.SIGALRM, extraction_timeout_handler)
        signal.alarm(timeout)

    try:
        # Load configuration
        config = load_config(project_path)
        if min_sessions is None:
            min_sessions = config.min_sessions

        # Load episodic records
        pms_dir = Path(project_path) / ".claude" / "pms"
        episodic_dir = pms_dir / "episodic"

        if not episodic_dir.exists():
            print("Error: No episodic records found - run /pms:encode first", file=sys.stderr)
            return False

        # Load all sessions from monthly files with corruption handling
        all_sessions, corrupted_files = load_all_sessions(episodic_dir)

        if corrupted_files:
            print(f"Warning: Skipped {len(corrupted_files)} corrupted file(s):", file=sys.stderr)
            for filepath in corrupted_files[:5]:  # Show first 5
                print(f"  - {filepath}", file=sys.stderr)
            if len(corrupted_files) > 5:
                print(f"  ... and {len(corrupted_files) - 5} more", file=sys.stderr)

        # Check threshold
        if len(all_sessions) < min_sessions:
            print(
                f"Insufficient sessions ({len(all_sessions)}/{min_sessions}). "
                f"Continue working to accumulate more data.",
                file=sys.stderr
            )
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            return False

        print(f"Analyzing {len(all_sessions)} episodic records...")

        # Frequency-based pattern detection
        try:
            patterns = detect_frequency_patterns(
                all_sessions,
                config.emerging_pattern,
                config.strong_pattern,
                config.critical_pattern
            )
        except Exception as e:
            print(f"Error during pattern detection: {e}", file=sys.stderr)
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            return False

        print(f"Detected {len(patterns)} patterns")

        # Categorize patterns
        preferences = [p for p in patterns if p["category"] == "preference"]
        code_patterns = [p for p in patterns if p["category"] == "code_pattern"]
        anti_patterns = [p for p in patterns if p["category"] == "anti_pattern"]

        print(f"  - {len(preferences)} preferences")
        print(f"  - {len(code_patterns)} code patterns")
        print(f"  - {len(anti_patterns)} anti-patterns")

        # TODO: Call prompt-based semantic analysis (prompts/detect-patterns.txt)
        # For now, use frequency-based results
        # If prompt fails, continue with frequency-based patterns
        # This ensures degraded but functional operation

        # Save semantic knowledge
        semantic_dir = pms_dir / "semantic"
        ensure_directory(semantic_dir)

        save_result = save_semantic_knowledge(semantic_dir, patterns, preferences, code_patterns, anti_patterns)
        if not save_result:
            print("Error: Failed to save semantic knowledge", file=sys.stderr)
            if hasattr(signal, 'SIGALRM'):
                signal.alarm(0)
            return False

        print(f"✓ Semantic knowledge saved to {semantic_dir}")

        # Trigger procedural synthesis if auto enabled
        if config.auto_synthesize:
            print("Auto-synthesis enabled - triggering rule generation...")
            # TODO: Call synthesize.py
            print("(synthesis will be implemented in Task 6)")
        else:
            # Notify user to run manual synthesis
            strong_pattern_count = sum(1 for p in patterns if p["strength"] == "strong" or p["strength"] == "critical")
            if strong_pattern_count > 0:
                print(f"\n{strong_pattern_count} strong patterns detected. Run /pms:synthesize to generate rules.")

        # Cancel timeout alarm
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)

        return True

    except ExtractionTimeoutError as e:
        print(f"Error: Extraction timeout ({timeout}s exceeded)", file=sys.stderr)
        print("Try reducing the number of sessions or increasing timeout", file=sys.stderr)

        # Cancel timeout alarm
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)

        return False

    except Exception as e:
        print(f"Error extracting patterns: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()

        # Cancel timeout alarm
        if hasattr(signal, 'SIGALRM'):
            signal.alarm(0)

        return False


def load_all_sessions(episodic_dir: Path) -> Tuple[List[Dict], List[str]]:
    """
    Load all session records from monthly files with corruption handling.

    Args:
        episodic_dir: Path to episodic directory

    Returns:
        Tuple of (all_sessions, corrupted_files)
        - all_sessions: List of all valid session records
        - corrupted_files: List of filepaths that failed to load
    """
    all_sessions = []
    corrupted_files = []

    # Find all monthly files
    for monthly_file in sorted(episodic_dir.glob("sessions-*.json")):
        try:
            data = safe_load(str(monthly_file), default=None)

            # Check if file loaded successfully
            if data is None:
                corrupted_files.append(str(monthly_file))
                print(f"Warning: Corrupted file: {monthly_file}", file=sys.stderr)
                continue

            # Validate structure
            if "sessions" not in data:
                corrupted_files.append(str(monthly_file))
                print(f"Warning: Invalid structure (missing 'sessions' key): {monthly_file}", file=sys.stderr)
                continue

            # Validate sessions is a list
            if not isinstance(data["sessions"], list):
                corrupted_files.append(str(monthly_file))
                print(f"Warning: Invalid structure ('sessions' not a list): {monthly_file}", file=sys.stderr)
                continue

            # Add valid sessions
            all_sessions.extend(data["sessions"])

        except Exception as e:
            corrupted_files.append(str(monthly_file))
            print(f"Warning: Error loading {monthly_file}: {e}", file=sys.stderr)
            continue

    return all_sessions, corrupted_files


def detect_frequency_patterns(
    sessions: List[Dict],
    emerging_threshold: int,
    strong_threshold: int,
    critical_threshold: int
) -> List[Dict]:
    """
    Detect patterns based on frequency of occurrences.

    Args:
        sessions: List of episodic records
        emerging_threshold: Min occurrences for emerging pattern (default: 2)
        strong_threshold: Min occurrences for strong pattern (default: 3)
        critical_threshold: Min occurrences for critical pattern (default: 5)

    Returns:
        List of detected patterns with evidence
    """
    patterns = []

    # Extract user preferences
    preferences = extract_user_preferences(sessions)
    for pref_description, evidence in preferences.items():
        occurrences = len(evidence)
        if occurrences >= emerging_threshold:
            strength = categorize_strength(occurrences, emerging_threshold, strong_threshold, critical_threshold)
            patterns.append({
                "pattern_id": f"pref_{hash(pref_description) % 1000000}",
                "description": pref_description,
                "category": "preference",
                "strength": strength,
                "occurrences": occurrences,
                "evidence": evidence[:10],  # Limit evidence to 10 examples
                "detected_at": get_timestamp()
            })

    # Extract code patterns
    code_patterns_data = extract_code_patterns(sessions)
    for pattern_description, evidence in code_patterns_data.items():
        occurrences = len(evidence)
        if occurrences >= emerging_threshold:
            strength = categorize_strength(occurrences, emerging_threshold, strong_threshold, critical_threshold)
            patterns.append({
                "pattern_id": f"code_{hash(pattern_description) % 1000000}",
                "description": pattern_description,
                "category": "code_pattern",
                "strength": strength,
                "occurrences": occurrences,
                "evidence": evidence[:10],
                "detected_at": get_timestamp()
            })

    # Extract anti-patterns
    anti_patterns_data = extract_anti_patterns(sessions)
    for anti_description, evidence in anti_patterns_data.items():
        occurrences = len(evidence)
        if occurrences >= emerging_threshold:
            strength = categorize_strength(occurrences, emerging_threshold, strong_threshold, critical_threshold)
            patterns.append({
                "pattern_id": f"anti_{hash(anti_description) % 1000000}",
                "description": anti_description,
                "category": "anti_pattern",
                "strength": strength,
                "occurrences": occurrences,
                "evidence": evidence[:10],
                "detected_at": get_timestamp()
            })

    return patterns


def extract_user_preferences(sessions: List[Dict]) -> Dict[str, List[str]]:
    """
    Extract user preferences from episodic records.

    Args:
        sessions: List of episodic records

    Returns:
        Dict mapping preference description → list of session IDs (evidence)
    """
    preferences = defaultdict(list)

    for session in sessions:
        session_id = session.get("session_id", "unknown")

        # Extract from user_preferences field
        if "user_preferences" in session:
            for pref in session["user_preferences"]:
                if isinstance(pref, str):
                    preferences[pref].append(session_id)
                elif isinstance(pref, dict) and "description" in pref:
                    preferences[pref["description"]].append(session_id)

    return dict(preferences)


def extract_code_patterns(sessions: List[Dict]) -> Dict[str, List[str]]:
    """
    Extract code patterns from episodic records.

    Args:
        sessions: List of episodic records

    Returns:
        Dict mapping pattern description → list of session IDs (evidence)
    """
    code_patterns = defaultdict(list)

    for session in sessions:
        session_id = session.get("session_id", "unknown")

        # Extract from code_patterns field
        if "code_patterns" in session:
            for pattern in session["code_patterns"]:
                if isinstance(pattern, str):
                    code_patterns[pattern].append(session_id)
                elif isinstance(pattern, dict) and "description" in pattern:
                    code_patterns[pattern["description"]].append(session_id)

    return dict(code_patterns)


def extract_anti_patterns(sessions: List[Dict]) -> Dict[str, List[str]]:
    """
    Extract anti-patterns (mistakes to avoid) from episodic records.

    Args:
        sessions: List of episodic records

    Returns:
        Dict mapping anti-pattern description → list of session IDs (evidence)
    """
    anti_patterns = defaultdict(list)

    for session in sessions:
        session_id = session.get("session_id", "unknown")

        # Extract from anti_patterns field
        if "anti_patterns" in session:
            for anti in session["anti_patterns"]:
                if isinstance(anti, str):
                    anti_patterns[anti].append(session_id)
                elif isinstance(anti, dict) and "description" in anti:
                    anti_patterns[anti["description"]].append(session_id)

    return dict(anti_patterns)


def categorize_strength(
    occurrences: int,
    emerging: int,
    strong: int,
    critical: int
) -> str:
    """
    Categorize pattern strength based on occurrence count.

    Args:
        occurrences: Number of occurrences
        emerging: Threshold for emerging pattern
        strong: Threshold for strong pattern
        critical: Threshold for critical pattern

    Returns:
        "emerging", "strong", or "critical"
    """
    if occurrences >= critical:
        return "critical"
    elif occurrences >= strong:
        return "strong"
    elif occurrences >= emerging:
        return "emerging"
    else:
        return "weak"


def save_semantic_knowledge(
    semantic_dir: Path,
    all_patterns: List[Dict],
    preferences: List[Dict],
    code_patterns: List[Dict],
    anti_patterns: List[Dict]
) -> bool:
    """
    Save semantic knowledge to JSON files.

    Args:
        semantic_dir: Path to semantic directory
        all_patterns: All detected patterns
        preferences: User preference patterns
        code_patterns: Code pattern patterns
        anti_patterns: Anti-pattern patterns

    Returns:
        True if successful
    """
    try:
        # Save all patterns
        patterns_file = semantic_dir / "patterns.json"
        safe_save(
            str(patterns_file),
            {
                "patterns": all_patterns,
                "count": len(all_patterns),
                "last_updated": get_timestamp()
            }
        )

        # Save preferences
        preferences_file = semantic_dir / "preferences.json"
        safe_save(
            str(preferences_file),
            {
                "preferences": preferences,
                "count": len(preferences),
                "last_updated": get_timestamp()
            }
        )

        # Save code patterns
        code_patterns_file = semantic_dir / "code-patterns.json"
        safe_save(
            str(code_patterns_file),
            {
                "code_patterns": code_patterns,
                "count": len(code_patterns),
                "last_updated": get_timestamp()
            }
        )

        # Save anti-patterns
        anti_patterns_file = semantic_dir / "anti-patterns.json"
        safe_save(
            str(anti_patterns_file),
            {
                "anti_patterns": anti_patterns,
                "count": len(anti_patterns),
                "last_updated": get_timestamp()
            }
        )

        return True

    except Exception as e:
        print(f"Error saving semantic knowledge: {e}", file=sys.stderr)
        return False


def main():
    """Main entry point for extract.py"""
    parser = argparse.ArgumentParser(
        description="Extract semantic patterns from episodic records"
    )
    parser.add_argument(
        "--project-path",
        type=str,
        default=None,
        help="Path to project root (uses $CLAUDE_PROJECT_DIR if not specified)"
    )
    parser.add_argument(
        "--min-sessions",
        type=int,
        default=None,
        help="Minimum sessions before extraction (uses config if not specified)"
    )

    args = parser.parse_args()

    # Determine project path
    project_path = args.project_path or get_project_path()

    # Extract patterns
    success = extract_patterns(project_path, args.min_sessions)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
