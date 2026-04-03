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

Example metric:
http_requests_total


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
spec:
  selector:
    matchLabels:
      app: platform-app
  namespaceSelector:
    matchNames:
      - dev
  endpoints:
    - port: http
      path: /metrics
      interval: 15s
```
### Deployment Workflow

CI Pipeline (platform-app repo)
1. Code pushed to GitHub
2. Jenkins pipeline triggered
3. Docker image built
4. Image pushed to ECR

### CD / GitOps (platform-environments repo)
1. Image tag updated
2. Argo CD syncs changes
3. Kubernetes deployment updated
4. New pods start with updated image

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
kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090 -n monitoring
```

Open:

```bash
http://localhost:9090/targets
```

Application target should be UP

Verify Grafana
```bash
kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring
```

Open:

```bash
http://localhost:3000
```
