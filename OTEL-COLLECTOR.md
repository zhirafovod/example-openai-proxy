# Setting up OpenTelemetry Collector with OAuth2 Authentication

This section explains how to set up the OpenTelemetry Collector (OTEL Collector) with OAuth2 authentication for use with the FastAPI-based proxy server for OpenAI's Chat API.

## OAuth2 Authentication Setup

The OAuth2 credentials are configured in the `extensions/oauth2client` section of the OpenTelemetry Collector's configuration file. Here's an example of what the OAuth2 client configuration might look like:

```yaml
extensions:
  oauth2client:
    client_id: <clientId from UI>
    client_secret: <clientSecret from UI>
    token_url: <tokenUrl from UI>
```

Replace `<clientId from UI>`, `<clientSecret from UI>`, and `<tokenUrl from UI>` with the `clientId`, `clientSecret`, and `tokenUrl` values generated from your OAuth2 provider's UI.

For additional options, see the [OAuth2Client extensions documentation](https://github.com/open-telemetry/opentelemetry-collector-contrib/tree/main/extension/oauth2clientextension).

## Exporter Configuration

To configure the OTEL Collector to send traces to a backend that supports OAuth2 authentication, configure an OTLP HTTP exporter (`otlphttp`). Here's an example of what the exporter configuration might look like:

```yaml
exporters:
  otlphttp:
    auth:
      authenticator: oauth2client
    traces_endpoint: https://<tenantHostName>/data/v1/trace
```

Replace `<tenantHostName>` with the hostname from your OAuth2 provider's `tokenUrl`.

For additional options, see the [OTLP HTTP Exporter documentation](https://github.com/open-telemetry/opentelemetry-collector/tree/main/exporter/otlpexporter).

## Logging Exporter

You can also configure a logging exporter to help with debugging. Here's an example:

```yaml
exporters:
  logging:
    loglevel: debug
```

## Service Configuration

To configure the service section of the OTEL Collector's configuration file:

- Add `oauth2client` to `service/extensions`.
- Add each exporter to `service/pipelines`.
- Optionally add a batch processor.

Here's an example of what the service configuration might look like:

```yaml
service:
  extensions:
    - oauth2client
  pipelines:
    traces:
      receivers: [otlp]
      processors: [batch]
      exporters: [otlphttp, logging]
  telemetry:
    logs:
      level: "debug"
```

For additional options, see the [OpenTelemetry Collector Service documentation](https://github.com/open-telemetry/opentelemetry-collector/blob/main/service/README.md).

## Optional: Batch Processor

Optionally, a batch processor can be configured to control the batching of trace data. Here's an example:

```yaml
processors:
  batch:
    send_batch_max_size: 1000
    send_batch_size: 1000
    timeout: 10s
```

For additional options, see the [Batch Processor documentation](https://github.com/open-telemetry/opentelemetry-collector/blob/main/processor/batchprocessor/README.md).

## Verify Configuration

To validate that your configuration is working properly, review your OpenTelemetry Collector logs. Ensure that your service logs in at the `debug` level to provide the most detailed logs.

Happy coding!
