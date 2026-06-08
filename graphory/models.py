"""Graphory data models."""

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class Node:
    """A node in the knowledge graph."""
    id: str
    label: str
    name: str
    properties: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> "Node":
        props = data.get("props") or data.get("properties") or {}
        return cls(
            id=data.get("id", ""),
            label=data.get("label", ""),
            name=data.get("name", props.get("name", "")),
            properties=props,
        )


@dataclass
class Edge:
    """A relationship in the knowledge graph."""
    type: str
    source: str
    target: str
    confidence: float = 0.0
    properties: dict = field(default_factory=dict)

    @classmethod
    def from_dict(cls, data: dict) -> "Edge":
        return cls(
            type=data.get("edge_type") or data.get("type", ""),
            source=data.get("from_id") or data.get("source", ""),
            target=data.get("to_id") or data.get("target", ""),
            confidence=data.get("confidence", 0.0),
            properties=data.get("properties", {}),
        )
