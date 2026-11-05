# Code Quality Review Checklist

Use the relevant questions to assess the changed implementation and its direct effects within the selected review snapshot. Expand into an existing problem only when the change worsens or depends on it. This is a thinking aid, not a requirement to find a problem in each category.

## 1. Control Flow and State

- Do deep nesting, repeated conditions, scattered special cases, or distant state mutations make supported execution paths hard to follow?
- Are flags, mutable variables, intermediate results, and separately tracked states necessary, or can they diverge from information already available?
- Would guard clauses, explicit preconditions, or merging equivalent branches make the flow clearer? Preserve condition precedence, mutual exclusion, evaluation order, and side effects.

## 2. Responsibilities and Abstraction

- Does a function, class, or module combine unrelated responsibilities that change for different business reasons?
- Does an abstraction establish a useful semantic boundary, or merely add navigation, forwarding, and concepts to understand?
- Keep simple logic used at one call site at that site by default. Recommend extraction when a named boundary materially improves reading, isolates a responsibility, enforces an invariant, or satisfies an interface; single use alone is not a reason to inline a useful boundary.
- Do frameworks, configuration options, extension points, wrappers, or design patterns serve actual callers and supported requirements, or only speculative future reuse?

## 3. Naming and Expression

- Do names convey business meaning, the nature of the data, operation results, and side effects? Identify ambiguous names, excessive abbreviations, unclear boolean semantics, or names that disagree with behavior.
- Do dense one-liners, complex comprehensions, implicit conversions, or clever constructs hide decisions or failure paths? Prefer a straightforward expression when it makes the logic easier to follow.
- Do comments explain necessary context, constraints, and reasons, and do they still match the code?

## 4. Duplication and Consistency

- Does duplicated logic encode the same business rule and need to evolve together? Identify a concrete change that would require synchronized edits and could be missed before recommending consolidation.
- Are apparently similar blocks different business rules or likely to evolve independently? Preserve their boundaries when sharing would introduce coupling or extra switches.
- Are repeated calculations, redundant conversions, unnecessary wrappers, or confirmed unused code adding cost without a purpose? Do not assume repeated operations are equivalent when their timing, inputs, or side effects differ.

## 5. Dependencies and Cost of Change

- Are inputs, outputs, dependencies, and side effects explicit enough to understand the behavior at the relevant boundary?
- Does the path depend on hidden global state, call order, implicit initialization, or details owned by another layer?
- For a representative business change, which locations must be understood and edited together? Does the structure make inconsistent updates or fault diagnosis likely?
- Can important logic be understood and verified independently? If verification is difficult, identify the responsibility or dependency causing it rather than treating testability alone as proof of a design defect.

## Assess a Proposed Improvement

- Compare the concrete maintenance benefit with added indirection, coupling, migration work, and behavior risk. A local adjustment should be the default; a larger refactor needs a clear benefit and conditions under which it is worthwhile.
- Apply the evidence and preservation checks in [SKILL.md, Validate Conclusions](../SKILL.md#3-validate-conclusions). When usage or equivalence is uncertain, identify the missing evidence and the smallest check needed instead of recommending unconditional removal or merging.
