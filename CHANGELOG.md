# Changelog

All notable changes to the Graphory Python SDK are documented in this file.

## [Unreleased] - 2026-06-02

### Added
- `skills/` directory: portable, MCP-based skill files any AI client can load. `save-to-graph` (the ingestion loop - learn the schema, dedupe, write only the delta, link to existing nodes), `save-on-stop` (session capture), `morning-brief` (daily brief), and `cleanup-stale` (review-queue hygiene), plus a `skills/README.md` index. Each runs on the user's own AI subscription at zero inference cost.
- `examples/` directory: runnable Python over the SDK - `save_chat_session.py` (two-step conversation save) and `priority_brief.py` (cron-ready daily brief), with a README.
- README "Teach your AI" section pointing at `skills/` and `examples/`.

### Fixed
- Reconciled published skill tool-call signatures with the live MCP server: `save_message` takes no `source` parameter, `get_latent_connections` requires an `entity_id`, `batch_merge_suggestions` takes `suggestion_ids`, and the suggestion `category` vocabulary matches the server (`merge_candidate`, `link_review`, `uncertain_relationship`, `incomplete_contact`, `unconnected_entity`).

## [Unreleased] - 2026-06-01 (fifth pass)

### Added
- Graphory logo added to the top of the README, centered above the H1, at 200px width. The logo file lives at `assets/logo.webp` in the SDK repo. The README references it via an absolute `raw.githubusercontent.com` URL so the image renders on both GitHub and PyPI (relative paths would break on PyPI's long-description renderer).

## [Unreleased] - 2026-06-01 (fourth pass)

### Changed
- "What you can build" section rewritten with pain-first, reader-led intro ("You should not have to remember any of it. Your AI should.") and direct "you" address throughout.
- Use cases broadened from deal-focused examples to six scenarios spanning AI developers, indie founders, consultants, portfolio managers, operations, and researchers. Each is a concrete role the reader can put themselves in, a natural-language question, and the cited outcome.
- "Built for" audience reordered and broadened to lead with AI developers and indie founders, then consultants, asset managers, operations, and researchers. AI client power users (Claude Code, Cursor, ChatGPT, Hermes, OpenClaw) moved to a cross-cutting line.
- Quick start search example rebalanced from a name-specific deal query to a universal pricing-history query.
- "Operational data" differentiator updated to use "accounts" instead of "deals" in the entity list.
- Mem0 and Zep comparison entries rebalanced away from name-specific deal framing.
- llms.txt audience list and "Compared to" updated to reflect the cross-stage, cross-business-type scope. Added a "Visual model" section describing the hub-and-spoke shape.

### Added
- Mermaid `graph LR` diagram in the README showing the central business or individual node with orbiting data sources (email, calls and texts, calendar, CRM, documents, invoices, code, AI chat sessions). Renders natively on GitHub with an ASCII fallback inside a `<details>` block for environments that do not render Mermaid.

## [Unreleased] - 2026-06-01 (third pass)

### Changed
- README FAQ trimmed: removed an entry that exposed advisor-layer implementation details. Cost framing in the remaining FAQ is benefit-led ("zero inference cost", "predictable pricing"), not architecture.

## [Unreleased] - 2026-06-01

### Changed
- README rewritten (second pass) with bolder positioning ("Stop your AI from forgetting your business"), free-tier callout, and the cross-AI chat session memory differentiator promoted to a first-class feature.
- All customer-facing vendor names stripped from README, llms.txt, and pyproject description. Replaced with benefit language ("encrypted credential vault", "per-org isolated knowledge graph") so the public surface no longer reveals which auth provider or graph database backs the service.
- `pyproject.toml` description rewritten to lead with the value prop, not the implementation.
- llms.txt updated with the cross-AI session memory angle, free-tier mention, and stripped vendor names.

### Added
- Cross-AI chat session memory framing in README ("save_conversation across clients", "one graph, every AI, every session") backed by the shipped `save_conversation` MCP tool and `POST /org/{id}/conversation` API endpoint.
- Free-tier section in the README (100K nodes, no credit card).
- New keywords: `cursor`, `chatgpt`, `zep-alternative`, `cross-ai-memory`, `chat-session-memory`.

## [Unreleased] - 2026-06-01 (first pass)

### Changed
- README rewritten with full positioning (hero, what-is, built-for, architecture, FAQ, links).
- `pyproject.toml` description and keywords expanded for SEO and AEO discoverability.
- Development status moved from Alpha to Beta.

### Added
- `llms.txt` at repository root for LLM and AEO crawlers (Claude, ChatGPT, Perplexity).

## [0.1.0] - 2026-04-12

Initial public release.

### Added
- `graphory login`, `graphory status`, `graphory logout`, `graphory --version` CLI commands.
- Local config at `~/.graphory/config.json` with 0600 permissions.
- `Graphory` HTTP client with methods: `search`, `traverse`, `entity`, `timeline`, `stats`, `write`.
- `Graphory.from_config()` helper to instantiate a client from saved credentials.
- `Node` and `Edge` typed models.
- `GraphoryError` exception type for API errors.
- httpx-based transport, Python 3.9+ supported.
