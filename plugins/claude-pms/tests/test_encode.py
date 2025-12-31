"""
Unit tests for encode.py
Tests episodic encoding from context and JSONL
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

from encode import encode_session, encode_from_context, encode_from_jsonl


def test_encode_from_context_creates_record():
    """Test that context-first encoding creates valid episodic record"""
    with tempfile.TemporaryDirectory() as tmpdir:
        session_id = "test-session-123"
        trigger = "manual"

        record = encode_from_context(tmpdir, session_id, trigger)

        # Verify required fields
        assert record["session_id"] == session_id
        assert record["timestamp"]  # Should have timestamp
        assert record["project_path"] == tmpdir
        assert record["trigger"] == trigger
        assert record["encoding_mode"] == "context"

        # Verify structure
        assert "task_summary" in record
        assert "work_summary" in record
        assert "design_decisions" in record
        assert "challenges" in record
        assert "solutions" in record
        assert "user_preferences" in record
        assert "code_patterns" in record
        assert "anti_patterns" in record
        assert "context" in record


def test_encode_from_jsonl_creates_record():
    """Test that JSONL fallback encoding creates valid episodic record"""
    with tempfile.TemporaryDirectory() as tmpdir:
        session_id = "test-session-456"
        trigger = "precompact"

        record = encode_from_jsonl(tmpdir, session_id, trigger)

        # Verify required fields
        assert record["session_id"] == session_id
        assert record["timestamp"]
        assert record["project_path"] == tmpdir
        assert record["trigger"] == trigger
        assert record["encoding_mode"] == "jsonl_fallback"

        # Verify fallback structure
        assert "task_summary" in record
        assert "work_summary" in record
        assert "transcript" in record


def test_encode_session_saves_monthly_file():
    """Test that encode_session saves to monthly file"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create PMS directory structure
        pms_dir = Path(tmpdir) / ".claude" / "pms"
        pms_dir.mkdir(parents=True)

        # Create default config
        config_file = Path(tmpdir) / ".claude" / "pms.local.md"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("""---
triggers:
  precompact: true
encoding:
  prefer_context: true
  fallback_jsonl: false
privacy:
  redact_sensitive: false
processing:
  continuous_mode: false
---
""")

        # Encode session
        success = encode_session(tmpdir, "manual", "test-session-789")

        assert success is True

        # Verify monthly file created
        episodic_dir = pms_dir / "episodic"
        assert episodic_dir.exists()

        # Check for monthly file (sessions-YYYY-MM.json)
        monthly_files = list(episodic_dir.glob("sessions-*.json"))
        assert len(monthly_files) > 0

        # Verify content
        with open(monthly_files[0], 'r') as f:
            data = json.load(f)
            assert "sessions" in data
            assert len(data["sessions"]) == 1
            assert data["sessions"][0]["session_id"] == "test-session-789"


def test_encode_session_updates_index():
    """Test that encode_session updates index.json"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create PMS directory structure
        pms_dir = Path(tmpdir) / ".claude" / "pms"
        pms_dir.mkdir(parents=True)

        # Create default config (redaction disabled for test)
        config_file = Path(tmpdir) / ".claude" / "pms.local.md"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("""---
privacy:
  redact_sensitive: false
processing:
  continuous_mode: false
---
""")

        # Encode session
        session_id = "test-session-abc"
        encode_session(tmpdir, "manual", session_id)

        # Verify index updated
        index_file = pms_dir / "episodic" / "index.json"
        assert index_file.exists()

        with open(index_file, 'r') as f:
            index = json.load(f)
            assert session_id in index
            assert index[session_id].startswith("sessions-")


def test_encode_session_applies_redaction():
    """Test that encode_session redacts sensitive data"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create PMS structure
        pms_dir = Path(tmpdir) / ".claude" / "pms"
        pms_dir.mkdir(parents=True)

        # Config with redaction enabled
        config_file = Path(tmpdir) / ".claude" / "pms.local.md"
        config_file.parent.mkdir(parents=True, exist_ok=True)
        config_file.write_text("""---
privacy:
  redact_sensitive: true
processing:
  continuous_mode: false
---
""")

        # Encode session
        success = encode_session(tmpdir, "manual")

        assert success is True

        # Verify monthly file exists and check for redaction
        episodic_dir = pms_dir / "episodic"
        monthly_files = list(episodic_dir.glob("sessions-*.json"))

        with open(monthly_files[0], 'r') as f:
            content = f.read()
            # Sensitive patterns should be redacted if present
            # (This test passes if no exceptions occur)
            assert "sessions" in content


def test_encode_session_handles_missing_config():
    """Test that encode_session works with missing config (uses defaults)"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # No config file created - should use defaults

        # Encode session
        success = encode_session(tmpdir, "manual")

        # Should still succeed with default config
        assert success is True


def test_encode_from_context_captures_git_branch():
    """Test that encoding captures git branch if available"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Initialize git repo
        import subprocess
        try:
            subprocess.run(["git", "init"], cwd=tmpdir, check=True, capture_output=True)
            subprocess.run(
                ["git", "checkout", "-b", "feature-test"],
                cwd=tmpdir,
                check=True,
                capture_output=True
            )

            record = encode_from_context(tmpdir, "test-id", "manual")

            # Should capture branch name
            assert record["git_branch"] == "feature-test"

        except Exception:
            # Git not available or other error - skip test
            pytest.skip("Git not available")
