---
name: semantic-config
description: Configure semantic validation sensitivity, interaction style, enabled domains, and custom user trigger words or phrases for personalized ambiguity detection
---

# Semantic Configuration Command

Configure semantic validation behavior, detection sensitivity, and custom user trigger phrases.

## Process

1. **Check for Existing Configuration**
   - Look for `.claude/semantic-linguist.local.md` in project
   - If exists, read current settings from YAML frontmatter
   - If not exists, use defaults

2. **Present Current Configuration**
   ```
   # Semantic Linguist Configuration

   **Current Settings:**

   ## Detection Sensitivity
   - **Threshold**: [current] (Options: low=50, medium=60, high=80)
   - **Meta-questions**: [enabled/disabled]
   - **Domain confusion**: [enabled/disabled]

   ## Interaction Style
   - **Mode**: [current] (conversational | explicit | minimal)
   - **Auto-validate**: [yes/no]

   ## Enabled Domains
   - **Autogen**: [✓/✗]
   - **Langroid**: [✓/✗]
   - **General**: [✓/✗]

   ## Custom User Triggers
   - [list of custom phrases]
   - (These are phrases unique to you that should trigger validation)

   ---

   What would you like to configure?
   1. Adjust sensitivity
   2. Change interaction style
   3. Enable/disable domains
   4. Add custom trigger phrases
   5. Reset to defaults
   6. View all settings
   ```

3. **Interactive Configuration**

   **Option 1: Adjust Sensitivity**
   ```
   ## Detection Sensitivity Settings

   **Confidence Threshold**:
   - Low (50): More detections, may include minor ambiguities
   - Medium (60): Balanced - catches significant ambiguities (default)
   - High (80): Only very ambiguous terms or meta-questions

   Current: [X]

   **Detection Categories** (enable/disable):
   - [ ] Meta-questions ("am I making sense?")
   - [ ] High-ambiguity terms ("make it talk", "we need an api")
   - [ ] Vague action verbs ("make it X", "do the thing")
   - [ ] Generic terms ("component", "service", "module")
   - [ ] Domain confusion (mixing framework terms)
   - [ ] Unclear references ("that", "it", "the thing")

   Which would you like to change?
   ```

   **Option 2: Interaction Style**
   ```
   ## Interaction Style

   **Conversational** (default):
   - Friendly, helpful tone
   - Presents options naturally
   - Minimal technical jargon
   - Good for: All users, especially non-technical

   **Explicit**:
   - Direct, structured responses
   - Clear numbered options
   - More technical precision
   - Good for: Technical users, rapid clarification

   **Minimal**:
   - Brief summaries only
   - Only triggers on high-confidence ambiguities
   - Assumes user prefers autonomy
   - Good for: Experienced users who know what they want

   Current: [X]

   **Auto-validate**: [yes/no]
   - If yes: Automatically analyze and clarify when ambiguity detected
   - If no: Detect but wait for user to request validation

   Select new style or keep current?
   ```

   **Option 3: Domain Selection**
   ```
   ## Enabled Domains

   Configure which frameworks to provide mappings for:

   - [ ] **Autogen** (multi-agent conversations, GroupChat, AssistantAgent)
   - [ ] **Langroid** (Task orchestration, ToolMessage, ChatAgent)
   - [ ] **General** (Cross-framework concepts, general AI patterns)

   Current selection: [X, Y]

   **Why disable a domain?**
   - Reduces noise if you only work with specific framework
   - Faster validation (fewer mappings to check)
   - Cleaner clarification suggestions

   **Recommendation**: Keep all enabled unless you exclusively use one framework.

   Which domains should be active?
   ```

   **Option 4: Custom Trigger Phrases**
   ```
   ## Custom User Triggers

   Add phrases that are unique to your communication style that should trigger validation.

   **Current custom triggers**:
   [list existing]

   **Why add custom triggers?**
   Different users have different quirks - phrases you use that might be ambiguous but aren't in the standard knowledge base.

   **Examples of good custom triggers**:
   - "hook it up" (could mean: connect systems, add event handler, integrate API)
   - "plug it in" (could mean: dependency injection, module import, literal plugin)
   - "wire everything together" (could mean: dependency wiring, event connections, integration)
   - Your unique jargon or shorthand

   **Add new trigger phrase**:
   Format: "phrase" → ambiguity_score (0.5-1.0) → categories → possible meanings

   Example:
   ```yaml
   "hook it up":
     score: 0.85
     categories: ["vague_action", "integration"]
     meanings:
       autogen: ["register_for_llm", "message routing"]
       langroid: ["Task connection", "agent chaining"]
       general: ["API integration", "event handler"]
   ```

   Enter custom phrase to add:
   ```

   **Option 5: Reset to Defaults**
   ```
   ## Reset to Defaults

   This will restore all settings to default values:
   - Threshold: 60 (medium)
   - Interaction: conversational
   - Domains: all enabled
   - Custom triggers: cleared

   **Your current custom triggers will be lost.**

   Are you sure? (yes/no)
   ```

   **Option 6: View All Settings**
   ```
   # Complete Semantic Linguist Configuration

   ## Detection
   - **Threshold**: [value]
   - **Meta-questions**: ✓
   - **High-ambiguity terms**: ✓
   - **Vague verbs**: ✓
   - **Generic terms**: ✓
   - **Domain confusion**: ✓
   - **Unclear references**: ✓

   ## Interaction
   - **Style**: conversational
   - **Auto-validate**: yes

   ## Domains
   - **Autogen**: ✓
   - **Langroid**: ✓
   - **General**: ✓

   ## Custom Triggers ([count])
   [detailed list with scores and meanings]

   ## Storage Location
   `.claude/semantic-linguist.local.md`

   (This file is git-ignored by default)
   ```

4. **Save Configuration**

   Write settings to `.claude/semantic-linguist.local.md`:
   ```markdown
   ---
   # Semantic Linguist Configuration
   # Do not commit this file - it contains user-specific settings

   detection:
     threshold: 60
     categories:
       meta_questions: true
       high_ambiguity: true
       vague_verbs: true
       generic_terms: true
       domain_confusion: true
       unclear_refs: true

   interaction:
     style: conversational  # conversational | explicit | minimal
     auto_validate: true

   domains:
     autogen: true
     langroid: true
     general: true

   custom_triggers:
     "hook it up":
       score: 0.85
       categories: ["vague_action", "integration"]
       meanings:
         autogen: ["register_for_llm", "message routing"]
         langroid: ["Task connection", "agent chaining"]
         general: ["API integration", "event handler"]
   ---

   # Semantic Linguist User Configuration

   This file stores your personal semantic validation preferences.

   ## How to Edit

   1. Run `/semantic-config` to use interactive configuration
   2. Or edit YAML frontmatter directly above
   3. Changes take effect immediately

   ## Custom Triggers Format

   Add your unique phrases that should trigger validation:

   ```yaml
   "your phrase here":
     score: 0.5-1.0  # How ambiguous (0.5=moderate, 1.0=very ambiguous)
     categories: [list of categories]
     meanings:
       framework: [list of possible meanings]
   ```

   ## Need Help?

   Run `/validate-terminology` to see how current settings affect detection.
   ```

5. **Confirm Changes**
   ```
   ✅ Configuration saved to `.claude/semantic-linguist.local.md`

   **New settings**:
   - [summary of changes]

   Changes are active immediately. Run `/validate-terminology` to test new settings.

   **Next steps**:
   - Test with recent conversation: `/validate-terminology`
   - View domain mappings: `/map-domain`
   - Continue working with new validation settings
   ```

## Usage Examples

**Interactive configuration:**
```
/semantic-config
```

**Quick threshold adjustment:**
```
/semantic-config threshold high
```

**Add custom trigger:**
```
/semantic-config add-trigger "wire it up"
```

**View current settings:**
```
/semantic-config show
```

**Reset to defaults:**
```
/semantic-config reset
```

## Configuration File

Settings stored in: `.claude/semantic-linguist.local.md`

**Format**: Markdown with YAML frontmatter
**Scope**: Project-specific (each project can have different settings)
**Version control**: Automatically added to `.gitignore`

## Default Values

```yaml
detection:
  threshold: 60
  categories:
    meta_questions: true
    high_ambiguity: true
    vague_verbs: true
    generic_terms: true
    domain_confusion: true
    unclear_refs: true

interaction:
  style: conversational
  auto_validate: true

domains:
  autogen: true
  langroid: true
  general: true

custom_triggers: {}
```

## Important Principles

- **User-specific**: Each user has unique communication patterns
- **Project-scoped**: Different projects may need different settings
- **Git-safe**: Configuration file is git-ignored by default
- **Immediately active**: No restart required
- **Reversible**: Can always reset to defaults
- **Transparent**: View all settings at any time

## Integration

- UserPromptSubmit hook reads these settings
- Detection threshold affects confidence scoring
- Custom triggers added to ambiguous-terms.json logic
- Domain selection filters mapping results
- Interaction style affects response formatting

## Advanced: Direct Editing

Power users can edit `.claude/semantic-linguist.local.md` directly:

1. Open file in editor
2. Modify YAML frontmatter
3. Save file
4. Changes apply immediately

Validate syntax with `/semantic-config validate`.
