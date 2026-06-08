# Cursor wiring for save-on-stop

Cursor reads `.cursorrules` files at the workspace root and applies them to every chat. Drop this block into your project's `.cursorrules` (create the file if it doesn't exist).

## Snippet

```
# Graphory: save-on-stop

Whenever the user says "save this", "remember this", "log this session",
"ingest this conversation", or closes the chat tab after substantive work,
invoke the save-on-stop behavior:

1. Compose a structured summary with sections: What we worked on, Decisions,
   Code / artifacts, Open questions, Next steps.
2. Call the Graphory MCP tool `save_message` with:
   - title: one-line session label that will make sense weeks from now,
     prefixed with the agent name (e.g. "Cursor session: ...")
   - content: the structured summary above
   - entity: the company or project this session is about (ask if unclear)
   - type: "session_log"
   - linked_entities: JSON list of {name, context} for any people / projects
     mentioned by name during the session. Contexts: subject | mentioned |
     participant | author | recipient.

Skip saving for trivial sessions (under ~10 substantive turns, no decisions,
no code changes). Never save credentials or secrets - redact first or ask.

After saving, write one sentence: 'Saved this session to your Graphory under
"<title>".' Do not echo the full saved content back.
```

## MCP setup

Cursor needs the Graphory MCP server in `~/.cursor/mcp.json` (or the workspace `.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "graphory": {
      "url": "https://api.graphory.io/mcp",
      "headers": {
        "Authorization": "Bearer gs_ak_YOUR_KEY_HERE"
      }
    }
  }
}
```

Restart Cursor after editing. Full tool reference: https://docs.graphory.io/mcp

## Trigger options

Cursor doesn't have a true "tab close" event you can hook into from a rule, so the practical pattern is:

1. **User-driven**: rely on the user saying "save this" at end of session. The rule above handles that.
2. **End-of-task**: at natural breakpoints (PR opened, feature merged, doc finalized) the agent itself can volunteer "want me to save this session?"
3. **Scheduled**: pair with a cron/launchd job that opens a Cursor chat at 6pm asking "anything from today worth saving?"

If Cursor adds proper lifecycle hooks in a later release, the rule body stays the same - just point the new hook at it.
