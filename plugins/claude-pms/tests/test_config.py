"""
Unit tests for config.py
Tests configuration loading, validation, and defaults
"""

import os
import tempfile
from pathlib import Path

import pytest

from scripts.config import (
    PMSConfig,
    get_default_config,
    load_config,
    validate_config,
)


def test_get_default_config():
    """Test default configuration values"""
    config = get_default_config()

    assert config.trigger_precompact is True
    assert config.trigger_session_end is True
    assert config.trigger_stop is False
    assert config.continuous_mode is True
    assert config.auto_synthesize is False
    assert config.min_sessions == 10
    assert config.emerging_pattern == 2
    assert config.strong_pattern == 3
    assert config.critical_pattern == 5
    assert config.redact_sensitive is True


def test_load_config_missing_file():
    """Test loading config when file doesn't exist"""
    with tempfile.TemporaryDirectory() as tmpdir:
        config = load_config(tmpdir)
        # Should return defaults
        assert config.trigger_precompact is True
        assert config.min_sessions == 10


def test_load_config_valid_yaml():
    """Test loading config from valid YAML frontmatter"""
    with tempfile.TemporaryDirectory() as tmpdir:
        # Create .claude directory
        claude_dir = Path(tmpdir) / ".claude"
        claude_dir.mkdir()

        # Create config file with YAML frontmatter
        config_file = claude_dir / "pms.local.md"
        config_file.write_text("""---
triggers:
  precompact: false
  session_end: true
  stop: true

processing:
  continuous_mode: false
  auto_synthesize: true

thresholds:
  min_sessions: 20
  emerging_pattern: 3
  strong_pattern: 5
  critical_pattern: 10

encoding:
  prefer_context: false
  fallback_jsonl: true

privacy:
  redact_sensitive: false

timeouts:
  encode: 60
  extract: 120
  synthesize: 90
---

# Config content
""")

        config = load_config(tmpdir)

        # Verify parsed values
        assert config.trigger_precompact is False
        assert config.trigger_session_end is True
        assert config.trigger_stop is True
        assert config.continuous_mode is False
        assert config.auto_synthesize is True
        assert config.min_sessions == 20
        assert config.emerging_pattern == 3
        assert config.strong_pattern == 5
        assert config.critical_pattern == 10
        assert config.prefer_context is False
        assert config.fallback_jsonl is True
        assert config.redact_sensitive is False
        assert config.timeout_encode == 60
        assert config.timeout_extract == 120
        assert config.timeout_synthesize == 90


def test_load_config_invalid_yaml():
    """Test loading config with invalid/corrupted YAML"""
    with tempfile.TemporaryDirectory() as tmpdir:
        claude_dir = Path(tmpdir) / ".claude"
        claude_dir.mkdir()

        # Create config with invalid YAML
        config_file = claude_dir / "pms.local.md"
        config_file.write_text("""---
this is not valid YAML: [[[
---
""")

        config = load_config(tmpdir)

        # Should fall back to defaults
        assert config.trigger_precompact is True
        assert config.min_sessions == 10


def test_load_config_partial_yaml():
    """Test loading config with only some fields specified"""
    with tempfile.TemporaryDirectory() as tmpdir:
        claude_dir = Path(tmpdir) / ".claude"
        claude_dir.mkdir()

        # Create config with only some fields
        config_file = claude_dir / "pms.local.md"
        config_file.write_text("""---
triggers:
  precompact: false

thresholds:
  min_sessions: 15
---
""")

        config = load_config(tmpdir)

        # Specified values should be loaded
        assert config.trigger_precompact is False
        assert config.min_sessions == 15

        # Unspecified values should use defaults
        assert config.trigger_session_end is True
        assert config.continuous_mode is True
        assert config.emerging_pattern == 2


def test_validate_config_valid():
    """Test validation of valid configuration"""
    config = get_default_config()
    assert validate_config(config) is True


def test_validate_config_invalid_thresholds():
    """Test validation catches invalid threshold ordering"""
    config = get_default_config()
    config.emerging_pattern = 5
    config.strong_pattern = 3  # Out of order
    config.critical_pattern = 10

    assert validate_config(config) is False


def test_validate_config_invalid_timeouts():
    """Test validation catches invalid timeout values"""
    config = get_default_config()

    # Too small
    config.timeout_encode = 1
    assert validate_config(config) is False

    # Too large
    config.timeout_encode = 500
    assert validate_config(config) is False


def test_validate_config_invalid_min_sessions():
    """Test validation catches invalid min_sessions"""
    config = get_default_config()

    # Too small
    config.min_sessions = 0
    assert validate_config(config) is False

    # Too large
    config.min_sessions = 5000
    assert validate_config(config) is False


def test_config_clamping():
    """Test that out-of-range values are clamped"""
    with tempfile.TemporaryDirectory() as tmpdir:
        claude_dir = Path(tmpdir) / ".claude"
        claude_dir.mkdir()

        # Create config with out-of-range values
        config_file = claude_dir / "pms.local.md"
        config_file.write_text("""---
thresholds:
  min_sessions: 99999

timeouts:
  encode: 999
---
""")

        config = load_config(tmpdir)

        # Values should be clamped to valid ranges
        assert config.min_sessions <= 1000  # Clamped to max
        assert config.timeout_encode <= 300  # Clamped to max
