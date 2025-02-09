import time

from sqlalchemy import create_engine
from sqlalchemy.orm import Session, sessionmaker

from postgresql.L_or_Not.make_table005 import AllInTag, Company, LCompanyTag, Tag

# PostgreSQL に接続
DATABASE_URL = "postgresql://postgres:password@localhost:5432/test_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def search_companies_by_tag(session: Session, tag_keyword: str):
    """
    指定した部分一致タグを持つ企業の名前を取得する (all_in_tag 経由)
    :param session: SQLAlchemy セッション
    :param tag_keyword: 検索するタグの部分文字列
    :return: 企業名のリスト
    """
    query = (
        session.query(Company.name)
        .join(AllInTag, Company.id == AllInTag.company_id)
        .filter(AllInTag.tag_name.ilike(f"%{tag_keyword}%"))  # 部分一致
        .distinct()  # 重複を防ぐ
    )
    return [company[0] for company in query.all()]


def search_companies_by_ltabl(session: Session, tag_keyword: str):
    """
    指定した部分一致タグを持つ企業の名前を取得する (l_company_tag 経由)
    :param session: SQLAlchemy セッション
    :param tag_keyword: 検索するタグの部分文字列
    :return: 企業名のリスト
    """
    query = (
        session.query(Company.name)
        .join(LCompanyTag, Company.id == LCompanyTag.company_id)  # 中間テーブルを結合
        .join(Tag, LCompanyTag.tag_id == Tag.id)  # タグテーブルを結合
        .filter(Tag.tag.ilike(f"%{tag_keyword}%"))  # 部分一致検索 (大文字小文字を無視)
        .distinct()  # 重複を防ぐ
    )
    return [company[0] for company in query.all()]


def measure_query_time(
    session: Session, query_function, tag_keyword: str, num_trials: int = 10
):
    """
    クエリの処理時間を測定して出力する
    :param session: SQLAlchemy セッション
    :param query_function: 実行するクエリ関数
    :param tag_keyword: 検索するタグの部分文字列
    :param num_trials: 試行回数
    """
    execution_times = []

    for _ in range(num_trials):
        start_time = time.perf_counter()
        result = query_function(session, tag_keyword)
        end_time = time.perf_counter()

        execution_times.append(end_time - start_time)
        print(len(result), "件の企業が見つかりました")

    print(f"\n[{query_function.__name__}] の検索結果")
    print(f"実行回数: {num_trials} 回")
    print(f"平均処理時間: {sum(execution_times) / num_trials:.5f} 秒")
    print(f"最小処理時間: {min(execution_times):.5f} 秒")
    print(f"最大処理時間: {max(execution_times):.5f} 秒\n")


# セッションを作成
session = SessionLocal()

# タグ "td" を含む企業名の検索と処理時間の計測
key_word = "td"
measure_query_time(session, search_companies_by_tag, key_word)
measure_query_time(session, search_companies_by_ltabl, key_word)

# セッションを閉じる
session.close()
