import random
import time

import pandas as pd
from sqlalchemy import ARRAY, Column, Integer, String, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# PostgreSQL に接続
DATABASE_URL = "postgresql://postgres:password@localhost:5432/test_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

Base = declarative_base()

TAG_LIST = [
    "IT",
    "製造",
    "金融",
    "小売",
    "サービス",
    "教育",
    "医療",
    "不動産",
    "運輸",
    "エネルギー",
]  # タグのリスト


# companies テーブル
class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    tags = Column(ARRAY(String))


def search_performance_test(session, num_searches=100) -> None:
    """検索のパフォーマンステスト：要素完全一致"""
    print("検索テスト開始！")
    test_result = []

    for _ in range(num_searches):
        start_time = time.perf_counter()
        test_dict = {}
        # ランダムなタグを生成
        # num_tags = random.randint(0, 3)
        search_tags = random.sample(TAG_LIST, 1)

        # 配列に対する検索 (ANY)
        results = session.query(Company).filter(Company.tags.any(search_tags[0])).all()

        test_dict["search_tags"] = search_tags
        test_dict["result_len"] = len(results)
        test_dict["time"] = time.perf_counter() - start_time  # 秒換算
        test_result.append(test_dict)

    # 基礎統計量の算出
    df = pd.DataFrame(test_result)
    print(df.describe())
    print("検索テスト完了！")


def update_performance_test(session, num_updates=1000) -> None:
    """更新（削除と追加）のパフォーマンステスト"""
    start_time = time.perf_counter()

    for _ in range(num_updates):
        # ランダムな企業を選択
        company_id = random.randint(1, 100)  # IDは1からNUM_COMPANIESの範囲
        company = session.query(Company).get(company_id)

        if company:
            # ランダムなタグを生成
            num_tags_to_remove = random.randint(0, len(company.tags))  # 削除するタグ数
            tags_to_remove = (
                random.sample(company.tags, num_tags_to_remove) if company.tags else []
            )  # タグが存在する場合のみ削除
            num_tags_to_add = random.randint(0, 3)  # 追加するタグ数
            tags_to_add = random.sample(TAG_LIST, num_tags_to_add)

            # タグの削除と追加
            company.tags = [
                tag for tag in company.tags if tag not in tags_to_remove
            ] + tags_to_add
            session.commit()

    elapsed_time = time.perf_counter() - start_time
    print(f"更新テスト完了！ 処理時間: {elapsed_time:.2f} 秒")


if __name__ == "__main__":
    search_performance_test(session)
    # update_performance_test(session)

    session.close()
