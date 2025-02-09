from sqlalchemy import ARRAY, Column, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# PostgreSQLの接続設定（適宜変更してください）
DATABASE_URL = "postgresql://postgres:password@localhost:5432/test_db"


# SQLAlchemyのエンジン作成
engine = create_engine(DATABASE_URL, echo=True)

# Baseクラスの作成
Base = declarative_base()


# companies テーブル
class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    tags = Column(ARRAY(String))


# データベースにテーブルを作成
Base.metadata.create_all(engine)

# セッション作成
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

print("テーブル作成完了！")
