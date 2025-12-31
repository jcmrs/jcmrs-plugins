"""
Unit tests for recovery utilities
Tests rebuild, backup, validation, and reset functions
"""

import json
import os
from pathlib import Path

import pytest

# Add parent directory to path for imports
import sys
sys.path.insert(0, str(Path(__file__).parent.parent / "scripts"))

from recovery import (
    rebuild_semantic,
    backup_corrupted,
    validate_memory_structure,
    reset_pms,
)
from json_handler import safe_save


class TestRebuildSemantic:
    """Tests for rebuild_semantic function"""

    def test_rebuild_from_episodic_records(self, tmp_path):
        """Test rebuilding semantic knowledge from episodic records"""
        # Create PMS directory structure
        pms_dir = tmp_path / ".claude" / "pms"
        episodic_dir = pms_dir / "episodic"
        semantic_dir = pms_dir / "semantic"
        episodic_dir.mkdir(parents=True)

        # Create sample episodic records
        session1 = {
            "session_id": "session-1",
            "timestamp": "2025-12-30T10:00:00Z",
            "user_preferences": ["Use JWT for auth"],
            "code_patterns": ["Middleware pattern"],
            "anti_patterns": []
        }
        session2 = {
            "session_id": "session-2",
            "timestamp": "2025-12-31T10:00:00Z",
            "user_preferences": ["Use JWT for auth"],  # Repeated
            "code_patterns": ["Repository pattern"],
            "anti_patterns": ["Avoid localStorage for tokens"]
        }

        monthly_file = episodic_dir / "sessions-2025-12.json"
        safe_save(
            str(monthly_file),
            {
                "sessions": [session1, session2],
                "count": 2,
                "last_updated": "2025-12-31T10:00:00Z"
            }
        )

        # Rebuild semantic knowledge
        result = rebuild_semantic(str(tmp_path))
        assert result is True

        # Verify semantic files created
        assert semantic_dir.exists()
        patterns_file = semantic_dir / "patterns.json"
        assert patterns_file.exists()

        # Verify patterns detected
        patterns_data = json.loads(patterns_file.read_text())
        assert "patterns" in patterns_data
        assert patterns_data["count"] > 0

    def test_rebuild_with_no_episodic_data(self, tmp_path):
        """Test rebuild with no episodic data returns error"""
        # Create empty PMS directory
        pms_dir = tmp_path / ".claude" / "pms"
        pms_dir.mkdir(parents=True)

        result = rebuild_semantic(str(tmp_path))
        assert result is False


class TestBackupCorrupted:
    """Tests for backup_corrupted function"""

    def test_backup_file_to_backup_directory(self, tmp_path):
        """Test backing up corrupted file"""
        # Create corrupted file
        corrupted_file = tmp_path / "corrupted.json"
        corrupted_file.write_text('{"incomplete')

        result = backup_corrupted(str(corrupted_file))
        assert result is True

        # Verify backup created
        backup_dir = tmp_path / ".backup"
        assert backup_dir.exists()

        # Verify backup file has timestamp in name (uses underscores)
        backup_files = list(backup_dir.glob("corrupted_*.json"))
        assert len(backup_files) == 1

        # Verify original file removed
        assert not corrupted_file.exists()

    def test_backup_nonexistent_file_returns_false(self, tmp_path):
        """Test backing up non-existent file returns false"""
        nonexistent_file = tmp_path / "nonexistent.json"

        result = backup_corrupted(str(nonexistent_file))
        assert result is False


class TestValidateMemoryStructure:
    """Tests for validate_memory_structure function"""

    def test_validate_valid_structure(self, tmp_path):
        """Test validating valid memory structure"""
        # Create valid PMS structure
        pms_dir = tmp_path / ".claude" / "pms"
        episodic_dir = pms_dir / "episodic"
        semantic_dir = pms_dir / "semantic"
        procedural_dir = pms_dir / "procedural"

        episodic_dir.mkdir(parents=True)
        semantic_dir.mkdir(parents=True)
        procedural_dir.mkdir(parents=True)

        # Create valid JSON files
        safe_save(
            str(episodic_dir / "sessions-2025-12.json"),
            {"sessions": [], "count": 0}
        )
        safe_save(
            str(episodic_dir / "index.json"),
            {}
        )
        safe_save(
            str(semantic_dir / "patterns.json"),
            {"patterns": [], "count": 0}
        )

        result, errors = validate_memory_structure(str(tmp_path))
        assert result is True
        assert len(errors) == 0

    def test_validate_corrupted_files(self, tmp_path):
        """Test validating structure with corrupted files"""
        # Create PMS structure with corrupted file
        pms_dir = tmp_path / ".claude" / "pms"
        episodic_dir = pms_dir / "episodic"
        episodic_dir.mkdir(parents=True)

        # Create corrupted JSON file
        corrupted_file = episodic_dir / "sessions-2025-12.json"
        corrupted_file.write_text('{"incomplete')

        result, errors = validate_memory_structure(str(tmp_path))
        assert result is False
        assert len(errors) > 0
        assert any("corrupted" in err.lower() or "invalid" in err.lower() for err in errors)

    def test_validate_missing_directories(self, tmp_path):
        """Test validating structure with missing directories"""
        # Create minimal structure
        pms_dir = tmp_path / ".claude" / "pms"
        pms_dir.mkdir(parents=True)

        result, errors = validate_memory_structure(str(tmp_path))
        # Missing directories is not fatal - structure can be rebuilt
        # But should note missing components
        assert isinstance(errors, list)


class TestResetPMS:
    """Tests for reset_pms function"""

    def test_reset_all_directories(self, tmp_path):
        """Test reset removes all PMS data"""
        # Create full PMS structure
        pms_dir = tmp_path / ".claude" / "pms"
        episodic_dir = pms_dir / "episodic"
        semantic_dir = pms_dir / "semantic"
        procedural_dir = pms_dir / "procedural"

        episodic_dir.mkdir(parents=True)
        semantic_dir.mkdir(parents=True)
        procedural_dir.mkdir(parents=True)

        # Create files
        (episodic_dir / "sessions-2025-12.json").write_text('{"sessions": []}')
        (semantic_dir / "patterns.json").write_text('{"patterns": []}')
        (procedural_dir / "rules-metadata.json").write_text('{}')

        # Reset without keeping episodic
        result = reset_pms(str(tmp_path), keep_episodic=False)
        assert result is True

        # Verify all directories removed
        assert not episodic_dir.exists()
        assert not semantic_dir.exists()
        assert not procedural_dir.exists()

    def test_reset_keep_episodic(self, tmp_path):
        """Test reset keeps episodic data when requested"""
        # Create full PMS structure
        pms_dir = tmp_path / ".claude" / "pms"
        episodic_dir = pms_dir / "episodic"
        semantic_dir = pms_dir / "semantic"
        procedural_dir = pms_dir / "procedural"

        episodic_dir.mkdir(parents=True)
        semantic_dir.mkdir(parents=True)
        procedural_dir.mkdir(parents=True)

        # Create files
        episodic_file = episodic_dir / "sessions-2025-12.json"
        episodic_file.write_text('{"sessions": [{"id": "test"}]}')
        (semantic_dir / "patterns.json").write_text('{"patterns": []}')
        (procedural_dir / "rules-metadata.json").write_text('{}')

        # Reset keeping episodic
        result = reset_pms(str(tmp_path), keep_episodic=True)
        assert result is True

        # Verify episodic preserved
        assert episodic_dir.exists()
        assert episodic_file.exists()
        content = json.loads(episodic_file.read_text())
        assert content["sessions"][0]["id"] == "test"

        # Verify semantic and procedural removed
        assert not semantic_dir.exists()
        assert not procedural_dir.exists()

    def test_reset_nonexistent_directory(self, tmp_path):
        """Test reset handles non-existent PMS directory"""
        result = reset_pms(str(tmp_path), keep_episodic=False)
        # Should return True even if directory doesn't exist
        assert result is True


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
