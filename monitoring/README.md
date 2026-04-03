# Application Monitoring (Prometheus & Grafana)

## Overview

This project implements end-to-end application monitoring in a Kubernetes-based DevOps platform using:

- Prometheus for metrics collection  
- Grafana for visualization  
- Kubernetes (EKS) for orchestration  
- Flask application exposing metrics  

The goal is to provide observability into application health, performance, and reliability.

---

## Architecture

### End-to-End Flow

``` Markdown
Application (Flask)
↓
/metrics endpoint
↓
ServiceMonitor (Kubernetes)
↓
Prometheus (scrapes metrics)
↓
Grafana (dashboards & visualization)

```

## Components

### 1. Application (platform-app)

- Built using Flask  
- Endpoints:
  - `/` → main endpoint  
  - `/health` → health check  
  - `/metrics` → Prometheus metrics  

# Update application to expose matrix

```bash
from flask import Flask, jsonify, Response
from prometheus_client import Counter, generate_latest, CONTENT_TYPE_LATEST
import os

app = Flask(__name__)

REQUESTS = Counter('http_requests_total', 'Total HTTP Requests')

@app.get("/health")
def health():
    return jsonify(app="DevOps-app", status="ok", version=os.getenv("APP_VERSION", "dev"))

@app.get("/")
def root():
    REQUESTS.inc()
    return "Welcome to the world of DevOps - Stage2:)\n"

@app.get("/metrics")
def metrics():
    return Response(generate_latest(), mimetype=CONTENT_TYPE_LATEST)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

This exposes:

/ for your app

/metrics for Prometheus

---

### 2. Prometheus

- Installed using kube-prometheus-stack  
- Scrapes:
  - Kubernetes cluster metrics  
  - Node metrics  
  - Application metrics via ServiceMonitor  

---

### 3. Grafana

- Connected to Prometheus as data source  
- Used for:
  - Dashboard visualization  
  - Monitoring application behaviour  
  - Observing resource usage  

---

### 4. ServiceMonitor

Defines how Prometheus discovers and scrapes the application.

```yaml
apiVersion: monitoring.coreos.com/v1
kind: ServiceMonitor
metadata:
  name: platform-app
  namespace: monitoring
  labels:
    release: monitoring
spec:
  namespaceSelector:
    matchNames:
      - dev
  selector:
    matchLabels:
      app.kubernetes.io/name: platform-app
  endpoints:
    - port: http
      path: /metrics
      interval: 15s
```

### Verification Steps
Check application pods
```bash
kubectl get pods -n dev
```

Port-forward service
```bash
kubectl port-forward svc/platform-app-dev 8080:80 -n dev
```

Test endpoints
```bash
curl http://127.0.0.1:8080/
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/metrics
```

Verify Prometheus target
```bash
kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090 -n monitoring --address 0.0.0.0
```

Open:

```bash
http://192.168.56.10:9090/targets
```

Application target should be UP

Verify Grafana
```bash
kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring
```

Open:

```bash
http://192.168.56.10:3000
```

# Build Grafana dashboards and alerts

Add panels for:

- request count/rate
- error count
- response latency if available
- CPU usage
- memory usage
- pod restarts

PromQL examples:

```promql
rate(container_cpu_usage_seconds_total{namespace="dev", pod=~"platform-app.*"}[5m])

container_memory_working_set_bytes{namespace="dev", pod=~"platform-app.*"}

kube_pod_container_status_restarts_total{namespace="dev", pod=~"platform-app.*"}

kube_deployment_status_replicas_available{namespace="dev", deployment="my-app"}

kube_deployment_spec_replicas{namespace="dev", deployment="my-app"}
```


# Promethus alerts

```yaml
apiVersion: monitoring.coreos.com/v1
kind: PrometheusRule
metadata:
  name: my-app-alerts
  namespace: monitoring
  labels:
    release: monitoring
spec:
  groups:
    - name: my-app.rules
      rules:
        - alert: MyAppTargetDown
          expr: up{job="my-app"} == 0
          for: 2m
          labels:
            severity: warning
          annotations:
            summary: "My app target is down"
            description: "Prometheus cannot scrape my app for 2 minutes"

        - alert: MyAppHighRestartCount
          expr: increase(kube_pod_container_status_restarts_total{namespace="dev", pod=~"my-app.*"}[10m]) > 1
          for: 5m
          labels:
            severity: warning
          annotations:
            summary: "My app pod restarting frequently"
            description: "Pod restart count increased in last 10 minutes"

        - alert: MyAppReplicasUnavailable
          expr: kube_deployment_status_replicas_available{namespace="dev", deployment="my-app"} < kube_deployment_spec_replicas{namespace="dev", deployment="my-app"}
          for: 3m
          labels:
            severity: critical
          annotations:
            summary: "My app replicas unavailable"
            description: "Available replicas are below desired count"
```

 - Verify alert rules in Prometheus

Go to Alerts page in Prometheus.
