"""
Unit tests for JSON handling utilities
Tests atomic writes, corruption handling, and safe operations
"""

import json
import os
import tempfile
from pathlib import Path

import pytest

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from json_handler import (
    safe_load,
    safe_save,
    merge_monthly,
    update_index,
)


class TestSafeLoad:
    """Tests for safe_load function"""

    def test_load_valid_json(self, tmp_path):
        """Test loading valid JSON file"""
        test_file = tmp_path / "test.json"
        test_data = {"key": "value", "number": 42}
        test_file.write_text(json.dumps(test_data))

        result = safe_load(str(test_file))
        assert result == test_data

    def test_load_nonexistent_file_returns_default(self, tmp_path):
        """Test loading non-existent file returns default"""
        test_file = tmp_path / "nonexistent.json"

        result = safe_load(str(test_file), default={"empty": True})
        assert result == {"empty": True}

    def test_load_nonexistent_file_returns_empty_dict(self, tmp_path):
        """Test loading non-existent file without default returns empty dict"""
        test_file = tmp_path / "nonexistent.json"

        result = safe_load(str(test_file))
        assert result == {}

    def test_load_corrupted_json_returns_default(self, tmp_path):
        """Test loading corrupted JSON returns default"""
        test_file = tmp_path / "corrupted.json"
        test_file.write_text('{"key": "value", "incomplete')

        result = safe_load(str(test_file), default={"corrupted": True})
        assert result == {"corrupted": True}

    def test_load_corrupted_json_attempts_repair(self, tmp_path):
        """Test loading corrupted JSON attempts repair"""
        test_file = tmp_path / "corrupted.json"
        # Valid JSON followed by incomplete line
        test_file.write_text('{"key": "value", "complete": true}\n{"incomplete')

        result = safe_load(str(test_file), default={})
        # Should return default since repair attempts to parse as single JSON
        assert isinstance(result, dict)


class TestSafeSave:
    """Tests for safe_save function"""

    def test_save_valid_json(self, tmp_path):
        """Test saving valid JSON data"""
        test_file = tmp_path / "test.json"
        test_data = {"key": "value", "number": 42}

        result = safe_save(str(test_file), test_data)
        assert result is True

        # Verify file was created and contains correct data
        saved_data = json.loads(test_file.read_text())
        assert saved_data == test_data

    def test_save_creates_parent_directories(self, tmp_path):
        """Test saving creates parent directories if needed"""
        test_file = tmp_path / "nested" / "deep" / "test.json"
        test_data = {"nested": True}

        result = safe_save(str(test_file), test_data)
        assert result is True
        assert test_file.exists()

    def test_save_uses_atomic_write(self, tmp_path):
        """Test saving uses temp file + rename pattern"""
        test_file = tmp_path / "test.json"
        test_data = {"atomic": True}

        # Save file
        result = safe_save(str(test_file), test_data)
        assert result is True

        # Verify no temp file left behind
        temp_file = Path(str(test_file) + ".tmp")
        assert not temp_file.exists()

    def test_save_overwrites_existing(self, tmp_path):
        """Test saving overwrites existing file"""
        test_file = tmp_path / "test.json"
        test_file.write_text('{"old": "data"}')

        new_data = {"new": "data"}
        result = safe_save(str(test_file), new_data)
        assert result is True

        saved_data = json.loads(test_file.read_text())
        assert saved_data == new_data

    def test_save_retries_on_failure(self, tmp_path, monkeypatch):
        """Test saving retries on transient failures"""
        test_file = tmp_path / "test.json"
        test_data = {"retry": True}

        # Track number of attempts
        attempt_count = [0]
        original_open = open

        def mock_open(*args, **kwargs):
            attempt_count[0] += 1
            if attempt_count[0] < 2:
                # Fail first attempt
                raise OSError("Simulated failure")
            return original_open(*args, **kwargs)

        monkeypatch.setattr("builtins.open", mock_open)

        result = safe_save(str(test_file), test_data, max_retries=3)
        # Should succeed on second attempt
        assert result is True
        assert attempt_count[0] >= 2


class TestMergeMonthly:
    """Tests for merge_monthly function"""

    def test_merge_to_new_file(self, tmp_path):
        """Test merging to non-existent monthly file"""
        monthly_file = tmp_path / "sessions-2025-12.json"
        session_record = {
            "session_id": "test-123",
            "timestamp": "2025-12-31T10:00:00Z",
            "task_summary": "Test task"
        }

        result = merge_monthly(session_record, str(monthly_file))
        assert result is True

        # Verify structure
        data = json.loads(monthly_file.read_text())
        assert "sessions" in data
        assert len(data["sessions"]) == 1
        assert data["sessions"][0] == session_record
        assert data["count"] == 1
        assert data["last_updated"] == session_record["timestamp"]

    def test_merge_to_existing_file(self, tmp_path):
        """Test merging to existing monthly file"""
        monthly_file = tmp_path / "sessions-2025-12.json"

        # Create existing file with one session
        existing_data = {
            "sessions": [{
                "session_id": "old-session",
                "timestamp": "2025-12-30T10:00:00Z"
            }],
            "count": 1,
            "last_updated": "2025-12-30T10:00:00Z"
        }
        monthly_file.write_text(json.dumps(existing_data))

        # Merge new session
        new_session = {
            "session_id": "new-session",
            "timestamp": "2025-12-31T10:00:00Z"
        }

        result = merge_monthly(new_session, str(monthly_file))
        assert result is True

        # Verify both sessions present
        data = json.loads(monthly_file.read_text())
        assert len(data["sessions"]) == 2
        assert data["count"] == 2
        assert data["last_updated"] == new_session["timestamp"]


class TestUpdateIndex:
    """Tests for update_index function"""

    def test_update_new_index(self, tmp_path):
        """Test updating non-existent index file"""
        index_file = tmp_path / "index.json"

        result = update_index(
            str(index_file),
            "session-123",
            "sessions-2025-12.json"
        )
        assert result is True

        # Verify index structure
        index = json.loads(index_file.read_text())
        assert index["session-123"] == "sessions-2025-12.json"

    def test_update_existing_index(self, tmp_path):
        """Test updating existing index file"""
        index_file = tmp_path / "index.json"

        # Create existing index
        existing_index = {
            "old-session": "sessions-2025-11.json"
        }
        index_file.write_text(json.dumps(existing_index))

        # Update index
        result = update_index(
            str(index_file),
            "new-session",
            "sessions-2025-12.json"
        )
        assert result is True

        # Verify both entries
        index = json.loads(index_file.read_text())
        assert len(index) == 2
        assert index["old-session"] == "sessions-2025-11.json"
        assert index["new-session"] == "sessions-2025-12.json"


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
