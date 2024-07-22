import threading
import time
import random
from opentelemetry import trace, metrics
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.sdk.metrics import MeterProvider
from opentelemetry.sdk.metrics.export import PeriodicExportingMetricReader
from opentelemetry.exporter.otlp.proto.grpc.trace_exporter import OTLPSpanExporter
from opentelemetry.exporter.otlp.proto.grpc.metric_exporter import OTLPMetricExporter

# Configuration
num_hosts = 5
transaction_interval = 5
metrics_interval = 5

# Resource attributes
resource = Resource(attributes={
    "service.name": "example-openai-proxy"
})

# Set up the OTLP Exporters
trace_exporter = OTLPSpanExporter(
    endpoint="localhost:4317",
    insecure=True,
)
metric_exporter = OTLPMetricExporter(
    endpoint="localhost:4317",
    insecure=True,
)

# Set up the Tracer Provider and add the OTLP exporter
tracer_provider = TracerProvider(resource=resource)
span_processor = BatchSpanProcessor(trace_exporter)
tracer_provider.add_span_processor(span_processor)
trace.set_tracer_provider(tracer_provider)

# Set up the Meter Provider and add the OTLP exporter
reader = PeriodicExportingMetricReader(metric_exporter, export_interval_millis=metrics_interval * 1000)
meter_provider = MeterProvider(metric_readers=[reader])
metrics.set_meter_provider(meter_provider)

# Create a tracer and meter
tracer = trace.get_tracer("example-openai-proxy", "0.1.0")
meter = metrics.get_meter_provider().get_meter("example-openai-proxy", "0.1.0")

# Create a counter instrument
transaction_counter = meter.create_counter(
    name="transaction_counter",
    description="Counts the number of transactions",
    unit="1",
)

# Function to simulate transactions
def simulate_host_transactions(host_id):
    while True:
        with tracer.start_as_current_span(f"transaction-{host_id}") as span:
            success = random.choice([True, False])
            if success:
                span.set_attribute("transaction.status", "success")
            else:
                span.set_attribute("transaction.status", "failure")
                span.record_exception(Exception("Transaction failed"))
            transaction_counter.add(1, {"host.id": host_id, "transaction.status": "success" if success else "failure"})
            print(f"Host {host_id} emitted a {'successful' if success else 'failed'} transaction")
            time.sleep(transaction_interval)

# Start threads for each host
threads = []
for i in range(num_hosts):
    thread = threading.Thread(target=simulate_host_transactions, args=(i,))
    threads.append(thread)
    thread.start()

# Wait for all threads to complete
for thread in threads:
    thread.join()
