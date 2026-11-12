# Frontend Web Rules

Use these rules for browser interfaces and their behavior, including HTML/CSS,
components, client state, and browser rendering. Follow the project's framework,
design system, and browser support policy. JavaScript and TypeScript code also
uses `languages/javascript-typescript.md`; plain HTML/CSS changes do not load
language rules merely because the project contains scripts.

## Project Structure And Component Boundaries

- Inspect neighboring pages, shared components, routing, styling, data access,
  and relevant scripts before adding another pattern. Reuse the established
  component library, design tokens, form helpers, and query tools when suitable;
  do not introduce a second stack for a local feature.
- Keep components cohesive and data flow explicit. Extract components or hooks
  for meaningful responsibilities, invariants, or actual reuse; avoid both
  monolithic pages and layers that only forward props without a clear purpose.
- Enforce authorization for server resources, shared-state invariants, and
  business constraints that must resist client tampering on a trusted server.
  Share or mirror validation for feedback where appropriate; browser checks
  do not replace that enforcement. Purely local calculations and offline
  business logic follow the project architecture and do not require a backend
  merely because they are business logic.
- Respect server/client rendering boundaries when the framework has them.
  Avoid browser APIs during server execution and request-specific data in
  shared module state. Keep initial rendering consistent across hydration;
  do not switch rendering strategy or suppress hydration errors as a shortcut.

## State, Requests, And Contracts

- Distinguish local interaction state, navigation or URL state, server data,
  and editable drafts. Use the existing owner for each; avoid duplicating
  derived data or introducing a global store for a local interaction.
- Give requests and caches keys that include all relevant identity, tenant,
  filter, sort, and pagination inputs. Prevent stale responses from replacing
  results for a newer selection. Clear or partition private cached data when
  user or tenant context changes.
- Match actual request, response, error, pagination, and serialization
  contracts. Reuse generated clients and their source-of-truth workflow when
  present; do not hand-edit generated output or invent fields to complete UI.
  Load `backend/api-route-design.md` when endpoint contracts are affected, and
  backend or database rules only when their behavior is materially involved.
- Account for loading, empty, error, success, and refreshing states as relevant
  to the feature. Distinguish empty results from failed requests; preserve
  useful existing data and user input where appropriate.
- For writes, make pending, success, and failure visible and guard duplicate
  submission. Automatic retries require safe operation semantics. Optimistic
  updates need rollback or reconciliation; invalidate or update affected
  cached views after success. Do not claim a cancelled request undid a write.

## Forms And Interaction

- Use semantic controls with labels, instructions, and actionable validation
  feedback. Preserve input on recoverable failure and move or announce errors
  in a way users can discover.
- Support keyboard use, logical focus order, visible focus, and appropriate
  focus management for dialogs and navigation. Prefer native semantics and
  established accessible primitives; adding ARIA alone does not implement
  keyboard behavior. See the
  [W3C form labeling guide](https://www.w3.org/WAI/tutorials/forms/labels/).
- Keep controls and navigation honest: a visible action must perform its
  stated function or clearly communicate its unavailable state. Use project
  confirmation patterns for destructive product actions, scaled to impact.
- Do not rely solely on color, hover, animation, or pointer input to convey
  essential information or expose required actions. Respect reduced-motion
  preferences when adding motion.

## Layout, Styling, And Compatibility

- Follow existing spacing, typography, colors, and component states. Reuse
  design variables and keep selectors scoped according to project convention;
  avoid global overrides and arbitrary specificity escalation for local fixes.
- Make layout work at relevant narrow and wide widths, with long text, empty
  content, validation errors, and zoom where affected. Avoid hiding essential
  content or introducing page overflow merely to fit one screenshot.
- Use project browser and device targets to select features and fallbacks.
  For version-sensitive capabilities, check current official documentation and
  compatibility evidence. [MDN Baseline](https://developer.mozilla.org/en-US/docs/Glossary/Baseline/Compatibility)
  summarizes browser support; it does not replace project targets or device
  and accessibility testing. Resolve material support gaps before depending
  on a feature; do not automatically target only the newest browser or add
  polyfills for unspecified legacy targets.

## Browser Security And Privacy

- Treat browser code, public environment variables, source maps, and bundled
  assets as accessible to users. Keep service credentials and secrets on the
  server; hiding controls does not enforce access rights.
- Render untrusted content as text by default. When rich HTML is required,
  use the established sanitization boundary; do not bypass escaping or trust
  raw HTML merely because it came from an API or model.
- Follow the application's session design. Do not introduce authentication
  tokens or session identifiers in localStorage or sessionStorage. Account
  for JavaScript access, cookie protections, and CSRF in the chosen design;
  existing auth changes require compatibility and access-control review rather
  than an incidental migration. See the
  [OWASP HTML5 security guide](https://cheatsheetseries.owasp.org/cheatsheets/HTML5_Security_Cheat_Sheet.html)
  and [session management guide](https://cheatsheetseries.owasp.org/cheatsheets/Session_Management_Cheat_Sheet.html).
- Avoid sensitive values in URLs, analytics, console output, and client-side
  persistence. Treat cross-window messages and redirects as trust boundaries
  when used, validating origins and allowed destinations.

## Performance And Verification

- Diagnose the affected path before adding memoization, caching, virtualized
  lists, or code splitting. Consider request waterfalls, bundle and asset
  sizes, rendering work, and layout shifts; preserve correctness and usability
  when optimizing. Do not equate fewer renders with measured improvement.
- Apply `workflow/verification.md` using existing tools and checks selected
  for the change. Exercise relevant state transitions and API failures; fully
  mocked data does not establish backend integration.
- For changed layout or interaction, inspect the actual rendered page at
  relevant viewport sizes and exercise the affected behavior. Use browser
  automation or manual observation as available; a successful build or a
  screenshot alone does not prove interactions work. If browser validation is
  unavailable, report what was checked and what remains unverified.
- Check keyboard access and focus when affected. Choose end-to-end tests for
  material user journeys and integration risks; do not require a new browser
  test framework, a full E2E suite, or every browser for every small change.
