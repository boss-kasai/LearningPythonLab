import csv
import logging
import os
import random
import string
import time
from tempfile import NamedTemporaryFile

import numpy as np
import psycopg2


# ロガー設定
def get_logger():
    logger = logging.getLogger(__name__)
    logger.setLevel(logging.INFO)
    handler = logging.StreamHandler()
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
    handler.setFormatter(formatter)
    logger.addHandler(handler)
    return logger


logger = get_logger()


# タグのダミーデータを生成する
def generate_tags(tag_length):
    return "".join(random.choices(string.ascii_lowercase, k=tag_length))


# ランダム数の生成
def generate_random_integer(mean=10000, std_dev=5000, low=50, high=100000, size=1):
    values = np.random.normal(mean, std_dev, size)
    values = np.clip(values, low, high)
    return np.round(values).astype(int)


# PostgreSQLに接続
def make_connection():
    return psycopg2.connect(
        dbname="test_db",
        user="postgres",
        password="password",
        host="localhost",
        port="5432",
    )


# 企業データの挿入（COPY FROMを使用）
def insert_companies():
    conn = make_connection()
    cursor = conn.cursor()

    # 企業名のダミーデータを生成
    start_time = time.time()
    company_names = [("株式会社" + generate_tags(5),) for _ in range(3_000_000)]
    logger.info(f"企業名ダミーデータ生成_処理時間: {time.time() - start_time:.5f} 秒")

    # 一時CSVファイルを作成
    with NamedTemporaryFile(mode="w", delete=False, newline="") as tmpfile:
        writer = csv.writer(tmpfile)
        writer.writerows(company_names)
        temp_file_path = tmpfile.name

    # COPY FROMを実行
    start_time = time.time()
    with open(temp_file_path, "r") as f:
        cursor.copy_from(f, "companies", sep=",", columns=("name",))

    conn.commit()
    logger.info(f"企業データ挿入（COPY）_処理時間: {time.time() - start_time:.5f} 秒")

    cursor.close()
    conn.close()


# タグデータの挿入（COPY FROMを使用）
def insert_tags():
    conn = make_connection()
    cursor = conn.cursor()

    # companiesの全IDを取得
    cursor.execute("SELECT id FROM companies")
    company_ids = [row[0] for row in cursor.fetchall()]

    # ダミーデータ生成
    tag_data = []
    for _ in range(200):
        # タグの生成
        start_time = time.time()
        tag_name = generate_tags(6)
        how_many = generate_random_integer(size=1)[0]
        selected_company_ids = random.sample(company_ids, how_many)

        print(f"{_}回目 - {how_many}件の企業に{tag_name}を付与")

        ## all_in_tag テーブルへの挿入
        tag_data = []
        tag_data.extend([(company_id, tag_name) for company_id in selected_company_ids])
        # 一時CSVファイルを作成
        with NamedTemporaryFile(mode="w", delete=False, newline="") as tmpfile:
            writer = csv.writer(tmpfile)
            writer.writerows(tag_data)
            temp_file_path = tmpfile.name

        # COPY FROMを実行
        start_time = time.time()
        with open(temp_file_path, "r") as f:
            cursor.copy_from(
                f, "all_in_tag", sep=",", columns=("company_id", "tag_name")
            )

        conn.commit()
        os.remove(temp_file_path)
        logger.info(
            f"中間テーブルなし_処理時間{len(tag_data)}: {time.time() - start_time:.5f} 秒"
        )

        ## tags テーブルへの挿入
        # tagsテーブルにタグが登録されているかを確認する
        start_time = time.time()
        cursor.execute("SELECT id, tag FROM tags WHERE tag = %s", (tag_name,))
        tag_id = cursor.fetchone()
        if tag_id is None:
            cursor.execute(
                "INSERT INTO tags (tag) VALUES (%s) RETURNING id", (tag_name,)
            )
            tag_id = cursor.fetchone()[0]
        else:
            tag_id = tag_id[0]
        tag_id = int(tag_id)
        # l_company_tag テーブルへの挿入
        l_company_tag_data = []
        for company_id in selected_company_ids:
            l_company_tag_data.append((company_id, tag_id))
        # 一時CSVファイルを作成
        with NamedTemporaryFile(mode="w", delete=False, newline="") as tmpfile:
            writer = csv.writer(tmpfile)
            writer.writerows(l_company_tag_data)
            temp_file_path = tmpfile.name

        # COPY FROMを実行
        with open(temp_file_path, "r") as f:
            cursor.copy_from(
                f, "l_company_tag", sep=",", columns=("company_id", "tag_id")
            )
        conn.commit()
        logger.info(
            f"中間テーブルあり_処理時間{len(l_company_tag_data)}: {time.time() - start_time:.5f} 秒"
        )

    cursor.close()
    conn.close()


# 実行
def main():
    # insert_companies()
    insert_tags()


main()
