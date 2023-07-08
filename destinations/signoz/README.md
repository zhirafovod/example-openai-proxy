# OpenAI Proxy Setup and Data Ingestion with SigNoz

This guide will help you setup a local environment on MacOS for ingesting OTEL data from the OpenAI proxy application to a local SigNoz.

more documentation on https://signoz.io/docs/install/docker/

## Prerequisites

- Docker

Note: ensure that docker-compose comes with your docker distribution 

```bash
# Install Docker
brew install --cask docker
```

Please ensure Docker is up and running before proceeding further.

## Deploying the service 

```bash
git clone -b main https://github.com/SigNoz/signoz.git && cd signoz/deploy/
docker-compose -f docker/clickhouse-setup/docker-compose.yaml up -d
```

## Stop hot-rod load generator

You can comment them in the docker-compose file or stop in the docker-desktop or with the docker command
```bash
docker stop hotrod
docker stop load-hotrod
```

## Starting the proxy

Start the proxy with SigNoz as the destination.

```bash
OTEL_RESOURCE_ATTRIBUTES=service.name=example-openai-proxy OTEL_EXPORTER_OTLP_ENDPOINT="http://localhost:4318" opentelemetry-instrument --traces_exporter otlp_proto_http,console --metrics_exporter otlp_proto_http,console uvicorn main:app
```

## Sending a sample request

You can now send a sample request to the OpenAI proxy:

```bash
python tests/main_test.py
```

You have successfully setup the OpenAI proxy to send data to a local Uptrace deployment.

## Find your traces and metrics in SigNoz

http://localhost:3301/
