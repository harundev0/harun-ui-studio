# Frontend integration and backend handoff

## Trace before changing

Follow the route/component to its hook/store, existing client, authentication attachment, response type, error mapping, and mock support. Read published contracts and relevant backend declarations for understanding only. Document their actual paths.

1. **Available contract and API:** reuse the existing client/hook with its base URL, auth, retries, cancellation, cache keys, and error handling. Do not introduce a parallel `fetch`/Axios client.
2. **Contract exists, API absent:** fixtures satisfy the current frontend or generated type. Reuse existing MSW handlers, Storybook args, test interception, or a local fixture seam. Do not install a mock server or add an API route.
3. **Contract absent:** define only the minimal frontend view model in the project's existing location. Label it PROPOSED, not backend-approved. Document consumer field requirements and open decisions. Do not modify backend-owned OpenAPI, shared contracts, or generated output by hand.
4. **API fails or differs:** preserve real error states. Document the discrepancy; never silently fall back to fixtures or claim integration passes. Continue the UI preview through explicitly selected fixture mode.

Use stable IDs, dates, values, and ordering. Cover applicable success, empty, loading, failure, validation, permission-denied, partial, and long-content cases. Derive fixtures from canonical types where available. Avoid private/production data. Frontend validation guides users; backend authorization/validation remains pending provider responsibility.

Mocks must be opt-in through an existing preview/test switch, default off for production, and excluded from production initialization. Where no switch exists, use the smallest isolated frontend preview seam and document the exit path. Keep fixture payloads outside presentation components. Do not manufacture production authentication, tokens, CORS changes, or service setup.

## Required handoff

Use the project's existing handoff document. If none exists, create `docs/frontend-handoff/<task-id>.md`. Write only relevant sections and link authoritative types rather than duplicating them.

```markdown
# Orders frontend handoff

## Status and access
Frontend status: READY FOR REVIEW / BLOCKED
Integration status: MOCK ONLY / CONNECTED AND VERIFIED / BLOCKED
Route and navigation: verified URL and exact access steps
Data source: actual client/hook/fixture paths

## Existing contract
Authority: actual file/export or NOT AVAILABLE
Operation: existing method/path, or PROPOSED consumer need
Owner: existing backend owner, or UNASSIGNED

## Consumer requirements
For each rendered/entered field: name, type, required/optional, null behavior,
format/units/timezone, allowed values, and UI usage.
Include pagination/filter/sort rules only if used.
Include expected errors and the UI state for each.

## Fixture-to-real mapping
Fixture path/export and supported scenarios.
Existing hook/client that consumes the contract.
Exact preview switch and production-off behavior.
Frontend files/checks required to replace fixtures with the real provider.

## Backend work pending
Concrete missing capabilities and acceptance examples.
Unresolved contract decisions and the owner expected to resolve them.
No database design, provider implementation, or migration has been performed.

## Verification
Commands and results; mock verification versus real integration verification.
Limitations and blocked behavior.
```

Completion example: a fixture-driven Orders page may be frontend-ready while its live integration is still MOCK ONLY. Those are separate statuses, not contradictory claims.
