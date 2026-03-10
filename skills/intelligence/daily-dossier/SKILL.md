---
name: daily-dossier
description: Generate and publish the daily intelligence dossier with ranked articles and insights.
version: 1.0.0
author: Birkin
metadata:
  hermes:
    tags: [intelligence, dossier, briefing, daily]
---

# Daily Dossier

## Trigger

Activate when the user says "daily dossier", "morning briefing", "today's brief", "what's new", or similar requests for a curated intelligence summary.

## Procedure

1. Call `depeche_dossier` with no arguments.
   - This ranks recent articles by interest fit and novelty, renders an HTML dossier, and attempts to publish to S3.

2. Handle the response:
   - **Success with URL:** Deliver the published URL, top stories, and total item count.
   - **Success without URL (`url` is null):** The dossier was generated and ranked but could not be published. Tell the user: "Dossier generated with {item_count} items but not published — configure S3_BUCKET to enable publishing." Still deliver the top stories and insights inline.
   - **Error:** Report the failure and suggest retrying or checking feed configuration.

## Delivery Template

```
Daily dossier published: {url}

**{date} — {item_count} items**

Top stories:
1. {story_1_title} — {why_it_matters}
2. {story_2_title} — {why_it_matters}
3. {story_3_title} — {why_it_matters}

Clusters: {cluster_summary}
```

## Notes

- If the user wants to refresh feeds before generating the dossier, run `depeche_intake` first, then `depeche_dossier`.
- The dossier reflects whatever articles are currently in the system. For best results, ensure intake has run recently.
