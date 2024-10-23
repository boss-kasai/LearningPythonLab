from src.converter_3 import to_camel_case, to_snake_case

import pytest


# 共通のテストデータフィクスチャ
@pytest.fixture
def test_cases():
    return [
        ("Hello World", "hello_world", "helloWorld"),
        ("Hello, World!", "hello_world", "helloWorld"),
        ("Hello    World", "hello_world", "helloWorld"),
        ("Python 3 is great", "python_3_is_great", "python3IsGreat"),
        ("", "", ""),
        ("hello_world", "hello_world", "helloWorld"),
        ("hello-world", "hello_world", "helloWorld"),
        ("hello@@world!!", "hello_world", "helloWorld"),
        ("   hello world   ", "hello_world", "helloWorld"),
        (
            "This is a very long sentence with multiple words",
            "this_is_a_very_long_sentence_with_multiple_words",
            "thisIsAVeryLongSentenceWithMultipleWords",
        ),
        ("123number starts", "123number_starts", "123numberStarts"),
        ("hello__world", "hello_world", "helloWorld"),
        ("hello\nworld\tpython", "hello_world_python", "helloWorldPython"),
    ]


# パラメータ化を使ってスネークケースとキャメルケースの両方をテスト
@pytest.mark.parametrize(
    "func, index",
    [
        (to_snake_case, 1),  # スネークケースの期待結果はインデックス1
        (to_camel_case, 2),  # キャメルケースの期待結果はインデックス2
    ],
)
def test_case_converter(func, index, test_cases):
    for input_text, expected_snake, expected_camel in test_cases:
        expected = expected_snake if index == 1 else expected_camel
        assert func(input_text) == expected
