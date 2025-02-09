from sqlalchemy import Column, ForeignKey, Integer, String, create_engine
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

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

    # リレーションシップ
    all_in_tags = relationship(
        "AllInTag", back_populates="company", cascade="all, delete-orphan"
    )
    l_company_tags = relationship(
        "LCompanyTag", back_populates="company", cascade="all, delete-orphan"
    )


# all_in_tag テーブル（企業ごとにタグを直接持つ）
class AllInTag(Base):
    __tablename__ = "all_in_tag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(
        Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False
    )
    tag_name = Column(String, nullable=False)

    # リレーションシップ
    company = relationship("Company", back_populates="all_in_tags")


# tags テーブル（正規化したタグ管理）
class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String, unique=True, nullable=False)

    # リレーションシップ
    l_company_tags = relationship(
        "LCompanyTag", back_populates="tag", cascade="all, delete-orphan"
    )


# l_company_tag テーブル（中間テーブル：企業とタグの多対多関係）
class LCompanyTag(Base):
    __tablename__ = "l_company_tag"

    id = Column(Integer, primary_key=True, autoincrement=True)
    company_id = Column(
        Integer, ForeignKey("companies.id", ondelete="CASCADE"), nullable=False
    )
    tag_id = Column(Integer, ForeignKey("tags.id", ondelete="CASCADE"), nullable=False)

    # リレーションシップ
    company = relationship("Company", back_populates="l_company_tags")
    tag = relationship("Tag", back_populates="l_company_tags")


# データベースにテーブルを作成
Base.metadata.create_all(engine)

# セッション作成
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

print("テーブル作成完了！")
