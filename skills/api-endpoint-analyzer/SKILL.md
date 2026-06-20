---
name: api-endpoint-analyzer
description: 基于代码、schema、运行时配置、测试和 API 规范，分析一个或多个 HTTP、REST、RPC、webhook 或流式端点的契约、调用链、业务分支、side effects 和错误行为。当 Codex 需要解释或评审接口、核对 OpenAPI/Swagger、排查接口异常，或回答依赖 API 入口、请求上下文、跨服务调用、状态变更、异步任务、缓存或持久化行为的业务问题时使用；即使用户未明确要求分析接口，只要问题的关键证据位于 endpoint 调用链，也应使用。纯领域算法、纯数据库或与 API 边界无关的问题不使用。
---

# API Endpoint Analyzer

## Purpose

Turn scattered endpoint artifacts into a concise, evidence-backed analysis of request contract, response contract, execution flow, side effects, and error behavior. Use one or more endpoint call paths when a business question crosses request, job, event, or webhook boundaries. Prefer runnable code and generated contracts over comments or prose docs. Separate verified facts from inference.

This is an analysis skill by default: read and explain. Do not edit code, schemas, tests, or docs unless the user explicitly asks for changes.

## Analysis Modes

- **Endpoint analysis mode**: Use when the user explicitly asks to explain, document, compare, troubleshoot, or review an API endpoint. Cover the endpoint contract and behavior at the requested depth.
- **Business-question mode**: Use when the user asks a business or system behavior question whose answer depends on an API boundary or downstream endpoint call path. Answer the business question first, then include only the contract, flow, side effects, errors, and evidence needed to support that answer.
- Do not force an endpoint-shaped report when the endpoint is only supporting evidence for a broader business question. Stop using this skill's workflow when the question is purely about domain algorithms, database internals, or behavior unrelated to an API boundary.

## Analysis Depth

- If the user asks for a quick endpoint explanation, provide a compact summary with request, response, main flow, and notable errors.
- If the user explicitly asks for a full endpoint analysis, compatibility check, OpenAPI comparison, or API review, use the full template in [references/endpoint-analysis-template.md](./references/endpoint-analysis-template.md).
- For business questions and targeted troubleshooting, lead with the direct answer, root cause, or decision path, then include only the relevant endpoint evidence and unresolved checks.
- If artifacts are incomplete or the call path is unclear, use [references/source-tracing-checklist.md](./references/source-tracing-checklist.md).
- If only docs/specs are available, analyze the declared contract and mark implementation behavior as `未验证`.

## Workflow

1. Frame the question and identify the relevant API boundary.
   - Restate the concrete behavior, symptom, decision, or risk that must be explained.
   - Decide whether the endpoint is the primary subject or supporting evidence for a broader business question.
   - When no endpoint is given, locate candidate boundaries from UI actions, service names, logs, errors, domain operations, jobs, events, or downstream calls.
   - Trace multiple endpoints or asynchronous continuations when behavior crosses request boundaries. Stop tracing unrelated branches once the question has enough evidence.

2. Locate the endpoint entry.
   - Search by path, method, route name, operation id, handler name, RPC method, or webhook topic.
   - Confirm versioned routers, decorators, generated routes, middleware, and mounted prefixes before naming the final endpoint.

3. Establish the contract.
   - Record method/path, content type, auth, permissions, idempotency, sync/async behavior, pagination, streaming, uploads/downloads, and version constraints.
   - Extract explicit inputs from path, query, headers, cookies, body, form/multipart fields, and files.
   - Identify implicit inputs from auth context, tenant context, dependency injection, middleware, feature flags, environment defaults, and server-generated values.

4. Trace the implementation.
   - Follow router -> handler/controller -> service/use case -> domain logic -> repository/gateway/external clients.
   - Capture validation, authorization, branching, transactions, retries, fallbacks, state transitions, side effects, async jobs, events, and cache behavior.
   - Note consistency semantics: immediate write/read, eventual consistency, compensation, timeout, cancellation, and partial failure behavior.

5. Reconstruct outputs.
   - Enumerate success status codes, response schemas, conditional fields, wrappers, headers, cookies, pagination metadata, redirects, files, or stream events.
   - Enumerate reachable failures: validation, auth, permission, not found, conflict, rate limit, dependency failure, timeout, cancellation, and framework defaults.
   - Distinguish documented errors from implementation-reachable errors.

6. Report with evidence.
   - Include local file/function references when code is available.
   - Mark unverified conclusions as `推断` or `未验证`.
   - If docs/specs and code disagree, report both and identify the likely source of truth.

## Evidence Order

Use this priority order when sources disagree:

1. Runtime route configuration and handler code
2. Request and response schema definitions
3. Service, domain, repository, and integration code
4. Automated tests and fixtures
5. OpenAPI, Swagger, protobuf, or other generated specs
6. Comments, README files, and issue discussions
7. Inference from framework conventions

Treat actual requests, responses, logs, traces, metrics, and deployed configuration as observed execution evidence. Record the environment, version, timestamp, request identity, and configuration scope when known. Use an observation to prove what happened for that execution, not as proof of the general contract. Check for environment or version differences before treating runtime evidence and source artifacts as contradictory.

## Output Rules

- Match the output depth to the user's request; do not force the full template for a small question.
- In business-question mode, lead with the answer, root cause, or decision path; use endpoint details as supporting evidence rather than the report structure.
- Keep facts, inference, and open questions separate.
- Prefer tables for parameter and error enumeration.
- Include Mermaid only when explaining a non-trivial flow; keep diagrams focused on business branches, not framework boilerplate.
- Always call out auth, idempotency, side effects, external dependencies, persistence changes, and cache behavior when present.
- For mutating endpoints, state what is written, emitted, queued, invalidated, or called externally.
- For multi-backend reads, state consistency expectations and failure propagation.
- Do not invent field types, status codes, validation rules, side effects, or security behavior.
- Avoid generic advice unless tied to evidence from the relevant endpoint call path.

## Special Cases

### OpenAPI or Swagger only

- Analyze the declared contract.
- Call out that implementation paths, hidden side effects, and real exception branches are not verified.

### File upload or multipart endpoints

- Record content type, file field names, size and type validation, storage destination, and cleanup behavior.

### Streaming, SSE, websocket, or async-job endpoints

- Explain connection lifecycle, event payload shape, completion semantics, retry behavior, and timeout or cancellation handling.

### Webhooks

- Explain signature verification, replay protection, idempotency strategy, downstream fan-out, and failure acknowledgement semantics.

### RPC or protobuf APIs

- Identify service/method, request and response messages, field presence/default semantics, metadata, auth interceptors, deadlines, streaming mode, and mapped error codes.

### API reviews

- Lead with concrete findings: contract breaks, auth or tenant gaps, unsafe side effects, data consistency risks, missing error mapping, N+1/unbounded reads, and meaningful test gaps.
- Separate design suggestions from correctness issues.

## References

- Read [references/endpoint-analysis-template.md](./references/endpoint-analysis-template.md) for the default report structure and Mermaid example.
- Read [references/source-tracing-checklist.md](./references/source-tracing-checklist.md) when artifacts are incomplete or the endpoint spans middleware, services, and external systems.
