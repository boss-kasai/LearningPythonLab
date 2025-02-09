import streamlit as st
from converter import to_snake_case


def main() -> None:
    st.title("Text Naming Convention Converter")

    # 入力欄
    input_text = st.text_input("Enter your text here")

    # ボタンで変換
    if st.button("Convert"):
        result = to_snake_case(input_text)

        # 結果表示
        st.success(f"{result}")


if __name__ == "__main__":
    main()
