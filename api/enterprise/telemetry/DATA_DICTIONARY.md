# NexusAI Enterprise Telemetry Data Dictionary

Quick reference for all telemetry signals emitted by NexusAI Enterprise. For configuration and architecture details, see [README.md](./README.md).

## Resource Attributes

Attached to every signal (Span, Metric, Log).

| Attribute | Type | Example |
|-----------|------|---------|
| `service.name` | string | `nexusai` |
| `host.name` | string | `nexusai-api-7f8b` |

## Traces (Spans)

### `nexusai.workflow.run`

| Attribute | Type | Description |
|-----------|------|-------------|
| `nexusai.trace_id` | string | Business trace ID (Workflow Run ID) |
| `nexusai.tenant_id` | string | Tenant identifier |
| `nexusai.app_id` | string | Application identifier |
| `nexusai.workflow.id` | string | Workflow definition ID |
| `nexusai.workflow.run_id` | string | Unique ID for this run |
| `nexusai.workflow.status` | string | `succeeded`, `failed`, `stopped`, etc. |
| `nexusai.workflow.error` | string | Error message if failed |
| `nexusai.workflow.elapsed_time` | float | Total execution time (seconds) |
| `nexusai.invoke_from` | string | `api`, `webapp`, `debug` |
| `nexusai.conversation.id` | string | Conversation ID (optional) |
| `nexusai.message.id` | string | Message ID (optional) |
| `nexusai.invoked_by` | string | User ID who triggered the run |
| `gen_ai.usage.total_tokens` | int | Total tokens across all nodes (optional) |
| `gen_ai.user.id` | string | End-user identifier (optional) |
| `nexusai.parent.trace_id` | string | Parent workflow trace ID (optional) |
| `nexusai.parent.workflow.run_id` | string | Parent workflow run ID (optional) |
| `nexusai.parent.node.execution_id` | string | Parent node execution ID (optional) |
| `nexusai.parent.app.id` | string | Parent app ID (optional) |

### `nexusai.node.execution`

| Attribute | Type | Description |
|-----------|------|-------------|
| `nexusai.trace_id` | string | Business trace ID |
| `nexusai.tenant_id` | string | Tenant identifier |
| `nexusai.app_id` | string | Application identifier |
| `nexusai.workflow.id` | string | Workflow definition ID |
| `nexusai.workflow.run_id` | string | Workflow Run ID |
| `nexusai.message.id` | string | Message ID (optional) |
| `nexusai.conversation.id` | string | Conversation ID (optional) |
| `nexusai.node.execution_id` | string | Unique node execution ID |
| `nexusai.node.id` | string | Node ID in workflow graph |
| `nexusai.node.type` | string | Node type (see appendix) |
| `nexusai.node.title` | string | Display title |
| `nexusai.node.status` | string | `succeeded`, `failed` |
| `nexusai.node.error` | string | Error message if failed |
| `nexusai.node.elapsed_time` | float | Execution time (seconds) |
| `nexusai.node.index` | int | Execution order index |
| `nexusai.node.predecessor_node_id` | string | Triggering node ID |
| `nexusai.node.iteration_id` | string | Iteration ID (optional) |
| `nexusai.node.loop_id` | string | Loop ID (optional) |
| `nexusai.node.parallel_id` | string | Parallel branch ID (optional) |
| `nexusai.node.invoked_by` | string | User ID who triggered execution |
| `gen_ai.usage.input_tokens` | int | Prompt tokens (LLM nodes only) |
| `gen_ai.usage.output_tokens` | int | Completion tokens (LLM nodes only) |
| `gen_ai.usage.total_tokens` | int | Total tokens (LLM nodes only) |
| `gen_ai.request.model` | string | LLM model name (LLM nodes only) |
| `gen_ai.provider.name` | string | LLM provider name (LLM nodes only) |
| `gen_ai.user.id` | string | End-user identifier (optional) |

### `nexusai.node.execution.draft`

Same attributes as `nexusai.node.execution`. Emitted during Preview/Debug runs.

## Counters

All counters are cumulative and emitted at 100% accuracy.

### Token Counters

| Metric | Unit | Description |
|--------|------|-------------|
| `nexusai.tokens.total` | `{token}` | Total tokens consumed |
| `nexusai.tokens.input` | `{token}` | Input (prompt) tokens |
| `nexusai.tokens.output` | `{token}` | Output (completion) tokens |

**Labels:**

- `tenant_id`, `app_id`, `operation_type`, `model_provider`, `model_name`, `node_type` (if node_execution)

⚠️ **Warning:** `nexusai.tokens.total` at workflow level includes all node tokens. Filter by `operation_type` to avoid double-counting.

#### Token Hierarchy & Query Patterns

Token metrics are emitted at multiple layers. Understanding the hierarchy prevents double-counting:

```
App-level total
├── workflow          ← sum of all node_execution tokens (DO NOT add both)
│   └── node_execution ← per-node breakdown
├── message           ← independent (non-workflow chat apps only)
├── rule_generate     ← independent helper LLM call
├── code_generate     ← independent helper LLM call
├── structured_output ← independent helper LLM call
└── instruction_monexusai← independent helper LLM call
```

**Key rule:** `workflow` tokens already include all `node_execution` tokens. Never sum both.

**Available labels on token metrics:** `tenant_id`, `app_id`, `operation_type`, `model_provider`, `model_name`, `node_type`.
App name is only available on span attributes (`nexusai.app.name`), not metric labels — use `app_id` for metric queries.

**Common queries** (PromQL):

```promql
# ── Totals ──────────────────────────────────────────────────
# App-level total (exclude node_execution to avoid double-counting)
sum by (app_id) (nexusai_tokens_total{operation_type!="node_execution"})

# Single app total
sum (nexusai_tokens_total{app_id="<app_id>", operation_type!="node_execution"})

# Per-tenant totals
sum by (tenant_id) (nexusai_tokens_total{operation_type!="node_execution"})

# ── Drill-down ──────────────────────────────────────────────
# Workflow-level tokens for an app
sum (nexusai_tokens_total{app_id="<app_id>", operation_type="workflow"})

# Node-level breakdown within an app
sum by (node_type) (nexusai_tokens_total{app_id="<app_id>", operation_type="node_execution"})

# Model breakdown for an app
sum by (model_provider, model_name) (nexusai_tokens_total{app_id="<app_id>"})

# Input vs output per model
sum by (model_name) (nexusai_tokens_input_total{app_id="<app_id>"})
sum by (model_name) (nexusai_tokens_output_total{app_id="<app_id>"})

# ── Rates ───────────────────────────────────────────────────
# Token consumption rate (per hour)
sum(rate(nexusai_tokens_total{operation_type!="node_execution"}[1h]))

# Per-app consumption rate
sum by (app_id) (rate(nexusai_tokens_total{operation_type!="node_execution"}[1h]))
```

**Finding `app_id` from app name** (trace query — Tempo / Jaeger):

```
{ resource.nexusai.app.name = "My Chatbot" } | select(resource.nexusai.app.id)
```

### Request Counters

| Metric | Unit | Description |
|--------|------|-------------|
| `nexusai.requests.total` | `{request}` | Total operations count |

**Labels by type:**

| `type` | Additional Labels |
|--------|-------------------|
| `workflow` | `tenant_id`, `app_id`, `status`, `invoke_from` |
| `node` | `tenant_id`, `app_id`, `node_type`, `model_provider`, `model_name`, `status` |
| `draft_node` | `tenant_id`, `app_id`, `node_type`, `model_provider`, `model_name`, `status` |
| `message` | `tenant_id`, `app_id`, `model_provider`, `model_name`, `status`, `invoke_from` |
| `tool` | `tenant_id`, `app_id`, `tool_name` |
| `moderation` | `tenant_id`, `app_id` |
| `suggested_question` | `tenant_id`, `app_id`, `model_provider`, `model_name` |
| `dataset_retrieval` | `tenant_id`, `app_id` |
| `generate_name` | `tenant_id`, `app_id` |
| `prompt_generation` | `tenant_id`, `app_id`, `operation_type`, `model_provider`, `model_name`, `status` |

### Error Counters

| Metric | Unit | Description |
|--------|------|-------------|
| `nexusai.errors.total` | `{error}` | Total failed operations |

**Labels by type:**

| `type` | Additional Labels |
|--------|-------------------|
| `workflow` | `tenant_id`, `app_id` |
| `node` | `tenant_id`, `app_id`, `node_type`, `model_provider`, `model_name` |
| `draft_node` | `tenant_id`, `app_id`, `node_type`, `model_provider`, `model_name` |
| `message` | `tenant_id`, `app_id`, `model_provider`, `model_name` |
| `tool` | `tenant_id`, `app_id`, `tool_name` |
| `prompt_generation` | `tenant_id`, `app_id`, `operation_type`, `model_provider`, `model_name` |

### Other Counters

| Metric | Unit | Labels |
|--------|------|--------|
| `nexusai.feedback.total` | `{feedback}` | `tenant_id`, `app_id`, `rating` |
| `nexusai.dataset.retrievals.total` | `{retrieval}` | `tenant_id`, `app_id`, `dataset_id`, `embedding_model_provider`, `embedding_model`, `rerank_model_provider`, `rerank_model` |
| `nexusai.app.created.total` | `{app}` | `tenant_id`, `app_id`, `mode` |
| `nexusai.app.updated.total` | `{app}` | `tenant_id`, `app_id` |
| `nexusai.app.deleted.total` | `{app}` | `tenant_id`, `app_id` |

## Histograms

| Metric | Unit | Labels |
|--------|------|--------|
| `nexusai.workflow.duration` | `s` | `tenant_id`, `app_id`, `status` |
| `nexusai.node.duration` | `s` | `tenant_id`, `app_id`, `node_type`, `model_provider`, `model_name`, `plugin_name` |
| `nexusai.message.duration` | `s` | `tenant_id`, `app_id`, `model_provider`, `model_name` |
| `nexusai.message.time_to_first_token` | `s` | `tenant_id`, `app_id`, `model_provider`, `model_name` |
| `nexusai.tool.duration` | `s` | `tenant_id`, `app_id`, `tool_name` |
| `nexusai.prompt_generation.duration` | `s` | `tenant_id`, `app_id`, `operation_type`, `model_provider`, `model_name` |

## Structured Logs

### Span Companion Logs

Logs that accompany spans. Signal type: `span_detail`

#### `nexusai.workflow.run` Companion Log

**Common attributes:** All span attributes (see Traces section) plus:

| Additional Attribute | Type | Always Present | Description |
|---------------------|------|----------------|-------------|
| `nexusai.app.name` | string | No | Application display name |
| `nexusai.workspace.name` | string | No | Workspace display name |
| `nexusai.workflow.version` | string | Yes | Workflow definition version |
| `nexusai.workflow.inputs` | string/JSON | Yes | Input parameters (content-gated) |
| `nexusai.workflow.outputs` | string/JSON | Yes | Output results (content-gated) |
| `nexusai.workflow.query` | string | No | User query text (content-gated) |

**Event attributes:**

- `nexusai.event.name`: `"nexusai.workflow.run"`
- `nexusai.event.signal`: `"span_detail"`
- `trace_id`, `span_id`, `tenant_id`, `user_id`

#### `nexusai.node.execution` and `nexusai.node.execution.draft` Companion Logs

**Common attributes:** All span attributes (see Traces section) plus:

| Additional Attribute | Type | Always Present | Description |
|---------------------|------|----------------|-------------|
| `nexusai.app.name` | string | No | Application display name |
| `nexusai.workspace.name` | string | No | Workspace display name |
| `nexusai.invoke_from` | string | No | Invocation source |
| `gen_ai.tool.name` | string | No | Tool name (tool nodes only) |
| `nexusai.node.total_price` | float | No | Cost (LLM nodes only) |
| `nexusai.node.currency` | string | No | Currency code (LLM nodes only) |
| `nexusai.node.iteration_index` | int | No | Iteration index (iteration nodes) |
| `nexusai.node.loop_index` | int | No | Loop index (loop nodes) |
| `nexusai.plugin.name` | string | No | Plugin name (tool/knowledge nodes) |
| `nexusai.credential.name` | string | No | Credential name (plugin nodes) |
| `nexusai.credential.id` | string | No | Credential ID (plugin nodes) |
| `nexusai.dataset.ids` | JSON array | No | Dataset IDs (knowledge nodes) |
| `nexusai.dataset.names` | JSON array | No | Dataset names (knowledge nodes) |
| `nexusai.node.inputs` | string/JSON | Yes | Node inputs (content-gated) |
| `nexusai.node.outputs` | string/JSON | Yes | Node outputs (content-gated) |
| `nexusai.node.process_data` | string/JSON | No | Processing data (content-gated) |

**Event attributes:**

- `nexusai.event.name`: `"nexusai.node.execution"` or `"nexusai.node.execution.draft"`
- `nexusai.event.signal`: `"span_detail"`
- `trace_id`, `span_id`, `tenant_id`, `user_id`

### Standalone Logs

Logs without structural spans. Signal type: `metric_only`

#### `nexusai.message.run`

| Attribute | Type | Description |
|-----------|------|-------------|
| `nexusai.event.name` | string | `"nexusai.message.run"` |
| `nexusai.event.signal` | string | `"metric_only"` |
| `trace_id` | string | OTEL trace ID (32-char hex) |
| `span_id` | string | OTEL span ID (16-char hex) |
| `tenant_id` | string | Tenant identifier |
| `user_id` | string | User identifier (optional) |
| `nexusai.app_id` | string | Application identifier |
| `nexusai.message.id` | string | Message identifier |
| `nexusai.conversation.id` | string | Conversation ID (optional) |
| `nexusai.workflow.run_id` | string | Workflow run ID (optional) |
| `nexusai.invoke_from` | string | `service-api`, `web-app`, `debugger`, `explore` |
| `gen_ai.provider.name` | string | LLM provider |
| `gen_ai.request.model` | string | LLM model |
| `gen_ai.usage.input_tokens` | int | Input tokens |
| `gen_ai.usage.output_tokens` | int | Output tokens |
| `gen_ai.usage.total_tokens` | int | Total tokens |
| `nexusai.message.status` | string | `succeeded`, `failed` |
| `nexusai.message.error` | string | Error message (if failed) |
| `nexusai.message.duration` | float | Duration (seconds) |
| `nexusai.message.time_to_first_token` | float | TTFT (seconds) |
| `nexusai.message.inputs` | string/JSON | Inputs (content-gated) |
| `nexusai.message.outputs` | string/JSON | Outputs (content-gated) |

#### `nexusai.tool.execution`

| Attribute | Type | Description |
|-----------|------|-------------|
| `nexusai.event.name` | string | `"nexusai.tool.execution"` |
| `nexusai.event.signal` | string | `"metric_only"` |
| `trace_id` | string | OTEL trace ID |
| `span_id` | string | OTEL span ID |
| `tenant_id` | string | Tenant identifier |
| `nexusai.app_id` | string | Application identifier |
| `nexusai.message.id` | string | Message identifier |
| `nexusai.tool.name` | string | Tool name |
| `nexusai.tool.duration` | float | Duration (seconds) |
| `nexusai.tool.status` | string | `succeeded`, `failed` |
| `nexusai.tool.error` | string | Error message (if failed) |
| `nexusai.tool.inputs` | string/JSON | Inputs (content-gated) |
| `nexusai.tool.outputs` | string/JSON | Outputs (content-gated) |
| `nexusai.tool.parameters` | string/JSON | Parameters (content-gated) |
| `nexusai.tool.config` | string/JSON | Configuration (content-gated) |

#### `nexusai.moderation.check`

| Attribute | Type | Description |
|-----------|------|-------------|
| `nexusai.event.name` | string | `"nexusai.moderation.check"` |
| `nexusai.event.signal` | string | `"metric_only"` |
| `trace_id` | string | OTEL trace ID |
| `span_id` | string | OTEL span ID |
| `tenant_id` | string | Tenant identifier |
| `nexusai.app_id` | string | Application identifier |
| `nexusai.message.id` | string | Message identifier |
| `nexusai.moderation.type` | string | `input`, `output` |
| `nexusai.moderation.action` | string | `pass`, `block`, `flag` |
| `nexusai.moderation.flagged` | boolean | Whether flagged |
| `nexusai.moderation.categories` | JSON array | Flagged categories |
| `nexusai.moderation.query` | string | Content (content-gated) |

#### `nexusai.suggested_question.generation`

| Attribute | Type | Description |
|-----------|------|-------------|
| `nexusai.event.name` | string | `"nexusai.suggested_question.generation"` |
| `nexusai.event.signal` | string | `"metric_only"` |
| `trace_id` | string | OTEL trace ID |
| `span_id` | string | OTEL span ID |
| `tenant_id` | string | Tenant identifier |
| `nexusai.app_id` | string | Application identifier |
| `nexusai.message.id` | string | Message identifier |
| `nexusai.suggested_question.count` | int | Number of questions |
| `nexusai.suggested_question.duration` | float | Duration (seconds) |
| `nexusai.suggested_question.status` | string | `succeeded`, `failed` |
| `nexusai.suggested_question.error` | string | Error message (if failed) |
| `nexusai.suggested_question.questions` | JSON array | Questions (content-gated) |

#### `nexusai.dataset.retrieval`

| Attribute | Type | Description |
|-----------|------|-------------|
| `nexusai.event.name` | string | `"nexusai.dataset.retrieval"` |
| `nexusai.event.signal` | string | `"metric_only"` |
| `trace_id` | string | OTEL trace ID |
| `span_id` | string | OTEL span ID |
| `tenant_id` | string | Tenant identifier |
| `nexusai.app_id` | string | Application identifier |
| `nexusai.message.id` | string | Message identifier |
| `nexusai.dataset.id` | string | Dataset identifier |
| `nexusai.dataset.name` | string | Dataset name |
| `nexusai.dataset.embedding_providers` | JSON array | Embedding model providers (one per dataset) |
| `nexusai.dataset.embedding_models` | JSON array | Embedding models (one per dataset) |
| `nexusai.retrieval.rerank_provider` | string | Rerank model provider |
| `nexusai.retrieval.rerank_model` | string | Rerank model name |
| `nexusai.retrieval.query` | string | Search query (content-gated) |
| `nexusai.retrieval.document_count` | int | Documents retrieved |
| `nexusai.retrieval.duration` | float | Duration (seconds) |
| `nexusai.retrieval.status` | string | `succeeded`, `failed` |
| `nexusai.retrieval.error` | string | Error message (if failed) |
| `nexusai.dataset.documents` | JSON array | Documents (content-gated) |

#### `nexusai.generate_name.execution`

| Attribute | Type | Description |
|-----------|------|-------------|
| `nexusai.event.name` | string | `"nexusai.generate_name.execution"` |
| `nexusai.event.signal` | string | `"metric_only"` |
| `trace_id` | string | OTEL trace ID |
| `span_id` | string | OTEL span ID |
| `tenant_id` | string | Tenant identifier |
| `nexusai.app_id` | string | Application identifier |
| `nexusai.conversation.id` | string | Conversation identifier |
| `nexusai.generate_name.duration` | float | Duration (seconds) |
| `nexusai.generate_name.status` | string | `succeeded`, `failed` |
| `nexusai.generate_name.error` | string | Error message (if failed) |
| `nexusai.generate_name.inputs` | string/JSON | Inputs (content-gated) |
| `nexusai.generate_name.outputs` | string | Generated name (content-gated) |

#### `nexusai.prompt_generation.execution`

| Attribute | Type | Description |
|-----------|------|-------------|
| `nexusai.event.name` | string | `"nexusai.prompt_generation.execution"` |
| `nexusai.event.signal` | string | `"metric_only"` |
| `trace_id` | string | OTEL trace ID |
| `span_id` | string | OTEL span ID |
| `tenant_id` | string | Tenant identifier |
| `nexusai.app_id` | string | Application identifier |
| `nexusai.prompt_generation.operation_type` | string | Operation type (see appendix) |
| `gen_ai.provider.name` | string | LLM provider |
| `gen_ai.request.model` | string | LLM model |
| `gen_ai.usage.input_tokens` | int | Input tokens |
| `gen_ai.usage.output_tokens` | int | Output tokens |
| `gen_ai.usage.total_tokens` | int | Total tokens |
| `nexusai.prompt_generation.duration` | float | Duration (seconds) |
| `nexusai.prompt_generation.status` | string | `succeeded`, `failed` |
| `nexusai.prompt_generation.error` | string | Error message (if failed) |
| `nexusai.prompt_generation.instruction` | string | Instruction (content-gated) |
| `nexusai.prompt_generation.output` | string/JSON | Output (content-gated) |

#### `nexusai.app.created`

| Attribute | Type | Description |
|-----------|------|-------------|
| `nexusai.event.name` | string | `"nexusai.app.created"` |
| `nexusai.event.signal` | string | `"metric_only"` |
| `tenant_id` | string | Tenant identifier |
| `nexusai.app_id` | string | Application identifier |
| `nexusai.app.mode` | string | `chat`, `completion`, `agent-chat`, `workflow` |
| `nexusai.app.created_at` | string | Timestamp (ISO 8601) |

#### `nexusai.app.updated`

| Attribute | Type | Description |
|-----------|------|-------------|
| `nexusai.event.name` | string | `"nexusai.app.updated"` |
| `nexusai.event.signal` | string | `"metric_only"` |
| `tenant_id` | string | Tenant identifier |
| `nexusai.app_id` | string | Application identifier |
| `nexusai.app.updated_at` | string | Timestamp (ISO 8601) |

#### `nexusai.app.deleted`

| Attribute | Type | Description |
|-----------|------|-------------|
| `nexusai.event.name` | string | `"nexusai.app.deleted"` |
| `nexusai.event.signal` | string | `"metric_only"` |
| `tenant_id` | string | Tenant identifier |
| `nexusai.app_id` | string | Application identifier |
| `nexusai.app.deleted_at` | string | Timestamp (ISO 8601) |

#### `nexusai.feedback.created`

| Attribute | Type | Description |
|-----------|------|-------------|
| `nexusai.event.name` | string | `"nexusai.feedback.created"` |
| `nexusai.event.signal` | string | `"metric_only"` |
| `trace_id` | string | OTEL trace ID |
| `span_id` | string | OTEL span ID |
| `tenant_id` | string | Tenant identifier |
| `nexusai.app_id` | string | Application identifier |
| `nexusai.message.id` | string | Message identifier |
| `nexusai.feedback.rating` | string | `like`, `dislike`, `null` |
| `nexusai.feedback.content` | string | Feedback text (content-gated) |
| `nexusai.feedback.created_at` | string | Timestamp (ISO 8601) |

#### `nexusai.telemetry.rehydration_failed`

Diagnostic event for telemetry system health monitoring.

| Attribute | Type | Description |
|-----------|------|-------------|
| `nexusai.event.name` | string | `"nexusai.telemetry.rehydration_failed"` |
| `nexusai.event.signal` | string | `"metric_only"` |
| `tenant_id` | string | Tenant identifier |
| `nexusai.telemetry.error` | string | Error message |
| `nexusai.telemetry.payload_type` | string | Payload type (see appendix) |
| `nexusai.telemetry.correlation_id` | string | Correlation ID |

## Content-Gated Attributes

When `ENTERPRISE_INCLUDE_CONTENT=false`, these attributes are replaced with reference strings (`ref:{id_type}={uuid}`).

| Attribute | Signal |
|-----------|--------|
| `nexusai.workflow.inputs` | `nexusai.workflow.run` |
| `nexusai.workflow.outputs` | `nexusai.workflow.run` |
| `nexusai.workflow.query` | `nexusai.workflow.run` |
| `nexusai.node.inputs` | `nexusai.node.execution` |
| `nexusai.node.outputs` | `nexusai.node.execution` |
| `nexusai.node.process_data` | `nexusai.node.execution` |
| `nexusai.message.inputs` | `nexusai.message.run` |
| `nexusai.message.outputs` | `nexusai.message.run` |
| `nexusai.tool.inputs` | `nexusai.tool.execution` |
| `nexusai.tool.outputs` | `nexusai.tool.execution` |
| `nexusai.tool.parameters` | `nexusai.tool.execution` |
| `nexusai.tool.config` | `nexusai.tool.execution` |
| `nexusai.moderation.query` | `nexusai.moderation.check` |
| `nexusai.suggested_question.questions` | `nexusai.suggested_question.generation` |
| `nexusai.retrieval.query` | `nexusai.dataset.retrieval` |
| `nexusai.dataset.documents` | `nexusai.dataset.retrieval` |
| `nexusai.generate_name.inputs` | `nexusai.generate_name.execution` |
| `nexusai.generate_name.outputs` | `nexusai.generate_name.execution` |
| `nexusai.prompt_generation.instruction` | `nexusai.prompt_generation.execution` |
| `nexusai.prompt_generation.output` | `nexusai.prompt_generation.execution` |
| `nexusai.feedback.content` | `nexusai.feedback.created` |

## Appendix

### Operation Types

- `workflow`, `node_execution`, `message`, `rule_generate`, `code_generate`, `structured_output`, `instruction_monexusai`

### Node Types

- `start`, `end`, `answer`, `llm`, `knowledge-retrieval`, `knowledge-index`, `if-else`, `code`, `template-transform`, `question-classifier`, `http-request`, `tool`, `datasource`, `variable-aggregator`, `loop`, `iteration`, `parameter-extractor`, `assigner`, `document-extractor`, `list-operator`, `agent`, `trigger-webhook`, `trigger-schedule`, `trigger-plugin`, `human-input`

### Workflow Statuses

- `running`, `succeeded`, `failed`, `stopped`, `partial-succeeded`, `paused`

### Payload Types

- `workflow`, `node`, `message`, `tool`, `moderation`, `suggested_question`, `dataset_retrieval`, `generate_name`, `prompt_generation`, `app`, `feedback`

### Null Value Behavior

**Spans:** Attributes with `null` values are omitted.

**Logs:** Attributes with `null` values appear as `null` in JSON.

**Content-Gated:** Replaced with reference strings, not set to `null`.
