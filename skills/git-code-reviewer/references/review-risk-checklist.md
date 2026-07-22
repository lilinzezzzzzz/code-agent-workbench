# Review Risk Checklist

Use only the questions relevant to the changed behavior. This is a thinking aid, not an output template.

## Correctness and Compatibility

- Does the implementation match the intended behavior on success, failure, partial-success, empty, omitted, and boundary cases?
- Did defaults, fallbacks, control flow, state transitions, or shared helpers change for existing callers?
- Did any public API, persisted format, message schema, configuration contract, or mixed-version behavior change?
- Can old and new readers, writers, producers, and consumers coexist during rollout and rollback?
- Were affected tests, schemas, generated artifacts, configuration, and documentation kept aligned?

## State, Concurrency, and External Effects

- Is authoritative state clear, and do create, update, delete, expire, retry, replay, repair, and rollback paths keep derived state consistent?
- Can partial failure, retries, duplicate delivery, reordering, cancellation, or timeout duplicate work or corrupt state?
- Is shared or distributed state protected by an appropriate transaction, ownership, lock, uniqueness, idempotency, or deduplication boundary?
- Are external calls bounded by appropriate timeout, cancellation, retry, and isolation behavior?
- Can old and new versions operate safely at the same time?

## Security, Performance, and Operations

- Are authentication, authorization, tenant isolation, and input validation preserved at every affected trust boundary?
- Could untrusted input reach injection, SSRF, path traversal, unsafe deserialization, privileged tools, or sensitive logs?
- Does the changed path introduce N+1 access, unbounded work or reads, full materialization, blocking I/O, or load-amplifying retries?
- Are resources released correctly, and can operators detect, diagnose, and roll back failures without exposing secrets?
- Did runtime defaults, feature flags, alerts, metrics, traces, or audit behavior change?

## Evidence and Verification

- Does each finding cite inspected evidence and a direct user or operational impact?
- Were immediate callers, callees, and nearest tests inspected when the conclusion depends on shared behavior?
- Were plausible counterexamples used to challenge high-risk conclusions?
- Is an unverified concern phrased as an assumption, question, or residual risk rather than a confirmed defect?
- Does the reported verification match commands and evidence actually observed?

## Exclusions

- Do not report style preferences without correctness, contract, or material maintainability impact.
- Do not split one root cause into multiple findings unless remediation differs.
- Do not recommend broad refactors unrelated to the changed risk surface.
- Do not report speculative or pre-existing issues unless the change worsens or depends on them.
