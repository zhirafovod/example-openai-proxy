# OpenAI Proxy Setup and Data Ingestion with Uptrace

Note: way easier to set up [Docker](./README.docker.md)

This guide will help you setup a local environment on MacOS for ingesting data from an OpenAI proxy application to a local Uptrace deployment.

more documentation on http://uptrace.dev

## Prerequisites

- Docker
- k3d
- Helm

You can install these prerequisites using Homebrew as follows:

```bash
# Install Docker
brew install --cask docker

# Install k3d
brew install k3d

# Install Helm
brew install helm
```

Please ensure Docker is up and running before proceeding further.

## Setting up the cluster

Create a k3d cluster named 'uptrace' and confiure port

```bash
k3d cluster create uptrace -p "8081:80@loadbalancer"
```

Install uptrace in your kubernetes cluster.

```bash
# Add Uptrace helm chart
helm repo add uptrace https://charts.uptrace.dev
helm repo update

# Create uptrace namespace and install
helm install -n uptrace --create-namespace my-uptrace uptrace/uptrace
```

## Configuring the /etc/hosts file

You will need to update your /etc/hosts file to point `uptrace.local` to `127.0.0.1`. You can use the following command:

```bash
echo "127.0.0.1 uptrace.local" | sudo tee -a /etc/hosts
```

## Deploying the service and setting up the ingress

Deploy a sample nginx service and setup the ingress.

```bash
# Create nginx deployment and service
kubectl create deployment nginx --image=nginx
kubectl create service clusterip nginx --tcp=80:80

# Apply the ingress configuration
kubectl apply -f destinations/uptrace_local/uptrace.ingress.yaml
```

## Port forwarding for Uptrace

This is required to send OTEL over HTTP to uptrace.

```bash
kubectl port-forward -n uptrace svc/my-uptrace 14318:14318 &
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

http://uptrace.local:8081/