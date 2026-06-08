# Examples

Runnable Python over the Graphory SDK. Install and authenticate first:

```bash
pip install graphory
graphory login
```

| File | What it shows |
|------|---------------|
| [`save_chat_session.py`](save_chat_session.py) | Save a conversation to your graph with the two-step schema flow. |
| [`priority_brief.py`](priority_brief.py) | A cron-ready daily brief: pull recent activity from your graph and let your own AI rank what matters. |

These use the SDK's HTTP methods. For agent-side capture - your AI reading a
transcript and writing structured nodes - see
[`../skills/save-to-graph`](../skills/save-to-graph).
