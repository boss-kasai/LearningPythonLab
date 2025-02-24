import logging

# トレース関連
# ログ関連
# メトリクス関連
from opentelemetry import _logs, metrics, trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.exporter.otlp.proto.grpc._log_exporter import OTLPLogExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
from opentelemetry.sdk._logs import LoggerProvider, LoggingHandler
from opentelemetry.sdk._logs.export import BatchLogRecordProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.semconv.resource import ResourceAttributes


def instrument(app):
    """FastAPI に OpenTelemetry の監視機能を適用"""

    # `service.name` を定義（アプリケーション識別用）
    resource = Resource.create(
        {
            ResourceAttributes.SERVICE_NAME: "fastapi-service",
            ResourceAttributes.SERVICE_INSTANCE_ID: "instance-1",
        }
    )

    # トレース関連の設定
    trace_provider = TracerProvider(resource=resource)
    trace.set_tracer_provider(trace_provider)

    jaeger_exporter = JaegerExporter(
        agent_host_name="localhost",
        agent_port=6831,
    )
    trace_provider.add_span_processor(BatchSpanProcessor(jaeger_exporter))

    # ログ関連の設定
    logger_provider = LoggerProvider(resource=resource)
    _logs.set_logger_provider(logger_provider)

    log_exporter = OTLPLogExporter(endpoint="http://localhost:4317", insecure=True)
    logger_provider.add_log_record_processor(BatchLogRecordProcessor(log_exporter))

    # Python のデフォルトログにも適用
    handler = LoggingHandler(level=logging.NOTSET, logger_provider=logger_provider)
    logging.getLogger().addHandler(handler)
    logging.getLogger().setLevel(logging.INFO)

    # メトリクス関連の設定
    metric_reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint="http://localhost:4317")
    )
    metrics.set_meter_provider(
        MeterProvider(resource=resource, metric_readers=[metric_reader])
    )

    # FastAPI の計装
    FastAPIInstrumentor.instrument_app(app)

    # # SQLAlchemy の計装
    # SQLAlchemyInstrumentor().instrument(enable_commenter=True, commenter_options={})
