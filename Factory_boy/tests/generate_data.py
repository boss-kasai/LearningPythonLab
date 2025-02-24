# generate_data.py
import time

from app.database import Base, SessionLocal, engine
from app.factories import CompanyFactory, JTagCompanyFactory

# 必要に応じて PrefectureFactory や TagFactory もインポート


def main():
    """
    Factory Boyを使って大量データを生成するサンプルスクリプト。
    """

    # ▼ 必要があれば、テーブルを一度作り直す
    #    ※性能テストを行うなら、まずは既存データやテーブルをDROPするか検討
    # Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)

    # セッション開始
    session = SessionLocal()

    # 例: Company と JTagCompany を大量生成
    # 何件作るかは性能テストの目安に応じて調整
    NUM_COMPANIES = 100_000
    print(f"Start generating {NUM_COMPANIES} companies...")

    start_time = time.time()

    for i in range(NUM_COMPANIES):
        # CompanyFactoryは内部でPrefectureも自動生成
        CompanyFactory()
        # ※単純にFactoryを呼ぶだけでコミットされる設定の場合、都度コミットが走るため
        #   大量生成では若干パフォーマンスに影響があります。
        #   必要に応じて、chunk単位でまとめてセッションcommitする手法も検討してください。

        # ある程度ごとにログを出して経過を把握
        if i > 0 and i % 100 == 0:
            print(f"  {i} records created...")

    # 例: CompanyとTagの中間テーブルJTagCompanyを別途大量生成
    #    会社を何社か取得して、その会社 + Tag を適当に生成する例
    #    必要に応じてロジックを変更
    companies = session.query(
        # ここでは全カラム取得でなくIDだけなど、用途に応じて
        # from app.models import Company
        # すでに大量生成しているのでなるべく効率的に
    ).all()
    print(companies)
    NUM_JTAG = 5_000
    for i in range(NUM_JTAG):
        JTagCompanyFactory()

    # まとめてセッション反映
    session.commit()

    end_time = time.time()
    print(f"Data generation completed in {end_time - start_time:.2f} seconds.")

    session.close()


if __name__ == "__main__":
    main()
