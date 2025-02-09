import streamlit as st
from converter import convert_case


def main() -> None:
    st.title("Text Naming Convention Converter")

    # 入力欄
    input_text = st.text_input("Enter your text here")

    # プルダウンメニューの選択肢
    options = [
        "snake",
        "camel",
        "pascal",
        "kebab",
        "dot",
        "train",
        "upper_snake",
        "lower",
    ]

    # プルダウンメニューの作成
    selected_option = st.selectbox("Choose an option", options)

    # ボタンで変換
    if st.button("Convert"):
        result = convert_case(input_text, selected_option)

        # 結果表示
        st.success(f"{result}")


if __name__ == "__main__":
    main()
