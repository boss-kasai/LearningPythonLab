import time

import psycopg2

# PostgreSQL接続情報
DB_NAME = "test_db"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

# JSON型の更新クエリ
JSON_UPDATE_QUERY = """
UPDATE company_json
SET details = (details::jsonb || '{"補助金": "東京都補助金"}'::jsonb)::json
WHERE details->>'営業時間' = '24時間'
  AND prefecture = 'Tokyo'
  AND industry = '飲食業';
"""

# JSONB型の更新クエリ
JSONB_UPDATE_QUERY = """
UPDATE company_jsonb
SET details = jsonb_set(details, '{補助金}', '"東京都補助金"'::jsonb)
WHERE details->>'営業時間' = '24時間'
  AND prefecture = 'Tokyo'
  AND industry = '飲食業';
"""


# データ更新と速度測定
def update_and_measure(query, table_name):
    try:
        # データベース接続
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        cursor = conn.cursor()

        # 実行前の時間を記録
        start_time = time.time()

        # クエリを実行
        cursor.execute(query)
        conn.commit()

        # 実行後の時間を記録
        end_time = time.time()

        # 実行時間の計測
        elapsed_time = end_time - start_time
        print(f"テーブル: {table_name}, 実行時間: {elapsed_time:.4f}秒")

    except Exception as e:
        print(f"エラー: {e}")
    finally:
        cursor.close()
        conn.close()


# 実行
if __name__ == "__main__":
    print("JSON型の更新処理:")
    update_and_measure(JSON_UPDATE_QUERY, "company_json")

    print("JSONB型の更新処理:")
    update_and_measure(JSONB_UPDATE_QUERY, "company_jsonb")
