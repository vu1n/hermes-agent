---
name: watch-topic
description: Create and manage wire watches for real-time push notifications on topics, entities, or keywords.
version: 1.0.0
author: Birkin
metadata:
  hermes:
    tags: [intelligence, wire, watch, notifications, alerts, tracking]
    related_skills: [daily-dossier, research-link]
---

# Watch Topic

## Trigger

Activate when the user says "watch", "follow this", "alert me about", "track", "notify me when", "keep an eye on", or similar requests to monitor a topic, entity, or keyword in real-time.

## Procedure

1. Parse the user's request to determine:
   - **name**: A short human-readable label for the watch
   - **watch_type**: `topic` (broad subject), `entity` (specific person/company/product), `keyword` (exact phrase), or `story` (developing story)
   - **query**: The search terms to match against incoming wire events
   - **priority**: Default P1 unless user indicates urgency

2. Confirm the watch configuration with the user, explaining the tier:
   - **P0**: "Immediate Telegram push when verified by 3+ independent sources. Reserved for critical breaking events."
   - **P1**: "Included in your 2-hourly wire digest via Telegram."
   - **P2**: "Boosted in your daily morning dossier."

3. Call `depeche_watch` with `action=create` and the parsed parameters.

4. Confirm creation with the watch ID and a brief explanation of when notifications will arrive.

## Examples

**User:** "Watch for anything about OpenAI"
- name: "OpenAI News"
- watch_type: entity
- query: "OpenAI"
- priority: P1

**User:** "Alert me immediately if there's a major earthquake"
- name: "Major Earthquakes"
- watch_type: keyword
- query: "earthquake magnitude"
- priority: P0

**User:** "Track the AI regulation story"
- name: "AI Regulation"
- watch_type: story
- query: "AI regulation policy legislation"
- priority: P1

## Management

- To list watches: `depeche_watch action=list`
- To disable: `depeche_watch action=disable watch_id=...`
- To delete: `depeche_watch action=delete watch_id=...`

## Notes

- Without active watches, all wire events default to P2 (daily dossier). Watches are the user's explicit opt-in to push notifications.
- P0 is intentionally rare — it requires both a P0-priority watch match AND verification by 3+ independent sources.
- The wire service polls every 15 minutes. P1 digests are sent every 2 hours.
