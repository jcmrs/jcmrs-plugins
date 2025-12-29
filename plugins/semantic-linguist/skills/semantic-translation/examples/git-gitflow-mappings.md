# Git/Gitflow-Specific Ambiguity Resolutions

Real-world examples of ambiguous user requests mapped to precise Git and Gitflow workflow implementations.

## Overview

Git is version control software, and Gitflow is a branching workflow strategy. Key concepts include:
- **Branch types** (Gitflow): feature/, release/, hotfix/, develop, main
- **Merge strategies**: merge commit (preserves history), squash merge (single commit), rebase (linear history)
- **Workflows**: Gitflow (structured), GitHub flow (simpler), GitLab flow (environment-based)
- **Operations**: commit, push, pull, merge, rebase, cherry-pick

Common ambiguities arise when users use general terms like "merge", "branch", "commit", or "workflow" without specifying strategy or context.

---

## Example 1: "merge my branch"

### User Request
```
"I need to merge my feature branch into main"
```

### Ambiguity Detected
- "merge" - three different merge strategies with different outcomes
- Need to clarify which merge strategy to use

### Semantic Validation Process

**Step 1: Domain Identified**
- User working with Git/Gitflow
- Needs to integrate feature branch into main

**Step 2: Query Knowledge**
- Three merge strategies: merge commit, squash merge, rebase
- Each has different history preservation and commit structure

**Step 3: Present Options**
```
Git offers three merge strategies with different outcomes:

1. **Merge Commit** (preserves full history)
   - Creates merge commit joining two branches
   - All feature branch commits visible in history
   - Command: git merge feature-branch
   - Result: Non-linear history with merge commit
   - Use case: Want to preserve detailed development history
   - Example history: A-B-C (main) → D-E-F (feature) → G (merge commit)

2. **Squash Merge** (combines into single commit)
   - Condenses all feature commits into one commit on main
   - Command: git merge --squash feature-branch && git commit
   - Result: Linear history, single commit for entire feature
   - Use case: Clean history, feature as atomic unit
   - Example history: A-B-C → D (single commit with all feature changes)

3. **Rebase and Merge** (linear history)
   - Replays feature commits on top of main
   - Command: git rebase main && git merge feature-branch (fast-forward)
   - Result: Linear history, all feature commits preserved
   - Use case: Linear history with detailed development steps
   - Example history: A-B-C → D'-E'-F' (feature commits rebased on C)

Which history structure do you need for your project?"
```

**Step 4: User Clarifies**
```
User: "We want to see all development commits but keep history clean"
```

**Step 5: Validated Translation**
```
"That's rebase and merge (linear history)! Here's the workflow:

**1. Update main and feature branches:**
```bash
# Switch to main and get latest
git checkout main
git pull origin main

# Switch to feature branch
git checkout feature/user-authentication
git pull origin feature/user-authentication
```

**2. Rebase feature onto main:**
```bash
# Replay feature commits on top of updated main
git rebase main

# If conflicts occur:
# 1. Resolve conflicts in files
# 2. git add <resolved-files>
# 3. git rebase --continue
# 4. Repeat until rebase complete

# Result: Feature commits now based on latest main
```

**3. Merge (fast-forward):**
```bash
# Switch to main
git checkout main

# Fast-forward merge (no merge commit needed)
git merge feature/user-authentication

# Should show: "Fast-forward" (linear history maintained)
```

**4. Push and cleanup:**
```bash
# Push updated main
git push origin main

# Delete feature branch
git branch -d feature/user-authentication
git push origin --delete feature/user-authentication
```

**Result:**
- Linear history on main: A-B-C-D-E-F (all commits from feature visible)
- No merge commit (fast-forward)
- Easy to follow development sequence
- Each commit in feature preserved with context

**Before:**
```
main:    A---B---C
               \
feature:         D---E---F
```

**After:**
```
main:    A---B---C---D---E---F (linear, all commits visible)
```

**When NOT to use:**
- Public branches already pushed (rebase rewrites history)
- Want merge commit to mark feature completion
- Team prefers atomic feature commits (use squash instead)"
```

---

## Example 2: "create a branch"

### User Request
```
"I need to create a branch for the new login feature"
```

### Ambiguity Detected
- "branch" - in Gitflow, branch type determines naming and merge target
- Need to clarify if this is feature, release, hotfix, or general branch

### Semantic Validation Process

**Step 1: Analyze Context**
```
Gitflow defines specific branch types with conventions:

1. **Feature Branch** (new functionality)
   - Naming: feature/<feature-name>
   - Branched from: develop
   - Merged into: develop
   - Use case: New features during development
   - Example: feature/user-login, feature/payment-integration

2. **Release Branch** (preparing for production release)
   - Naming: release/<version>
   - Branched from: develop
   - Merged into: main AND develop
   - Use case: Final testing, bug fixes before release
   - Example: release/1.2.0, release/v2.0.0

3. **Hotfix Branch** (urgent production fixes)
   - Naming: hotfix/<issue>
   - Branched from: main
   - Merged into: main AND develop
   - Use case: Critical bugs in production
   - Example: hotfix/security-vulnerability, hotfix/payment-bug

4. **General Branch** (not following Gitflow)
   - Naming: Any name
   - Branched from: Any branch
   - Merged into: Any branch
   - Use case: Simple projects not using Gitflow

Your "login feature" sounds like new functionality. Is this:"
- **Feature branch** (develop → feature/login → develop)
- **Hotfix** (urgent fix for broken login in production)
- **Something else**
```

**Step 2: User Clarifies**
```
User: "New feature being developed, not urgent fix"
```

**Step 3: Validated Translation**
```
"That's a Gitflow feature branch! Here's the proper workflow:

**1. Create feature branch from develop:**
```bash
# Ensure develop is up to date
git checkout develop
git pull origin develop

# Create and switch to feature branch
git checkout -b feature/user-login

# Push to remote (optional, for collaboration)
git push -u origin feature/user-login
```

**2. Develop feature with regular commits:**
```bash
# Make changes
git add src/auth/login.py
git commit -m "feat: add login endpoint"

git add src/auth/session.py
git commit -m "feat: implement session management"

git add tests/test_login.py
git commit -m "test: add login endpoint tests"

# Push commits
git push origin feature/user-login
```

**3. Keep feature branch updated with develop:**
```bash
# Periodically sync with develop to avoid large merge conflicts
git checkout develop
git pull origin develop

git checkout feature/user-login
git merge develop  # or git rebase develop for linear history

# Resolve any conflicts
git push origin feature/user-login
```

**4. Complete feature - merge back to develop:**
```bash
# Option A: Merge commit (preserves feature branch history)
git checkout develop
git pull origin develop
git merge --no-ff feature/user-login  # --no-ff creates merge commit
git push origin develop

# Option B: Squash merge (single commit for feature)
git checkout develop
git pull origin develop
git merge --squash feature/user-login
git commit -m "feat: add user login functionality"
git push origin develop

# Delete feature branch
git branch -d feature/user-login
git push origin --delete feature/user-login
```

**Gitflow branch structure:**
```
main (production)
  |
  └─── hotfix/... (urgent fixes) → merge to main + develop
  |
develop (integration)
  |
  ├─── feature/user-login (new features) → merge to develop
  ├─── feature/payments
  └─── release/1.2.0 (release prep) → merge to main + develop
```

**Naming conventions:**
- feature/descriptive-name (kebab-case)
- Examples: feature/oauth-integration, feature/csv-export, feature/dark-mode"
```

---

## Example 3: "use gitflow for our project"

### User Request
```
"Should we use Gitflow or something simpler?"
```

### Ambiguity Detected
- "Gitflow" vs other workflows (GitHub flow, GitLab flow, trunk-based)
- Need to clarify project needs to recommend workflow

### Semantic Validation Process

**Step 1: Present Workflow Options**
```
Three main Git workflows, each for different project types:

1. **Gitflow** (structured, multiple parallel versions)
   - Branches: main, develop, feature/, release/, hotfix/
   - Best for: Products with scheduled releases, multiple versions in production
   - Example: Desktop software with v1.0, v2.0, v2.1 supported simultaneously
   - Pros: Structured, supports hotfixes, clear release process
   - Cons: Complex, overhead for simple projects

2. **GitHub Flow** (simple, continuous deployment)
   - Branches: main, feature/* (only)
   - Best for: Web apps with continuous deployment, single production version
   - Example: SaaS application deployed from main constantly
   - Pros: Simple, fast, encourages small changes
   - Cons: No release branches, harder to manage versions

3. **GitLab Flow** (environment branches)
   - Branches: main, production, pre-production, feature/*
   - Best for: Apps with staging environments, controlled production
   - Example: API with dev → staging → production pipeline
   - Pros: Environment-based deployments, structured but simpler than Gitflow
   - Cons: More complex than GitHub flow

What's your deployment model?"
- Multiple versions in production at once → **Gitflow**
- Continuous deployment to single production → **GitHub Flow**
- Environment-based deployments (dev/staging/prod) → **GitLab Flow**
```

**Step 2: User Clarifies**
```
User: "We deploy to production continuously from main, no scheduled releases"
```

**Step 3: Validated Translation**
```
"That's GitHub Flow - perfect for continuous deployment! Here's how it works:

**GitHub Flow Workflow:**

**1. Branch structure (simple):**
```
main (production - always deployable)
  |
  ├─── feature/add-search
  ├─── fix/payment-bug
  └─── enhance/ui-polish
```

**2. Feature development:**
```bash
# Create feature branch from main
git checkout main
git pull origin main
git checkout -b feature/add-search

# Develop and commit
git add src/search.py
git commit -m "Add search functionality"

# Push frequently (collaboration + backup)
git push origin feature/add-search
```

**3. Pull Request (code review):**
```bash
# Open PR on GitHub: feature/add-search → main
# Team reviews code
# CI runs tests automatically
# Must pass checks before merge
```

**4. Merge to main (triggers deployment):**
```bash
# After PR approval, merge to main (GitHub UI or command line)
git checkout main
git pull origin main
git merge feature/add-search
git push origin main

# Automatic deployment triggers (CI/CD)
# Feature goes live immediately
```

**5. Cleanup:**
```bash
# Delete merged branch
git branch -d feature/add-search
git push origin --delete feature/add-search
```

**GitHub Flow principles:**
- main is always deployable (protected branch)
- All changes via short-lived feature branches
- Pull Requests for code review
- Merge to main = deploy to production
- No develop, release, or hotfix branches

**When to use:**
- ✅ Continuous deployment
- ✅ Single production environment
- ✅ Fast iteration
- ✅ Small, frequent releases

**When NOT to use:**
- ❌ Need to support multiple production versions
- ❌ Scheduled release cycles
- ❌ Long-running release branches
- → Use Gitflow instead"
```

---

## Example 4: "fix commit history"

### User Request
```
"I need to fix my last few commits before merging"
```

### Ambiguity Detected
- "fix commits" - could mean interactive rebase, amend, or reset
- Need to understand what needs fixing

### Semantic Validation Process

**Step 1: Clarify What to Fix**
```
"Fixing commit history" has different approaches:

1. **Amend Last Commit** (change most recent commit)
   - Fix commit message typo
   - Add forgotten files to last commit
   - Command: git commit --amend
   - Affects: Only most recent commit

2. **Interactive Rebase** (edit multiple commits)
   - Rewrite commit messages
   - Squash commits together
   - Reorder commits
   - Split commits
   - Command: git rebase -i HEAD~N
   - Affects: Last N commits

3. **Reset** (undo commits, keep changes)
   - Remove commits but keep file changes
   - Command: git reset --soft HEAD~N
   - Affects: Removes N commits, stages changes

What do you need to fix:
- Change last commit message/content → **Amend**
- Combine/reorder/edit multiple commits → **Interactive Rebase**
- Remove commits but keep changes → **Reset**
```

**Step 2: User Clarifies**
```
User: "I have 5 commits with messy messages, want to squash into 2 clean commits"
```

**Step 3: Validated Translation**
```
"That's interactive rebase! Here's how to squash commits:

**Current messy history:**
```bash
git log --oneline
# a1b2c3d fix typo
# d4e5f6g oops forgot file
# g7h8i9j add feature part 2
# j0k1l2m add feature part 1
# m3n4o5p previous work
```

**1. Start interactive rebase:**
```bash
# Rebase last 4 commits (keeps m3n4o5p unchanged)
git rebase -i HEAD~4

# Git opens editor showing:
pick j0k1l2m add feature part 1
pick g7h8i9j add feature part 2
pick d4e5f6g oops forgot file
pick a1b2c3d fix typo

# Rebase commands:
# pick = use commit as-is
# squash (s) = combine with previous commit
# reword (r) = change commit message
# drop (d) = delete commit
```

**2. Edit to squash commits:**
```bash
# Edit to this:
pick j0k1l2m add feature part 1
squash g7h8i9j add feature part 2
squash d4e5f6g oops forgot file
squash a1b2c3d fix typo

# Save and close editor
```

**3. Write combined commit message:**
```bash
# Git opens editor for new commit message:
# feat: implement search functionality
#
# - Add search API endpoint
# - Integrate with frontend
# - Add tests for search feature
#
# Squashed commits:
# - add feature part 1
# - add feature part 2
# - oops forgot file
# - fix typo
```

**4. Result:**
```bash
git log --oneline
# x9y8z7w feat: implement search functionality
# m3n4o5p previous work
```

**Advanced example - reorder and squash differently:**
```bash
git rebase -i HEAD~5

# Original:
pick a111111 add search endpoint
pick b222222 add tests
pick c333333 fix bug
pick d444444 add pagination
pick e555555 fix pagination bug

# Reorder and squash:
pick a111111 add search endpoint
squash c333333 fix bug
pick d444444 add pagination
squash e555555 fix pagination bug
pick b222222 add tests

# Result: 3 clean commits instead of 5 messy ones
```

**⚠️ Important rules:**
- Only rebase commits not yet pushed to shared branch
- If already pushed: force push required (git push --force)
- Never rebase public/main branches
- Communicate with team before force-pushing"
```

---

## Example 5: "handle merge conflicts"

### User Request
```
"I'm getting merge conflicts, what should I do?"
```

### Ambiguity Detected
- "handle conflicts" - could mean manual resolution, abort merge, or use merge strategy
- Need to clarify conflict resolution approach

### Semantic Validation Process

**Step 1: Explain Conflict Scenarios**
```
Merge conflicts occur when Git can't auto-merge changes. You have options:

1. **Manually Resolve Conflicts** (standard approach)
   - Edit conflicted files
   - Choose which changes to keep
   - Mark as resolved
   - Complete merge
   - Use when: Changes are incompatible, need human decision

2. **Abort Merge** (cancel and retry later)
   - Cancel merge operation
   - Return to pre-merge state
   - Command: git merge --abort
   - Use when: Wrong time to merge, need to rethink approach

3. **Use Merge Strategy** (favor one side)
   - Automatically favor "ours" or "theirs"
   - Command: git merge -X ours / git merge -X theirs
   - Use when: Know which version to keep entirely

Which approach makes sense for your situation?"
```

**Step 2: User Clarifies**
```
User: "Changes are incompatible, need to manually decide what to keep"
```

**Step 3: Validated Translation**
```
"That's manual conflict resolution! Here's the complete workflow:

**1. Identify conflicted files:**
```bash
git status

# Output shows:
# Unmerged paths:
#   both modified:   src/user.py
#   both modified:   tests/test_user.py
```

**2. Open conflicted file (example):**
```python
# src/user.py
def get_user(user_id):
    \"\"\"Get user by ID\"\"\"
<<<<<<< HEAD (your current branch)
    # Your changes:
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise UserNotFoundError(f"User {user_id} not found")
    return user
=======
    # Their changes (branch being merged):
    user = User.objects.get(id=user_id)
    if user is None:
        raise ValueError("User not found")
    return user
>>>>>>> feature/new-user-logic (branch being merged)
```

**3. Resolve conflict (edit file):**
```python
# Choose best parts from both:
def get_user(user_id):
    \"\"\"Get user by ID\"\"\"
    # Taking their ORM approach but your error handling
    user = User.objects.get(id=user_id)
    if user is None:
        raise UserNotFoundError(f"User {user_id} not found")
    return user

# Remove conflict markers (<<<, ===, >>>)
```

**4. Mark as resolved:**
```bash
# Add resolved file
git add src/user.py

# Check remaining conflicts
git status
# If more conflicts, repeat steps 2-4
```

**5. Complete merge:**
```bash
# Commit merge resolution
git commit

# Git opens editor with merge commit message:
# Merge branch 'feature/new-user-logic' into develop
#
# Conflicts resolved:
#   - src/user.py: Combined ORM change with better error handling
#   - tests/test_user.py: Updated tests for new ORM

# Save and close editor
```

**6. Verify:**
```bash
# Run tests to ensure resolution correct
pytest

# Push if tests pass
git push origin develop
```

**Tools for conflict resolution:**

**VS Code:**
```
Conflict markers show:
- Accept Current Change (your version)
- Accept Incoming Change (their version)
- Accept Both Changes
- Compare Changes (side-by-side diff)
```

**Command line diff:**
```bash
# Show three-way diff
git diff --ours src/user.py   # Your changes
git diff --theirs src/user.py # Their changes
git diff --base src/user.py   # Common ancestor
```

**Conflict strategies for specific scenarios:**

**Prefer ours globally:**
```bash
git merge -X ours feature-branch
# Auto-resolves conflicts favoring current branch
```

**Prefer theirs globally:**
```bash
git merge -X theirs feature-branch
# Auto-resolves conflicts favoring merged branch
```

**Aborting if conflicts too complex:**
```bash
git merge --abort  # Cancel merge, return to pre-merge state
# Then: Rethink approach or resolve conflicts differently
```

**Best practices:**
- Resolve conflicts in small batches (don't let branches diverge too much)
- Run tests after resolution
- Communicate with teammates if their code affected
- Consider pair programming for complex conflicts"
```

---

## Pattern Summary

Common Git/Gitflow ambiguity patterns:

1. **"merge"** → Merge commit (preserves history) vs Squash merge (single commit) vs Rebase (linear history)
2. **"branch"** → Gitflow branch type (feature/release/hotfix from specific source) vs general branch
3. **"workflow"** → Gitflow (structured, multiple versions) vs GitHub Flow (simple, continuous) vs GitLab Flow (environment-based)
4. **"fix commits"** → Amend (last commit) vs Interactive rebase (multiple commits) vs Reset (remove commits)
5. **"merge conflicts"** → Manual resolve (edit files) vs Abort merge vs Merge strategy (ours/theirs)
6. **"rebase"** → Interactive rebase (-i, edit commits) vs Standard rebase (replay commits) vs Rebase merge (linear history)

**Key insights:**
- **Merge strategies** change history structure (linear vs non-linear, detail vs summary)
- **Gitflow branch types** determine naming convention, source branch, and merge target
- **Workflows** match deployment model (scheduled releases → Gitflow, continuous → GitHub Flow)
- **Commit editing** requires interactive rebase for multiple commits, amend for last commit only
- **Conflict resolution** almost always requires manual editing for incompatible changes

Always clarify merge strategy, branch type, workflow model, and conflict approach before executing Git operations!
