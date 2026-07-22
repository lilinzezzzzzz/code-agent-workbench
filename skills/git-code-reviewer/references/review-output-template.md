# Review Output Template

Put findings first. Preserve findings, supporting evidence, scope, verification results, and material caveats. Omit repeated summaries, generic praise, empty sections, and background that does not change the conclusion.

## Findings

Order findings by severity, then impact. Use one item per root cause:

```text
1. [high] Concise defect title
   - Evidence: inspected file and line, configuration, schema, test, or command output
   - Impact: direct user, data, compatibility, security, or operational consequence
   - Recommendation: smallest reasonable correction or follow-up
   - Unverified: optional assumption on which the impact depends
```

Use these severity levels:

| Level | Meaning |
| --- | --- |
| `critical` | Security breach, auth bypass, data loss or corruption, irreversible migration failure, or outage |
| `high` | User-visible bug, contract break, race, unsafe rollback, or major failure-path gap |
| `medium` | Missing validation, error-handling gap, performance regression, observability gap, or test gap hiding concrete risk |
| `low` | Changed-path maintainability issue that materially increases future defect risk |

## Scope

Always state:

- Review artifact or comparison range.
- User-provided base and exact resolved ref.
- Whether the ref is remote-tracking, local, or another explicit ref.
- Fetch status and base commit SHA, or the approved cached-ref downgrade and freshness warning.
- Included and excluded workspace changes when relevant.

## Verification

State commands or checks that ran and their observed outcomes. If none ran, say the review was limited to static inspection. State skipped or blocked checks only when they leave material risk.

## Open Questions

Put plausible but unverified concerns here. Do not present them as confirmed findings.

## No Findings

If there are no findings, say so explicitly and report only material verification gaps or residual risks. For Redis or stateful changes, name the relevant cardinality, atomicity, and lifecycle edges inspected.
