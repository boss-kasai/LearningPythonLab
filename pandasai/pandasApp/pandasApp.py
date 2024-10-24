# import os

# import pandas as pd
# import streamlit as st
# from dotenv import load_dotenv

# from pandasai import PandasAI
# from pandasai.llm.openai import OpenAI

# # .env ファイルの読み込み
# load_dotenv()

# # 環境変数からAPIキーを取得
# openai_api_key = os.getenv("OPENAI_API_KEY")

# if openai_api_key is None:
#     st.error("APIキーが見つかりません。'.env' ファイルを確認してください。")
# else:
#     llm = OpenAI(api_token=openai_api_key)
#     pandas_ai = PandasAI(llm)

#     # Streamlitアプリの内容は前の例と同様
#     st.title("CSVファイルのデータ抽出サービス")

#     uploaded_file = st.file_uploader("CSVファイルをアップロード", type="csv")

#     if uploaded_file is not None:
#         df = pd.read_csv(uploaded_file)
#         st.write("アップロードされたデータ:")
#         st.write(df)

#         user_query = st.text_input("データ抽出に関する質問を入力してください:")

#         if user_query:
#             with st.spinner("データを抽出中..."):
#                 extracted_data = pandas_ai.run(df, prompt=user_query)
#                 st.write("抽出されたデータ:")
#                 st.write(extracted_data)

#                 # データをダウンロード可能なCSVに変換
#                 @st.cache_data
#                 def convert_df(df):
#                     return df.to_csv(index=False).encode("utf-8")

#                 csv = convert_df(extracted_data)

#                 st.download_button(
#                     label="抽出データをCSVでダウンロード",
#                     data=csv,
#                     file_name="extracted_data.csv",
#                     mime="text/csv",
#                 )
