---
name: skill-creator
description: Guide for creating and formatting OpenClaw skills correctly
---

# SKILL: skill-creator

Guide for creating properly formatted OpenClaw skills that can be discovered and used by the agent.

## When to Use This Skill

Use this skill when:
- Creating a new skill for OpenClaw
- Fixing skill format issues
- Adding metadata to existing skills
- Understanding skill structure requirements

## Skill File Structure

### Required Files

```
skills/<skill-name>/
├── SKILL.md          # Main skill definition (REQUIRED)
└── README.md         # Optional documentation
```

### SKILL.md Format (CRITICAL)

```markdown
---
name: skill-name              # Machine-readable ID (lowercase, hyphens)
description: Brief description for skill listing
---

# SKILL: skill-name

## Description

Detailed description of what this skill does.

## When to Invoke

Describe when this skill should be used:
- Specific scenarios
- Problem types
- User requests that match

## Capabilities

| Capability | Description | Example |
|------------|-------------|---------|
| Feature 1 | What it does | Usage example |
| Feature 2 | What it does | Usage example |

## Usage Flow

```
1. Step one
   ↓
2. Step two
   ↓
3. Step three
```

## Constraints

⚠️ **Important Rules**

1. Rule one
2. Rule two
3. Rule three

## Examples

### Example 1: [Name]
**Input**: User request
**Process**: Steps taken
**Output**: Result

### Example 2: [Name]
**Input**: User request
**Process**: Steps taken
**Output**: Result

## References

- Related skills
- External documentation
- Important notes
```

## Critical Format Requirements

### 1. Front Matter (MUST HAVE)

```yaml
---
name: skill-name                    # REQUIRED
description: Brief description      # REQUIRED
version: 1.0.0                      # Optional
author: Name                        # Optional
tags: [tag1, tag2]                  # Optional
---
```

**Common Mistakes**:
- ❌ Missing front matter entirely
- ❌ Front matter after markdown content
- ❌ Wrong format (not YAML)
- ❌ Missing `name` or `description`

### 2. Name Format

**Correct**:
- `code-optimizer`
- `xiuxian-gamedev`
- `stock-analyzer`

**Incorrect**:
- ❌ `Code Optimizer` (spaces, uppercase)
- ❌ `code_optimizer` (underscores)
- ❌ `mySkill` (camelCase)

### 3. Description Guidelines

- Keep it under 100 characters
- Describe what the skill does
- Use active voice
- Be specific

**Good**: "自动分析 C# 代码并提供性能优化建议"
**Bad**: "A skill for code stuff"

## Creating a New Skill: Step-by-Step

### Step 1: Check Existing Skills

```bash
npx clawhub@latest list
```

Avoid duplicating functionality.

### Step 2: Create Directory Structure

```bash
mkdir -p skills/<skill-name>
```

### Step 3: Write SKILL.md

Use template above. Ensure:
- Front matter at very top
- No BOM (Byte Order Mark)
- UTF-8 encoding
- Proper markdown formatting

### Step 4: Test Format

Verify:
- [ ] Front matter is first 3 lines
- [ ] Name is lowercase with hyphens
- [ ] Description is present
- [ ] # SKILL: header matches name
- [ ] File saved as UTF-8

### Step 5: Register in MEMORY.md

Add to installed skills list:

```markdown
### [Category]（日期安装）
- **skill-name** (版本) - 描述
  - 关键功能1
  - 关键功能2
```

## Skill Design Best Practices

### 1. Clear Scope

Each skill should do ONE thing well.

**Good**: "C#代码性能优化"
**Bad**: "代码优化+文档生成+测试+部署"

### 2. Actionable Content

Include concrete:
- Command examples
- Code snippets
- Decision trees
- Checklists

### 3. Self-Contained

Skill should work without external context:
- Define all terms
- Link prerequisites
- Include setup steps

### 4. Version Control

Track changes:
```markdown
## Changelog

### v1.1.0 (2026-02-10)
- Added feature X
- Fixed bug Y

### v1.0.0 (2026-02-09)
- Initial release
```

## Common Errors and Fixes

### Error 1: Skill Not Detected

**Symptom**: Skill doesn't appear in `npx clawhub@latest list`

**Causes**:
- Missing front matter
- Front matter format wrong
- File not named `SKILL.md`

**Fix**:
```markdown
---
name: my-skill
description: Description here
---

# SKILL: my-skill
...
```

### Error 2: Description Too Long

**Symptom**: Truncated in skill list

**Fix**: Keep under 100 characters

### Error 3: Wrong File Encoding

**Symptom**: Garbled characters in skill content

**Fix**: Save as UTF-8 without BOM

### Error 4: Missing SKILL Header

**Symptom**: Agent can't identify skill purpose

**Fix**: Always include `# SKILL: name` after front matter

## Template Variations

### For Code Tools

```markdown
---
name: language-tool
description: Description
---

# SKILL: language-tool

## Supported Operations

| Operation | Description |
|-----------|-------------|
| analyze | Analyze code |
| optimize | Optimize code |
| format | Format code |

## Usage Examples

...
```

### For Knowledge Bases

```markdown
---
name: domain-knowledge
description: Description
---

# SKILL: domain-knowledge

## Domain Overview

...

## Key Concepts

...

## Common Patterns

...
```

### For API Integrations

```markdown
---
name: api-integration
description: Description
---

# SKILL: api-integration

## Prerequisites

- API key
- Dependencies

## Authentication

...

## API Methods

...
```

## Integration with AGENTS.md

Skills should reference user context:

```markdown
## User Context

See [AGENTS.md](../../AGENTS.md) for:
- User preferences
- Project structure
- Important constraints
```

## Summary Checklist

Before considering a skill complete:

- [ ] `SKILL.md` exists in `skills/<name>/`
- [ ] Front matter at top with `name` and `description`
- [ ] Name is lowercase with hyphens
- [ ] Description under 100 chars
- [ ] `# SKILL: name` header present
- [ ] Clear "When to Use" section
- [ ] Concrete examples included
- [ ] Constraints documented
- [ ] Added to MEMORY.md
- [ ] File encoded as UTF-8

## Quick Reference Card

```
SKILL CREATION CHEAT SHEET

1. Create: mkdir skills/my-skill
2. File: skills/my-skill/SKILL.md
3. Front matter:
   ---
   name: my-skill
   description: What it does
   ---
4. Header: # SKILL: my-skill
5. Sections: Description, When, Capabilities, Examples
6. Register: Add to MEMORY.md
```
