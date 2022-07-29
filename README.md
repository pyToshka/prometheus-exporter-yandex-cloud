# Prometheus exporter for Yandex cloud

## Pre-requirements
- Python 3.8 for running without docker
- Docker
- Yandex service account with [permissions](https://cloud.yandex.com/en/docs/iam/concepts/access-control/roles#monitoring-roles).
- [IAM token](https://cloud.yandex.com/en/docs/monitoring/api-ref/authentication)
- Yandex cloud [directory id](https://cloud.yandex.com/en/docs/resource-manager/operations/folder/get-id)

## Environments variables

| Variable name | Type   | Sensitive | Mandatory | Description                                                               |
|---------------|--------|-----------|-----------|---------------------------------------------------------------------------|
| YC_TOKEN      | string | true      | true      | Yandex Cloud IAM token                                                    |
| YC_FOLDER_ID  | string | false     | true      | A folder is a space where Yandex Cloud resources are created and grouped. |
| YC_SERVICES   | list   | false     | false     | List of services for getting metrics.                                     |

## How to run

### Locally

Checkout repository

Install dependencies

```shell
pip install -r requirements.txt
```
Export YC_TOKEN and YC_FOLDER_ID

```shell
export YC_TOKEN="your_token"
export YC_FOLDER_ID="directory_id"
```
Run exporter

```shell
python main.py
```
After up and running exporter will listen on `0.0.0.0` port 9000

### Build docker image

```shell
docker build . -t some_name:tag
```

### Run via docker compose
Export YC_TOKEN and YC_FOLDER_ID

```shell
export YC_TOKEN="your_token"
export YC_FOLDER_ID="directory_id"
```
Run
```shell
docker-compose up -d --build
```

### Use docker hub image

```shell
docker pull kennyopennix/prometheus-exporter-yandex-cloud
```

## Endpoints

`/metrics/all` - Get all metrics
`/metrics/<service_name>` - Get metrics for some service for example, getting metrics for compute `/metrics/compute`

## List of services
- application-load-balancer — Application Load Balancer.
- audit-trails — Audit Trails.
- certificate-manager — Certificate Manager.
- compute — Compute Cloud.
- container-registry — Container Registry.
- data-proc — Data Proc.
- data-streams — Data Streams.
- data-transfer — Data Transfer.
- iam — Identity and Access Management.
- interconnect — Cloud Interconnect.
- kms — Key Management Service.
- logging — Cloud Logging.
- managed-clickhouse — Managed Service for ClickHouse.
- managed-elasticsearch — Managed Service for Elasticsearch.
- managed-greenplum — Managed Service for Greenplum®.
- managed-kafka — Managed Service for Apache Kafka®.
- managed-kubernetes — Managed Service for Kubernetes.
- managed-mongodb — Managed Service for MongoDB.
- managed-mysql — Managed Service for MySQL.
- managed-postgresql — Managed Service for PostgreSQL.
- managed-redis — Managed Service for Redis.
- managed-sqlserver — Managed Service for SQL Server.
- message-queue — Message Queue.
- monitoring — Yandex Monitoring.
- network-load-balancer — Network Load Balancer.
- serverless-apigateway — API Gateway.
- serverless-containers — Serverless Containers.
- serverless-functions — Cloud Functions.
- speechkit — SpeechKit.
- storage — Object Storage.
- translate — Translate.
- vision — Vision.
- ydb — Managed Service for YDB.

## Configuration for prometheus
```yaml
global:
  scrape_interval: 1m

scrape_configs:
  - job_name: "compute"
    scrape_interval: 1m
    metrics_path: "/metrics/compute"
    static_configs:
    - targets: ["exporter_ip:9000"]
  - job_name: "audit-trails"
    scrape_interval: 1m
    metrics_path: "/metrics/audit-trails"
    static_configs:
    - targets: ["exporter_ip:9000"]
  - job_name: "all"
    scrape_interval: 1m
    metrics_path: "/metrics/all"
    static_configs:
    - targets: ["exporter_ip:9000"]


```
## Grafana Dashboard for audit trail

Example of dashboard you can find in `configs/dashboards/yandex_cloud_audit.json`
