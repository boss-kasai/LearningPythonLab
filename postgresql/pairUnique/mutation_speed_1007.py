from sqlalchemy import create_engine, func, text
from sqlalchemy.orm import sessionmaker

from postgresql.pairUnique.make_table007 import LCompanyTag

# PostgreSQL に接続
DATABASE_URL = "postgresql://postgres:password@localhost:5432/test_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)


def check_unique_constraint() -> None:
    """
    1. `l_company_tag` テーブルのユニーク制約を確認
    2. 重複データが存在しないか確認
    3. 重複データの INSERT を試みる
    4. `ON CONFLICT DO NOTHING` の動作確認
    """
    session = SessionLocal()

    # **1. `l_company_tag` のテーブル定義を確認**
    print("`l_company_tag` のユニーク制約を確認 (SQL 出力)")
    with engine.connect() as conn:
        result = conn.execute(
            text(
                "SELECT conname FROM pg_constraint WHERE conrelid = 'l_company_tag'::regclass;"
            )
        )
        constraints = [row[0] for row in result]
        print("適用されている制約:", constraints)

    # **2. 重複データがないか確認**
    print("`l_company_tag` の重複チェック")
    duplicate_check = (
        session.query(LCompanyTag.company_id, LCompanyTag.tag_id, func.count())
        .group_by(LCompanyTag.company_id, LCompanyTag.tag_id)
        .having(func.count() > 1)
        .all()
    )

    if duplicate_check:
        print("重複データあり:", duplicate_check)
    else:
        print("重複データなし（ユニーク制約が機能している可能性が高い）")

    # **3. 重複データの INSERT を試みる**
    print("\n🔍 重複データの `INSERT` を試行")
    test_entry = LCompanyTag(company_id=1, tag_id=1)

    try:
        session.add(test_entry)
        session.commit()
        print("`INSERT` が成功（ユニーク制約が機能していない可能性あり）")
    except Exception as e:
        session.rollback()
        print("`INSERT` に失敗（ユニーク制約が機能している）")
        print("エラーメッセージ:", str(e))

    # **4. `ON CONFLICT DO NOTHING` の動作確認**
    print("`ON CONFLICT DO NOTHING` の動作テスト")
    from sqlalchemy.dialects.postgresql import insert

    stmt = insert(LCompanyTag).values(company_id=1, tag_id=1).on_conflict_do_nothing()
    session.execute(stmt)
    session.commit()
    print("`ON CONFLICT DO NOTHING` により、エラーなくスキップ")

    session.close()


# **検証を実行**
check_unique_constraint()
