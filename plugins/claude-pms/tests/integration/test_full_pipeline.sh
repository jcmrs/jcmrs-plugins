#!/bin/bash
#
# Integration test for full PMS pipeline
# Tests: Encode → Extract → Synthesize workflow
#

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Get script directory
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
PLUGIN_DIR="$( cd "$SCRIPT_DIR/../.." && pwd )"
SCRIPTS_DIR="$PLUGIN_DIR/scripts"

# Test project directory
TEST_PROJECT="/tmp/claude-pms-test-$$"

echo -e "${YELLOW}=== Claude PMS Full Pipeline Integration Test ===${NC}"
echo "Test project: $TEST_PROJECT"
echo ""

# Clean up function
cleanup() {
    echo -e "${YELLOW}Cleaning up test directory...${NC}"
    rm -rf "$TEST_PROJECT"
}

# Set trap to cleanup on exit
trap cleanup EXIT

# Step 1: Create test project structure
echo -e "${GREEN}Step 1: Creating test project structure${NC}"
mkdir -p "$TEST_PROJECT/.claude/pms"
cd "$TEST_PROJECT"

# Step 2: Create test configuration
echo -e "${GREEN}Step 2: Creating test configuration${NC}"
cat > .claude/pms.local.md << 'EOF'
---
triggers:
  precompact: true
  session_end: true
  stop: false
  session_start: false

thresholds:
  min_sessions: 3  # Low threshold for testing
  emerging_pattern: 2
  strong_pattern: 3
  critical_pattern: 5

privacy:
  redact_sensitive: true
  custom_redaction_patterns: []

encoding:
  prefer_context: false  # Use JSONL for testing
  fallback_jsonl: true

extraction:
  auto_extract: false
  continuous_mode: false

synthesis:
  auto_synthesize: false
  require_approval: false  # Auto-approve for testing
---
EOF

# Step 3: Create mock JSONL transcripts for multiple sessions
echo -e "${GREEN}Step 3: Creating mock session transcripts${NC}"
mkdir -p "$TEST_PROJECT/.claude/projects/test-project/transcripts"

# Session 1
cat > "$TEST_PROJECT/.claude/projects/test-project/transcripts/session-1.jsonl" << 'EOF'
{"type":"user_message","timestamp":"2025-12-30T10:00:00Z","content":"Implement JWT authentication"}
{"type":"tool_use","timestamp":"2025-12-30T10:01:00Z","tool_name":"Write","tool_input":{"file_path":"auth.py"}}
{"type":"assistant_message","timestamp":"2025-12-30T10:02:00Z","content":"Implemented JWT auth with HTTPOnly cookies"}
EOF

# Session 2
cat > "$TEST_PROJECT/.claude/projects/test-project/transcripts/session-2.jsonl" << 'EOF'
{"type":"user_message","timestamp":"2025-12-30T11:00:00Z","content":"Add refresh token endpoint"}
{"type":"tool_use","timestamp":"2025-12-30T11:01:00Z","tool_name":"Edit","tool_input":{"file_path":"auth.py"}}
{"type":"assistant_message","timestamp":"2025-12-30T11:02:00Z","content":"Added refresh token using same HTTPOnly cookie pattern"}
EOF

# Session 3
cat > "$TEST_PROJECT/.claude/projects/test-project/transcripts/session-3.jsonl" << 'EOF'
{"type":"user_message","timestamp":"2025-12-30T12:00:00Z","content":"Implement middleware for auth validation"}
{"type":"tool_use","timestamp":"2025-12-30T12:01:00Z","tool_name":"Write","tool_input":{"file_path":"middleware.py"}}
{"type":"assistant_message","timestamp":"2025-12-30T12:02:00Z","content":"Created middleware pattern for auth, used HTTPOnly cookies again"}
EOF

# Session 4
cat > "$TEST_PROJECT/.claude/projects/test-project/transcripts/session-4.jsonl" << 'EOF'
{"type":"user_message","timestamp":"2025-12-30T13:00:00Z","content":"Add user repository"}
{"type":"tool_use","timestamp":"2025-12-30T13:01:00Z","tool_name":"Write","tool_input":{"file_path":"repository.py"}}
{"type":"assistant_message","timestamp":"2025-12-30T13:02:00Z","content":"Implemented repository pattern for user data"}
EOF

# Step 4: Run episodic encoding for each session
echo -e "${GREEN}Step 4: Running episodic encoding (4 sessions)${NC}"
for i in 1 2 3 4; do
    python "$SCRIPTS_DIR/encode.py" \
        --project-path "$TEST_PROJECT" \
        --trigger "manual" \
        --session-id "session-$i" || {
        echo -e "${RED}FAILED: Encoding session $i${NC}"
        exit 1
    }
    echo "  Encoded session $i"
done

# Verify episodic files created
echo -e "${YELLOW}Verifying episodic files...${NC}"
EPISODIC_DIR="$TEST_PROJECT/.claude/pms/episodic"
if [ ! -d "$EPISODIC_DIR" ]; then
    echo -e "${RED}FAILED: Episodic directory not created${NC}"
    exit 1
fi

MONTHLY_FILE=$(ls "$EPISODIC_DIR"/sessions-*.json 2>/dev/null | head -n 1)
if [ -z "$MONTHLY_FILE" ]; then
    echo -e "${RED}FAILED: No monthly session file created${NC}"
    exit 1
fi

# Check session count (use basename to get relative path)
MONTHLY_BASENAME=$(basename "$MONTHLY_FILE")
SESSION_COUNT=$(python -c "import json, sys; data = json.load(open('.claude/pms/episodic/$MONTHLY_BASENAME')); print(len(data.get('sessions', [])))")
if [ "$SESSION_COUNT" -ne 4 ]; then
    echo -e "${RED}FAILED: Expected 4 sessions, found $SESSION_COUNT${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ 4 episodic records created${NC}"

# Verify index file
if [ ! -f "$EPISODIC_DIR/index.json" ]; then
    echo -e "${RED}FAILED: Index file not created${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ Index file created${NC}"

# Step 4.5: Populate pattern data in episodic records
# Note: JSONL encoding doesn't extract patterns, so we manually add them for testing
echo -e "${GREEN}Step 4.5: Populating pattern data in episodic records${NC}"
python -c "
import json

# Read the monthly file
with open('.claude/pms/episodic/$MONTHLY_BASENAME', 'r') as f:
    data = json.load(f)

# Add patterns to each session
for i, session in enumerate(data['sessions'], 1):
    if i == 1:
        session['user_preferences'] = ['Use HTTPOnly cookies for auth']
        session['code_patterns'] = ['JWT authentication pattern']
        session['anti_patterns'] = []
    elif i == 2:
        session['user_preferences'] = ['Use HTTPOnly cookies for auth']
        session['code_patterns'] = ['Token refresh pattern']
        session['anti_patterns'] = []
    elif i == 3:
        session['user_preferences'] = ['Use HTTPOnly cookies for auth']
        session['code_patterns'] = ['Middleware pattern', 'JWT authentication pattern']
        session['anti_patterns'] = []
    elif i == 4:
        session['user_preferences'] = []
        session['code_patterns'] = ['Repository pattern']
        session['anti_patterns'] = ['Avoid exposing sensitive data']

# Save back
with open('.claude/pms/episodic/$MONTHLY_BASENAME', 'w') as f:
    json.dump(data, f, indent=2)

print('  ✓ Added pattern data to episodic records')
"
if [ $? -ne 0 ]; then
    echo -e "${RED}FAILED: Could not populate pattern data${NC}"
    exit 1
fi

# Step 5: Run semantic extraction
echo -e "${GREEN}Step 5: Running semantic extraction${NC}"
python "$SCRIPTS_DIR/extract.py" \
    --project-path "$TEST_PROJECT" \
    --min-sessions 3 || {
    echo -e "${RED}FAILED: Semantic extraction${NC}"
    exit 1
}

# Verify semantic files created
echo -e "${YELLOW}Verifying semantic files...${NC}"
SEMANTIC_DIR="$TEST_PROJECT/.claude/pms/semantic"
if [ ! -d "$SEMANTIC_DIR" ]; then
    echo -e "${RED}FAILED: Semantic directory not created${NC}"
    exit 1
fi

if [ ! -f "$SEMANTIC_DIR/patterns.json" ]; then
    echo -e "${RED}FAILED: Patterns file not created${NC}"
    exit 1
fi

# Check pattern count (use relative path)
PATTERN_COUNT=$(python -c "import json; data = json.load(open('.claude/pms/semantic/patterns.json')); print(data.get('count', 0))")
if [ "$PATTERN_COUNT" -eq 0 ]; then
    echo -e "${RED}FAILED: No patterns detected${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ $PATTERN_COUNT patterns detected${NC}"

# Step 6: Run procedural synthesis
echo -e "${GREEN}Step 6: Running procedural synthesis${NC}"
python "$SCRIPTS_DIR/synthesize.py" \
    --project-path "$TEST_PROJECT" \
    --auto-approve || {
    echo -e "${RED}FAILED: Procedural synthesis${NC}"
    exit 1
}

# Verify rule files created
echo -e "${YELLOW}Verifying rule files...${NC}"
RULES_DIR="$TEST_PROJECT/.claude/rules/pms"
if [ ! -d "$RULES_DIR" ]; then
    echo -e "${RED}FAILED: Rules directory not created${NC}"
    exit 1
fi

# Check for at least one rule file
RULE_FILES=$(ls "$RULES_DIR"/*.md 2>/dev/null | wc -l)
if [ "$RULE_FILES" -eq 0 ]; then
    echo -e "${RED}FAILED: No rule files generated${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ $RULE_FILES rule file(s) generated${NC}"

# Verify procedural metadata
PROCEDURAL_DIR="$TEST_PROJECT/.claude/pms/procedural"
if [ ! -f "$PROCEDURAL_DIR/rules-metadata.json" ]; then
    echo -e "${RED}FAILED: Rules metadata not created${NC}"
    exit 1
fi
echo -e "${GREEN}  ✓ Procedural metadata created${NC}"

# Step 7: Validate JSON schemas
echo -e "${GREEN}Step 7: Validating JSON schemas${NC}"

# Validate episodic schema (use relative path)
python -c "
import json
import sys

with open('.claude/pms/episodic/$MONTHLY_BASENAME') as f:
    data = json.load(f)

# Check required fields
if 'sessions' not in data:
    print('Missing sessions array')
    sys.exit(1)
if 'count' not in data:
    print('Missing count field')
    sys.exit(1)

# Check session structure
for session in data['sessions']:
    required = ['session_id', 'timestamp', 'project_path']
    for field in required:
        if field not in session:
            print(f'Session missing {field}')
            sys.exit(1)

print('Episodic schema valid')
" || {
    echo -e "${RED}FAILED: Episodic schema validation${NC}"
    exit 1
}
echo -e "${GREEN}  ✓ Episodic schema valid${NC}"

# Validate semantic schema (use relative path)
python -c "
import json
import sys

with open('.claude/pms/semantic/patterns.json') as f:
    data = json.load(f)

# Check required fields
if 'patterns' not in data:
    print('Missing patterns array')
    sys.exit(1)

# Check pattern structure
for pattern in data['patterns']:
    required = ['pattern_id', 'description', 'category', 'strength', 'occurrences', 'evidence']
    for field in required:
        if field not in pattern:
            print(f'Pattern missing {field}')
            sys.exit(1)

print('Semantic schema valid')
" || {
    echo -e "${RED}FAILED: Semantic schema validation${NC}"
    exit 1
}
echo -e "${GREEN}  ✓ Semantic schema valid${NC}"

# Step 8: Test recovery utilities
echo -e "${GREEN}Step 8: Testing recovery utilities${NC}"

# Test validation (use current directory)
PYTHONPATH="$SCRIPTS_DIR" python -c "
import sys
import os
from recovery import validate_memory_structure

result, errors = validate_memory_structure(os.getcwd())
if not result:
    print('Validation errors:', errors)
    sys.exit(1)
print('Memory structure valid')
" || {
    echo -e "${RED}FAILED: Memory structure validation${NC}"
    exit 1
}
echo -e "${GREEN}  ✓ Memory structure validated${NC}"

# All tests passed
echo ""
echo -e "${GREEN}=== ALL INTEGRATION TESTS PASSED ===${NC}"
echo ""
echo "Summary:"
echo "  - 4 sessions encoded"
echo "  - $PATTERN_COUNT patterns detected"
echo "  - $RULE_FILES rule file(s) generated"
echo "  - All JSON schemas valid"
echo "  - Memory structure validated"
echo ""

exit 0
