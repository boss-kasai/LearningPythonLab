# PostgreSQLへのSQL Alchemyの動作を比較する

SQLAlchemyのJOINの種類の性能を比較します。

1. INNER JOIN（内部結合）
2. LEFT JOIN（LEFT OUTER JOIN）
3. RIGHT JOIN（RIGHT OUTER JOIN）
4. FULL JOIN（FULL OUTER JOIN）
5. CROSS JOIN（直積結合）
6. LATERAL JOIN（相関サブクエリJOIN）

## JOINの挙動の違いを知る

basic フォルダーでのテスト。
JOINの種類と実際の挙動を確認する。

## JOINの処理速度を比較する

advance フォルダーにてテスト。
100万件のデータを用いて

## 実際に検索をして、処理速度を比較する

## 中間テーブルのある処理

## 仮想環境の作成

```bash
# 仮想環境の作成
python3.13 -m venv venv

# 仮想環境の有効化
source venv/bin/activate

# 依存関係のインストール
pip install -r ./app/requirements.txt

# 依存関係の保存
pip freeze > ./app/requirements.txt

# Dockerの起動
docker-compose up -d

```
