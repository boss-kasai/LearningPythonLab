import random
import string
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from postgresql.pairUnique.make_table007 import Company, LCompanyTag, Tag

# PostgreSQLの接続設定（適宜変更してください）
DATABASE_URL = "postgresql://postgres:password@localhost:5432/test_db"
engine = create_engine(DATABASE_URL, echo=True)

# セッション作成
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# 企業数とタグ数の設定
NUM_COMPANIES = 1_000_000
NUM_TAGS = 5_000
MIN_TAGS_PER_COMPANY = 20
MAX_TAGS_PER_COMPANY = 5_000


def generate_random_string(length=6) -> str:
    """ランダムなタグ名や企業名を生成"""
    return "".join(random.choices(string.ascii_lowercase, k=length))


def insert_dummy_data() -> None:
    """ダミーデータを挿入"""
    start_time = time.perf_counter()

    # **企業データを生成**
    companies = []
    for i in range(NUM_COMPANIES):
        companies.append(Company(name=f"株式会社_{generate_random_string(6)}"))
    session.bulk_save_objects(companies)
    session.commit()
    print(f"企業データの挿入完了-処理時間: {time.perf_counter() - start_time:.2f} 秒")

    # **企業IDを取得**
    company_ids = [c.id for c in session.query(Company.id).all()]

    # **タグデータを生成**
    tags = [Tag(tag=generate_random_string(6)) for _ in range(NUM_TAGS)]
    tags = list(set(tags))  # 重複を削除
    session.bulk_save_objects(tags)
    session.commit()
    print(f"タグデータの挿入完了-処理時間: {time.perf_counter() - start_time:.2f} 秒")

    # **タグIDを取得**
    tag_ids = [t.id for t in session.query(Tag.id).all()]

    # **`l_company_tag`（中間テーブル）のデータを作成**
    for tag_id in tag_ids:
        l_company_tag_data = []
        selected_company_ids = random.sample(
            company_ids, random.randint(MIN_TAGS_PER_COMPANY, MAX_TAGS_PER_COMPANY)
        )
        l_company_tag_data.extend(
            [
                LCompanyTag(company_id=company_id, tag_id=tag_id)
                for company_id in selected_company_ids
            ]
        )
        # for company_id in company_ids:
        #     l_company_tag_data = []
        #     selected_tag_ids = random.sample(
        #         tag_ids, random.randint(MIN_TAGS_PER_COMPANY, MAX_TAGS_PER_COMPANY)
        #     )
        #     l_company_tag_data.extend(
        #         [
        #             LCompanyTag(company_id=company_id, tag_id=tag_id)
        #             for tag_id in selected_tag_ids
        #         ]
        #     )

        session.bulk_save_objects(l_company_tag_data)
    session.commit()

    elapsed_time = time.perf_counter() - start_time
    print(f"ダミーデータの作成完了！ 処理時間: {elapsed_time:.2f} 秒")


# **ダミーデータの挿入実行**
insert_dummy_data()

# **セッションを閉じる**
session.close()
