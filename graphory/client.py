"""Graphory Python SDK - Query your knowledge graph from any AI tool.

Usage:
    from graphory import Graphory

    g = Graphory(api_key="gs_ak_...", org_id="org_01...")

    # Search
    results = g.search("Acme Corp")

    # Get entity
    entity = g.entity("contact:dana@acme.example")

    # Traverse
    neighbors = g.traverse("contact:dana@acme.example", depth=2)

    # Timeline
    timeline = g.timeline("acme-corp")

    # Stats
    stats = g.stats()

    # Write
    g.write(action="upsert_node", label="Activity", node_id="meeting:123",
            properties={"name": "Meeting"}, confidence=0.95)

    # Save conversation (2-step)
    schema = g.conversation_schema()
    g.save_conversation(data="---\\ntitle: ...\\n---\\n...")
"""

from typing import Optional
import httpx


class GraphoryError(Exception):
    """Raised when the Graphory API returns an error."""

    def __init__(self, message: str, status_code: int = 0, detail: str = ""):
        self.message = message
        self.status_code = status_code
        self.detail = detail
        super().__init__(message)


class Graphory:
    """Client for the Graphory Graph API.

    Args:
        api_key: Your Graphory API key (gs_ak_... or admin key).
        org_id: Your organization ID (org_01...).
        base_url: API base URL. Defaults to https://api.graphory.io.
        timeout: Request timeout in seconds. Defaults to 30.
    """

    def __init__(
        self,
        api_key: str,
        org_id: str,
        base_url: str = "https://api.graphory.io",
        timeout: float = 30.0,
    ):
        self.api_key = api_key
        self.org_id = org_id
        self.base_url = base_url.rstrip("/")
        self._client = httpx.Client(
            base_url=self.base_url,
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json",
            },
            timeout=timeout,
        )

    @classmethod
    def from_config(
        cls,
        config_path: Optional[str] = None,
        timeout: float = 30.0,
    ) -> "Graphory":
        """Load credentials from ~/.graphory/config.json (written by `graphory login`).

        Args:
            config_path: Optional override path to a config JSON file.
            timeout: Request timeout in seconds.

        Returns:
            A Graphory client configured from the saved credentials.

        Raises:
            GraphoryError: If the config file is missing or malformed.
        """
        import json
        from pathlib import Path

        path = Path(config_path) if config_path else Path.home() / ".graphory" / "config.json"
        if not path.exists():
            raise GraphoryError(
                f"No Graphory config found at {path}. Run `graphory login` first."
            )
        try:
            with open(path, "r", encoding="utf-8") as f:
                cfg = json.load(f)
        except (OSError, json.JSONDecodeError) as e:
            raise GraphoryError(f"Failed to read {path}: {e}")

        api_key = cfg.get("api_key")
        org_id = cfg.get("org_id")
        base_url = cfg.get("base_url", "https://api.graphory.io")
        if not api_key or not org_id:
            raise GraphoryError(
                f"Config at {path} is missing api_key or org_id. Run `graphory login` again."
            )
        return cls(api_key=api_key, org_id=org_id, base_url=base_url, timeout=timeout)

    def _url(self, path: str) -> str:
        """Build org-scoped URL path."""
        return f"/org/{self.org_id}/{path}"

    def _handle_response(self, resp: httpx.Response) -> dict:
        """Parse response, raise GraphoryError on failure."""
        if resp.status_code >= 400:
            try:
                body = resp.json()
                detail = body.get("detail", resp.text)
            except Exception:
                detail = resp.text
            raise GraphoryError(
                message=f"API error {resp.status_code}: {detail}",
                status_code=resp.status_code,
                detail=str(detail),
            )
        return resp.json()

    # -- Read endpoints --------------------------------------------------------

    def search(
        self,
        query: str,
        limit: int = 20,
        node_type: Optional[str] = None,
        entity: Optional[str] = None,
    ) -> list[dict]:
        """Search the graph using BM25-style keyword matching.

        Args:
            query: Search text (matched against name, title, email, id).
            limit: Max results (1-1000, default 20).
            node_type: Filter by node label (Person, Organization, Activity,
                       Asset, Account, Thread).
            entity: Filter by entity slug within the org.

        Returns:
            List of matching node dicts with id, label, name, email, type,
            entity, occurred_at, source.
        """
        payload: dict = {"q": query, "limit": limit}
        if node_type:
            payload["node_type"] = node_type
        if entity:
            payload["entity"] = entity

        resp = self._client.post(self._url("search"), json=payload)
        data = self._handle_response(resp)
        return data.get("results", [])

    def entity(self, entity_id: str) -> dict:
        """Get a node and its 1-hop neighborhood.

        Args:
            entity_id: The node ID (e.g. "contact:dana@acme.example").

        Returns:
            Dict with node properties and edges.
        """
        resp = self._client.get(self._url(f"entity/{entity_id}"))
        return self._handle_response(resp)

    def traverse(
        self,
        start_id: str,
        depth: int = 2,
        edge_types: Optional[list[str]] = None,
    ) -> dict:
        """Multi-hop traversal from a starting node.

        Args:
            start_id: Starting node ID.
            depth: How many hops (1-4, default 2).
            edge_types: Optional list of edge types to follow
                        (e.g. ["works_for", "sent"]).

        Returns:
            Dict with paths (list of edge dicts) and count.
        """
        payload: dict = {"start_id": start_id, "depth": depth}
        if edge_types:
            payload["edge_types"] = edge_types

        resp = self._client.post(self._url("traverse"), json=payload)
        return self._handle_response(resp)

    def timeline(
        self,
        entity: Optional[str] = None,
        days: int = 30,
        limit: int = 50,
    ) -> list[dict]:
        """Get recent activities sorted by date.

        Args:
            entity: Filter by entity slug (optional).
            days: How far back to look (1-365, default 30).
            limit: Max results (1-200, default 50).

        Returns:
            List of activity dicts with id, name, type, entity, occurred_at,
            source, amount.
        """
        params: dict = {"days": days, "limit": limit}
        if entity:
            params["entity"] = entity

        resp = self._client.get(self._url("timeline"), params=params)
        data = self._handle_response(resp)
        return data.get("events", [])

    def stats(self) -> dict:
        """Get graph statistics - node and edge counts by type.

        Returns:
            Dict with org_id, nodes (list), edges (list), total_nodes,
            total_edges.
        """
        resp = self._client.get(self._url("stats"))
        return self._handle_response(resp)

    def connections(self) -> list[dict]:
        """List active data source connections for the org.

        Returns:
            List of connection dicts with id, app, entity, status, source.
        """
        resp = self._client.get(self._url("connections"))
        data = self._handle_response(resp)
        return data.get("connections", data) if isinstance(data, dict) else data

    # -- Write endpoints -------------------------------------------------------

    def write(
        self,
        action: str,
        label: Optional[str] = None,
        node_id: Optional[str] = None,
        properties: Optional[dict] = None,
        from_id: Optional[str] = None,
        to_id: Optional[str] = None,
        edge_type: Optional[str] = None,
        confidence: float = 0.95,
        evidence: Optional[str] = None,
    ) -> dict:
        """Write nodes or edges to the graph with confidence gating.

        Confidence thresholds:
        - >= 0.90: direct merge
        - 0.70-0.89: queued for review
        - < 0.70: rejected

        Args:
            action: One of "upsert_node", "create_edge", "correction".
            label: Node label for upsert_node (Person, Organization, etc).
            node_id: Node ID for upsert_node or correction.
            properties: Dict of node/edge properties.
            from_id: Source node ID for create_edge.
            to_id: Target node ID for create_edge.
            edge_type: Relationship type for create_edge.
            confidence: Confidence score (0.0-1.0, default 0.95).
            evidence: Optional text explaining the write.

        Returns:
            Dict with status ("merged", "queued", or "rejected") and details.
        """
        payload: dict = {"action": action, "confidence": confidence}
        if label is not None:
            payload["label"] = label
        if node_id is not None:
            payload["node_id"] = node_id
        if properties is not None:
            payload["properties"] = properties
        if from_id is not None:
            payload["from_id"] = from_id
        if to_id is not None:
            payload["to_id"] = to_id
        if edge_type is not None:
            payload["edge_type"] = edge_type
        if evidence is not None:
            payload["evidence"] = evidence

        resp = self._client.post(self._url("write"), json=payload)
        return self._handle_response(resp)

    # -- Conversation endpoints ------------------------------------------------

    def conversation_schema(self) -> str:
        """Get the conversation save schema (Step 1 of 2-step flow).

        Returns the YAML frontmatter format expected by save_conversation().

        Returns:
            Schema instructions as a string.
        """
        resp = self._client.get(self._url("conversation/schema"))
        data = self._handle_response(resp)
        return data.get("schema", "")

    def save_conversation(self, data: str) -> dict:
        """Save structured conversation data (Step 2 of 2-step flow).

        Args:
            data: Complete .md content with YAML frontmatter and body text.
                  Must include company, title, type, and who fields.

        Returns:
            Dict with created node/edge IDs and status.
        """
        resp = self._client.post(
            self._url("conversation"), json={"data": data}
        )
        return self._handle_response(resp)

    # -- Utility ---------------------------------------------------------------

    def usage(self) -> dict:
        """Get node count, plan limits, and usage percentage.

        Returns:
            Dict with plan, current node count, limit, percent used.
        """
        resp = self._client.get(self._url("usage"))
        return self._handle_response(resp)

    def close(self):
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.close()

    def __repr__(self):
        return f"Graphory(org_id={self.org_id!r}, base_url={self.base_url!r})"
