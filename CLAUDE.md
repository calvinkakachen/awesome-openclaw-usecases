# CLAUDE.md — AI Assistant Guide for awesome-openclaw-usecases

## Repository Overview

**Awesome OpenClaw Use Cases** is a community-curated documentation repository of real-world applications built with [OpenClaw](https://openclaw.ai) — an AI agent framework. It contains 40+ verified use cases organized by category, with multilingual READMEs and automated CI to track the use case count.

**This is a documentation-only repository.** There is no code, no build system, and no runtime dependencies.

---

## Directory Structure

```
awesome-openclaw-usecases/
├── usecases/               # One markdown file per use case (~40 files)
├── .github/
│   └── workflows/
│       └── update-badge.yml  # Auto-updates README badge on push to main
├── .coderabbit.yaml          # CodeRabbit AI review configuration
├── README.md                 # Primary docs (English) with category tables
├── README_CN.md              # Chinese translation
├── README_KR.md              # Korean translation
├── CONTRIBUTING.md           # Contribution guidelines
└── LICENSE                   # MIT
```

---

## Contribution Workflow

1. **Create** a new markdown file in `/usecases/` following the standard template (see below).
2. **Add** a row to the appropriate category table in `README.md` (and optionally `README_CN.md`, `README_KR.md`).
3. **Open a PR** — CodeRabbit will auto-review it.
4. After merge to `main`, the GitHub Actions workflow auto-updates the use case count badge in `README.md`.

### Hard Rules (from CONTRIBUTING.md)
- One use case per markdown file.
- Must be **personally tested and verified** — no AI-generated or untested ideas.
- No crypto-related use cases.
- Duplicates are acceptable only if the approach differs meaningfully.

---

## Use Case Markdown Template

Every file in `usecases/` should follow this structure:

```markdown
# [Use Case Title]

## Pain Point
Describe the problem or bottleneck being solved.

## What It Does
Brief summary of the workflow or automation.

## Skills Needed
List required OpenClaw skills, plugins, or third-party services.

## How to Set It Up
Step-by-step instructions with example prompts, YAML, or configs.

## Key Insights
Lessons learned, caveats, or tips for replication.

## Related Links
- [Resource](https://...)
```

Optional sections: `Based On`, `Inspired By` for attribution.

---

## README Table Format

When adding a use case to `README.md`, insert a row in the correct category table:

```markdown
| [Title](usecases/filename.md) | Brief one-line description |
```

The eight current categories are:
1. Social Media
2. Creative & Building
3. Infrastructure & DevOps
4. Productivity
5. Research & Learning
6. Finance & Trading
7. *(and any new categories as needed)*

---

## CI / Automation

### Badge Update Workflow (`.github/workflows/update-badge.yml`)
- **Triggers**: Push to `main` when `usecases/*.md` files change.
- **Action**: Counts `.md` files in `usecases/`, updates the count badge in `README.md`, and auto-commits.
- **Committer**: `github-actions[bot]`

Do not manually edit the badge count line in `README.md` — the workflow manages it.

### CodeRabbit (`.coderabbit.yaml`)
- Reviews all PRs automatically.
- **Path-specific focus for `usecases/**/*.md`**:
  - Checks for supply-chain risks (typosquatting, suspicious installs).
  - Flags unknown or untrusted OpenClaw skills/plugins.
  - Evaluates practical utility vs. product promotion.
  - Looks for hardcoded credentials or overly permissive permissions.

---

## Security Conventions

The README includes a prominent security warning about community-built skills. When reviewing or writing use cases, flag:
- Skills or plugins installed from unknown sources.
- `pip install`, `npm install`, or shell commands referencing unverified packages.
- Hardcoded API keys, tokens, or passwords in examples.
- Remote execution patterns without clear trust boundaries.

Preferred patterns from existing use cases:
- Store secrets in a password manager (e.g., 1Password) rather than inline.
- Use n8n or a webhook proxy to isolate credentials from the agent environment.
- Pin versions of any external tools.

---

## Common OpenClaw Patterns in This Repository

| Pattern | Example Use Case File |
|---|---|
| Multi-agent teams with Telegram control | `multi-agent-team.md` |
| Decentralized coordination via `STATE.yaml` | `autonomous-project-management.md` |
| Webhook proxy for credential isolation | `n8n-workflow-orchestration.md` |
| Heartbeat / cron-driven autonomous work | `self-healing-home-server.md` |
| Semantic memory / RAG over saved URLs | `knowledge-base-rag.md` |
| Skill-based composition (sessions_spawn, ssh, web_fetch) | `project-state-management.md` |

---

## What AI Assistants Should and Should Not Do

### Do
- Follow the use case template exactly when creating new files.
- Maintain the README table structure and category organization.
- Write in the same concise, problem-first style as existing use cases.
- Provide actionable, replicable setup instructions.
- Attribute sources when adapting from existing community work.

### Do Not
- Add or modify code files — this repo has none.
- Invent use cases that have not been tested by a real user.
- Edit the badge count line in `README.md` manually.
- Add crypto-related use cases.
- Include hardcoded credentials or insecure install patterns in examples.
- Modify `README_CN.md` or `README_KR.md` unless you can produce accurate translations.

---

## Git Conventions

- Default development branch for AI-assisted work: `claude/add-claude-documentation-8SVrr`
- Push with: `git push -u origin <branch-name>`
- Commit messages should be descriptive (e.g., `Add use case: arxiv paper reader`).
- The `github-actions[bot]` commits badge updates automatically — do not revert them.
