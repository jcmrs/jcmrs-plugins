"""
Unit tests for synthesize.py
Tests procedural rule generation from semantic patterns
"""

import json
import os
import tempfile
from pathlib import Path
from unittest.mock import patch

import pytest

# Import from scripts
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from synthesize import (
    synthesize_rules,
    generate_rules_from_patterns,
    convert_pattern_to_rule,
    load_procedural_metadata,
    check_existing_rules
)


def test_synthesize_rules_with_no_semantic_knowledge():
    """Test that synthesis fails when no semantic knowledge exists"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # No semantic directory
        success = synthesize_rules(tmpdir, require_approval=False)
        assert success is False


def test_synthesize_rules_with_no_patterns():
    """Test that synthesis fails when patterns file is empty"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create empty semantic directory
        semantic_dir = Path(tmpdir) / ".claude" / "pms" / "semantic"
        semantic_dir.mkdir(parents=True)

        # Create empty patterns file
        patterns_file = semantic_dir / "patterns.json"
        patterns_file.write_text(json.dumps({"patterns": [], "count": 0}))

        success = synthesize_rules(tmpdir, require_approval=False)
        assert success is False


def test_synthesize_rules_filters_weak_patterns():
    """Test that only strong/critical patterns are used for rules"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create semantic directory
        semantic_dir = Path(tmpdir) / ".claude" / "pms" / "semantic"
        semantic_dir.mkdir(parents=True)

        # Create patterns with mixed strengths
        patterns_file = semantic_dir / "patterns.json"
        patterns = {
            "patterns": [
                {
                    "pattern_id": "weak_1",
                    "description": "Weak pattern",
                    "category": "preference",
                    "strength": "emerging",
                    "occurrences": 2,
                    "evidence": ["s1", "s2"]
                },
                {
                    "pattern_id": "strong_1",
                    "description": "Strong pattern",
                    "category": "preference",
                    "strength": "strong",
                    "occurrences": 3,
                    "evidence": ["s1", "s2", "s3"]
                }
            ],
            "count": 2
        }
        patterns_file.write_text(json.dumps(patterns))

        # Create config
        config_file = Path(tmpdir) / ".claude" / "pms.local.md"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("---\nprocessing:\n  auto_synthesize: true\n---\n")

        # Synthesize
        success = synthesize_rules(tmpdir, require_approval=False)
        assert success is True

        # Verify only strong pattern generated rule
        rules_dir = Path(tmpdir) / ".claude" / "rules" / "pms"
        assert rules_dir.exists()

        rule_file = rules_dir / "user-preferences.md"
        assert rule_file.exists()

        content = rule_file.read_text()
        assert "Strong pattern" in content
        assert "Weak pattern" not in content


def test_synthesize_rules_creates_rule_files_by_category():
    """Test that rules are grouped into category files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create semantic directory
        semantic_dir = Path(tmpdir) / ".claude" / "pms" / "semantic"
        semantic_dir.mkdir(parents=True)

        # Create patterns for each category
        patterns_file = semantic_dir / "patterns.json"
        patterns = {
            "patterns": [
                {
                    "pattern_id": "pref_1",
                    "description": "User preference pattern",
                    "category": "preference",
                    "strength": "strong",
                    "occurrences": 3,
                    "evidence": ["s1", "s2", "s3"]
                },
                {
                    "pattern_id": "code_1",
                    "description": "Code pattern",
                    "category": "code_pattern",
                    "strength": "strong",
                    "occurrences": 4,
                    "evidence": ["s1", "s2", "s3", "s4"]
                },
                {
                    "pattern_id": "anti_1",
                    "description": "Anti-pattern",
                    "category": "anti_pattern",
                    "strength": "critical",
                    "occurrences": 5,
                    "evidence": ["s1", "s2", "s3", "s4", "s5"]
                }
            ],
            "count": 3
        }
        patterns_file.write_text(json.dumps(patterns))

        # Create config
        config_file = Path(tmpdir) / ".claude" / "pms.local.md"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("---\n---\n")

        # Synthesize
        success = synthesize_rules(tmpdir, require_approval=False)
        assert success is True

        # Verify all category files created
        rules_dir = Path(tmpdir) / ".claude" / "rules" / "pms"
        assert (rules_dir / "user-preferences.md").exists()
        assert (rules_dir / "code-patterns.md").exists()
        assert (rules_dir / "anti-patterns.md").exists()


def test_synthesize_rules_updates_metadata():
    """Test that procedural metadata is created and updated"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create semantic directory
        semantic_dir = Path(tmpdir) / ".claude" / "pms" / "semantic"
        semantic_dir.mkdir(parents=True)

        # Create patterns
        patterns_file = semantic_dir / "patterns.json"
        patterns = {
            "patterns": [
                {
                    "pattern_id": "pref_1",
                    "description": "Test preference",
                    "category": "preference",
                    "strength": "strong",
                    "occurrences": 3,
                    "evidence": ["s1", "s2", "s3"]
                }
            ],
            "count": 1
        }
        patterns_file.write_text(json.dumps(patterns))

        # Create config
        config_file = Path(tmpdir) / ".claude" / "pms.local.md"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("---\n---\n")

        # Synthesize
        success = synthesize_rules(tmpdir, require_approval=False)
        assert success is True

        # Verify metadata created
        metadata_file = Path(tmpdir) / ".claude" / "pms" / "procedural" / "rules-metadata.json"
        assert metadata_file.exists()

        with open(metadata_file) as f:
            metadata = json.load(f)
            assert "last_synthesis" in metadata
            assert "rule_files" in metadata
            assert "user-preferences.md" in metadata["rule_files"]
            assert metadata["pattern_count"] == 1
            assert metadata["breakdown"]["preferences"] == 1


def test_generate_rules_from_patterns():
    """Test rule generation from pattern list"""
    patterns = [
        {
            "pattern_id": "p1",
            "description": "Always run tests",
            "category": "preference",
            "strength": "strong",
            "occurrences": 3,
            "evidence": ["s1", "s2", "s3"]
        },
        {
            "pattern_id": "p2",
            "description": "Use type hints",
            "category": "preference",
            "strength": "critical",
            "occurrences": 5,
            "evidence": ["s1", "s2", "s3", "s4", "s5"]
        }
    ]

    content = generate_rules_from_patterns(patterns, "Test Category")

    # Verify structure
    assert "# Test Category" in content
    assert "Auto-generated by Claude PMS" in content
    assert "Pattern Count: 2" in content

    # Verify patterns included
    assert "Always run tests" in content
    assert "Use type hints" in content

    # Verify evidence included
    assert "Observed 3 times" in content
    assert "Observed 5 times" in content
    assert "Evidence:" in content


def test_generate_rules_sorts_by_strength():
    """Test that rules are sorted by strength and occurrences"""
    patterns = [
        {
            "pattern_id": "p1",
            "description": "Emerging pattern",
            "strength": "emerging",
            "occurrences": 2,
            "evidence": ["s1", "s2"]
        },
        {
            "pattern_id": "p2",
            "description": "Strong pattern",
            "strength": "strong",
            "occurrences": 3,
            "evidence": ["s1", "s2", "s3"]
        },
        {
            "pattern_id": "p3",
            "description": "Critical pattern",
            "strength": "critical",
            "occurrences": 5,
            "evidence": ["s1", "s2", "s3", "s4", "s5"]
        }
    ]

    content = generate_rules_from_patterns(patterns, "Test")

    # Critical should come first
    critical_pos = content.find("Critical pattern")
    strong_pos = content.find("Strong pattern")
    emerging_pos = content.find("Emerging pattern")

    assert critical_pos < strong_pos < emerging_pos


def test_convert_pattern_to_rule():
    """Test pattern to rule conversion"""
    # Strong pattern gets preserved
    rule = convert_pattern_to_rule("Always run tests", "strong")
    assert "Always run tests" in rule

    # Pattern without imperative gets prefix for strong patterns
    rule = convert_pattern_to_rule("Run tests before commits", "strong")
    assert "Follow this pattern" in rule or "Run tests" in rule

    # Emerging pattern unchanged
    rule = convert_pattern_to_rule("Some pattern", "emerging")
    assert "Some pattern" in rule


def test_load_procedural_metadata():
    """Test loading procedural metadata"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # No metadata exists
        metadata = load_procedural_metadata(tmpdir)
        assert metadata is None

        # Create metadata
        procedural_dir = Path(tmpdir) / ".claude" / "pms" / "procedural"
        procedural_dir.mkdir(parents=True)

        metadata_file = procedural_dir / "rules-metadata.json"
        test_metadata = {
            "last_synthesis": "2025-12-31T00:00:00Z",
            "rule_files": ["user-preferences.md"]
        }
        metadata_file.write_text(json.dumps(test_metadata))

        # Load metadata
        metadata = load_procedural_metadata(tmpdir)
        assert metadata is not None
        assert metadata["last_synthesis"] == "2025-12-31T00:00:00Z"


def test_check_existing_rules():
    """Test checking for existing rule files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # No rules directory
        rules = check_existing_rules(tmpdir)
        assert rules == []

        # Create rules directory with files
        rules_dir = Path(tmpdir) / ".claude" / "rules" / "pms"
        rules_dir.mkdir(parents=True)

        (rules_dir / "user-preferences.md").write_text("# Test")
        (rules_dir / "code-patterns.md").write_text("# Test")

        # Check existing
        rules = check_existing_rules(tmpdir)
        assert len(rules) == 2


def test_synthesize_rules_with_no_strong_patterns():
    """Test synthesis fails when no patterns meet threshold"""
    with tempfile.TemporaryDirectory() as tmpdir:
        semantic_dir = Path(tmpdir) / ".claude" / "pms" / "semantic"
        semantic_dir.mkdir(parents=True)

        # Only emerging patterns
        patterns_file = semantic_dir / "patterns.json"
        patterns = {
            "patterns": [
                {
                    "pattern_id": "weak_1",
                    "description": "Weak",
                    "category": "preference",
                    "strength": "emerging",
                    "occurrences": 2,
                    "evidence": ["s1"]
                }
            ],
            "count": 1
        }
        patterns_file.write_text(json.dumps(patterns))

        # Create config
        config_file = Path(tmpdir) / ".claude" / "pms.local.md"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("---\n---\n")

        success = synthesize_rules(tmpdir, require_approval=False)
        assert success is False


def test_rule_file_markdown_format():
    """Test that generated rule files have correct markdown format"""
    with tempfile.TemporaryDirectory() as tmpdir:
        semantic_dir = Path(tmpdir) / ".claude" / "pms" / "semantic"
        semantic_dir.mkdir(parents=True)

        patterns_file = semantic_dir / "patterns.json"
        patterns = {
            "patterns": [
                {
                    "pattern_id": "p1",
                    "description": "Test pattern",
                    "category": "preference",
                    "strength": "strong",
                    "occurrences": 3,
                    "evidence": ["s1", "s2", "s3"]
                }
            ],
            "count": 1
        }
        patterns_file.write_text(json.dumps(patterns))

        config_file = Path(tmpdir) / ".claude" / "pms.local.md"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("---\n---\n")

        success = synthesize_rules(tmpdir, require_approval=False)
        assert success is True

        # Check markdown format
        rule_file = Path(tmpdir) / ".claude" / "rules" / "pms" / "user-preferences.md"
        content = rule_file.read_text()

        # Check header format
        assert content.startswith("# User Preferences")
        assert "<!-- Auto-generated" in content
        assert "## User Preferences" in content

        # Check pattern format
        assert "**" in content  # Bold rules
        assert "- Observed" in content  # Bullet points
        assert "- Evidence:" in content
