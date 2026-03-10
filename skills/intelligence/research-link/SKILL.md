---
name: research-link
description: Ingest a URL, run deep research on it, and publish a research brief.
version: 1.0.0
author: Birkin
metadata:
  hermes:
    tags: [intelligence, research, ingest, publish]
---

# Research Link

## Trigger

Activate when the user drops a URL or says "research this", "look into this", "what do you make of this article?", or similar requests to analyze a link.

## Procedure

Three composable tool calls, each visible in the conversation:

### Step 1 — Ingest

Call `depeche_ingest` with the URL.

- If `already_exists` is true, note it but continue — the user wants fresh analysis.
- If `error` is returned, report the extraction failure and stop:
  ```
  Could not extract content from {url}: {error}
  Try a different URL or check that the page is publicly accessible.
  ```

### Step 2 — Research

Derive a research question from the article title and user context. Call `depeche_research` with:
- `question`: a concise research question (e.g. "What are the implications of {title}?")
- `context`: the article summary from Step 1 plus any conversation context

This returns a `brief_id`, title, summary, finding count, and source count.

- If research fails, report it and stop:
  ```
  Ingestion succeeded but research failed: {error}
  The article has been stored. You can ask me to research it again later.
  ```

### Step 3 — Publish

Call `depeche_publish_brief` with the `brief_id` from Step 2.

This renders the brief as HTML, publishes to S3, and regenerates the index.

## Delivery Template

```
Research brief published: {url}

**{title}**

{summary}

Key findings:
1. {finding_1}
2. {finding_2}
3. {finding_3}

Sources consulted: {source_count}
```

## Notes

- For follow-up questions after publishing, use `depeche_query` with `sources: ["artifacts", "graph", "interests"]` to pull additional context.
- For executive-formatted output, chain with the `format-brief` skill.
- The full pipeline is: ingest → research → publish. Each step is independent and can be run separately if needed.
