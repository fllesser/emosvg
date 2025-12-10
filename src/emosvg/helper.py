from enum import Enum
from typing import Final, NamedTuple

from emoji import EMOJI_DATA

# Build emoji language pack mapping English names to emoji characters
UNICODE_EMOJI_SET: Final[set[str]] = {
    emj for emj, data in EMOJI_DATA.items() if data["status"] <= 2
}


class NodeType(Enum):
    TEXT = 0
    EMOJI = 1


class Node(NamedTuple):
    """Represents a parsed node inside of a string."""

    type: NodeType
    content: str


def contains_emoji(lines: list[str]) -> bool:
    """Check if a string contains any emoji characters"""
    for line in lines:
        for char in line:
            if char in UNICODE_EMOJI_SET:
                return True
    return False


def parse_lines(lines: list[str]) -> list[list[Node]]:
    return [_parse_line(line) for line in lines]


def _parse_line(line: str):
    """Parse a line of text, identifying Unicode emojis."""
    nodes: list[Node] = []
    for char in line:
        if char in UNICODE_EMOJI_SET:
            nodes.append(Node(NodeType.EMOJI, char))
        else:
            nodes.append(Node(NodeType.TEXT, char))
    return nodes
