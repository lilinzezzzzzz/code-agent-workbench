# Review Output Template

Start with a brief overall judgment about the material issues and code clarity, then report issues to address and optional improvements separately. Preserve supporting evidence, scope, verification results, and material caveats. Omit repeated summaries, generic praise, empty sections, and background that does not change the conclusion.

## Findings

Order findings by severity, then impact. Use one item per root cause:

A finding must connect a specific change to a reachable trigger or concrete maintenance scenario, an incorrect outcome or material risk, and inspected evidence. For maintainability issues, explain how the structure increases the chance of missed updates, inconsistency, or future defects; a size metric or style preference is insufficient. Static reasoning can establish a finding without an executed reproduction. If the core trigger or causal link is only hypothetical, use Open Questions instead. Cite the smallest relevant code location in the reviewed version, rather than an entire function or file.

```text
1. [high] Concise defect title
   - Location: file path and line or specific symbol in the reviewed snapshot
   - Problem and impact: specific structure or behavior and its user, operational, or maintenance consequence
   - Evidence: reachable execution path, call relationship, or typical modification scenario supported by inspected code, configuration, schema, tests, or command output
   - Recommendation: smallest viable adjustment or follow-up; add a short local example only when it clarifies the change
   - Trade-offs and verification: expected benefit and cost, behavior to preserve, key scenarios to check, and material evidence gaps; distinguish suggested checks from observed results
```

Assess severity using impact, affected scope, triggering conditions, and recoverability. These examples are guides, not keyword-based assignments; a race is not automatically high, nor every outage critical.

| Level | Meaning |
| --- | --- |
| `critical` | Security breach, auth bypass, data loss or corruption, irreversible migration failure, or outage |
| `high` | User-visible bug, contract break, race, unsafe rollback, or major failure-path gap |
| `medium` | Missing validation, error-handling gap, performance regression, observability gap, or test gap hiding concrete risk |
| `low` | Changed-path maintainability issue that materially increases future defect risk |

## Optional Improvements

Use this section for evidence-backed reductions in complexity or maintenance effort that do not establish a defect requiring correction. Order them by practical benefit and use the same location, problem, evidence, recommendation, and trade-off fields as findings. Label them optional rather than assigning defect severity. Explain the actual benefit and cost; personal style preferences and speculative reuse do not qualify. Do not repeat a finding here or move an unverified defect into this section.

Examples should illustrate only the relevant local adjustment. Do not rewrite entire functions or modules as a substitute for explaining the issue, and do not apply suggested edits during a review-only task.

## Scope

Always state:

- Review mode and artifact or comparison range.
- Included and excluded workspace changes when relevant.

For complete-branch review, also state the user-provided base, exact resolved ref, whether it is remote-tracking, local, or another explicit ref, fetch status and base commit SHA (or the approved cached-ref downgrade and freshness warning), actual merge-base SHA, and reviewed HEAD SHA.

For staged review, state `HEAD` → index, with the inspected `HEAD` SHA (or empty tree for an unborn branch) and index snapshot identifier, or the limitation preventing identification. Make clear that unstaged and untracked changes are excluded. No user-provided base or fetch details are required.

Disclose material uninspected portions and any snapshot changes that limit the report. Do not imply the current revision was reviewed when conclusions apply only to an earlier snapshot.

## Verification

State commands or checks that ran, their observed outcomes, and whether they validated committed content, the staged snapshot, or the working tree. If none ran, say the review was limited to static inspection. State skipped or blocked checks only when they leave material risk.

## Open Questions

Put plausible but unverified concerns here. Do not present them as confirmed findings.

## No Findings

If there are no confirmed issues to address, say so explicitly; report optional improvements only when their benefit is supported by evidence. Say the code is sufficiently clear and recommend retaining it only when inspected evidence supports that judgment, no material coverage gap or unresolved question affects it, and no change offers enough benefit to justify its cost. Limit that conclusion to the inspected scope.

When a coverage gap or unresolved question materially affects the conclusion, state that no issue has been confirmed in the inspected content, identify the missing evidence, and recommend the smallest check needed to resolve it. Do not turn the absence of confirmed findings into a positive assessment of the affected scope. Preserve material verification gaps or residual risks. For Redis or stateful changes, name the relevant cardinality, atomicity, and lifecycle edges inspected.

## Priority

End with the most valuable next action, referring to the reported items without repeating their analysis. A recommendation to keep the current implementation must satisfy the prerequisites in [No Findings](#no-findings); when missing evidence materially affects the conclusion, prioritize the check needed to resolve it. Do not treat optional improvements as release blockers or infer approval to implement them.
