from typing import List, Tuple

from app.converter import to_snake_case

import pytest


# フィクスチャで入力データを提供
@pytest.fixture  # type: ignore[attr-defined, misc]
def input_data() -> List[Tuple[str, str]]:
    return [
        ("Hello World", "hello_world"),  # 通常の文
        ("Hello, World!", "hello_world"),  # 句読点あり
        ("Hello    World", "hello_world"),  # 複数のスペース
        ("Python 3 is great", "python_3_is_great"),  # 数字を含む
        ("", ""),  # 空の入力
        ("hello_world", "hello_world"),  # 既にスネークケース
        ("hello-world", "hello_world"),  # ハイフンを含む
        ("hello@@world!!", "hello_world"),  # 連続する特殊文字
        ("   hello world   ", "hello_world"),  # 前後のスペース
        (
            "This is a very long sentence with multiple words",
            "this_is_a_very_long_sentence_with_multiple_words",
        ),  # 長い文
        ("123number starts", "123number_starts"),  # 数字で始まる単語
        ("hello__world", "hello_world"),  # 連続するアンダースコア
        ("hello\nworld\tpython", "hello_world_python"),  # 改行とタブ
    ]


# テスト関数でフィクスチャを使用
def test_to_snake_case(input_data: List[Tuple[str, str]]) -> None:
    for input_text, expected in input_data:
        assert to_snake_case(input_text) == expected
