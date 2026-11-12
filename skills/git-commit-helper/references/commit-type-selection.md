# Commit Type Selection

Use this guide to classify the selected change set by its primary intent. Follow the [skill's format policy](../SKILL.md#conventional-commits-contract); apply Conventional Commits syntax only when that format is selected.

## Type Mapping

Use these common classifications when applicable to the selected format and repository conventions.

- `feat`: introduces a new user-facing or developer-facing capability.
- `fix`: corrects incorrect behavior, regression, data bug, validation gap, or runtime failure.
- `refactor`: changes structure without changing intended behavior.
- `perf`: materially improves latency, throughput, memory, query shape, or resource usage.
- `docs`: changes documentation only.
- `test`: adds or updates tests without changing production behavior.
- `ci`: changes CI workflows, pipelines, or automation config.
- `build`: changes build system, packaging, bundling, or dependency build tooling.
- `chore`: repository maintenance that does not fit better elsewhere.
- `style`: formatting or non-semantic code style changes only.
- `revert`: explicitly reverts a prior commit.

Under the specification's SemVer mapping, a non-breaking `fix` corresponds to PATCH, a non-breaking `feat` to MINOR, and a breaking change of any type to MAJOR. Other types have no implicit version effect. This classification does not authorize a release, tag, version edit, or publication; actual release behavior depends on project tooling and policy.

## Scope Selection

These are writing suggestions, not additional syntax requirements.

- Use a scope only when it adds real signal, such as `auth`, `api`, `db`, `ui`, `config`, `vector`, or a bounded module name.
- Prefer the narrowest stable module or subsystem name.
- Omit scope when no meaningful codebase area describes the change. Touching multiple modules alone does not require omitting a shared scope.

## Subject Rules

The imperative style and punctuation guidance below are skill defaults, not additional specification requirements. Follow applicable user or repository writing conventions.

- Use imperative mood.
- Keep it short and concrete.
- Describe what changed, not why the person changed it.
- Follow the skill's language policy.
- Do not end the subject with punctuation.
- Honor actual repository length limits; Conventional Commits does not mandate a 50/72-character limit.

## Body Rules

The body is optional and free-form; it may have any number of paragraphs. Include it when requested or when it adds useful context, for example:

- the diff has tightly related subchanges worth explaining
- the rationale or previous behavior helps readers understand the change
- rollout or compatibility detail matters
- the subject alone would hide an important behavior change

Body guidance:

- use bullets for parallel subchanges or independently useful facts; use concise prose for a connected rationale, following the user's requested format and applicable repository convention
- each bullet should capture one subchange or one piece of critical context
- keep bullets concise
- do not restate the subject verbatim

## Footer Rules

- A footer uses a word token followed by `: ` or ` #` and a string value, for example `Refs: #123` or `Closes #123`.
- Replace whitespace in tokens with hyphens, as in `Reviewed-by`. The uppercase `BREAKING CHANGE` token is the exception. Values may span lines until the next valid footer token/separator pair.
- Follow the main contract for breaking-change markers; include known migration steps when useful.
- Include issue references only when known and appropriate. In particular, use a closing keyword such as `Closes` only when the change resolves the referenced issue; use `Refs` for an association.
- For reverts, include the verified reverted commit reference when available. Conventional Commits does not prescribe revert semantics; use the repository's tooling convention for its body/footer rather than assuming an automatic version effect.

## Edge Cases

### Mixed staged changes

- Recommend splitting the commit or restaging before committing.

### Dependency updates

- Use `build` when the change is packaging or build-tool related.
- Use `chore` for routine dependency maintenance when no better type applies.
- Use `fix` or `feat` if the dependency change is part of a functional fix or feature and the diff clearly shows that intent.

### Generated files

- Classify by the source change, not by the generated artifact alone.
- If only generated output changed and source intent is unknown, say that confidence is limited.

### Test and docs with code changes

- Choose the type based on the primary production change, not the supporting tests or docs.

## Recommended Output Bias

- Prefer one strong recommendation over several equally plausible messages.
- Use a concise assumption for low-risk classification or wording choices. Do not use an assumption to resolve authorization or commit-scope ambiguity; follow the Skill's clarification boundary.
