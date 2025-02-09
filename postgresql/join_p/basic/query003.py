from sqlalchemy import (
    Column,
    DateTime,
    ForeignKey,
    Integer,
    String,
    create_engine,
    func,
    select,
    text,
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


# セッション作成
SessionLocal = sessionmaker(bind=engine)
session = SessionLocal()


# INNER JOIN
# users と orders の両方に一致するデータのみ取得
# Charlie は orders に関連データがないため取得されない
stmt = select(User.name, Order.amount).join(Order)
result = session.execute(stmt).fetchall()
print("---INNER JOIN---")
print(result)  # [('Alice', 100), ('Alice', 200), ('Bob', 300)]

# LEFT JOIN
# Charlie も NULL 付きで取得される
stmt = select(User.name, Order.amount).outerjoin(Order)
result = session.execute(stmt).fetchall()
print("---LEFT JOIN---")
print(result)  # [('Alice', 100), ('Alice', 200), ('Bob', 300), ('Charlie', None)]


# RIGHT JOIN（SQLAlchemyではLEFT JOINで代用）
# SQLAlchemy では RIGHT JOIN は LEFT JOIN で代用する
stmt = select(User.name, Order.amount).join(Order, isouter=True)
result = session.execute(stmt).fetchall()
print("---RIGHT JOIN---")
print(result)  # [('Alice', 100), ('Alice', 200), ('Bob', 300), ('Charlie', None)]

# FULL OUTER JOIN
# LEFT JOIN と RIGHT JOIN を組み合わせた結果
stmt = session.execute(
    text(
        """
        SELECT users.name, orders.amount
        FROM users
        FULL JOIN orders ON users.id = orders.user_id
        """
    )
).fetchall()
print("---FULL OUTER JOIN---")
print(result)  # [('Alice', 100), ('Alice', 200), ('Bob', 300), ('Charlie', None)]


# CROSS JOIN
# 全ての組み合わせが取得される
stmt = select(User.name, Order.amount).join(Order, isouter=False, full=False)
result = session.execute(stmt).fetchall()
print("---CROSS JOIN---")
print(result)  # [('Alice', 100), ('Alice', 200), ('Bob', 300)]

# LATERAL JOIN
# ユーザーごとの最新の注文を取得
stmt = session.execute(
    text(
        """
        SELECT users.name, latest_order.amount
        FROM users
        LEFT JOIN LATERAL (
            SELECT * FROM orders WHERE orders.user_id = users.id ORDER BY orders.created_at DESC LIMIT 1
        ) latest_order ON true
        """
    )
).fetchall()
print("---LATERAL JOIN---")
print(result)  # [('Alice', 100), ('Alice', 200), ('Bob', 300)]
