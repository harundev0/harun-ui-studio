# Reuse-first workflow

## 1. Map the existing implementation

Read repository guidance and inspect Git status/diff when Git exists. Do not initialize Git merely for this workflow. Capture existing user edits before making changes.

Read the manifest and lockfile, route entry, imports/callers, related components, token/theme definitions, styles, and frontend data client. Inspect current screenshots or the running target if available. Locate the project's actual check commands. Search before creating anything.

Record a compact reuse map:

| Concern | Existing path/export | Decision and reason |
| --- | --- | --- |
| Route and layout | Actual path | Preserve navigation and boundaries |
| Components | Actual exports and callers | Reuse, compose, extend, or justified new component |
| Design | Tokens, font, spacing, icon family | Preserve existing values |
| Data | Client, hooks, types, mocks | Reuse existing integration seam |
| Verification | Commands and test files | Select checks for changed behavior |

Missing information is UNKNOWN, not an invented path. Search relevant local patterns, not the entire repository repeatedly.

## 2. Choose scope and direction

- **Refine:** preserve visual identity, content, routes, and behavior outside the requested change.
- **Redesign:** change only the expressly requested visual scope; retain product facts and integrations.
- **New surface:** inherit the surrounding application. If no existing system exists at all, use a suitable installed library or native primitives; document the reason for new tokens/components.

Classify each surface: Persuade (marketing), Operate (product UI), Read (documentation), or Experience (portfolio). Marketing aesthetics do not govern dense settings/forms/tables.

Design read example: “Saya membaca ini sebagai halaman pengaturan untuk pengguna aktif, mengikuti komponen, token, dan pola navigasi aplikasi.”

Define completion through observable outcomes: route opens, expected controls work, keyboard navigation works, responsive content stays usable, fixtures cover pending providers, and review evidence is current. Continue autonomously when the brief is clear. Ask only when an essential unresolved requirement prevents a correct implementation.

## 3. Implement within the architecture

Follow existing feature folders, naming, imports, exports, state ownership, and component APIs. Do not replace the architecture with a preferred folder diagram. Separate presentation from data access at the existing boundary; do not invent a repository/factory layer for one component.

Keep changes cohesive and narrow. Read other consumers before changing shared components. Prefer a compatible variant over a global change that breaks sibling routes. Use the project's state solution; do not add a second store, query client, HTTP wrapper, or icon family.

Use installed styling and animation mechanisms. Do not force Next.js onto React/Vue, or apply Server Component rules to a plain client application. Verify installed versions and official documentation before using unfamiliar APIs.

## 4. Craft floor

- Reuse semantic tokens for surfaces, text, actions, feedback, spacing, radii, and typography. A single brand accent does not prohibit semantic error/success colors.
- Preserve icon family and accessible names. Never use placeholder text as a field label.
- Normal text contrast at least 4.5:1; large text at least 3:1 (24 CSS px regular or approximately 18.67 CSS px bold). Meaningful control boundaries/icons need 3:1. Do not apply text contrast requirements to purely decorative dividers.
- Visible, unobscured keyboard focus; semantic controls; labels, linked errors, and appropriate dialog focus management. Never communicate state through color alone.
- Web targets meet WCAG 2.2's applicable 24 CSS px minimum or spacing exception; aim for 44 px on touch. Native iOS uses 44 pt and Android 48 dp. Do not mix units.
- Preserve readable reflow, zoom, long text, and responsive layouts. Never truncate essential copy merely to meet a two-line headline preference.
- Default English UI copy to sentence case: “Save changes”, “Email address”, “Payment failed”. Preserve proper nouns, acronyms, product names, and repository casing conventions. Human-facing prose uses complete grammar; Caveman never compresses product copy or documentation.
- Motion needs a purpose. Frequent/keyboard actions remain immediate. Use existing timing tokens, explicit transition properties, interruptible transitions, and reduced-motion support at every intensity. Gate pointer hover effects appropriately.
- Prefer transform/opacity; profile expensive effects instead of promising universal GPU acceleration. Keep one animation owner per element/property. No perpetual dashboard motion just to satisfy a preset.

## 5. Verify and stop

Use the actual existing frontend commands for typecheck, lint, build, and relevant tests. Do not run backend migrations, seeds, or service setup as preparation. Add targeted behavior coverage for consequential logic; trivial styling changes use existing checks plus visual verification.

Playwright checks the real route: primary journey, state transitions, console failures, unexpected requests, focus, responsive overflow, and the themes the project supports. Capture deterministic current screenshots at desktop and mobile sizes, recording route, viewport, state, and data mode. A typical web pair is 1440x900 and 390x844; include 320px reflow where applicable.

Use role/label locators and observable state waits, not arbitrary sleep or unconditional network-idle waits. Register expected response waits before actions when necessary. In fixture mode, verify relevant requests never reach missing backend services. Authentication fixtures must be scoped to browser tests or isolated preview, never a production bypass.

One batched inspection, one fix batch, one confirmation. Additional work requires a specific failed check or new change; no unbounded aesthetic loops. If tools or app access are blocked, mark runtime verification BLOCKED. Static checks are not a substitute for browser evidence.

## Common mistakes

| Temptation | Required response |
| --- | --- |
| “A new component is faster.” | Record existing candidates and why composition cannot satisfy the need. |
| “A mock API route is frontend work.” | Use browser/local fixtures; server route handlers are backend work. |
| “The screenshot looks good, so ship.” | Verify interaction and report checks separately. |
| “Premium means replacing the brand.” | Refine the incumbent design unless replacement was requested. |
| “The reviewer said done.” | Retain artifacts and Git state until separate explicit instructions. |

Stop before a backend write, duplicate client, unverified URL, stale evidence claim, or destructive cleanup without ownership evidence.
