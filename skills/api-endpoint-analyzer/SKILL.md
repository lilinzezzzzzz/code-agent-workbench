---
name: api-endpoint-analyzer
description: 基于代码、schema、测试、运行时证据和 API 规范，分析 HTTP/REST、RPC、webhook、流式或异步 API 的契约、调用链、业务分支、side effects 与错误行为。用于解释、评审、对照规范或排查 endpoint，以及回答关键证据位于 API boundary、跨服务调用或后续 job/event/webhook 链路中的业务问题；纯领域算法、纯数据库内部或与 API 边界无关的问题不使用。
---

# API Endpoint Analyzer

## Objective

Answer the user's actual endpoint or business-behavior question with evidence from contracts, implementation paths, tests, runtime artifacts, and configuration. Cover request, response, execution flow, side effects, consistency, and failures only to the depth needed by the request.

When behavior crosses request boundaries, trace the relevant downstream endpoint, job, event, stream, or webhook continuation. Separate verified facts, inference, and unresolved questions.

## Authorization

For explanation, review, diagnosis, or planning requests, inspect relevant local files, diffs, schemas, configuration, tests, logs, and other available evidence. Run relevant non-destructive diagnostics when needed.

Do not edit code, schemas, tests, documentation, or external systems unless the user explicitly asks for changes.

## Workflow

1. Define the question and boundary.
   - Identify the concrete behavior, symptom, decision, compatibility concern, or risk to explain.
   - Decide whether the endpoint is the primary subject or supporting evidence for a broader business question.
   - If no endpoint is given, locate candidate boundaries from paths, UI actions, service names, logs, errors, domain operations, jobs, events, or downstream calls.
   - Follow cross-boundary continuations only while they materially affect the answer.

2. Locate the active entry point.
   - Search by method/path, route name, operation id, handler, RPC method, webhook topic, or stream entry.
   - Confirm mounted prefixes, versioned or generated routers, decorators, middleware, gateways, and registration order before naming the endpoint.

3. Establish the contract.
   - Record method/path, media types, auth, resource- or tenant-level permissions, idempotency, version constraints, and sync, async, or streaming semantics.
   - Extract explicit inputs from path, query, headers, cookies, body, form or multipart fields, and files.
   - For fields, capture type, requiredness, nullability, defaults, aliases, enums, coercion, and validation when evidenced.
   - Identify implicit inputs from identity or tenant context, middleware, dependency injection, feature flags, environment defaults, and server-generated values.

4. Trace reachable behavior.
   - Follow route or transport registration through handler/controller, service/use case, domain logic, repository/gateway, external clients, and asynchronous continuations.
   - Capture material validation, authorization, branches, state transitions, transactions, locks, retries, fallbacks, compensation, timeout, cancellation, and partial failures.
   - Identify reads, writes, external calls, emitted events, queued jobs, notifications, object storage operations, and cache reads or invalidations.

5. Reconstruct outputs and failures.
   - Enumerate evidenced success statuses, response schemas, conditional fields, wrappers, headers, cookies, pagination metadata, redirects, files, and stream events.
   - Enumerate reachable validation, auth, permission, tenant, not-found, conflict, quota, rate-limit, dependency, timeout, cancellation, and framework-default failures.
   - Distinguish documented errors from implementation-reachable errors.

6. Resolve uncertainty and stop.
   - Stop when the user's core question is answered, material claims have evidence, conflicts are exposed, and remaining unknowns are labeled.
   - Ask only when an ambiguity cannot be resolved from available artifacts and would materially change the conclusion.
   - Otherwise state the assumption, missing evidence, affected conclusion, and smallest useful next check.

## Evidence Contract

Classify evidence before resolving disagreements:

- **Observed execution**: Actual requests, responses, logs, traces, metrics, and deployed configuration. Record environment, version, timestamp, request identity, and configuration scope when known. An observation proves that execution, not the general contract.
- **Implementation-reachable behavior**: Active route configuration, middleware, handlers, schemas, services, repositories, integrations, and workers. Prefer artifacts that directly control the path being analyzed.
- **Declared contract**: OpenAPI, Swagger, protobuf, generated specifications, and maintained API documentation. Treat these as advertised expectations, not proof of implementation behavior.
- **Tests and fixtures**: Evidence of expected or covered behavior, not proof of deployed behavior.
- **Context and inference**: Comments, README files, issues, and framework conventions. Use them only as supporting context and label inference explicitly.

When sources disagree, report each representation and its impact instead of silently reconciling them. Use observed evidence for what happened in a specific execution, implementation evidence for generally reachable behavior, and the declared contract for compatibility expectations.

Call a conclusion `root cause` only when the evidence supports the causal path. Otherwise label it `可能原因`, `推断`, or `未验证` and give the minimum confirming check.

## Conditional Coverage

Apply only the checks relevant to the endpoint:

- **Mutations and multi-backend reads**: State writes, emitted or queued work, external calls, cache invalidation, transaction boundaries, consistency expectations, and failure propagation.
- **File upload or multipart**: Record field names, media type, size and type validation, storage destination, and cleanup after failure.
- **Streaming, SSE, websocket, or async job**: Explain lifecycle, event payloads, completion semantics, retry, timeout, cancellation, and reconnect or polling behavior.
- **Webhook**: Explain signature verification, replay protection, idempotency, acknowledgement semantics, retries, and downstream fan-out.
- **RPC or protobuf**: Identify service/method, messages, presence and default semantics, metadata, interceptors, deadlines, streaming mode, and mapped errors.

## Output Contract

Match the answer to the task:

- **Brief endpoint explanation**: Include the request, response, main execution path, notable failures, and material caveats.
- **Business question or troubleshooting**: Lead with the direct answer, supported cause or decision path, relevant endpoint evidence, and unresolved checks. Do not force an endpoint-shaped report.
- **Compatibility, OpenAPI comparison, or API review**: Lead with concrete findings in severity order. Compare the available declared, implemented, and observed representations; state impact and confidence. Separate correctness or compatibility issues from design suggestions.
- **Comprehensive endpoint documentation**: Cover request, response, flow, errors, side effects, consistency, and evidence using the full template.
- **Docs or specification only**: Analyze the declared contract and mark implementation paths, hidden side effects, and real exception behavior as `未验证`.

For important conclusions, cite a repository-relative `path:line` or `path:symbol` when available. Always surface material auth or tenant behavior, idempotency, state changes, external dependencies, persistence or cache effects, consistency, and failure propagation when present.

Use tables when repeated parameter, field, error, or comparison mappings become clearer. Use Mermaid only for non-trivial flows or branches. Do not invent fields, types, status codes, validation, security behavior, side effects, or runtime results. Avoid generic advice not tied to the analyzed path.

## Resource Routing

- Read [references/endpoint-analysis-template.md](./references/endpoint-analysis-template.md) only for comprehensive endpoint documentation or when the user explicitly requests that structure.
- Read [references/source-tracing-checklist.md](./references/source-tracing-checklist.md) when implementation artifacts are expected but incomplete, generated, distributed across layers, or the active path remains unclear. Do not load it when the user intentionally limits the task to docs/specs or implementation artifacts are confirmed unavailable.
