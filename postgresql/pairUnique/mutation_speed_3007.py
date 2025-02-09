import random
import string
import time
from typing import Tuple

import pandas as pd
from sqlalchemy import create_engine, exists
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.orm import sessionmaker

from postgresql.pairUnique.make_table007 import Company, LCompanyTag, Tag

# PostgreSQL の接続設定
DATABASE_URL = "postgresql://postgres:password@localhost:5432/test_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# テストの回数
num_trials = 50


# 既存の組み合わせを取得（重複テスト用）
def get_existing_company_tag_ids(session) -> Tuple[int, int]:
    existing_ids = session.query(LCompanyTag.company_id, LCompanyTag.tag_id).all()
    return random.choice(existing_ids)


# ランダムなタグを生成する
def generate_random_string(length=8) -> str:
    return "".join(random.choices(string.ascii_lowercase, k=length))


# tags テーブルにタグがあるかを確認する
def check_tag_exists(session, tag) -> int:
    """
    tags テーブルにタグが存在するか確認。存在しない場合は新規に追加する。

    戻り値：tag_id
    """
    tag_id = session.query(Tag.id).filter(Tag.tag == tag).scalar()
    if tag_id is None:
        new_tag = Tag(tag=tag)
        session.add(new_tag)
        session.commit()
        tag_id = new_tag.id
    return tag_id


# ランダムな企業IDを取得
def get_random_company_ids(session, num_ids) -> list:
    company_ids = session.query(Company.id).all()
    company_ids = [
        id[0] for id in company_ids
    ]  # タプルから企業IDを取り出してリストに変換
    return random.sample(
        company_ids, num_ids
    )  # 指定された数の企業IDを重複なしでランダムに選択して返す


# 計測データの保存用
results = {
    "UNIQUE制約 + 通常INSERT": {"新規": [], "重複": []},
    "ON CONFLICT DO NOTHING": {"新規": [], "重複": []},
    "SELECTで事前チェック": {"新規": [], "重複": []},
    "INSERT ... WHERE NOT EXISTS": {"新規": [], "重複": []},
}


# 各方法の挿入処理
def insert_with_unique_constraint(company_id, tag_id) -> float:
    session = SessionLocal()
    start_time = time.perf_counter()
    try:
        new_entry = LCompanyTag(company_id=company_id, tag_id=tag_id)
        session.add(new_entry)
        session.commit()
    except Exception:
        session.rollback()
    session.close()
    elapsed_time = time.perf_counter() - start_time
    return elapsed_time


def insert_with_on_conflict(company_id, tag_id) -> float:
    session = SessionLocal()
    start_time = time.perf_counter()
    stmt = (
        insert(LCompanyTag)
        .values(company_id=company_id, tag_id=tag_id)
        .on_conflict_do_nothing()
    )
    session.execute(stmt)
    session.commit()
    session.close()
    elapsed_time = time.perf_counter() - start_time
    return elapsed_time


def insert_with_select_check(company_id, tag_id) -> float:
    session = SessionLocal()
    start_time = time.perf_counter()
    exists_query = session.query(
        exists().where(
            (LCompanyTag.company_id == company_id) & (LCompanyTag.tag_id == tag_id)
        )
    ).scalar()
    if not exists_query:
        new_entry = LCompanyTag(company_id=company_id, tag_id=tag_id)
        session.add(new_entry)
        session.commit()
    session.close()
    elapsed_time = time.perf_counter() - start_time
    return elapsed_time


def insert_with_where_not_exists_orm(company_id, tag_id) -> float:
    """
    ORM を使用した `INSERT ... WHERE NOT EXISTS`
    """
    session = SessionLocal()
    start_time = time.perf_counter()

    # `company_id` と `tag_id` の組み合わせが存在するか確認
    exists_query = session.query(
        exists().where(
            (LCompanyTag.company_id == company_id) & (LCompanyTag.tag_id == tag_id)
        )
    ).scalar()

    if not exists_query:
        new_entry = LCompanyTag(company_id=company_id, tag_id=tag_id)
        session.add(new_entry)
        session.commit()

    session.close()
    elapsed_time = time.perf_counter() - start_time
    return elapsed_time


# 各方法の処理時間を計測
for _ in range(num_trials):
    session = SessionLocal()

    # 新規データの挿入
    # 企業IDとタグIDを取得
    company_ids = get_random_company_ids(session, 4)
    tag = generate_random_string()
    tag_id = check_tag_exists(session, tag)
    results["UNIQUE制約 + 通常INSERT"]["新規"].append(
        insert_with_unique_constraint(company_ids[0], tag_id)
    )
    results["ON CONFLICT DO NOTHING"]["新規"].append(
        insert_with_on_conflict(company_ids[1], tag_id)
    )
    results["SELECTで事前チェック"]["新規"].append(
        insert_with_select_check(company_ids[2], tag_id)
    )
    results["INSERT ... WHERE NOT EXISTS"]["新規"].append(
        insert_with_where_not_exists_orm(company_ids[3], tag_id)
    )

    # 既存データの挿入（重複テスト）
    existing_company_id, existing_tag_id = get_existing_company_tag_ids(session)
    results["UNIQUE制約 + 通常INSERT"]["重複"].append(
        insert_with_unique_constraint(existing_company_id, existing_tag_id)
    )
    results["ON CONFLICT DO NOTHING"]["重複"].append(
        insert_with_on_conflict(existing_company_id, existing_tag_id)
    )
    results["SELECTで事前チェック"]["重複"].append(
        insert_with_select_check(existing_company_id, existing_tag_id)
    )
    results["INSERT ... WHERE NOT EXISTS"]["重複"].append(
        insert_with_where_not_exists_orm(existing_company_id, existing_tag_id)
    )

    session.close()

# 結果の集計
summary = {
    method: {
        "新規": {
            "平均": round(sum(times["新規"]) / num_trials, 6),
            "標準偏差": round(
                (
                    sum(
                        (x - sum(times["新規"]) / num_trials) ** 2
                        for x in times["新規"]
                    )
                    / num_trials
                )
                ** 0.5,
                6,
            ),
            "最大値": round(max(times["新規"]), 6),
            "最小値": round(min(times["新規"]), 6),
        },
        "重複": {
            "平均": round(sum(times["重複"]) / num_trials, 6),
            "標準偏差": round(
                (
                    sum(
                        (x - sum(times["重複"]) / num_trials) ** 2
                        for x in times["重複"]
                    )
                    / num_trials
                )
                ** 0.5,
                6,
            ),
            "最大値": round(max(times["重複"]), 6),
            "最小値": round(min(times["重複"]), 6),
        },
    }
    for method, times in results.items()
}

# 結果を表示
df = pd.DataFrame.from_dict(
    {(i, j): summary[i][j] for i in summary.keys() for j in summary[i].keys()},
    orient="index",
)
print(df)
print("---------------")
print(summary)
