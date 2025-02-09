import random
import string
import time

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from postgresql.arryTest.make_table001 import Company


def generate_random_string(length=6) -> str:
    """ランダムなタグ名や企業名を生成"""
    return "".join(random.choices(string.ascii_lowercase, k=length))


# ダミーデータ生成の設定
NUM_COMPANIES = 1000000  # 生成する企業数
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


def insert_dummy_data(session) -> None:  # sessionを引数として受け取る
    """ダミーデータを挿入"""
    start_time = time.perf_counter()

    # 企業データを生成
    companies = []
    for i in range(NUM_COMPANIES):
        company = Company(name=f"株式会社_{generate_random_string(6)}")
        # ランダムにタグを付与
        num_tags = random.randint(0, 6)  # 0〜6個のタグをランダムに付与
        company.tags = random.sample(TAG_LIST, num_tags)
        companies.append(company)

    session.bulk_save_objects(companies)
    session.commit()
    print(f"企業データの挿入完了-処理時間: {time.perf_counter() - start_time:.2f} 秒")

    elapsed_time = time.perf_counter() - start_time
    print(f"ダミーデータの作成完了！ 処理時間: {elapsed_time:.2f} 秒")


if __name__ == "__main__":
    # PostgreSQLの接続設定（適宜変更してください）
    DATABASE_URL = "postgresql://postgres:password@localhost:5432/test_db"
    engine = create_engine(DATABASE_URL, echo=True)

    # セッション作成
    SessionLocal = sessionmaker(bind=engine)
    session = SessionLocal()

    insert_dummy_data(session)  # sessionを渡す

    session.close()
