# Web Frontend Review Checklist

Select questions from the user journey affected by the diff. For a layout-only change, start with the affected controls and viewport. For a contract change, start with the producer and its actual consumer.

## Client and Server Contracts

- Follow the data from the form or URL through the request serializer to the handler, and from the response or error back to the rendered view. For partial updates, does leaving a field untouched preserve the stored value? Check omission, explicit `null`, zero, and false wherever the contract gives them different meanings.
- Compare the handler and schema with the client code that actually ships, including generated clients when used. Could an old browser tab encounter a new response shape, pagination rule, or status code during a supported rollout? Trace what the user would see.
- Does the UI distinguish a failed request from an empty result? On a recoverable save failure, check whether the user can see the error, retain their draft, and retry safely.

## State, Requests, and Identity

- If a user changes projects, filters, or pages while a request is pending, which response can update the visible view? Inspect both the cache key and the state update. Check private cached and in-flight data across account or tenant switches.
- Trace a write through pending, success, and failure. Could a second submission duplicate the operation, an optimistic update survive rejection, or a stale list hide a successful save? A cancelled client request can still leave a committed server write.
- When navigation or unmount changes ownership, check that affected subscriptions, listeners, and timers stop updating the old view.

## Interaction, Rendering, and Trust Boundaries

- Can a keyboard user reach, identify, and activate each changed control? For dialogs, follow focus on open and close. For failed forms, check how users discover the error and return to the field.
- At the affected viewport sizes and zoom levels, can users still read the content and reach primary actions with long labels or validation messages present?
- For server-rendered pages, check that server execution and initial browser rendering agree and that request-specific state belongs to the request. For changes crossing the client bundle boundary, check which values and implementations actually ship to the browser.
- When changing access controls or rich content, locate server-side authorization for protected operations and the escaping or sanitization step for untrusted data. Report a defect only when the changed path and its impact are supported by evidence.

## Verification

Choose the smallest check that answers the review question. Compare actual serialized values with handler behavior for a contract mismatch. Exercise reversed response order for a stale view, or keyboard navigation at the affected width for an unreachable control. Type checks establish static compatibility, builds establish compilation or bundling, and browser exercises establish the interactions observed. A browser test with a mocked API leaves the real service contract unverified.
