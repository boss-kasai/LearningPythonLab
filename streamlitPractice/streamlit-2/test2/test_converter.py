from typing import Dict, List, Tuple

from app2.converter import convert_case

import pytest


# テストデータ
@pytest.fixture  # type: ignore[attr-defined, misc]
def test_cases() -> List[Tuple[str, Dict[str, str]]]:
    return [
        # 通常の文
        (
            "hello world",
            {
                "snake": "hello_world",
                "camel": "helloWorld",
                "pascal": "HelloWorld",
                "kebab": "hello-world",
                "dot": "hello.world",
                "train": "Hello-World",
                "upper_snake": "HELLO_WORLD",
                "lower": "helloworld",
            },
        ),
        # 大文字あり
        (
            "Hello World",
            {
                "snake": "hello_world",
                "camel": "helloWorld",
                "pascal": "HelloWorld",
                "kebab": "hello-world",
                "dot": "hello.world",
                "train": "Hello-World",
                "upper_snake": "HELLO_WORLD",
                "lower": "helloworld",
            },
        ),
        # 句読点あり
        (
            "Hello, World!",
            {
                "snake": "hello_world",
                "camel": "helloWorld",
                "pascal": "HelloWorld",
                "kebab": "hello-world",
                "dot": "hello.world",
                "train": "Hello-World",
                "upper_snake": "HELLO_WORLD",
                "lower": "helloworld",
            },
        ),
        # 文末や文頭にスペース
        (
            " hello world ",
            {
                "snake": "hello_world",
                "camel": "helloWorld",
                "pascal": "HelloWorld",
                "kebab": "hello-world",
                "dot": "hello.world",
                "train": "Hello-World",
                "upper_snake": "HELLO_WORLD",
                "lower": "helloworld",
            },
        ),
        # 複数のスペース
        (
            "Hello    World",
            {
                "snake": "hello_world",
                "camel": "helloWorld",
                "pascal": "HelloWorld",
                "kebab": "hello-world",
                "dot": "hello.world",
                "train": "Hello-World",
                "upper_snake": "HELLO_WORLD",
                "lower": "helloworld",
            },
        ),
        # 数字を含む
        (
            "Python 3 is great",
            {
                "snake": "python_3_is_great",
                "camel": "python3IsGreat",
                "pascal": "Python3IsGreat",
                "kebab": "python-3-is-great",
                "dot": "python.3.is.great",
                "train": "Python-3-Is-Great",
                "upper_snake": "PYTHON_3_IS_GREAT",
                "lower": "python3isgreat",
            },
        ),
        # 空の入力
        (
            "",
            {
                "snake": "",
                "camel": "",
                "pascal": "",
                "kebab": "",
                "dot": "",
                "train": "",
                "upper_snake": "",
                "lower": "",
            },
        ),
        # 既にスネークケース
        (
            "hello_world",
            {
                "snake": "hello_world",
                "camel": "helloWorld",
                "pascal": "HelloWorld",
                "kebab": "hello-world",
                "dot": "hello.world",
                "train": "Hello-World",
                "upper_snake": "HELLO_WORLD",
                "lower": "helloworld",
            },
        ),
        # ハイフンを含む
        (
            "hello-world",
            {
                "snake": "hello_world",
                "camel": "helloWorld",
                "pascal": "HelloWorld",
                "kebab": "hello-world",
                "dot": "hello.world",
                "train": "Hello-World",
                "upper_snake": "HELLO_WORLD",
                "lower": "helloworld",
            },
        ),
        # 連続する特殊文字
        (
            "hello@@world!!",
            {
                "snake": "hello_world",
                "camel": "helloWorld",
                "pascal": "HelloWorld",
                "kebab": "hello-world",
                "dot": "hello.world",
                "train": "Hello-World",
                "upper_snake": "HELLO_WORLD",
                "lower": "helloworld",
            },
        ),
        # 前後のスペース
        (
            "   hello world   ",
            {
                "snake": "hello_world",
                "camel": "helloWorld",
                "pascal": "HelloWorld",
                "kebab": "hello-world",
                "dot": "hello.world",
                "train": "Hello-World",
                "upper_snake": "HELLO_WORLD",
                "lower": "helloworld",
            },
        ),
        # 長い文
        (
            "This is a very long sentence with multiple words",
            {
                "snake": "this_is_a_very_long_sentence_with_multiple_words",
                "camel": "thisIsAVeryLongSentenceWithMultipleWords",
                "pascal": "ThisIsAVeryLongSentenceWithMultipleWords",
                "kebab": "this-is-a-very-long-sentence-with-multiple-words",
                "dot": "this.is.a.very.long.sentence.with.multiple.words",
                "train": "This-Is-A-Very-Long-Sentence-With-Multiple-Words",
                "upper_snake": "THIS_IS_A_VERY_LONG_SENTENCE_WITH_MULTIPLE_WORDS",
                "lower": "thisisaverylongsentencewithmultiplewords",
            },
        ),
        # 数字で始まる単語
        (
            "123number starts",
            {
                "snake": "123number_starts",
                "camel": "123numberStarts",
                "pascal": "123NumberStarts",
                "kebab": "123number-starts",
                "dot": "123number.starts",
                "train": "123Number-Starts",
                "upper_snake": "123NUMBER_STARTS",
                "lower": "123numberstarts",
            },
        ),
        # 連続するアンダースコア
        (
            "hello__world",
            {
                "snake": "hello_world",
                "camel": "helloWorld",
                "pascal": "HelloWorld",
                "kebab": "hello-world",
                "dot": "hello.world",
                "train": "Hello-World",
                "upper_snake": "HELLO_WORLD",
                "lower": "helloworld",
            },
        ),
        # 改行とタブ
        (
            "hello\nworld\tpython",
            {
                "snake": "hello_world_python",
                "camel": "helloWorldPython",
                "pascal": "HelloWorldPython",
                "kebab": "hello-world-python",
                "dot": "hello.world.python",
                "train": "Hello-World-Python",
                "upper_snake": "HELLO_WORLD_PYTHON",
                "lower": "helloworldpython",
            },
        ),
    ]


@pytest.mark.parametrize(  # type: ignore[attr-defined, misc]
    "case_type",
    [
        "snake",
        "camel",
        "pascal",
        "kebab",
        "dot",
        "train",
        "upper_snake",
        "lower",
    ],
)
def test_convert_case(
    case_type: str, test_cases: List[Tuple[str, Dict[str, str]]]
) -> None:
    for input_text, expected_outputs in test_cases:
        assert convert_case(input_text, case_type) == expected_outputs[case_type]
