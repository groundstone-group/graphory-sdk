# Morning brief - {date}

**{headline_sentence}**

## Yesterday in 3 bullets
- {yesterday_bullet_1}
- {yesterday_bullet_2}
- {yesterday_bullet_3}

## Worth your attention
- {attention_item_1}
- {attention_item_2}
- {attention_item_3}

## Warm intros available
- {warm_intro_1}
- {warm_intro_2}

## Review queue
{review_queue_summary}

## Suggested first move
{first_move_sentence}

---
<!--
Template usage notes for the agent:

- Drop any section that has no real content (don't render an empty header).
- Each bullet = one line, two max. Cut adjectives before you cut signal.
- {date} = today's date in the user's locale (e.g. "Mon Apr 27").
- {headline_sentence} = one sentence summarizing the day's signal density.
  Examples: "Quiet day - 3 new items overnight." or "Busy week - 47 new
  items, 2 connection issues."
- {yesterday_bullet_*} = pick the 3 most signal-rich items from
  timeline(days=1). NOT all of them, just the 3 highest-leverage.
- {attention_item_*} = drifting threads, stale contacts, missed deadlines,
  past-due commitments. Pull from get_weekly_digest() + get_stale_entities().
- {warm_intro_*} = same-community pairs from get_latent_connections. First
  derive the day's most active entity from timeline(days=1), then call
  get_latent_connections(entity_id=<that entity id>, limit=5). If no entity
  is clearly active, drop this whole section. Phrase each line as
  "Person A (your Source) and Person B (your Source) are both at Org and you
  haven't directly connected them." 1-3 max.
- {review_queue_summary} = "N pending merge suggestions, M unresolved name
  mentions. Want me to walk the queue?" If 0 pending, drop this section.
- {first_move_sentence} = the single highest-leverage action, picked from
  what you just summarized. One sentence. No "you should consider..." -
  direct.

Total brief target: 200-400 words. Cut the lowest-signal section before
shrinking text.

Translate ALL internal vocabulary (Contact / Activity / Asset / etc.) into
plain business language ("person", "event", "file", etc.). The translation
rules live at https://docs.graphory.io/mcp.
-->
