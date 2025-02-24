from app.database import Base, engine

import pytest


@pytest.fixture(scope="session", autouse=True)
def setup_database():
    # テーブルを一旦削除して再作成
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    yield

    # テスト終了時にテーブルを削除 (必要に応じて)
    Base.metadata.drop_all(bind=engine)
