# OpenTelemetry + Jaeger で計装してみる

FastAPIの簡単なAPIを作成して、それにOpenTelemetryを使って計装する。
APIのエンドポイントのテストは、Postmanで作成してみる。

## 環境の構築

```bash

# 仮想環境の作成
python3.13 -m venv venv

# 仮想環境の有効化
source venv/bin/activate

# 依存関係のインストール
pip install -r requirements.txt

# 依存関係の保存
pip freeze > requirements.txt

# 仮想環境の非有効化
deactivate

# docker-composeの起動
docker-compose up -d

# 起動
uvicorn app.main:app --reload

```
