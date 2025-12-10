import re
from enum import Enum
from typing import Final, NamedTuple

from emoji import EMOJI_DATA

# Build emoji language pack mapping English names to emoji characters
UNICODE_EMOJI_SET: Final[set[str]] = {
    emj for emj, data in EMOJI_DATA.items() if data["status"] <= 2
}

# Regex patterns for matching emojis
_UNICODE_EMOJI_REGEX: Final[str] = "|".join(
    map(re.escape, sorted(UNICODE_EMOJI_SET, key=len, reverse=True))
)
UNICODE_EMOJI_PATTERN: Final[re.Pattern[str]] = re.compile(_UNICODE_EMOJI_REGEX)


class NodeType(Enum):
    TEXT = 0
    EMOJI = 1


class Node(NamedTuple):
    """Represents a parsed node inside of a string."""

    type: NodeType
    content: str


def contains_emoji(lines: list[str]) -> bool:
    """Check if a string contains any emoji characters using a fast regex pattern.
    Parameters
    ----------
    text : str | list[str]
        The text to check

    Returns
    -------
    bool
        True if the text contains any emoji characters, False otherwise
    """
    for line in lines:
        for char in line:
            if char in UNICODE_EMOJI_SET:
                return True
    return False


def parse_lines(lines: list[str]) -> list[list[Node]]:
    return [_parse_line(line) for line in lines]


def _parse_line(line: str) -> list[Node]:
    """Parse a line of text, identifying Unicode emojis."""
    last_end = 0
    nodes: list[Node] = []

    for matched in UNICODE_EMOJI_PATTERN.finditer(line):
        start, end = matched.span()

        # Add text before the emoji
        if start > last_end:
            nodes.append(Node(NodeType.TEXT, line[last_end:start]))

        # Add emoji node
        emoji_text = matched.group()
        nodes.append(Node(NodeType.EMOJI, emoji_text))

        last_end = end

    # Add remaining text after the last emoji
    if last_end < len(line):
        nodes.append(Node(NodeType.TEXT, line[last_end:]))

    return nodes
