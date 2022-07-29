#!/usr/bin/env python
import os

import requests
from flask import Flask, Response
from flask_caching import Cache

config = {"DEBUG": True, "CACHE_TYPE": "SimpleCache", "CACHE_DEFAULT_TIMEOUT": 300}

app = Flask(__name__)
app.config.from_mapping(config)
cache = Cache(app)
services = os.environ.get(
    "YC_SERVICES",
    [
        "application-load-balancer",
        "audit-trails",
        "certificate-manager",
        "compute",
        "container-registry",
        "data-proc",
        "data-streams",
        "data-transfer",
        "iam",
        "interconnect",
        "kms",
        "logging",
        "managed-clickhouse",
        "managed-elasticsearch",
        "managed-greenplum",
        "managed-kafka",
        "managed-kubernetes",
        "managed-mongodb",
        "managed-mysql",
        "managed-postgresql",
        "managed-redis",
        "managed-sqlserver",
        "message-queue",
        "monitoring",
        "network-load-balancer",
        "serverless-apigateway",
        "serverless-containers",
        "serverless-functions",
        "speechkit",
        "storage",
        "translate",
        "vision",
        "ydb",
    ],
)


def check_none(environments):
    for key, value in environments.items():
        if value is None:
            return key, value
        else:
            return key, True
    return


@app.route("/metrics/all", methods=["GET"])
@cache.cached()
def get_all_metrics():
    all_metrics = []
    for service in services:
        params = {"folderId": folder_id, "service": service}
        get_prometheus = requests.get(
            monitoring_endpoint, params=params, headers=headers
        )
        if get_prometheus.content.decode() == "":
            app.logger.info(f"Metrics for {service} is not available or empty")
            pass
        else:
            all_metrics.append(get_prometheus.text)
            app.logger.debug(
                f"Response return metrics for service {service}, "
                f"summarize metrics has been increased, new length {len(all_metrics)}"
            )
    metrics = "".join([str(elem) for elem in all_metrics])
    metrics = metrics.split("\n")
    none_empty = [metric for metric in metrics if metric.strip() != ""]
    all_metrics = ""
    for metric_data in none_empty:
        all_metrics += metric_data + "\n"

    return Response(all_metrics, mimetype="text/plain")


@app.route("/metrics/<service>", methods=["GET"])
@cache.cached()
def get_metrics(service):
    params = {"folderId": folder_id, "service": service}
    get_prometheus = requests.get(monitoring_endpoint, params=params, headers=headers)
    if get_prometheus.content.decode() == "":
        return "metrics are not available"
    else:
        return Response(get_prometheus.text.encode(), mimetype="text/plain")


if __name__ == "__main__":
    bearer_token = os.environ.get("YC_TOKEN")
    folder_id = os.environ.get("YC_FOLDER_ID")
    variables = check_none({"bearer_token": bearer_token, "folder_id": folder_id})
    if None in list(variables):
        app.logger.error(
            f"{variables[0]} variable are not present, "
            f"please export variables YC_TOKEN and YC_FOLDER_ID are required"
            f"Documentations reference https://cloud.yandex.com/en/docs/monitoring/api-ref/authentication"
        )
        exit(1)
    monitoring_endpoint = (
        "https://monitoring.api.cloud.yandex.net/monitoring/v2/prometheusMetrics"
    )
    headers = {"Authorization": f"Bearer {bearer_token}"}
    cache.app.run("0.0.0.0", 9000, debug=False)  # nosec B104
