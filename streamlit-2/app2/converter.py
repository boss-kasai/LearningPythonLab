import re
from typing import Match


def capitalize_after_digits(text: str) -> str:
    # 数字の後に続く文字をキャプチャする正規表現パターン
    pattern = r"(\d)([a-zA-Z])"

    # キャプチャした文字を大文字に変換する関数
    def capitalize_match(match: Match[str]) -> str:
        return match.group(1) + match.group(2).upper()

    # re.subを使用して置換
    return re.sub(pattern, capitalize_match, text)


def convert_case(text: str, case_type: str) -> str:
    """
    テキストを指定されたケースに変換します。

    :param text: 変換する文字列
    :param case_type: 変換するケースのタイプ
        - 'snake': スネークケース
        - 'camel': キャメルケース
        - 'pascal': パスカルケース
        - 'kebab': ケバブケース
        - 'dot': ドットケース
        - 'train': トレインケース
        - 'upper_snake': アッパースネークケース
        - 'lower': ローワーケース
    :return: 変換された文字列
    """
    # 文末と文頭の空白を削除
    text = text.strip()
    # 非アルファベット文字で単語を分割（スペースや特殊文字を含む）
    words = re.split(r"[\W_]+", text.strip())
    # words内の空文字を削除
    words = [word for word in words if word]  ## この行を追加

    if not words:
        return ""

    if case_type == "snake":
        return "_".join(word.lower() for word in words)

    elif case_type == "camel":
        return words[0].lower() + "".join(word.capitalize() for word in words[1:])

    elif case_type == "pascal":
        return capitalize_after_digits("".join(word.capitalize() for word in words))
    elif case_type == "kebab":
        return "-".join(word.lower() for word in words)

    elif case_type == "dot":
        return ".".join(word.lower() for word in words)

    elif case_type == "train":
        return capitalize_after_digits("-".join(word.capitalize() for word in words))

    elif case_type == "upper_snake":
        return "_".join(word.upper() for word in words)

    elif case_type == "lower":
        return "".join(word.lower() for word in words)

    else:
        raise ValueError(f"Unsupported case type: {case_type}")
