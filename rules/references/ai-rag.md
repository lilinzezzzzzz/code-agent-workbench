---
trigger: model_decision
description: Load for LLM or multimodal applications, prompts, structured output, tool calling, agents, embeddings, retrieval, vector search, reranking, RAG ingestion, evaluation, model safety, latency, or cost.
---
# AI And RAG Rules

Use these rules for language-independent AI application and RAG behavior.
Treat model output and retrieved content as untrusted, nondeterministic input;
correctness must come from explicit contracts, validation, authorization, and
measured evaluation rather than a single successful example.

## Model And Prompt Contracts

- Define the task, input/output schema, tool surface, model configuration,
  token budget, latency target, cost budget, and failure behavior before
  integrating a model call.
- Keep system instructions, prompt templates, tool schemas, and evaluation
  cases versioned with the implementation. Avoid hiding critical business
  rules only in an untracked prompt or provider dashboard.
- Validate structured output before domain use, persistence, or side effects.
  Handle refusal, truncation, malformed output, missing fields, unsupported
  content, and schema-version mismatch explicitly.
- Treat prompt text, retrieved documents, user files, web content, and model
  output as untrusted data. Do not let embedded instructions override system
  policy, authorization, tenant boundaries, or tool constraints.
- Tool calls require schema validation, resource-level authorization,
  idempotency where side effects can repeat, and explicit limits. Do not grant
  a model broader credentials or tools than the current task needs.

## Retrieval And Indexing

- Define ingestion ownership, supported formats, parsing, chunking, metadata,
  deduplication, embedding model, index version, and deletion/update behavior.
  Make re-indexing resumable and observable.
- Apply tenant and document permissions before content enters the model
  context. Post-filtering unauthorized retrieval is not an acceptable primary
  access-control boundary.
- Preserve source identity and enough provenance to attribute answers and debug
  retrieval. Do not fabricate citations for content absent from retrieved
  evidence.
- Bound candidate count, context size, document size, and memory. Choose dense,
  sparse, hybrid, metadata filtering, and reranking from measured retrieval
  quality rather than applying one strategy universally.
- Define freshness and consistency for changed or deleted content. Coordinate
  source updates, embedding generation, index writes, cache invalidation, and
  rollback so stale or orphaned chunks are detectable.

## Reliability, Cost, And Observability

- Set end-to-end timeout, retry, rate-limit, concurrency, streaming
  cancellation, and fallback behavior. Retry only safe transient failures and
  avoid multiplying retries across application, SDK, and gateway layers.
- Bound tokens, context, output length, batch size, parallel requests, and
  per-request or per-job cost. Reject or degrade oversized work explicitly
  rather than allowing unbounded provider spend.
- Cache only when model, prompt, parameters, tool schema, retrieval inputs,
  authorization scope, and freshness are represented in the cache key. Protect
  sensitive cached content and define invalidation.
- Record model/provider, model identifier, prompt/index version, token usage,
  latency, retries, tool outcomes, and failure category with approved
  redaction. Do not log secrets, credentials, private prompts, personal data,
  or full retrieved content by default.
- Define fallback semantics explicitly. A cheaper model, stale cache, empty
  retrieval, or non-AI heuristic must not silently claim equivalent quality or
  completion.

## Evaluation And Change Safety

- Maintain representative evaluation cases for normal, edge, adversarial,
  multilingual, long-context, permission, and no-answer behavior as applicable.
- Evaluate retrieval and generation separately. Measure retrieval relevance or
  recall, answer correctness and groundedness, citation validity, tool success,
  latency, and cost using task-appropriate metrics and human review where
  automated judgment is insufficient.
- Compare prompt, model, embedding, chunking, reranking, and index changes
  against a stable baseline. Do not approve a material change from anecdotal
  examples alone.
- Test prompt injection, data exfiltration, cross-tenant retrieval, unsafe tool
  arguments, duplicate side effects, malformed provider output, timeout,
  cancellation, and provider degradation on critical paths.
- Roll out material model or retrieval changes with observable versioning,
  bounded exposure, rollback, and compatibility for in-flight jobs or stored
  artifacts when applicable.
