# Audit Logging

This page includes an anchor you can deep-link to.

## What we log

- Who asked
- Which app/context
- Which sources retrieved
- Model used
- Token usage (if available)

## Audit event fields

<a id="audit-event-fields"></a>

| Field | Example | Notes |
|---|---|---|
| timestamp | 2026-MM-DDThh:mm:ssZ | ISO format |
| user_id | abc123 | pseudonymous where possible |
| app_id | eva-da-jp | app context |
| query_hash | sha256(...) | protects raw text |

---

**Asset Source**: Governance dashboard screenshots from EVA-JP-reference
