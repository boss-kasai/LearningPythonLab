import random
import string
import time
from collections import Counter

import numpy as np

# 結果を出力
import pandas as pd
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from postgresql.L_or_Not.make_table005 import AllInTag, Company, LCompanyTag, Tag

# PostgreSQL の接続設定
DATABASE_URL = "postgresql://postgres:password@localhost:5432/test_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# 追加回数
NUM_INSERTS = 1000


# タグを生成する関数
def generate_tag():
    return "".join(random.choices(string.ascii_lowercase, k=3))


# データ追加のスピード測定
def insert_all_in_tag(session, tag_name, company_id):
    """all_in_tag にデータを追加"""
    start_time = time.perf_counter()

    # タグを追加
    new_tag = AllInTag(company_id=company_id, tag_name=tag_name)
    session.add(new_tag)
    session.commit()

    elapsed_time = time.perf_counter() - start_time
    return elapsed_time


def insert_l_company_tag(session, tag_name, company_id):
    """l_company_tag にデータを追加"""
    start_time = time.perf_counter()

    # タグがすでに存在するか確認
    tag = session.query(Tag).filter_by(tag=tag_name).first()
    if not tag:
        tag = Tag(tag=tag_name)
        session.add(tag)
        session.commit()

    # 中間テーブルにデータを追加
    new_entry = LCompanyTag(company_id=company_id, tag_id=tag.id)
    session.add(new_entry)
    session.commit()

    elapsed_time = time.perf_counter() - start_time
    return elapsed_time


# セッションを作成
session = SessionLocal()

# 記録用リスト
all_in_tag_times = []
l_company_tag_times = []
existing_tag_count = 0

# 1000件のデータ追加
for _ in range(NUM_INSERTS + 1):
    new_tag = generate_tag()

    # 企業IDをランダムで1つ取得
    company_id = session.query(Company.id).order_by(func.random()).limit(1).scalar()

    # all_in_tag に追加
    all_in_tag_times.append(insert_all_in_tag(session, new_tag, company_id))

    # l_company_tag に追加
    existing_tags_before = session.query(Tag.id).filter_by(tag=new_tag).count()
    l_company_tag_times.append(insert_l_company_tag(session, new_tag, company_id))
    existing_tags_after = session.query(Tag.id).filter_by(tag=new_tag).count()

    if existing_tags_after > existing_tags_before:
        existing_tag_count += 1  # 過去と同じタグがあった場合

# セッションを閉じる
session.close()


# 統計情報を計算
def compute_statistics(times):
    return {
        "平均": np.mean(times),
        "標準偏差": np.std(times),
        "最頻値": Counter(times).most_common(1)[0][0],
        "中央値": np.median(times),
        "最小": np.min(times),
        "最大": np.max(times),
    }


result = {
    "all_in_tag の処理速度": compute_statistics(all_in_tag_times),
    "l_company_tag の処理速度": compute_statistics(l_company_tag_times),
    "過去と同じタグの件数": existing_tag_count,
}
print(result)


df = pd.DataFrame(result)
print(df)
