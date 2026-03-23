# n8n Workflow Templates

**Scope:** Ready-to-import workflow skeletons for `n8n-Connector` and `Workflow-Composer` specialists.  
**Usage:** Reference these templates when a user requests n8n workflow assistance. Adapt node parameters to the user's specific services before importing.

---

## Template 1: HTTP Webhook + Transform + Notify

**Use Case:** Receive an inbound HTTP webhook payload, transform the data, and post a formatted notification to a Slack channel (or generic HTTP endpoint).

**Trigger:** Webhook node — listens on `POST /webhook/notify-transform`

**Node Flow:**

1. **Webhook** (`n8n-nodes-base.webhook`) — Captures the inbound POST payload; responds immediately with `{ "status": "received" }` to avoid client timeouts.
2. **Set** (`n8n-nodes-base.set`) — Extracts and renames key fields from `{{ $json.body }}` into a clean message object (`title`, `severity`, `detail`, `timestamp`).
3. **If** (`n8n-nodes-base.if`) — Routes on `severity`: if `critical` → direct Slack DM to on-call engineer; else → post to `#general-alerts` channel.
4. **HTTP Request** (`n8n-nodes-base.httpRequest`) — `POST` to Slack Incoming Webhook URL with formatted `text` block.
5. **Respond to Webhook** (`n8n-nodes-base.respondToWebhook`) — Returns `{ "status": "delivered" }` (optional; only if `responseMode: lastNode`).

**JSON Skeleton:**

```json
{
  "name": "HTTP Webhook + Transform + Notify",
  "nodes": [
    {
      "id": "w1-n1",
      "name": "Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [240, 300],
      "parameters": {
        "httpMethod": "POST",
        "path": "notify-transform",
        "responseMode": "lastNode"
      }
    },
    {
      "id": "w1-n2",
      "name": "Extract Fields",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3,
      "position": [460, 300],
      "parameters": {
        "mode": "manual",
        "fields": {
          "values": [
            { "name": "title",     "value": "={{ $json.body.title }}" },
            { "name": "severity",  "value": "={{ $json.body.severity }}" },
            { "name": "detail",    "value": "={{ $json.body.detail }}" },
            { "name": "timestamp", "value": "={{ $now }}" }
          ]
        }
      }
    },
    {
      "id": "w1-n3",
      "name": "Route on Severity",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [680, 300],
      "parameters": {
        "conditions": {
          "string": [{ "value1": "={{ $json.severity }}", "operation": "equal", "value2": "critical" }]
        }
      }
    },
    {
      "id": "w1-n4",
      "name": "Post to Slack",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [900, 300],
      "parameters": {
        "method": "POST",
        "url": "={{ $vars.SLACK_WEBHOOK_URL }}",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            { "name": "text", "value": "={{ '[' + $json.severity.toUpperCase() + '] ' + $json.title + ' — ' + $json.detail }}" }
          ]
        }
      }
    }
  ],
  "connections": {
    "Webhook":           { "main": [[{ "node": "Extract Fields",    "type": "main", "index": 0 }]] },
    "Extract Fields":    { "main": [[{ "node": "Route on Severity", "type": "main", "index": 0 }]] },
    "Route on Severity": { "main": [[{ "node": "Post to Slack",     "type": "main", "index": 0 }], [{ "node": "Post to Slack", "type": "main", "index": 0 }]] }
  },
  "settings": { "executionOrder": "v1" }
}
```

**Success Criteria:**
- `POST /webhook/notify-transform` with `{ "title": "Test", "severity": "critical", "detail": "Disk full" }` triggers a Slack message within 2 seconds.
- Non-critical payload routes without error.

**n8n-Connector Hint:** Replace `$vars.SLACK_WEBHOOK_URL` with the environment variable or hardcoded Slack Incoming Webhook URL before activating.

---

## Template 2: Scheduled Data Sync / ETL

**Use Case:** Every 6 hours, pull records from a source REST API, normalise them, and upsert into a target database or second REST API.

**Trigger:** Schedule node — cron `0 */6 * * *`

**Node Flow:**

1. **Schedule Trigger** (`n8n-nodes-base.scheduleTrigger`) — Fires every 6 hours; passes trigger timestamp downstream.
2. **HTTP Request — Fetch Source** (`n8n-nodes-base.httpRequest`) — `GET` the source API with Bearer token from n8n credentials.
3. **Split In Batches** (`n8n-nodes-base.splitInBatches`) — Processes records 50 at a time to avoid rate-limit errors.
4. **Set — Normalise** (`n8n-nodes-base.set`) — Maps source fields to target schema (rename, type-cast, drop unused keys).
5. **Code** (`n8n-nodes-base.code`) — Validates each record; filters out items missing required fields; logs skipped count.
6. **HTTP Request — Upsert Target** (`n8n-nodes-base.httpRequest`) — `POST /upsert` to target API with normalised payload.
7. **Set — Summary** (`n8n-nodes-base.set`) — Builds a run-summary object: `{ processed, skipped, errors, runAt }`.
8. **HTTP Request — Notify** (`n8n-nodes-base.httpRequest`) — Posts summary to a monitoring webhook.

**JSON Skeleton:**

```json
{
  "name": "Scheduled ETL Sync",
  "nodes": [
    {
      "id": "etl-n1",
      "name": "Every 6 Hours",
      "type": "n8n-nodes-base.scheduleTrigger",
      "typeVersion": 1,
      "position": [240, 300],
      "parameters": { "rule": { "interval": [{ "field": "hours", "hoursInterval": 6 }] } }
    },
    {
      "id": "etl-n2",
      "name": "Fetch Source",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [460, 300],
      "parameters": {
        "method": "GET",
        "url": "={{ $vars.SOURCE_API_BASE }}/records",
        "authentication": "genericCredentialType",
        "genericAuthType": "httpBearerAuth"
      }
    },
    {
      "id": "etl-n3",
      "name": "Batch 50",
      "type": "n8n-nodes-base.splitInBatches",
      "typeVersion": 3,
      "position": [680, 300],
      "parameters": { "batchSize": 50 }
    },
    {
      "id": "etl-n4",
      "name": "Normalise",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3,
      "position": [900, 300],
      "parameters": {
        "mode": "manual",
        "fields": {
          "values": [
            { "name": "id",    "value": "={{ $json.record_id }}" },
            { "name": "name",  "value": "={{ $json.display_name }}" },
            { "name": "updatedAt", "value": "={{ $json.last_modified }}" }
          ]
        }
      }
    },
    {
      "id": "etl-n5",
      "name": "Validate",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [1120, 300],
      "parameters": {
        "jsCode": "const valid = items.filter(i => i.json.id && i.json.name);\nreturn valid;"
      }
    },
    {
      "id": "etl-n6",
      "name": "Upsert Target",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [1340, 300],
      "parameters": {
        "method": "POST",
        "url": "={{ $vars.TARGET_API_BASE }}/upsert",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ $json }}"
      }
    }
  ],
  "connections": {
    "Every 6 Hours": { "main": [[{ "node": "Fetch Source", "type": "main", "index": 0 }]] },
    "Fetch Source":  { "main": [[{ "node": "Batch 50",     "type": "main", "index": 0 }]] },
    "Batch 50":      { "main": [[{ "node": "Normalise",    "type": "main", "index": 0 }]] },
    "Normalise":     { "main": [[{ "node": "Validate",     "type": "main", "index": 0 }]] },
    "Validate":      { "main": [[{ "node": "Upsert Target","type": "main", "index": 0 }]] }
  },
  "settings": { "executionOrder": "v1" }
}
```

**Success Criteria:**
- Execution appears in n8n history every 6 hours with no error status.
- Target API receives normalised records; records with missing `id` or `name` are absent from target.

**n8n-Connector Hint:** Store `SOURCE_API_BASE` and `TARGET_API_BASE` as n8n environment variables or workflow-level variables, not hardcoded in node parameters.

---

## Template 3: Code Review Notification

**Use Case:** On every GitHub pull-request event (webhook), post a structured code-review request to a Slack channel with PR metadata and a direct link.

**Trigger:** Webhook node — receives GitHub `pull_request` events via a configured GitHub webhook

**Node Flow:**

1. **Webhook** (`n8n-nodes-base.webhook`) — Listens on `POST /webhook/github-pr`; pass-through response mode.
2. **If — Action Filter** (`n8n-nodes-base.if`) — Continues only when `action` is `opened` or `synchronize`; discards `closed`, `labeled`, etc.
3. **Set — Extract PR Data** (`n8n-nodes-base.set`) — Pulls `pr_title`, `pr_url`, `author`, `base_branch`, `head_branch`, `changed_files` from the GitHub payload.
4. **HTTP Request — Post to Slack** (`n8n-nodes-base.httpRequest`) — Posts a formatted Block Kit message to the `#code-review` channel.
5. **Respond to Webhook** (`n8n-nodes-base.respondToWebhook`) — Returns HTTP 200 to GitHub immediately.

**JSON Skeleton:**

```json
{
  "name": "Code Review Notification",
  "nodes": [
    {
      "id": "cr-n1",
      "name": "GitHub PR Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [240, 300],
      "parameters": {
        "httpMethod": "POST",
        "path": "github-pr",
        "responseMode": "onReceived",
        "responseData": "firstEntryJson"
      }
    },
    {
      "id": "cr-n2",
      "name": "Filter: opened or sync",
      "type": "n8n-nodes-base.if",
      "typeVersion": 2,
      "position": [460, 300],
      "parameters": {
        "conditions": {
          "string": [{ "value1": "={{ $json.body.action }}", "operation": "regex", "value2": "opened|synchronize" }]
        }
      }
    },
    {
      "id": "cr-n3",
      "name": "Extract PR Data",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3,
      "position": [680, 300],
      "parameters": {
        "mode": "manual",
        "fields": {
          "values": [
            { "name": "pr_title",      "value": "={{ $json.body.pull_request.title }}" },
            { "name": "pr_url",        "value": "={{ $json.body.pull_request.html_url }}" },
            { "name": "author",        "value": "={{ $json.body.pull_request.user.login }}" },
            { "name": "base_branch",   "value": "={{ $json.body.pull_request.base.ref }}" },
            { "name": "changed_files", "value": "={{ $json.body.pull_request.changed_files }}" }
          ]
        }
      }
    },
    {
      "id": "cr-n4",
      "name": "Post to Slack",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [900, 300],
      "parameters": {
        "method": "POST",
        "url": "={{ $vars.SLACK_WEBHOOK_URL }}",
        "sendBody": true,
        "bodyParameters": {
          "parameters": [
            { "name": "text", "value": "={{ ':pr: *PR Review Requested*\\n*Title:* ' + $json.pr_title + '\\n*Author:* ' + $json.author + '\\n*Files changed:* ' + $json.changed_files + '\\n<' + $json.pr_url + '|Open PR>' }}" }
          ]
        }
      }
    }
  ],
  "connections": {
    "GitHub PR Webhook":    { "main": [[{ "node": "Filter: opened or sync", "type": "main", "index": 0 }]] },
    "Filter: opened or sync": { "main": [[{ "node": "Extract PR Data", "type": "main", "index": 0 }]] },
    "Extract PR Data":      { "main": [[{ "node": "Post to Slack",    "type": "main", "index": 0 }]] }
  },
  "settings": { "executionOrder": "v1" }
}
```

**Success Criteria:**
- Opening a GitHub PR triggers the workflow; a Slack message appears in `#code-review` within 5 seconds.
- Closing a PR (action = `closed`) produces no Slack message.

**n8n-Connector Hint:** Configure the GitHub webhook secret in the Webhook node's `Secret` field and verify it using n8n's header validation; do not expose the secret in `$vars`.

---

## Template 4: Multi-System Data Aggregation

**Use Case:** On-demand aggregation — query three independent APIs (CRM, billing, support), merge results by a common `customer_id`, and return a unified 360° customer record.

**Trigger:** Webhook node — `POST /webhook/customer-360` with body `{ "customer_id": "..." }`

**Node Flow:**

1. **Webhook** (`n8n-nodes-base.webhook`) — Receives `customer_id` from caller.
2. **[Parallel] HTTP Request — CRM** (`n8n-nodes-base.httpRequest`) — `GET /crm/customers/{id}`.
3. **[Parallel] HTTP Request — Billing** (`n8n-nodes-base.httpRequest`) — `GET /billing/accounts/{id}`.
4. **[Parallel] HTTP Request — Support** (`n8n-nodes-base.httpRequest`) — `GET /support/customers/{id}/tickets?status=open`.
5. **Merge** (`n8n-nodes-base.merge`) — Mode `mergeByKey` on `customer_id`; combines all three response objects.
6. **Code — Flatten** (`n8n-nodes-base.code`) — Flattens nested arrays (open tickets) into a summary count; removes raw API-specific envelope fields.
7. **Respond to Webhook** (`n8n-nodes-base.respondToWebhook`) — Returns the unified record as JSON.

**JSON Skeleton:**

```json
{
  "name": "Customer 360 Aggregation",
  "nodes": [
    {
      "id": "agg-n1",
      "name": "Receive Request",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [240, 300],
      "parameters": { "httpMethod": "POST", "path": "customer-360", "responseMode": "lastNode" }
    },
    {
      "id": "agg-n2",
      "name": "CRM Lookup",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [460, 180],
      "parameters": { "method": "GET", "url": "={{ $vars.CRM_BASE }}/customers/{{ $json.body.customer_id }}" }
    },
    {
      "id": "agg-n3",
      "name": "Billing Lookup",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [460, 300],
      "parameters": { "method": "GET", "url": "={{ $vars.BILLING_BASE }}/accounts/{{ $json.body.customer_id }}" }
    },
    {
      "id": "agg-n4",
      "name": "Support Lookup",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [460, 420],
      "parameters": { "method": "GET", "url": "={{ $vars.SUPPORT_BASE }}/customers/{{ $json.body.customer_id }}/tickets?status=open" }
    },
    {
      "id": "agg-n5",
      "name": "Merge 360",
      "type": "n8n-nodes-base.merge",
      "typeVersion": 3,
      "position": [700, 300],
      "parameters": { "mode": "combine", "combinationMode": "mergeByKey", "mergeByFields": { "values": [{ "field1": "id", "field2": "id" }] } }
    },
    {
      "id": "agg-n6",
      "name": "Flatten & Clean",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [920, 300],
      "parameters": {
        "jsCode": "return items.map(i => ({ json: { customer_id: i.json.id, name: i.json.name, plan: i.json.plan, open_tickets: Array.isArray(i.json.tickets) ? i.json.tickets.length : 0 } }));"
      }
    }
  ],
  "connections": {
    "Receive Request": { "main": [[{ "node": "CRM Lookup",     "type": "main", "index": 0 }, { "node": "Billing Lookup", "type": "main", "index": 0 }, { "node": "Support Lookup", "type": "main", "index": 0 }]] },
    "CRM Lookup":      { "main": [[{ "node": "Merge 360",      "type": "main", "index": 0 }]] },
    "Billing Lookup":  { "main": [[{ "node": "Merge 360",      "type": "main", "index": 1 }]] },
    "Support Lookup":  { "main": [[{ "node": "Merge 360",      "type": "main", "index": 2 }]] },
    "Merge 360":       { "main": [[{ "node": "Flatten & Clean","type": "main", "index": 0 }]] }
  },
  "settings": { "executionOrder": "v1" }
}
```

**Success Criteria:**
- `POST /webhook/customer-360` with a valid `customer_id` returns a merged JSON object containing fields from all three APIs within 3 seconds.
- If one upstream API is down, the workflow errors gracefully and returns a partial result (add error-output handling in production).

**n8n-Connector Hint:** Add credentials for each API as separate n8n Credential entries (`CRM_API`, `BILLING_API`, `SUPPORT_API`) and reference them by name in each HTTP Request node rather than using raw `$vars` tokens.

---

## Template 5: Agent-to-n8n Bridge

**Use Case:** Allow a VS Code Copilot agent (e.g., Automation-Atlas) to trigger an n8n workflow via HTTP and receive the result synchronously, enabling agent→n8n→external-service round-trips.

**Trigger:** Webhook node — `POST /webhook/agent-bridge` — designed to be called by an agent's HTTP Request tool.

**Node Flow:**

1. **Webhook** (`n8n-nodes-base.webhook`) — Receives agent payload: `{ "action": "...", "payload": { ... } }`.
2. **Switch — Route by Action** (`n8n-nodes-base.switch`) — Routes to different sub-flows based on `action` value (e.g., `send-email`, `create-ticket`, `query-db`).
3. **[Branch A] HTTP Request — Execute Action A** (`n8n-nodes-base.httpRequest`) — Implements the first routed action.
4. **[Branch B] Code — Execute Action B** (`n8n-nodes-base.code`) — Implements a second action inline.
5. **Set — Normalise Response** (`n8n-nodes-base.set`) — Wraps result in `{ "success": true, "result": ..., "action": ... }` for consistent agent consumption.
6. **Respond to Webhook** (`n8n-nodes-base.respondToWebhook`) — Returns structured response to the calling agent.

**JSON Skeleton:**

```json
{
  "name": "Agent-to-n8n Bridge",
  "nodes": [
    {
      "id": "br-n1",
      "name": "Agent Webhook",
      "type": "n8n-nodes-base.webhook",
      "typeVersion": 2,
      "position": [240, 300],
      "parameters": {
        "httpMethod": "POST",
        "path": "agent-bridge",
        "responseMode": "lastNode",
        "options": { "rawBody": false }
      }
    },
    {
      "id": "br-n2",
      "name": "Route Action",
      "type": "n8n-nodes-base.switch",
      "typeVersion": 3,
      "position": [460, 300],
      "parameters": {
        "dataType": "string",
        "value1": "={{ $json.body.action }}",
        "rules": {
          "rules": [
            { "value2": "send-email",    "output": 0 },
            { "value2": "create-ticket", "output": 1 }
          ]
        },
        "fallbackOutput": 2
      }
    },
    {
      "id": "br-n3",
      "name": "Send Email",
      "type": "n8n-nodes-base.httpRequest",
      "typeVersion": 4,
      "position": [680, 180],
      "parameters": {
        "method": "POST",
        "url": "={{ $vars.EMAIL_SERVICE_URL }}/send",
        "sendBody": true,
        "specifyBody": "json",
        "jsonBody": "={{ $json.body.payload }}"
      }
    },
    {
      "id": "br-n4",
      "name": "Create Ticket",
      "type": "n8n-nodes-base.code",
      "typeVersion": 2,
      "position": [680, 300],
      "parameters": {
        "jsCode": "// Placeholder: call ticketing system SDK or API\nreturn [{ json: { ticket_id: 'T-' + Date.now(), status: 'created' } }];"
      }
    },
    {
      "id": "br-n5",
      "name": "Unknown Action",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3,
      "position": [680, 420],
      "parameters": {
        "mode": "manual",
        "fields": { "values": [{ "name": "error", "value": "Unknown action" }] }
      }
    },
    {
      "id": "br-n6",
      "name": "Normalise Response",
      "type": "n8n-nodes-base.set",
      "typeVersion": 3,
      "position": [900, 300],
      "parameters": {
        "mode": "manual",
        "fields": {
          "values": [
            { "name": "success", "value": "={{ !$json.error }}" },
            { "name": "result",  "value": "={{ $json }}" },
            { "name": "action",  "value": "={{ $('Agent Webhook').first().json.body.action }}" }
          ]
        }
      }
    }
  ],
  "connections": {
    "Agent Webhook":      { "main": [[{ "node": "Route Action",        "type": "main", "index": 0 }]] },
    "Route Action":       { "main": [[{ "node": "Send Email",          "type": "main", "index": 0 }], [{ "node": "Create Ticket", "type": "main", "index": 0 }], [{ "node": "Unknown Action", "type": "main", "index": 0 }]] },
    "Send Email":         { "main": [[{ "node": "Normalise Response",  "type": "main", "index": 0 }]] },
    "Create Ticket":      { "main": [[{ "node": "Normalise Response",  "type": "main", "index": 0 }]] },
    "Unknown Action":     { "main": [[{ "node": "Normalise Response",  "type": "main", "index": 0 }]] }
  },
  "settings": { "executionOrder": "v1" }
}
```

**Success Criteria:**
- A VS Code agent calling `POST /webhook/agent-bridge` with `{ "action": "send-email", "payload": { ... } }` receives `{ "success": true, "result": {...}, "action": "send-email" }` synchronously.
- An unknown `action` returns `{ "success": false, "result": { "error": "Unknown action" }, "action": "..." }` with HTTP 200 (not 4xx), so the calling agent can handle it gracefully.

**n8n-Connector Hint:** Secure the bridge webhook with an `x-agent-token` header check (use n8n's Header Auth credential type) to prevent unauthorised triggering from outside the agent system.

---

## Usage Notes for n8n-Connector

- All JSON skeletons use `typeVersion` values current as of n8n ≥ 1.30. Verify version compatibility before import.
- Replace all `$vars.*` references with actual n8n variables or credentials.
- For production deployments, add error-output handling on every HTTP Request node.
- Test each template with n8n's built-in **Test Workflow** feature before activating.
- Refer to `plugins/automation-mcp-workflow/agents/n8n-Connector.agent.md` for routing decisions on which template to recommend for a given user request.
