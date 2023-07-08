# OpenAI Proxy Setup and Data Ingestion with Uptrace

This guide will help you setup a local environment on MacOS for ingesting data from an OpenAI proxy application to a local Uptrace deployment.

more documentation on http://uptrace.dev

## Prerequisites

- Docker

You can install these prerequisites using Homebrew as follows:

```bash
# Install Docker
brew install --cask docker
```

Please ensure Docker is up and running before proceeding further.


## Deploying the service and setting up the ingress

```bash
git clone https://github.com/uptrace/uptrace.git
cd uptrace/example/docker

docker-compose pull
docker-compose up -d
```

## Starting the proxy

Start the proxy with Uptrace as the destination.

```bash
OTEL_RESOURCE_ATTRIBUTES=service.name=example-openai-proxy OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:14318" OTEL_EXPORTER_OTLP_HEADERS="uptrace-dsn=http://project1_secret_token@localhost:14318/1" opentelemetry-instrument --traces_exporter otlp_proto_http,console --metrics_exporter otlp_proto_http,console uvicorn main:app
```

## Sending a sample request

You can now send a sample request to the OpenAI proxy:

```bash
python tests/main_test.py
```

You have successfully setup the OpenAI proxy to send data to a local Uptrace deployment.

## Find your traces and metrics in uptrace.local

http://localhost:14318/