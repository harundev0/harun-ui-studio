# Review artifact and delivery contract

## Artifact fidelity

The **application URL** is the running changed application. The **artifact URL** is its review report with current evidence and a direct link to that application. This provides an artifact-like review surface without pretending to be a native Claude feature.

Prefer the project's existing Storybook, preview, Playwright report, or review surface. The live preview must use the actual route/component implementation with the same assets, providers, styles, viewport, and explicit data state. Do not maintain a second HTML/CSS replica of the UI.

Screenshots are current captures, not interactive previews. Record capture time, route, viewport, theme, state, and data mode. Match these conditions before any visual comparison. Do not claim pixel identity merely because the same component is used; fonts, browser, assets, and state may differ.

If an iframe is blocked by CSP or authentication, use a top-level application link plus fresh screenshots. Do not weaken security headers, bypass login, or pass off stale screenshots. If the app cannot run, report BLOCKED and provide code/check evidence only. Never invent a reachable preview URL.

## Optional report utility

Use only if the repository has no adequate review report. Python 3 standard library; no package install. Commands use paths relative to this skill's base directory:

```bash
python3 scripts/artifact.py create --base /absolute/review-root --id orders-review --report /absolute/report.json
python3 scripts/artifact.py serve --base /absolute/review-root --id orders-review --port 8765
```

Use a project-owned ignored artifact folder if one already exists. Otherwise use a task-specific directory under the harness's approved temporary root, or an untracked `.ui-artifacts` directory. Do not edit `.gitignore` merely to hide source changes. Serve only the artifact directory, on loopback by default. Do not expose the repository root. Record actual bound port, process owner/handle, and restart command. Check port availability and actual URL instead of assuming the example port.

Required report JSON fields:

- `title`, `status`, `data_mode`, `summary`: nonempty strings. Status is READY FOR REVIEW, BLOCKED, or PARTIAL.
- `app_url`: verified HTTP(S) application URL, or `null` when unavailable.
- `changes`: list of `{ "path": "actual path", "change": "what changed and why" }`.
- `flows`: list of `{ "name": "flow name", "precondition": "setup/state", "steps": ["numbered in rendered report"], "expected": "observable result" }`.
- `checks`: list of `{ "name": "check", "status": "PASS|FAIL|BLOCKED|NOT RUN", "evidence": "command, exit code, observation or blocker" }`.
- `backend`: handoff summary and document location, or `Not applicable`.
- `limitations`: list of unresolved limitations; empty only when actually none known.
- `screenshots`: list of `{ "path": "/absolute/current-capture.png", "caption": "capture time, route, viewport, theme and state" }`. Only PNG, JPEG, and WebP.

The utility escapes text, copies screenshots, and records file hashes. It does not test the application or certify the truth of supplied evidence. Fill the report only from observed results. A missing Python runtime is a reported limitation; use existing report tools instead of installing Python.

## Link verification

1. Start the application's existing frontend command, without backend setup.
2. Open the exact target route; HTTP 200 alone does not prove a page rendered correctly.
3. Test flow preconditions and UI transitions with Playwright.
4. Create the report with actual URLs and fresh captures; verify the report in a browser.
5. Open it in the harness Review pane where supported. Otherwise provide the verified local URL and local report path. Remote users need an existing approved forwarded URL; `localhost` is machine-local, not a public deployment. Do not create a public tunnel automatically.
6. Explain link lifetime: live URLs require their servers; screenshots/report files persist until deleted. Record a restart command.

## Required final delivery

Use these ordered fields, even with concise chat. Put long details in the report and handoff, but do not omit access instructions:

1. **Status:** frontend status, data mode, and integration status.
2. **Links:** clickable application and artifact links, or explicitly unavailable with reason; local artifact path and server lifetime.
3. **Access flow:** prerequisites, starting route/navigation, numbered actions, expected states, relevant fixture/theme choice.
4. **Changes:** each actual file/component, what changed, reused dependency/token, and reason for anything newly created. Include integration/mock/test/document changes.
5. **Verification:** command/check and PASS/FAIL/BLOCKED/NOT RUN; evidence links and current capture details.
6. **Backend handoff:** document link, missing capabilities, consumer fields, fixture-to-real path, and unresolved owner decisions. `Not applicable` for purely visual work.
7. **Review and cleanup:** retained artifact ID, known limitations, no automatic commit/push; exact cleanup phrase and restart details.

English UI code review follows the Emil format when reviewing concrete before/after code:

| Before | After | Why |
| --- | --- | --- |
| Actual prior implementation | Actual change | Evidence-based rationale |

## Cleanup only on instruction

Keep artifacts after delivery and after a bare “sudah”. “Hapus artifact orders-review” or “sudah, hapus artifact orders-review” explicitly requests deletion. If the user requests cleanup without an ID and exactly one current task artifact is recorded, use that ID. If several could match, ask which one. Never infer cleanup from positive review feedback.

For utility-owned artifacts, run:

```bash
python3 scripts/artifact.py clean --base /absolute/review-root --id orders-review --confirm orders-review
```

This removes only unchanged manifest-owned files. Unknown, modified, or symlinked files block deletion. Investigate rather than force-delete. Stop only the preview/report process this task started, with a verified handle; never terminate the shared application server. Cleanup never removes frontend source, fixtures needed by the implementation, handoff documentation, other artifacts, or Git changes. Report removed files and resulting link availability. There is no auto-expiry.
