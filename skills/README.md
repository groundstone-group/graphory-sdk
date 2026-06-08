# Graphory skills

Portable instruction files that teach any MCP-aware AI how to use your Graphory
graph well - not just call the API, but capture, recall, and maintain your
business memory the right way.

A skill is a single `SKILL.md` (plus optional examples) with YAML frontmatter.
Drop it where your AI client looks for skills (for example `~/.claude/skills/`
for Claude Code and Claude Desktop, or your tool's equivalent) and the agent
picks it up automatically when the moment fits.

## The model

Graphory is the data layer. It does not run an LLM on your content - your AI
does. These skills run entirely on your own AI subscription: Graphory stores and
serves the graph, your agent does the reading, extraction, and synthesis. Zero
Graphory inference, and your data stays yours.

Every skill calls Graphory's MCP tools, so you need the Graphory MCP server
connected in your client first. See https://docs.graphory.io/mcp.

## The skills

| Skill | What it does |
|-------|--------------|
| [save-to-graph](save-to-graph/SKILL.md) | The ingestion loop. Turn any content - a chat session, a video transcript, an article - into clean, linked memory: learn the live schema, check what already exists, write only what is new, link it to what is there. |
| [save-on-stop](save-on-stop/SKILL.md) | Auto-capture a working session when it ends (stop hook, tab close), so the next session in any tool picks up where you left off. |
| [morning-brief](morning-brief/SKILL.md) | A daily situational brief assembled from your graph and rendered by your own AI. Read-only. |
| [cleanup-stale](cleanup-stale/SKILL.md) | Walk the review queue and adjudicate ambiguous matches (duplicate contacts, unresolved names) with you in the loop. |

`save-to-graph` is the engine; the others are specific applications of it. Start
there.

## How the schema works

None of these skills hardcode Graphory's vocabulary. They call
`describe_schema` at runtime, which returns the live node labels, allowed
relationship types, and recommended properties for your graph. Always ask the
graph for its shape rather than guessing - the skill stays correct as the
schema evolves.

## One graph

Graphory is one graph per organization. These skills never ask you to pick a
graph or a "knowledge base" - there is not one to pick. Material you capture to
learn from (videos, articles, research) is tagged `domain: content`; real
business activity is `domain: operations`. Same graph, soft separation, so you
can later ask "just show me what I have been learning" without a second store.

## License

MIT, same as the SDK. Copy them, fork them, adapt them to your own agent.
