from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
    func,
)
from sqlalchemy.orm import declarative_base, relationship, sessionmaker

# PostgreSQL接続（適宜変更）
DATABASE_URL = "postgresql+psycopg2://postgres:password@localhost:5432/join_test_db"
engine = create_engine(DATABASE_URL, echo=True)

Base = declarative_base()


# Users テーブル
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)

    orders = relationship("Order", back_populates="user")


# Orders テーブル
class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    amount = Column(Integer, nullable=False)
    created_at = Column(DateTime, default=func.now())

    user = relationship("User", back_populates="orders")


# テーブル作成
Base.metadata.create_all(engine)

# セッション作成
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()

# サンプルデータ挿入
users = [User(name="Alice"), User(name="Bob"), User(name="Charlie")]
session.add_all(users)
session.commit()

orders = [
    Order(user_id=1, amount=100),
    Order(user_id=1, amount=200),
    Order(user_id=2, amount=300),
]
session.add_all(orders)
session.commit()
print("データ挿入完了")
