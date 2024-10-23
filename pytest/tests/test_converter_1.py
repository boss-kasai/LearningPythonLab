from src.converter_1 import (
    convert_to_snake_case,  # 先ほど作成した関数をimportする
)


def test_convert_to_snake_case():
    assert (
        convert_to_snake_case("hello world") == "hello_world"
    )  # 入力と出力の理想系を入力する
