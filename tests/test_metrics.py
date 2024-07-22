from opentelemetry import metrics
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
import time
import random

# Set up the OTLP Metric Exporter
otlp_exporter = OTLPMetricExporter(
    endpoint="localhost:4317",  # Replace with your collector's endpoint
    insecure=True,
)

# Set up the Meter Provider and add the OTLP exporter
reader = PeriodicExportingMetricReader(otlp_exporter, export_interval_millis=1000)
provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(provider)

# Create a meter
meter = metrics.get_meter_provider().get_meter("example-openai-proxy", "0.1.0")

# Create a counter instrument
counter = meter.create_counter(
    name="example_counter",
    description="An example counter",
    unit="1",
)

# Emit periodic metrics
while True:
    counter.add(random.randint(1, 10), {"service.name": "example-openai-proxy"})
    print("Metric emitted")
    time.sleep(5)
