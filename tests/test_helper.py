import time


def test_parse_line_by_regex():
    from emosvg.helper import Node, NodeType, _parse_line_by_regex

    line = "👍🏻|👍🏼|👍🏽|👍🏾|👍🏿"
    nodes = _parse_line_by_regex(line)
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
    from emosvg.helper import Node, NodeType, _parse_line_by_regex

    line = "Hello World!"
    nodes = _parse_line_by_regex(line)
    assert nodes == [
        Node(NodeType.TEXT, "Hello World!"),
    ]


def test_parse_line_by_regex_with_mixed_content():
    from emosvg.helper import Node, NodeType, _parse_line_by_regex

    line = "Hello 👍🏻 World 👍🏼!"
    nodes = _parse_line_by_regex(line)
    assert nodes == [
        Node(NodeType.TEXT, "Hello "),
        Node(NodeType.EMOJI, "👍🏻"),
        Node(NodeType.TEXT, " World "),
        Node(NodeType.EMOJI, "👍🏼"),
        Node(NodeType.TEXT, "!"),
    ]


def test_parse_line():
    from emosvg.helper import Node, NodeType, _parse_line

    line = "👍🏻|👍🏼|👍🏽|👍🏾|👍🏿"
    nodes = _parse_line(line)
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


def test_parse_line_with_no_emoji():
    from emosvg.helper import Node, NodeType, _parse_line

    line = "Hello World!"
    nodes = _parse_line(line)
    assert nodes == [
        Node(NodeType.TEXT, "Hello World!"),
    ]


def test_parse_line_with_mixed_content():
    from emosvg.helper import Node, NodeType, _parse_line

    line = "Hello 👍🏻 World 👍🏼!"
    nodes = _parse_line(line)
    assert nodes == [
        Node(NodeType.TEXT, "Hello "),
        Node(NodeType.EMOJI, "👍🏻"),
        Node(NodeType.TEXT, " World "),
        Node(NodeType.EMOJI, "👍🏼"),
        Node(NodeType.TEXT, "!"),
    ]


def test_performance_comparison():
    """性能比较测试：正则表达式 vs emoji_list方法"""
    from emosvg.helper import _parse_line, _parse_line_by_regex

    # 测试用例：包含各种表情的复杂文本
    test_cases = [
        # 简单文本
        ("简单文本", "Hello World!"),
        # 单个表情
        ("单个表情", "😀"),
        # 多个简单表情
        ("多个简单表情", "😀😁😂😃😄😅😆😉😊😋"),
        # 混合文本和表情
        ("混合文本", "Hello 😀 World 😁 Test 😂"),
        # 肤色变体表情
        ("肤色变体", "👍🏻|👍🏼|👍🏽|👍🏾|👍🏿"),
        # 组合表情
        ("组合表情", "👨‍👩‍👧‍👦 👩‍❤️‍👨 👨‍👨‍👧‍👧"),
        # 复杂混合
        (
            "复杂混合",
            "😀 和 😁 还有 😂 一些组合表情 👨‍👩‍👧‍👦 和肤色变体 👍🏻👍🏼👍🏽👍🏾👍🏿",
        ),
    ]

    # 性能测试
    iterations = 1000  # 每个测试用例的迭代次数

    print("\n=== 性能比较测试 ===")
    print(f"每个测试用例迭代次数: {iterations}")
    print("=" * 50)

    results = []

    for case_name, test_case in test_cases:
        print(f"\n测试用例: {case_name}")
        print(f"文本长度: {len(test_case)} 字符")

        # 测试正则表达式方法
        start_time = time.perf_counter()
        result_regex = None
        for _ in range(iterations):
            result_regex = _parse_line_by_regex(test_case)
        regex_time = time.perf_counter() - start_time

        # 测试emoji_list方法
        start_time = time.perf_counter()
        result_emoji = None
        for _ in range(iterations):
            result_emoji = _parse_line(test_case)
        emoji_time = time.perf_counter() - start_time

        # 验证结果一致性
        try:
            assert result_regex == result_emoji, "结果不一致"
            consistency = "✅ 一致"
        except AssertionError:
            consistency = "❌ 不一致"

        # 计算性能差异
        if regex_time < emoji_time:
            faster_method = "正则表达式"
            speed_ratio = emoji_time / regex_time
        else:
            faster_method = "emoji_list"
            speed_ratio = regex_time / emoji_time

        # 输出性能结果
        print(f"  正则表达式方法: {regex_time:.6f} 秒")
        print(f"  emoji_list方法: {emoji_time:.6f} 秒")
        print(f"  结果一致性: {consistency}")
        print(f"  更快的方法: {faster_method} ({speed_ratio:.2f}x)")

        results.append(
            {
                "case": case_name,
                "regex_time": regex_time,
                "emoji_time": emoji_time,
                "faster_method": faster_method,
                "speed_ratio": speed_ratio,
                "consistent": consistency == "✅ 一致",
            }
        )

    # 总结报告
    print("\n" + "=" * 50)
    print("性能测试总结:")
    print("=" * 50)

    regex_wins = sum(1 for r in results if r["faster_method"] == "正则表达式")
    emoji_wins = sum(1 for r in results if r["faster_method"] == "emoji_list")
    consistent_cases = sum(1 for r in results if r["consistent"])

    print(f"正则表达式获胜: {regex_wins}/{len(results)} 个测试用例")
    print(f"emoji_list获胜: {emoji_wins}/{len(results)} 个测试用例")
    print(f"结果一致性: {consistent_cases}/{len(results)} 个测试用例")

    # 平均性能比
    avg_ratio_regex = sum(
        r["speed_ratio"] for r in results if r["faster_method"] == "正则表达式"
    ) / max(regex_wins, 1)
    avg_ratio_emoji = sum(
        r["speed_ratio"] for r in results if r["faster_method"] == "emoji_list"
    ) / max(emoji_wins, 1)

    print(f"正则表达式平均优势: {avg_ratio_regex:.2f}x")
    print(f"emoji_list平均优势: {avg_ratio_emoji:.2f}x")


def test_accuracy_comparison():
    """准确性比较测试：验证两种方法对组合表情的处理"""
    from emosvg.helper import _parse_line, _parse_line_by_regex

    # 测试组合表情的准确性
    complex_emojis = [
        "👨‍👩‍👧‍👦",  # 家庭
        "👩‍❤️‍👨",  # 情侣
        "👍🏻",  # 肤色变体
        "🏴",  # 旗帜
    ]

    print("\n=== 准确性比较测试 ===")

    for emoji in complex_emojis:
        result_regex = _parse_line_by_regex(emoji)
        result_emoji = _parse_line(emoji)

        print(f"\n表情: {emoji}")
        print(f"正则表达式结果: {result_regex}")
        print(f"emoji_list结果: {result_emoji}")
        print(f"是否一致: {result_regex == result_emoji}")

        # 检查节点数量
        print(f"正则表达式节点数: {len(result_regex)}")
        print(f"emoji_list节点数: {len(result_emoji)}")

        if len(result_regex) != len(result_emoji):
            print("⚠️ 节点数量不一致，可能存在组合表情识别问题")


def test_memory_usage_comparison():
    """内存使用比较测试（简单估算）"""
    import sys

    from emosvg.helper import _parse_line, _parse_line_by_regex

    test_text = "Hello 😀 World 😁 with 👨‍👩‍👧‍👦 family and 👍🏻👍🏼👍🏽👍🏾👍🏿"

    # 测试正则表达式方法的内存使用
    result_regex = _parse_line_by_regex(test_text)
    regex_memory = sys.getsizeof(result_regex) + sum(
        sys.getsizeof(node) for node in result_regex
    )

    # 测试emoji_list方法的内存使用
    result_emoji = _parse_line(test_text)
    emoji_memory = sys.getsizeof(result_emoji) + sum(
        sys.getsizeof(node) for node in result_emoji
    )

    print("\n=== 内存使用比较 ===")
    print(f"测试文本: {test_text}")
    print(f"正则表达式方法内存: {regex_memory} 字节")
    print(f"emoji_list方法内存: {emoji_memory} 字节")
    print(f"内存差异: {abs(regex_memory - emoji_memory)} 字节")

    if regex_memory < emoji_memory:
        print("✅ 正则表达式方法更节省内存")
    else:
        print("✅ emoji_list方法更节省内存")
