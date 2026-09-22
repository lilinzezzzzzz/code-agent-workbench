# RAG And Retrieval Rules

Use these rules for retrieval and knowledge-index behavior, including systems
without generation. Model/provider calls, prompts, structured output, and tool
calling belong to `ai/applications.md`; load it only when those behaviors are
in scope. Ordinary SQL queries and embeddings unrelated to retrieval do not
by themselves require this reference.

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

## Retrieval Reliability And Observability

- Bound ingestion and retrieval timeouts, retries, batch sizes, concurrency,
  and resource budgets according to the pipeline's failure modes. Make retries
  safe for index writes and do not multiply retries across pipeline layers.
- Retrieval cache identity must account for the query, index and embedding
  versions, retrieval/reranking parameters, filters, authorization scope, and
  freshness. Invalidate affected entries after document or permission changes;
  protect sensitive cached content.
- Record ingestion/index versions, retrieval stages, candidate counts, latency,
  failures, and source identifiers where permitted, with approved redaction.
  Do not log credentials, personal data, or full retrieved content by default.
- Define empty-result, stale-index, partial-retrieval, and fallback behavior.
  Reduced retrieval or stale evidence must not silently claim equivalent
  quality, freshness, or completion.

## Retrieval Evaluation And Change Safety

- Maintain representative queries and evidence judgments for relevant domains,
  languages, ambiguous queries, no-answer cases, and permission boundaries.
  Measure retrieval relevance or recall with task-appropriate metrics.
- For end-to-end RAG, evaluate retrieval and generation separately, then verify
  answer support and citation validity against the retrieved evidence. Use
  human review where automated judgment is insufficient.
- Compare embedding, chunking, reranking, and index changes against a stable
  baseline. Do not approve a material change from anecdotal examples alone.
- Test cross-tenant retrieval, document permission changes, deleted or stale
  content, interrupted ingestion, partial index writes, retries, and retrieval
  degradation on critical paths. Retrieved documents are untrusted evidence;
  embedded instructions must not alter retrieval permissions or tool authority.
- Roll out material retrieval changes with observable index/version identity,
  bounded exposure, rollback, and compatibility for in-flight ingestion jobs,
  stored embeddings, and consumers when applicable.
