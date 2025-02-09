import psycopg2

# PostgreSQL接続情報
DB_NAME = "test_db"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"

# テーブル作成クエリ
CREATE_JSON_TABLE = """
-- 企業情報テーブル
CREATE TABLE company_json (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    prefecture VARCHAR(100) NOT NULL,
    industry VARCHAR(50) NOT NULL,
    details JSON
);
"""

CREATE_JSONB_TABLE = """
-- 企業情報テーブル
CREATE TABLE company_jsonb (
    id SERIAL PRIMARY KEY,
    company_name VARCHAR(100) NOT NULL,
    prefecture VARCHAR(100) NOT NULL,
    industry VARCHAR(50) NOT NULL,
    details JSONB
);
"""


def create_tables():
    try:
        # PostgreSQLに接続
        conn = psycopg2.connect(
            dbname=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD,
            host=DB_HOST,
            port=DB_PORT,
        )
        cursor = conn.cursor()

        # テーブル作成
        cursor.execute(CREATE_JSON_TABLE)
        cursor.execute(CREATE_JSONB_TABLE)

        # コミットして接続を閉じる
        conn.commit()
        print("テーブルが作成されました。")
    except Exception as e:
        print(f"エラーが発生しました: {e}")
    finally:
        cursor.close()
        conn.close()


# 関数を実行
create_tables()
