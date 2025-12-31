#!/usr/bin/env python3
"""
Procedural Synthesis Engine for Claude PMS
Converts confirmed patterns into project-scoped rule files
"""

import argparse
import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional, Tuple

# Add parent directory to path for imports
sys.path.insert(0, str(Path(__file__).parent))

from config import load_config
from json_handler import safe_load, safe_save
from utils import ensure_directory, get_project_path, get_timestamp


def synthesize_rules(project_path: str, require_approval: bool = True) -> bool:
    """
    Synthesize procedural rules from semantic patterns.

    Args:
        project_path: Path to project root
        require_approval: Whether to require user approval for rules

    Returns:
        True if successful, False otherwise
    """
    try:
        # Load configuration
        config = load_config(project_path)

        # Load semantic knowledge
        pms_dir = Path(project_path) / ".claude" / "pms"
        semantic_dir = pms_dir / "semantic"

        if not semantic_dir.exists():
            print("No semantic knowledge found. Run extraction first.", file=sys.stderr)
            return False

        # Load patterns
        patterns_file = semantic_dir / "patterns.json"
        if not patterns_file.exists():
            print("No patterns found. Run extraction first.", file=sys.stderr)
            return False

        patterns_data = safe_load(str(patterns_file), default={"patterns": []})
        all_patterns = patterns_data.get("patterns", [])

        if not all_patterns:
            print("No patterns to synthesize.", file=sys.stderr)
            return False

        print(f"Loaded {len(all_patterns)} patterns from semantic knowledge")

        # Filter strong patterns (≥3 occurrences)
        strong_patterns = [p for p in all_patterns if p.get("strength") in ("strong", "critical")]

        if not strong_patterns:
            print("No strong patterns found (need strength='strong' or 'critical')", file=sys.stderr)
            return False

        print(f"Found {len(strong_patterns)} strong patterns for rule generation")

        # Group patterns by category
        preferences = [p for p in strong_patterns if p.get("category") == "preference"]
        code_patterns = [p for p in strong_patterns if p.get("category") == "code_pattern"]
        anti_patterns = [p for p in strong_patterns if p.get("category") == "anti_pattern"]

        print(f"  - {len(preferences)} user preferences")
        print(f"  - {len(code_patterns)} code patterns")
        print(f"  - {len(anti_patterns)} anti-patterns")

        # Generate rules for each category
        rule_files = {}

        if preferences:
            rules = generate_rules_from_patterns(preferences, "User Preferences")
            rule_files["user-preferences.md"] = rules

        if code_patterns:
            rules = generate_rules_from_patterns(code_patterns, "Code Patterns")
            rule_files["code-patterns.md"] = rules

        if anti_patterns:
            rules = generate_rules_from_patterns(anti_patterns, "Anti-Patterns")
            rule_files["anti-patterns.md"] = rules

        # User approval workflow (if enabled)
        if require_approval and not config.auto_synthesize:
            print("\n=== Proposed Rules ===")
            for filename, content in rule_files.items():
                print(f"\n{filename}:")
                print(content[:500] + "..." if len(content) > 500 else content)

            # In real implementation, this would use interactive approval
            # For now, auto-approve if called programmatically
            approval = True

            if not approval:
                print("Rule generation cancelled by user.")
                return False

        # Save rule files with permission error handling
        rules_dir = Path(project_path) / ".claude" / "rules" / "pms"

        try:
            ensure_directory(rules_dir)
        except PermissionError as e:
            print(f"Error: Permission denied creating rules directory: {rules_dir}", file=sys.stderr)
            print(f"Check directory permissions and try again", file=sys.stderr)
            return False

        saved_files = []
        failed_files = []

        for filename, content in rule_files.items():
            rule_file = rules_dir / filename
            try:
                # Validate markdown content before writing
                if not content or len(content.strip()) == 0:
                    print(f"Warning: Empty content for {filename}, skipping", file=sys.stderr)
                    failed_files.append((filename, "Empty content"))
                    continue

                # Write rule file
                rule_file.write_text(content, encoding='utf-8')
                saved_files.append(filename)
                print(f"Generated: {filename}")

            except PermissionError as e:
                print(f"Error: Permission denied writing {filename}", file=sys.stderr)
                failed_files.append((filename, "Permission denied"))
            except OSError as e:
                print(f"Error: Failed to write {filename}: {e}", file=sys.stderr)
                failed_files.append((filename, str(e)))
            except Exception as e:
                print(f"Error: Unexpected error writing {filename}: {e}", file=sys.stderr)
                failed_files.append((filename, str(e)))

        # Report failures
        if failed_files:
            print(f"\nWarning: Failed to generate {len(failed_files)} file(s):", file=sys.stderr)
            for filename, reason in failed_files:
                print(f"  - {filename}: {reason}", file=sys.stderr)

        # If no files saved, report error
        if not saved_files:
            print("Error: No rule files generated", file=sys.stderr)
            return False

        # Update procedural metadata
        procedural_dir = pms_dir / "procedural"
        try:
            ensure_directory(procedural_dir)

            metadata = {
                "last_synthesis": get_timestamp(),
                "rule_files": saved_files,
                "pattern_count": len(strong_patterns),
                "breakdown": {
                    "preferences": len(preferences),
                    "code_patterns": len(code_patterns),
                    "anti_patterns": len(anti_patterns)
                },
                "files": {
                    filename: {
                        "created": get_timestamp(),
                        "pattern_count": len([p for p in strong_patterns if p["category"] == category]),
                        "confidence": "high" if any(p.get("strength") == "critical" for p in strong_patterns) else "medium"
                    }
                    for filename, category in [
                        ("user-preferences.md", "preference"),
                        ("code-patterns.md", "code_pattern"),
                        ("anti-patterns.md", "anti_pattern")
                    ]
                    if filename in saved_files
                },
                "failed_files": failed_files if failed_files else []
            }

            metadata_file = procedural_dir / "rules-metadata.json"
            safe_save(str(metadata_file), metadata)

        except PermissionError as e:
            print(f"Warning: Failed to save metadata (permission denied): {e}", file=sys.stderr)
            # Continue anyway - metadata is secondary

        print(f"\n✓ Generated {len(saved_files)} rule file(s) in .claude/rules/pms/")
        print("✓ Restart Claude Code session to load new rules")

        return True

    except Exception as e:
        print(f"Error synthesizing rules: {e}", file=sys.stderr)
        import traceback
        traceback.print_exc()
        return False


def generate_rules_from_patterns(patterns: List[Dict], category_title: str) -> str:
    """
    Generate markdown rule content from patterns.

    Args:
        patterns: List of pattern dictionaries
        category_title: Title for the rule category

    Returns:
        Markdown content for rule file
    """
    # TODO: In Task 7, this will call prompt-based synthesis
    # For now, use template-based generation

    timestamp = datetime.utcnow().strftime("%Y-%m-%d %H:%M UTC")

    # Header
    lines = [
        f"# {category_title}",
        "",
        f"<!-- Auto-generated by Claude PMS on {timestamp} -->",
        f"<!-- Pattern Count: {len(patterns)} | Confidence: {'High' if any(p.get('strength') == 'critical' for p in patterns) else 'Medium'} -->",
        "",
        f"## {category_title}",
        ""
    ]

    # Sort by strength and occurrences
    sorted_patterns = sorted(
        patterns,
        key=lambda p: (
            {"critical": 3, "strong": 2, "emerging": 1}.get(p.get("strength", "emerging"), 0),
            p.get("occurrences", 0)
        ),
        reverse=True
    )

    # Generate rules
    for pattern in sorted_patterns:
        description = pattern.get("description", "")
        occurrences = pattern.get("occurrences", 0)
        strength = pattern.get("strength", "emerging")
        evidence = pattern.get("evidence", [])

        # Convert pattern to rule format
        rule_text = convert_pattern_to_rule(description, strength)

        lines.append(f"**{rule_text}**")
        lines.append(f"- Observed {occurrences} times ({strength} pattern)")

        # Add evidence (limit to 5 sessions)
        if evidence:
            evidence_preview = evidence[:5]
            lines.append(f"- Evidence: {', '.join(evidence_preview)}")
            if len(evidence) > 5:
                lines.append(f"  (and {len(evidence) - 5} more)")

        lines.append("")

    return "\n".join(lines)


def convert_pattern_to_rule(description: str, strength: str) -> str:
    """
    Convert pattern description to rule format.

    Args:
        description: Pattern description
        strength: Pattern strength (emerging, strong, critical)

    Returns:
        Rule text
    """
    # TODO: In Task 7, this will use prompt-based synthesis
    # For now, apply simple transformations

    # Add imperative prefix for strong patterns
    if strength in ("strong", "critical"):
        # Convert to imperative if not already
        if not description.lower().startswith(("always", "never", "avoid", "prefer", "use")):
            return f"Follow this pattern: {description}"
        return description

    return description


def load_procedural_metadata(project_path: str) -> Optional[Dict]:
    """
    Load procedural metadata if exists.

    Args:
        project_path: Path to project root

    Returns:
        Metadata dict or None
    """
    metadata_file = Path(project_path) / ".claude" / "pms" / "procedural" / "rules-metadata.json"
    if not metadata_file.exists():
        return None

    return safe_load(str(metadata_file), default=None)


def check_existing_rules(project_path: str) -> List[str]:
    """
    Check for existing rule files.

    Args:
        project_path: Path to project root

    Returns:
        List of existing rule file paths
    """
    rules_dir = Path(project_path) / ".claude" / "rules" / "pms"
    if not rules_dir.exists():
        return []

    return [str(f) for f in rules_dir.glob("*.md")]


def main():
    """Main entry point for synthesize.py"""
    parser = argparse.ArgumentParser(
        description="Synthesize procedural rules from semantic patterns"
    )
    parser.add_argument(
        "--project-path",
        type=str,
        default=None,
        help="Path to project root (uses $CLAUDE_PROJECT_DIR if not specified)"
    )
    parser.add_argument(
        "--auto-approve",
        action="store_true",
        help="Skip user approval and auto-approve rules"
    )

    args = parser.parse_args()

    # Determine project path
    project_path = args.project_path or get_project_path()

    # Synthesize rules
    require_approval = not args.auto_approve
    success = synthesize_rules(project_path, require_approval)

    sys.exit(0 if success else 1)


if __name__ == "__main__":
    main()
