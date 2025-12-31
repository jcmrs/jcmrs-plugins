"""
Unit tests for extract.py
Tests semantic pattern extraction from episodic records
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

from extract import (
    extract_patterns,
    load_all_sessions,
    detect_frequency_patterns,
    extract_user_preferences,
    extract_code_patterns,
    extract_anti_patterns,
    categorize_strength,
    save_semantic_knowledge
)


def test_extract_patterns_insufficient_sessions():
    """Test that extraction fails with insufficient sessions"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create PMS structure with only 5 sessions (need 10)
        pms_dir = Path(tmpdir) / ".claude" / "pms"
        episodic_dir = pms_dir / "episodic"
        episodic_dir.mkdir(parents=True)

        # Create config with default min_sessions=10
        config_file = Path(tmpdir) / ".claude" / "pms.local.md"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("""---
thresholds:
  min_sessions: 10
---
""")

        # Create monthly file with only 5 sessions
        sessions_file = episodic_dir / "sessions-2025-12.json"
        sessions = {
            "sessions": [
                {"session_id": f"session-{i}", "user_preferences": ["test"]}
                for i in range(5)
            ]
        }
        sessions_file.write_text(json.dumps(sessions, indent=2))

        # Should fail due to insufficient sessions
        success = extract_patterns(tmpdir)
        assert success is False


def test_extract_patterns_creates_semantic_files():
    """Test that extraction creates semantic knowledge files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create PMS structure
        pms_dir = Path(tmpdir) / ".claude" / "pms"
        episodic_dir = pms_dir / "episodic"
        episodic_dir.mkdir(parents=True)

        # Create config
        config_file = Path(tmpdir) / ".claude" / "pms.local.md"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("""---
thresholds:
  min_sessions: 10
  emerging_pattern: 2
  strong_pattern: 3
  critical_pattern: 5
processing:
  continuous_mode: false
  auto_synthesize: false
---
""")

        # Create monthly file with 12 sessions
        sessions_file = episodic_dir / "sessions-2025-12.json"
        sessions = {
            "sessions": [
                {
                    "session_id": f"session-{i}",
                    "user_preferences": ["Always run tests before commits"],
                    "code_patterns": ["Use TDD workflow"],
                    "anti_patterns": ["Avoid mocking everything"]
                }
                for i in range(12)
            ]
        }
        sessions_file.write_text(json.dumps(sessions, indent=2))

        # Extract patterns
        success = extract_patterns(tmpdir)
        assert success is True

        # Verify semantic files created
        semantic_dir = pms_dir / "semantic"
        assert (semantic_dir / "patterns.json").exists()
        assert (semantic_dir / "preferences.json").exists()
        assert (semantic_dir / "code-patterns.json").exists()
        assert (semantic_dir / "anti-patterns.json").exists()


def test_load_all_sessions_from_multiple_files():
    """Test loading sessions from multiple monthly files"""
    with tempfile.TemporaryDirectory() as tmpdir:
        episodic_dir = Path(tmpdir)

        # Create two monthly files
        file1 = episodic_dir / "sessions-2025-11.json"
        file1.write_text(json.dumps({
            "sessions": [
                {"session_id": "session-1"},
                {"session_id": "session-2"}
            ]
        }))

        file2 = episodic_dir / "sessions-2025-12.json"
        file2.write_text(json.dumps({
            "sessions": [
                {"session_id": "session-3"},
                {"session_id": "session-4"}
            ]
        }))

        # Load all (returns tuple: sessions, corrupted_files)
        all_sessions, corrupted_files = load_all_sessions(episodic_dir)

        assert len(all_sessions) == 4
        assert all_sessions[0]["session_id"] == "session-1"
        assert all_sessions[3]["session_id"] == "session-4"
        assert len(corrupted_files) == 0  # No corrupted files


def test_categorize_strength():
    """Test pattern strength categorization"""
    # Test emerging (2+)
    assert categorize_strength(2, 2, 3, 5) == "emerging"

    # Test strong (3+)
    assert categorize_strength(3, 2, 3, 5) == "strong"
    assert categorize_strength(4, 2, 3, 5) == "strong"

    # Test critical (5+)
    assert categorize_strength(5, 2, 3, 5) == "critical"
    assert categorize_strength(10, 2, 3, 5) == "critical"

    # Test weak (below threshold)
    assert categorize_strength(1, 2, 3, 5) == "weak"


def test_extract_user_preferences():
    """Test user preference extraction"""
    sessions = [
        {
            "session_id": "session-1",
            "user_preferences": ["Always run tests", "Use type hints"]
        },
        {
            "session_id": "session-2",
            "user_preferences": ["Always run tests"]
        },
        {
            "session_id": "session-3",
            "user_preferences": ["Use type hints"]
        }
    ]

    prefs = extract_user_preferences(sessions)

    assert "Always run tests" in prefs
    assert len(prefs["Always run tests"]) == 2
    assert "session-1" in prefs["Always run tests"]
    assert "session-2" in prefs["Always run tests"]

    assert "Use type hints" in prefs
    assert len(prefs["Use type hints"]) == 2


def test_extract_code_patterns():
    """Test code pattern extraction"""
    sessions = [
        {
            "session_id": "session-1",
            "code_patterns": ["TDD workflow", "Atomic commits"]
        },
        {
            "session_id": "session-2",
            "code_patterns": ["TDD workflow"]
        }
    ]

    patterns = extract_code_patterns(sessions)

    assert "TDD workflow" in patterns
    assert len(patterns["TDD workflow"]) == 2

    assert "Atomic commits" in patterns
    assert len(patterns["Atomic commits"]) == 1


def test_extract_anti_patterns():
    """Test anti-pattern extraction"""
    sessions = [
        {
            "session_id": "session-1",
            "anti_patterns": ["Avoid god objects", "No global state"]
        },
        {
            "session_id": "session-2",
            "anti_patterns": ["Avoid god objects"]
        }
    ]

    anti = extract_anti_patterns(sessions)

    assert "Avoid god objects" in anti
    assert len(anti["Avoid god objects"]) == 2

    assert "No global state" in anti
    assert len(anti["No global state"]) == 1


def test_detect_frequency_patterns_filters_by_threshold():
    """Test that patterns below threshold are filtered out"""
    sessions = [
        {
            "session_id": "session-1",
            "user_preferences": ["Common preference"],
            "code_patterns": [],
            "anti_patterns": []
        },
        {
            "session_id": "session-2",
            "user_preferences": ["Common preference", "Rare preference"],
            "code_patterns": [],
            "anti_patterns": []
        },
        {
            "session_id": "session-3",
            "user_preferences": ["Common preference"],
            "code_patterns": [],
            "anti_patterns": []
        }
    ]

    # emerging_threshold = 2
    patterns = detect_frequency_patterns(sessions, emerging_threshold=2, strong_threshold=3, critical_threshold=5)

    # "Common preference" appears 3 times - should be included
    common_prefs = [p for p in patterns if p["description"] == "Common preference"]
    assert len(common_prefs) == 1
    assert common_prefs[0]["occurrences"] == 3

    # "Rare preference" appears 1 time - should be excluded
    rare_prefs = [p for p in patterns if p["description"] == "Rare preference"]
    assert len(rare_prefs) == 0


def test_detect_frequency_patterns_assigns_correct_strength():
    """Test that patterns are assigned correct strength levels"""
    sessions = [
        {
            "session_id": f"session-{i}",
            "user_preferences": ["Critical pattern"],  # Will appear 10 times
            "code_patterns": ["Strong pattern"] if i < 4 else [],  # Appears 4 times
            "anti_patterns": ["Emerging pattern"] if i < 2 else []  # Appears 2 times
        }
        for i in range(10)
    ]

    patterns = detect_frequency_patterns(sessions, emerging_threshold=2, strong_threshold=3, critical_threshold=5)

    # Critical pattern (10 occurrences)
    critical = [p for p in patterns if p["description"] == "Critical pattern"][0]
    assert critical["strength"] == "critical"
    assert critical["occurrences"] == 10

    # Strong pattern (4 occurrences)
    strong = [p for p in patterns if p["description"] == "Strong pattern"][0]
    assert strong["strength"] == "strong"
    assert strong["occurrences"] == 4

    # Emerging pattern (2 occurrences)
    emerging = [p for p in patterns if p["description"] == "Emerging pattern"][0]
    assert emerging["strength"] == "emerging"
    assert emerging["occurrences"] == 2


def test_save_semantic_knowledge():
    """Test semantic knowledge file creation"""
    with tempfile.TemporaryDirectory() as tmpdir:
        semantic_dir = Path(tmpdir)

        all_patterns = [
            {
                "pattern_id": "pref_1",
                "description": "Test preference",
                "category": "preference",
                "strength": "strong",
                "occurrences": 3,
                "evidence": ["s1", "s2", "s3"],
                "detected_at": "2025-12-31T00:00:00Z"
            },
            {
                "pattern_id": "code_1",
                "description": "Test code pattern",
                "category": "code_pattern",
                "strength": "emerging",
                "occurrences": 2,
                "evidence": ["s1", "s2"],
                "detected_at": "2025-12-31T00:00:00Z"
            }
        ]

        preferences = [all_patterns[0]]
        code_patterns = [all_patterns[1]]
        anti_patterns = []

        success = save_semantic_knowledge(semantic_dir, all_patterns, preferences, code_patterns, anti_patterns)
        assert success is True

        # Verify patterns.json
        patterns_file = semantic_dir / "patterns.json"
        assert patterns_file.exists()
        with open(patterns_file) as f:
            data = json.load(f)
            assert data["count"] == 2
            assert len(data["patterns"]) == 2

        # Verify preferences.json
        prefs_file = semantic_dir / "preferences.json"
        assert prefs_file.exists()
        with open(prefs_file) as f:
            data = json.load(f)
            assert data["count"] == 1
            assert len(data["preferences"]) == 1

        # Verify code-patterns.json
        code_file = semantic_dir / "code-patterns.json"
        assert code_file.exists()
        with open(code_file) as f:
            data = json.load(f)
            assert data["count"] == 1

        # Verify anti-patterns.json
        anti_file = semantic_dir / "anti-patterns.json"
        assert anti_file.exists()
        with open(anti_file) as f:
            data = json.load(f)
            assert data["count"] == 0


def test_extract_patterns_handles_dict_preferences():
    """Test extraction with dict-based preferences (not just strings)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        pms_dir = Path(tmpdir) / ".claude" / "pms"
        episodic_dir = pms_dir / "episodic"
        episodic_dir.mkdir(parents=True)

        # Create config
        config_file = Path(tmpdir) / ".claude" / "pms.local.md"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("""---
thresholds:
  min_sessions: 10
processing:
  continuous_mode: false
---
""")

        # Sessions with dict-based preferences
        sessions_file = episodic_dir / "sessions-2025-12.json"
        sessions = {
            "sessions": [
                {
                    "session_id": f"session-{i}",
                    "user_preferences": [
                        {"description": "Use TDD", "context": "testing"},
                        "String preference"
                    ],
                    "code_patterns": [],
                    "anti_patterns": []
                }
                for i in range(12)
            ]
        }
        sessions_file.write_text(json.dumps(sessions, indent=2))

        success = extract_patterns(tmpdir)
        assert success is True

        # Verify both types of preferences extracted
        semantic_dir = pms_dir / "semantic"
        with open(semantic_dir / "preferences.json") as f:
            data = json.load(f)
            descriptions = [p["description"] for p in data["preferences"]]
            assert "Use TDD" in descriptions
            assert "String preference" in descriptions
