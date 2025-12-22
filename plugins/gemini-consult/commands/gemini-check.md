---
name: jcmrs:gemini-check
description: Verify Google Gemini CLI installation and readiness
allowed-tools:
  - Bash
---

# Gemini Check Command

Diagnose Google Gemini CLI installation and configuration status.

## Purpose

Quickly verify that:
- Gemini CLI is installed
- Command is in PATH
- Version information is available
- System is ready for `/jcmrs:gemini-consult` usage

## Execution Protocol

### 1. Check CLI Availability

Test if `gemini` command exists:

```bash
which gemini || echo "NOT_FOUND"
```

**On Windows** (if which fails):
```bash
where gemini || echo "NOT_FOUND"
```

### 2. Get Version Information

If gemini is found, retrieve version:

```bash
gemini --version
```

**Expected output**: Version number (e.g., "1.0.0" or similar)

### 3. Test Basic Functionality

Run a minimal test query to verify gemini works:

```bash
gemini -p "test query" --help
```

**Purpose**: Verify gemini responds to commands without actually executing a query

### 4. Format Diagnostic Report

Present results in clear status format:

**If everything works**:

```markdown
✅ Gemini CLI Status: Ready

**Installation**
- Command: gemini
- Location: [path from which/where]
- Version: [version number]

**Functionality**
- Basic commands: ✅ Working
- Ready for queries: ✅ Yes

**Next Steps**
- Run queries with: /jcmrs:gemini-consult
- Example: /jcmrs:gemini-consult @src/ Analyze architecture
```

**If gemini not found**:

```markdown
❌ Gemini CLI Status: Not Installed

**Problem**
- gemini command not found in PATH

**Solution**
Install Google Gemini CLI:

1. Using npm:
   ```bash
   npm install -g @google/generative-ai
   ```

2. Verify installation:
   ```bash
   gemini --version
   ```

3. Authenticate (if needed):
   ```bash
   gemini auth login
   ```

4. Test with:
   ```bash
   /jcmrs:gemini-check
   ```

**Documentation**
- Installation guide: https://ai.google.dev/gemini-api/docs/cli
```

**If gemini found but errors**:

```markdown
⚠️ Gemini CLI Status: Installed but Issues Detected

**Installation**
- Command: gemini
- Location: [path]
- Version: [version or error]

**Issues**
- [Specific error from version check]

**Troubleshooting**
1. Verify installation:
   ```bash
   npm list -g @google/generative-ai
   ```

2. Reinstall if needed:
   ```bash
   npm install -g @google/generative-ai
   ```

3. Check authentication:
   ```bash
   gemini auth status
   ```

4. Test query:
   ```bash
   gemini -p "@README.md Summarize this file"
   ```

**Need Help?**
- Run diagnostics: /jcmrs:gemini-check
- Check installation docs: https://ai.google.dev/gemini-api/docs/cli
```

## Diagnostic Details

### PATH Check

Verify gemini is in system PATH:
- **macOS/Linux**: `which gemini`
- **Windows**: `where gemini`

**Expected**: Full path to gemini executable

### Version Verification

Check installed version:
```bash
gemini --version
```

**Purpose**: Confirms not only installation but that gemini binary works

### Authentication Status

Optionally check authentication (if gemini supports it):
```bash
gemini auth status
```

**Note**: Some gemini installations may not require auth or may handle it differently

## Common Issues & Solutions

### Issue: Command Not Found

**Symptom**: `gemini: command not found`

**Solutions**:
1. Install globally: `npm install -g @google/generative-ai`
2. Check npm global bin in PATH: `npm config get prefix`
3. Restart terminal after installation

### Issue: Permission Denied

**Symptom**: `Permission denied` when running gemini

**Solutions**:
1. Fix permissions: `chmod +x [gemini path]`
2. Reinstall with proper permissions: `sudo npm install -g @google/generative-ai`
3. Use npm without sudo: Configure npm prefix to user directory

### Issue: Wrong Version

**Symptom**: Old version installed

**Solutions**:
1. Update: `npm update -g @google/generative-ai`
2. Check version: `gemini --version`
3. Uninstall and reinstall if update fails

### Issue: Authentication Required

**Symptom**: Gemini asks for auth when running queries

**Solutions**:
1. Login: `gemini auth login`
2. Follow authentication prompts
3. Verify: `gemini auth status`

## Integration with Plugin

This diagnostic command helps troubleshoot:
- `/jcmrs:gemini-consult` failures
- Hook suggestion errors
- Setup verification for new users

**Recommended workflow**:
1. User installs plugin
2. Run `/jcmrs:gemini-check` to verify setup
3. Fix any issues identified
4. Proceed with `/jcmrs:gemini-consult` queries

## Quick Reference

```bash
# Check status
/jcmrs:gemini-check

# If issues, install
npm install -g @google/generative-ai

# Verify
gemini --version

# Test query
gemini -p "@README.md Summarize"

# Recheck
/jcmrs:gemini-check
```

## Exit Conditions

Command completes successfully when:
- ✅ Status report generated
- ✅ Installation state determined
- ✅ Clear next steps provided (if issues found)
- ✅ User knows whether they can use `/jcmrs:gemini-consult`

**Do not**:
- Attempt to install gemini automatically
- Modify user's PATH
- Change system configuration

**Only**: Report status and provide clear instructions
