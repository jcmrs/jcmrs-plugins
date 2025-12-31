#!/usr/bin/env python3
"""
Recovery Utilities for Claude PMS
Provides rebuild, backup, validation, and reset functions
"""

import argparse
import shutil
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import load_config
from extract import load_all_sessions, detect_frequency_patterns
from json_handler import safe_load, safe_save
from utils import ensure_directory, get_project_path, get_timestamp


def rebuild_semantic(project_path: str) -> bool:
    """
    Rebuild semantic knowledge from episodic records.
    Use when semantic files are corrupted or deleted.

    Args:
        project_path: Path to project root

    Returns:
        True if successful, False otherwise
    """
    try:
        print("Rebuilding semantic knowledge from episodic records...")

        pms_dir = Path(project_path) / ".claude" / "pms"
        episodic_dir = pms_dir / "episodic"

        if not episodic_dir.exists():
            print("Error: No episodic directory found", file=sys.stderr)
            return False

        # Load all sessions (with corruption handling)
        all_sessions, corrupted_files = load_all_sessions(episodic_dir)

        if corrupted_files:
            print(f"Warning: Skipped {len(corrupted_files)} corrupted file(s)", file=sys.stderr)

        if not all_sessions:
            print("Error: No episodic records found", file=sys.stderr)
            return False

        print(f"Loaded {len(all_sessions)} episodic records")

        # Load config for thresholds
        config = load_config(project_path)

        # Detect patterns
        patterns = detect_frequency_patterns(
            all_sessions,
            config.emerging_pattern,
            config.strong_pattern,
            config.critical_pattern
        )

        if not patterns:
            print("No patterns detected")
            return False

        print(f"Detected {len(patterns)} patterns")

        # Categorize
        preferences = [p for p in patterns if p.get("category") == "preference"]
        code_patterns = [p for p in patterns if p.get("category") == "code_pattern"]
        anti_patterns = [p for p in patterns if p.get("category") == "anti_pattern"]

        # Save semantic knowledge
        semantic_dir = pms_dir / "semantic"
        ensure_directory(semantic_dir)

        # Save patterns.json
        patterns_file = semantic_dir / "patterns.json"
        safe_save(
            str(patterns_file),
            {
                "patterns": patterns,
                "count": len(patterns),
                "last_updated": get_timestamp()
            }
        )

        # Save preferences.json
        safe_save(
            str(semantic_dir / "preferences.json"),
            {
                "preferences": preferences,
                "count": len(preferences),
                "last_updated": get_timestamp()
            }
        )

        # Save code-patterns.json
        safe_save(
            str(semantic_dir / "code-patterns.json"),
            {
                "code_patterns": code_patterns,
                "count": len(code_patterns),
                "last_updated": get_timestamp()
            }
        )

        # Save anti-patterns.json
        safe_save(
            str(semantic_dir / "anti-patterns.json"),
            {
                "anti_patterns": anti_patterns,
                "count": len(anti_patterns),
                "last_updated": get_timestamp()
            }
        )

        print(f"✓ Rebuilt semantic knowledge successfully")
        print(f"  - {len(preferences)} preferences")
        print(f"  - {len(code_patterns)} code patterns")
        print(f"  - {len(anti_patterns)} anti-patterns")

        return True

    except Exception as e:
        print(f"Error rebuilding semantic knowledge: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False


def backup_corrupted(filepath: str, backup_dir: Optional[str] = None) -> bool:
    """
    Move corrupted file to backup directory.

    Args:
        filepath: Path to corrupted file
        backup_dir: Optional backup directory (defaults to .backup in same dir)

    Returns:
        True if successful, False otherwise
    """
    try:
        source = Path(filepath)

        if not source.exists():
            print(f"File not found: {filepath}", file=sys.stderr)
            return False

        # Default backup directory
        if backup_dir is None:
            backup_dir = source.parent / ".backup"
        else:
            backup_dir = Path(backup_dir)

        ensure_directory(backup_dir)

        # Add timestamp to backup filename
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        backup_filename = f"{source.stem}_{timestamp}{source.suffix}"
        backup_path = backup_dir / backup_filename

        # Move file
        shutil.move(str(source), str(backup_path))

        print(f"✓ Backed up corrupted file:")
        print(f"  From: {source}")
        print(f"  To: {backup_path}")

        return True

    except Exception as e:
        print(f"Error backing up file: {e}", file=sys.stderr)
        return False


def validate_memory_structure(project_path: str) -> Tuple[bool, List[str]]:
    """
    Validate all PMS memory files are valid JSON and structurally correct.

    Args:
        project_path: Path to project root

    Returns:
        Tuple of (all_valid, error_messages)
    """
    errors = []
    pms_dir = Path(project_path) / ".claude" / "pms"

    if not pms_dir.exists():
        errors.append("PMS directory not initialized")
        return False, errors

    print("Validating PMS memory structure...")

    # Validate episodic records
    episodic_dir = pms_dir / "episodic"
    if episodic_dir.exists():
        for monthly_file in episodic_dir.glob("sessions-*.json"):
            data = safe_load(str(monthly_file), default=None)
            if data is None:
                errors.append(f"Corrupted: {monthly_file}")
            elif "sessions" not in data:
                errors.append(f"Missing 'sessions' key: {monthly_file}")

        # Validate index
        index_file = episodic_dir / "index.json"
        if index_file.exists():
            index = safe_load(str(index_file), default=None)
            if index is None:
                errors.append(f"Corrupted: {index_file}")

    # Validate semantic knowledge
    semantic_dir = pms_dir / "semantic"
    if semantic_dir.exists():
        for semantic_file in ["patterns.json", "preferences.json", "code-patterns.json", "anti-patterns.json"]:
            filepath = semantic_dir / semantic_file
            if filepath.exists():
                data = safe_load(str(filepath), default=None)
                if data is None:
                    errors.append(f"Corrupted: {filepath}")

    # Validate procedural metadata
    procedural_dir = pms_dir / "procedural"
    if procedural_dir.exists():
        metadata_file = procedural_dir / "rules-metadata.json"
        if metadata_file.exists():
            data = safe_load(str(metadata_file), default=None)
            if data is None:
                errors.append(f"Corrupted: {metadata_file}")

    # Report results
    if errors:
        print(f"❌ Validation failed - {len(errors)} errors:")
        for error in errors:
            print(f"  - {error}")
        return False, errors
    else:
        print("✓ All PMS memory files valid")
        return True, []


def reset_pms(project_path: str, keep_episodic: bool = True) -> bool:
    """
    Reset PMS to clean state.

    Args:
        project_path: Path to project root
        keep_episodic: If True, preserve episodic records

    Returns:
        True if successful, False otherwise
    """
    try:
        pms_dir = Path(project_path) / ".claude" / "pms"

        if not pms_dir.exists():
            print("PMS not initialized - nothing to reset")
            return True

        # Backup episodic if requested
        if keep_episodic:
            episodic_dir = pms_dir / "episodic"
            if episodic_dir.exists():
                backup_dir = pms_dir.parent / "pms_backup_episodic"
                ensure_directory(backup_dir)

                timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
                backup_path = backup_dir / f"episodic_{timestamp}"

                shutil.copytree(str(episodic_dir), str(backup_path))
                print(f"✓ Backed up episodic records to: {backup_path}")

        # Remove semantic and procedural
        semantic_dir = pms_dir / "semantic"
        if semantic_dir.exists():
            shutil.rmtree(str(semantic_dir))
            print("✓ Removed semantic knowledge")

        procedural_dir = pms_dir / "procedural"
        if procedural_dir.exists():
            shutil.rmtree(str(procedural_dir))
            print("✓ Removed procedural metadata")

        # Remove rule files
        rules_dir = Path(project_path) / ".claude" / "rules" / "pms"
        if rules_dir.exists():
            shutil.rmtree(str(rules_dir))
            print("✓ Removed rule files")

        # If not keeping episodic, remove everything
        if not keep_episodic:
            shutil.rmtree(str(pms_dir))
            print("✓ Removed all PMS data")

        print("")
        print("✓ PMS reset complete")

        if keep_episodic:
            print("  Episodic records preserved")
            print("  Run /pms:reflect to rebuild from scratch")
        else:
            print("  All data removed")
            print("  System will start fresh on next session")

        return True

    except Exception as e:
        print(f"Error resetting PMS: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main entry point for recovery.py"""
    parser = argparse.ArgumentParser(
        description="PMS Recovery Utilities"
    )
    parser.add_argument(
        "--project-path",
        type=str,
        default=None,
        help="Path to project root (uses $CLAUDE_PROJECT_DIR if not specified)"
    )

    subparsers = parser.add_subparsers(dest="command", help="Recovery command")

    # rebuild-semantic
    rebuild_parser = subparsers.add_parser(
        "rebuild-semantic",
        help="Rebuild semantic knowledge from episodic records"
    )

    # backup-corrupted
    backup_parser = subparsers.add_parser(
        "backup-corrupted",
        help="Backup a corrupted file"
    )
    backup_parser.add_argument("filepath", help="Path to corrupted file")

    # validate
    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate all PMS memory files"
    )

    # reset
    reset_parser = subparsers.add_parser(
        "reset",
        help="Reset PMS to clean state"
    )
    reset_parser.add_argument(
        "--remove-episodic",
        action="store_true",
        help="Also remove episodic records (default: keep)"
    )

    args = parser.parse_args()

    # Determine project path
    project_path = args.project_path or get_project_path()

    # Execute command
    if args.command == "rebuild-semantic":
        success = rebuild_semantic(project_path)
        sys.exit(0 if success else 1)

    elif args.command == "backup-corrupted":
        success = backup_corrupted(args.filepath)
        sys.exit(0 if success else 1)

    elif args.command == "validate":
        valid, errors = validate_memory_structure(project_path)
        sys.exit(0 if valid else 1)

    elif args.command == "reset":
        keep_episodic = not args.remove_episodic
        success = reset_pms(project_path, keep_episodic)
        sys.exit(0 if success else 1)

    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
