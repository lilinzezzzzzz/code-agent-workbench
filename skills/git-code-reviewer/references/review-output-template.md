# Review Output Template

Put findings first. Preserve findings, supporting evidence, scope, verification results, and material caveats. Omit repeated summaries, generic praise, empty sections, and background that does not change the conclusion.

## Findings

Order findings by severity, then impact. Use one item per root cause:

A finding must connect a specific change to a reachable trigger, an incorrect outcome or concrete risk, and inspected evidence. Static reasoning can establish a finding without an executed reproduction. If the core trigger or causal link is only hypothetical, use Open Questions instead. Cite the smallest relevant code location in the reviewed version, rather than an entire function or file.

```text
1. [high] Concise defect title
   - Trigger: reachable condition under which the changed behavior fails
   - Evidence: inspected file and line, configuration, schema, test, or command output
   - Impact: direct user, data, compatibility, security, or operational consequence
   - Recommendation: smallest reasonable correction or follow-up
   - Verification limits: optional detail not established, such as the full impact extent
```

Assess severity using impact, affected scope, triggering conditions, and recoverability. These examples are guides, not keyword-based assignments; a race is not automatically high, nor every outage critical.

| Level | Meaning |
| --- | --- |
| `critical` | Security breach, auth bypass, data loss or corruption, irreversible migration failure, or outage |
| `high` | User-visible bug, contract break, race, unsafe rollback, or major failure-path gap |
| `medium` | Missing validation, error-handling gap, performance regression, observability gap, or test gap hiding concrete risk |
| `low` | Changed-path maintainability issue that materially increases future defect risk |

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

If there are no findings, say so explicitly and report only material verification gaps or residual risks. For Redis or stateful changes, name the relevant cardinality, atomicity, and lifecycle edges inspected.
