# Harun UI Studio: creation and verification

## Design

Create a personal, reusable frontend skill with a small mandatory core and on-demand references. Existing repository architecture and design are authoritative. Work covers UI/UX, frontend implementation, and consumption of existing integrations. Missing providers use frontend fixtures and a backend handoff. Delivery includes accurate review links, user flows, changed files, evidence, and explicitly owned artifacts. No automatic Git writes or cleanup.

The existing `ui-start` is a useful local predecessor but lacks ownership boundaries, conditional reference routing, accurate artifact delivery, and backend handoff requirements. The supplied design skills contain conflicting defaults; the custom skill resolves these explicitly. No upstream skills are modified.

## Checklist

- [x] Discover local skills, workspace, and OpenCode V2 installation rules.
- [x] Capture requirements, scope, and design; use the user's detailed requirements as the brief.
- [x] Define pressure scenarios with deadline, conflicting recommendations, and requested completion claims.
- [x] Run baseline without the new skill and inspect actual responses.
- [x] Identify failures and choose mandatory structural fields plus explicit boundaries.
- [x] Write a lowercase-hyphen skill ID and valid, concise discovery frontmatter.
- [x] Write a short core, conditional reference routing, examples, and common mistakes.
- [x] Write artifact utility tests before implementation; verify initial failure (missing module, not behavioral assertion).
- [x] Implement the artifact utility and test it (9 checks).
- [x] Run the same pressure scenarios with the skill and inspect compliance.
- [x] Run five fresh-context wording samples, each with a no-guidance control.
- [x] Resolve observed failures and recheck affected scenarios; no new behavioral boundary failure observed.
- [x] Check reference paths, structure, word count, and deployment parity.
- [x] Verify actual artifact links and browser rendering through Playwright.
- [x] Install the skill globally without overwriting existing user work; discovery confirmed by runtime.
- [x] Prepare usage, access flow, test evidence, cleanup instructions, and limitations in README and report.
- [x] Git commit/push checklist from upstream is overridden by the user's explicit prohibition.

## Baseline evidence

Session: `ses_f0aa2400effeaHVmtukZrk4Ffu`. Five simulated scenarios; no filesystem changes.

Cases 1-4 broadly respected existing components, backend scope, verification honesty, and CSP. No invented failures are attributed to these cases.

Case 5 leaves unsafe ambiguity:

> Remove only identified, disposable session-owned outputs

It did not require an explicit cleanup request before removing such outputs. The user's request requires retention until instructed.

> Commit/push only after clear review approval and applicable authorization

This does not distinguish review approval from a separate explicit Git command. The new skill must do so.

Delivery skeletons omit a mandatory per-file change map, step preconditions, expected states, and a complete field-level backend handoff. These are output-shape failures, addressed by a required delivery structure rather than vague reminders.

## Evaluation limits

Behavioral tests are simulations, not proof that every future model will comply. No price-ranked model benchmark has been requested with a specific model ID; pricing is absent from the available model catalog. Do not claim cheap-model parity or perfection. Obsidian tools are unavailable in this session; project records remain here.
