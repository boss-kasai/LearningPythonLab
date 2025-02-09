from collections import Counter

import numpy as np
from sqlalchemy import create_engine, func
from sqlalchemy.orm import sessionmaker

from postgresql.L_or_Not.make_table005 import Company, LCompanyTag, Tag

# PostgreSQL に接続（適宜変更）
DATABASE_URL = "postgresql://postgres:password@localhost:5432/test_db"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(bind=engine)

# セッションを作成
session = SessionLocal()

# 企業数
company_count = session.query(func.count(Company.id)).scalar()

# タグ数（ユニークなタグの数）
tag_count = session.query(func.count(Tag.id)).scalar()

# １企業あたりのタグ数を計算
tag_counts = (
    session.query(LCompanyTag.company_id, func.count(LCompanyTag.tag_id))
    .group_by(LCompanyTag.company_id)
    .all()
)

# タグ数のリストを作成
tag_count_list = [count for _, count in tag_counts]


if tag_count_list:
    mean_tags_per_company = np.mean(tag_count_list)
    std_tags_per_company = np.std(tag_count_list)
    median_tags_per_company = np.median(tag_count_list)
    most_common_tags_per_company = Counter(tag_count_list).most_common(1)[0][0]
else:
    mean_tags_per_company = std_tags_per_company = median_tags_per_company = (
        most_common_tags_per_company
    ) = 0

# タグの種類（ユニークなタグのリスト）
unique_tags = session.query(Tag.tag).distinct().all()
unique_tags = [tag[0] for tag in unique_tags]

# セッションを閉じる
session.close()

# 結果を表示
result = {
    "企業数": company_count,
    "タグ数": tag_count,
    "１企業あたりのタグ数": {
        "平均": mean_tags_per_company,
        "標準偏差": std_tags_per_company,
        "最頻値": most_common_tags_per_company,
        "中央値": median_tags_per_company,
    },
}

print(result)
