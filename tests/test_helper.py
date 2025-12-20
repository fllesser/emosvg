def test_parse_line_by_regex():
    from emosvg.regex import Node, NodeType, parse_line_by_regex

    line = "👍🏻|👍🏼|👍🏽|👍🏾|👍🏿"
    nodes = parse_line_by_regex(line)
    assert nodes == [
        Node(NodeType.EMOJI, "👍🏻"),
        Node(NodeType.TEXT, "|"),
        Node(NodeType.EMOJI, "👍🏼"),
        Node(NodeType.TEXT, "|"),
        Node(NodeType.EMOJI, "👍🏽"),
        Node(NodeType.TEXT, "|"),
        Node(NodeType.EMOJI, "👍🏾"),
        Node(NodeType.TEXT, "|"),
        Node(NodeType.EMOJI, "👍🏿"),
    ]


def test_parse_line_by_regex_with_no_emoji():
    from emosvg.regex import Node, NodeType, parse_line_by_regex

    line = "Hello World!"
    nodes = parse_line_by_regex(line)
    assert nodes == [
        Node(NodeType.TEXT, "Hello World!"),
    ]


def test_parse_line_by_regex_with_mixed_content():
    from emosvg.regex import Node, NodeType, parse_line_by_regex

    line = "Hello 👍🏻 World 👍🏼!"
    nodes = parse_line_by_regex(line)
    assert nodes == [
        Node(NodeType.TEXT, "Hello "),
        Node(NodeType.EMOJI, "👍🏻"),
        Node(NodeType.TEXT, " World "),
        Node(NodeType.EMOJI, "👍🏼"),
        Node(NodeType.TEXT, "!"),
    ]


def test_parse_line():
    from emosvg.helper import Node, NodeType, parse_line

    line = "👍🏻|👍🏼|👍🏽|👍🏾|👍🏿"
    nodes = parse_line(line)
    assert nodes == [
        Node(NodeType.EMOJI, "👍🏻"),
        Node(NodeType.TEXT, "|"),
        Node(NodeType.EMOJI, "👍🏼"),
        Node(NodeType.TEXT, "|"),
        Node(NodeType.EMOJI, "👍🏽"),
        Node(NodeType.TEXT, "|"),
        Node(NodeType.EMOJI, "👍🏾"),
        Node(NodeType.TEXT, "|"),
        Node(NodeType.EMOJI, "👍🏿"),
    ]


def test_parse_line_with_mixed_content():
    from emosvg.helper import Node, NodeType, parse_line

    line = "Hello 👍🏻 World 👍🏼!"
    nodes = parse_line(line)
    assert nodes == [
        Node(NodeType.TEXT, "Hello "),
        Node(NodeType.EMOJI, "👍🏻"),
        Node(NodeType.TEXT, " World "),
        Node(NodeType.EMOJI, "👍🏼"),
        Node(NodeType.TEXT, "!"),
    ]


def test_parse_line_with_no_emoji():
    from emosvg.helper import Node, NodeType, parse_line

    line = "Hello World!"
    nodes = parse_line(line)
    assert nodes == [
        Node(NodeType.TEXT, "Hello World!"),
    ]


def test_parse_lines():
    from emosvg.helper import Node, NodeType, parse_lines

    lines = ["Hello 👍🏻 World 👍🏼!", "👍🏽|👍🏾|👍🏿"]
    nodes = parse_lines(lines)
    assert nodes == [
        [
            Node(NodeType.TEXT, "Hello "),
            Node(NodeType.EMOJI, "👍🏻"),
            Node(NodeType.TEXT, " World "),
            Node(NodeType.EMOJI, "👍🏼"),
            Node(NodeType.TEXT, "!"),
        ],
        [
            Node(NodeType.EMOJI, "👍🏽"),
            Node(NodeType.TEXT, "|"),
            Node(NodeType.EMOJI, "👍🏾"),
            Node(NodeType.TEXT, "|"),
            Node(NodeType.EMOJI, "👍🏿"),
        ],
    ]


def test_parse_lines_by_regex():
    from emosvg.regex import Node, NodeType, parse_lines_by_regex

    lines = ["Hello 👍🏻 World 👍🏼!", "👍🏽|👍🏾|👍🏿"]
    nodes = parse_lines_by_regex(lines)
    assert nodes == [
        [
            Node(NodeType.TEXT, "Hello "),
            Node(NodeType.EMOJI, "👍🏻"),
            Node(NodeType.TEXT, " World "),
            Node(NodeType.EMOJI, "👍🏼"),
            Node(NodeType.TEXT, "!"),
        ],
        [
            Node(NodeType.EMOJI, "👍🏽"),
            Node(NodeType.TEXT, "|"),
            Node(NodeType.EMOJI, "👍🏾"),
            Node(NodeType.TEXT, "|"),
            Node(NodeType.EMOJI, "👍🏿"),
        ],
    ]
