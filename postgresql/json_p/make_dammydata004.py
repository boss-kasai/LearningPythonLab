import json
import random

import psycopg2

# 47都道府県リスト
PREFECTURES = [
    "Hokkaido",
    "Aomori",
    "Iwate",
    "Miyagi",
    "Akita",
    "Yamagata",
    "Fukushima",
    "Ibaraki",
    "Tochigi",
    "Gunma",
    "Saitama",
    "Chiba",
    "Tokyo",
    "Kanagawa",
    "Niigata",
    "Toyama",
    "Ishikawa",
    "Fukui",
    "Yamanashi",
    "Nagano",
    "Gifu",
    "Shizuoka",
    "Aichi",
    "Mie",
    "Shiga",
    "Kyoto",
    "Osaka",
    "Hyogo",
    "Nara",
    "Wakayama",
    "Tottori",
    "Shimane",
    "Okayama",
    "Hiroshima",
    "Yamaguchi",
    "Tokushima",
    "Kagawa",
    "Ehime",
    "Kochi",
    "Fukuoka",
    "Saga",
    "Nagasaki",
    "Kumamoto",
    "Oita",
    "Miyazaki",
    "Kagoshima",
    "Okinawa",
]

# 業種リスト
INDUSTRIES = ["飲食業", "製造業", "物流業", "医療"]


# 業種に応じたJSONデータ生成
def generate_details(industry):
    if industry == "飲食業":
        return {
            "ジャンル": random.choice(["和食", "洋食", "中華", "ファストフード"]),
            "店舗数": random.randint(1, 100),
            "営業時間": random.choice(["9:00-18:00", "11:00-23:00", "24時間"]),
        }
    elif industry == "製造業":
        return {
            "ジャンル": random.choice(["食品", "機械", "化学", "電子"]),
            "工場情報": {
                "所在地": random.choice(PREFECTURES),
                "従業員数": random.randint(10, 1000),
            },
        }
    elif industry == "物流業":
        return {"所有トラック台数": random.randint(1, 500)}
    elif industry == "医療":
        return {"対応科": random.choice(["内科", "外科", "小児科", "皮膚科", "眼科"])}


# ダミーデータ生成
def generate_data():
    data = []
    for i in range(100000):
        industry = random.choice(INDUSTRIES)
        data.append(
            {
                "company_name": f"Company_{i}",
                "prefecture": random.choice(PREFECTURES),
                "industry": industry,
                "details": generate_details(industry),
            }
        )
    return data


# PostgreSQLに接続してデータを挿入
def insert_data():
    conn = psycopg2.connect(
        dbname="test_db",
        user="postgres",
        password="password",
        host="localhost",
        port="5432",
    )
    cursor = conn.cursor()

    data = generate_data()

    for record in data:
        # company_json (JSON型のテーブル) への挿入
        cursor.execute(
            "INSERT INTO company_json (company_name, prefecture, industry, details) VALUES (%s, %s, %s, %s)",
            (
                record["company_name"],
                record["prefecture"],
                record["industry"],
                json.dumps(record["details"]),
            ),
        )

        # company_jsonb (JSONB型のテーブル) への挿入
        cursor.execute(
            "INSERT INTO company_jsonb (company_name, prefecture, industry, details) VALUES (%s, %s, %s, %s)",
            (
                record["company_name"],
                record["prefecture"],
                record["industry"],
                json.dumps(record["details"]),
            ),
        )

    conn.commit()
    cursor.close()
    conn.close()


insert_data()
