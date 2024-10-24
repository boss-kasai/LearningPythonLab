import re


def to_snake_case(text: str) -> str:
    # 非単語文字（スペース、句読点、記号、タブ、改行など）をアンダースコアで置き換える
    # 連続するアンダースコアや、末尾のアンダースコアが残らないように調整
    text = re.sub(
        r"[\W_]+", "_", text.strip()
    )  # 非単語文字をアンダースコアに変換し、前後の空白を削除
    return text.lower().rstrip("_")  # 末尾の余分なアンダースコアを削除
