# Factory boy を使ってダミーデータをたくさん作る

以前、Postgresql の性能テストをやった時のやつを作成する。
中間テーブルありで、実施。

テーブル構造は

company
- id
- name str
- sales int
- prefecture fk int

j_tag_company
- id
- company_id fk
- tag_id fk

prefecture
- id
- name

tag
- id
- name

## 仮想環境の作成

```bash
# 仮想環境の作成
python3.13 -m venv venv

# 仮想環境の有効化
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# 依存関係の保存
pip freeze > requirements.txt

# Dockerの起動
docker-compose up -d

```
