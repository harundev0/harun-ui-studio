---
name: harun-ui-studio
description: Use when Harun requests UI/UX design, frontend implementation or integration, component refinement, responsive fixes, or a review artifact in an existing or new project. Also use for harun-ui-studio requests and cleanup of its review artifacts.
allowed-tools:
  - read
  - edit
  - write
  - shell
  - execute
  - skill
  - webfetch
---

# Harun UI Studio

Frontend delivery: understand, reuse, verify, hand over.
Scope: UI/UX, frontend code, and existing API consumption only.

## Non-negotiable boundaries

- Read repository instructions, the target, its callers, components, tokens, routes, and data flow before editing. Preserve user changes.
- Reuse components, typography, colors, styles, icons, helpers, clients, hooks, and contracts. Compose or extend first. Create only after recording the searched paths and the unmet need. Follow existing architecture; no speculative layers or stack migration.
- Never implement backend work: endpoints, route handlers, server actions, databases, migrations, authentication services, provider logic, or infrastructure. Read backend contracts only. Server-rendered presentation using established patterns is allowed; creating server-side data logic is not.
- Missing backend: use deterministic frontend fixtures through an existing mock seam, or a minimal local seam. Never silently replace a failed real request with dummy success. Document pending backend work.
- Never automatically stage, commit, push, deploy, or open a PR. Review approval is not Git authorization. A later explicit Git request is a separate task.
- Keep artifacts until an explicit cleanup instruction. Bare “sudah” or “sudah bagus” means review acknowledgment. “Sudah, hapus artifact” authorizes cleanup of the identified artifact only. Preserve source files, older artifacts, and shared servers.

## Execution

1. **Inspect:** classify surface and stack. Record reusable paths, current visual evidence, frontend-only scope, and acceptance criteria in existing task notes. No existing notes: use one compact task file.
2. **Decide:** load [workflow.md](references/workflow.md). State the design read in one sentence. Existing design is authoritative. Load [skill-routing.md](references/skill-routing.md) only for an actual knowledge gap; do not load every source skill.
3. **Build:** implement a small vertical slice using existing patterns. Include applicable loading, empty, error, success, disabled, and validation states. For data work, read [integration.md](references/integration.md).
4. **Verify:** run relevant existing frontend checks and Playwright flows against the actual application. Inspect desktop/mobile together, fix identified issues together, then confirm once. Stop discretionary polish; unresolved defects remain blockers. Report PASS, FAIL, BLOCKED, or NOT RUN with evidence.
5. **Deliver:** read [delivery.md](references/delivery.md). Provide verified application and artifact links, exact access steps, per-file changes, state coverage, checks, backend handoff, limitations, and cleanup instructions. A report links to the actual application; never substitute a separately reimplemented lookalike.

## Quality and economy

Accessibility and product truth outrank decoration. Use correct English grammar and sentence case unless existing copy specifies otherwise. Explain in Indonesian by default; keep code identifiers and established product language intact.

Keep chat concise, but access flows and handoffs complete. Persist a small checkpoint before compaction: scope, reusable paths, changed files, fixture mode, checks, URLs, artifact ownership, next action. No broad skill loading, unrequested delegation, or endless QA. Model price never changes acceptance criteria. Do not claim perfection, unmeasured parity, or verification that did not run.
