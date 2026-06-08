# Windsurf / Cline / OpenClaw wiring for save-on-stop

These three MCP-aware agents share a similar setup pattern: configure the Graphory MCP server, add a workspace or global rule that delegates to the skill.

## MCP server config

All three accept the same shape (path differs):

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

| Tool      | Config path                                     |
|-----------|-------------------------------------------------|
| Windsurf  | `~/.codeium/windsurf/mcp_config.json`           |
| Cline     | VS Code Settings -> Cline > MCP Servers (UI)    |
| OpenClaw  | `~/.openclaw/mcp.json`                          |

Full tool reference: https://docs.graphory.io/mcp

## Rule snippet (drop into the appropriate rules file)

| Tool      | Rules file                                          |
|-----------|-----------------------------------------------------|
| Windsurf  | `.windsurfrules` (workspace root)                   |
| Cline     | `.clinerules` (workspace root)                      |
| OpenClaw  | `~/.openclaw/rules/save-on-stop.md`                 |

```
# Graphory: save-on-stop

When the user says "save this", "remember this", "log this session", or the
session reaches a natural end after substantive work, invoke the save-on-stop
skill:

1. Compose a structured summary with sections: What we worked on, Decisions,
   Code / artifacts, Open questions, Next steps.
2. Call the Graphory MCP tool `save_message` with:
   - title: one-line label, prefixed with the agent name you're in
     (e.g. "Windsurf: ...", "Cline: ...", "OpenClaw: ...")
   - content: structured summary
   - entity: company/project (ask if unclear)
   - type: "session_log"
   - linked_entities: JSON list of {name, context} for people/projects mentioned

Skip trivial sessions. Never save credentials. After saving, confirm with one
sentence and stop.
```

## Lifecycle hooks (where supported)

- **Windsurf**: cascade rules can mention end-of-session triggers but Windsurf doesn't expose a true stop event yet. Pattern: rely on user prompt, or have the agent volunteer at natural breakpoints.
- **Cline**: same - no stop event. Use task-completion as the trigger ("when the current task finishes, ask the user if it's worth saving").
- **OpenClaw**: supports a `~/.openclaw/hooks/on_exit` script. Have it print a prompt to stdin asking the running agent to invoke save-on-stop before shutdown.

If your tool of choice adds a real stop hook later, the rule body stays the same - just delegate to the skill from the new hook.
