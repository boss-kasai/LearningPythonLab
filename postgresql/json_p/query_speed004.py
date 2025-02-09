import time

import psycopg2

# PostgreSQL接続情報
DB_NAME = "test_db"
DB_USER = "postgres"
DB_PASSWORD = "password"
DB_HOST = "localhost"
DB_PORT = "5432"


# クエリの検索速度を測定する関数
def measure_query_speed(table_name, condition):
    conn = psycopg2.connect(
        dbname=DB_NAME, user=DB_USER, password=DB_PASSWORD, host=DB_HOST, port=DB_PORT
    )
    cursor = conn.cursor()

    query = f"SELECT COUNT(*) FROM {table_name} WHERE details ->> 'ジャンル' = %s;"
    start_time = time.time()
    cursor.execute(query, (condition,))
    result = cursor.fetchone()
    end_time = time.time()

    cursor.close()
    conn.close()

    return result[0], end_time - start_time


# 検索条件とテーブル
condition = "和食"  # 飲食業のジャンルを条件とする
tables = ["company_json", "company_jsonb"]


def main():
    for table in tables:
        count, duration = measure_query_speed(table, condition)
        print(f"テーブル: {table}, 該当件数: {count}, 実行時間: {duration:.4f}秒")


if __name__ == "__main__":
    main()
