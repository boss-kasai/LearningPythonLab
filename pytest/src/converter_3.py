import re


# スネークケースに変換する関数
def to_snake_case(text: str) -> str:
    # 非単語文字で区切り、小文字に変換しアンダースコアで結合
    words = re.split(r"[\W_]+", text.strip())
    return "_".join(word.lower() for word in words if word)


# キャメルケースに変換する関数
def to_camel_case(text: str) -> str:
    # 非単語文字で区切り、最初の単語は小文字、それ以降は大文字で結合
    words = re.split(r"[\W_]+", text.strip())
    if not words:
        return ""
    return words[0].lower() + "".join(word.capitalize() for word in words[1:] if word)
