from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """アプリケーションの設定"""

    # アプリの基本設定
    APP_NAME: str = "FastAPI OpenTelemetry Example"
    APP_VERSION: str = "1.0.0"

    # OpenTelemetry & Jaeger の設定
    JAEGER_HOST: str = "localhost"
    JAEGER_PORT: int = 6831  # UDP のデフォルトポート
    OTEL_EXPORTER_OTLP_ENDPOINT: str = "http://localhost:4317"

    # ロギング設定
    LOG_LEVEL: str = "info"

    class Config:
        env_file = ".env"  # `.env` ファイルを読み込む設定


# 設定を読み込む
settings = Settings()
