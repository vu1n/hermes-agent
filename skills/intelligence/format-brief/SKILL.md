---
name: format-brief
description: Format research findings into a Kelly-style executive brief.
version: 1.0.0
author: Birkin
metadata:
  hermes:
    tags: [intelligence, formatting, executive, brief]
---

# Format Brief (Kelly)

## Trigger

Activate when the user asks to format research findings, wants an executive summary, says "Kelly format", "clean this up", or requests a polished version of research output.

## Format: Kelly Executive Brief

Apply this structure to the source material. Do not add information that is not in the source — only reorganize and sharpen.

### 1. Bottom Line Up Front (BLUF)

2-3 sentences of prose. State the core finding and its significance. Lead with the conclusion, not the process. Active voice, concrete language.

### 2. Key Findings

3-5 numbered items, each one sentence stating a discrete finding. Order by importance, not source order. Prefix with confidence level:
- **High confidence:** Strong evidence from multiple independent sources.
- **Moderate confidence:** Supported by credible sources but not independently verified.
- **Low confidence:** Preliminary signals, single-source, or speculative.

### 3. Counterpoints and Risks

List credible opposing views or risks that qualify the findings. If none exist in the source material, state: "No significant counterpoints identified."

### 4. Implications and Recommended Actions

What should the principal do or watch for? Separate into:
- **Immediate actions** — things to do now.
- **Monitoring items** — things to track over time.

### 5. Sources Consulted

List sources with titles and relevance notes. Group by type (web, internal artifacts, graph).

## Style Guide

- Write for a time-constrained reader. Front-load important information.
- Use concrete numbers and specifics over vague qualifiers.
- Avoid hedging language unless genuinely uncertain.
- Keep total output under 500 words unless source material is exceptionally complex.
- Do not use bullet points in the BLUF section — use prose.

## Tool Usage

- Use `depeche_query` to pull relevant findings if the user references stored research but does not provide the content inline.
- This skill formats and delivers directly in conversation. Output is not published to S3 unless the user explicitly requests publication.
