from typing import Any

from sqlalchemy import (
    Column,
    ForeignKey,
    Integer,
    String,
    UniqueConstraint,
    create_engine,
)
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker

# PostgreSQLの接続設定（適宜変更してください）
DATABASE_URL = "postgresql://postgres:password@localhost:5432/test_db"


# SQLAlchemyのエンジン作成
engine = create_engine(DATABASE_URL, echo=True)

# Baseクラスの作成
Base: Any = declarative_base()


# companies テーブル
class Company(Base):
    __tablename__ = "companies"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)

    # リレーションシップ
    l_company_tags = relationship(
        "LCompanyTag", back_populates="company", cascade="all, delete-orphan"
    )


# tags テーブル（正規化したタグ管理）
class Tag(Base):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, autoincrement=True)
    tag = Column(String, unique=True, nullable=False)

    # リレーションシップ
    l_company_tags = relationship(
        "LCompanyTag", back_populates="tag", cascade="all, delete-orphan"
    )


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

    # **ユニーク制約の追加**
    __table_args__ = (
        UniqueConstraint("company_id", "tag_id", name="unique_company_tag"),
    )


# データベースにテーブルを作成
Base.metadata.create_all(engine)

# セッション作成
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

print("テーブル作成完了！")
