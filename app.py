"""Application code to test the library-level telemetry."""
from fake_evaluator.foo import do_something
from opentelemetry import metrics, trace
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import \
    OTLPMetricExporter
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import \
    OTLPSpanExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import (ConsoleMetricExporter,
                                              PeriodicExportingMetricReader)
from opentelemetry.sdk.resources import SERVICE_NAME, Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import (BatchSpanProcessor,
                                            ConsoleSpanExporter)

COLLECTOR_ENDPOINT = "http://localhost:4317"  # do not use https for all-in-one local test
if COLLECTOR_ENDPOINT:
    processor = BatchSpanProcessor(OTLPSpanExporter(endpoint=COLLECTOR_ENDPOINT))
    reader = PeriodicExportingMetricReader(
        OTLPMetricExporter(endpoint=COLLECTOR_ENDPOINT)
    )
else:
    processor = BatchSpanProcessor(ConsoleSpanExporter())
    reader = PeriodicExportingMetricReader(ConsoleMetricExporter())

resource = Resource(attributes={
    SERVICE_NAME: "guardrail-service"
})
traceProvider = TracerProvider(resource=resource)
traceProvider.add_span_processor(processor)
trace.set_tracer_provider(traceProvider)
meterProvider = MeterProvider(resource=resource, metric_readers=[reader])
metrics.set_meter_provider(meterProvider)


if __name__ == "__main__":
    do_something(123)
    do_something("456")
