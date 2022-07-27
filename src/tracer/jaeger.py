from config import settings
from flask import Flask
from opentelemetry import trace
from opentelemetry.exporter.jaeger.thrift import JaegerExporter
from opentelemetry.instrumentation.flask import FlaskInstrumentor
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)


def configure_tracer() -> None:
    trace.set_tracer_provider(
        TracerProvider(
            resource=Resource.create({SERVICE_NAME: "Auth-service"}),)
    )
    trace.get_tracer_provider().add_span_processor(
        BatchSpanProcessor(
            JaegerExporter(
                agent_host_name=settings.JAEGER_HOST,
                agent_port=settings.JAEGER_PORT,
            )
        )
    )
    if settings.DEBUG:
        trace.get_tracer_provider().add_span_processor(
            BatchSpanProcessor(ConsoleSpanExporter())
        )


def tracer_init(app: Flask) -> None:
    configure_tracer()
    FlaskInstrumentor().instrument_app(app)
