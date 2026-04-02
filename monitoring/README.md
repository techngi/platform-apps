Application Monitoring with Prometheus & Grafana
📌 Overview

This project implements application-level monitoring for the DevOps platform using:

Prometheus → metrics collection
Grafana → visualization
Kubernetes (EKS) → workload orchestration
Flask application → exposes /metrics endpoint

The goal is to provide observability into application health, performance, and reliability.

🏗️ Architecture
Application (Flask)
        ↓
/metrics endpoint
        ↓
ServiceMonitor (Kubernetes)
        ↓
Prometheus (scrapes metrics)
        ↓
Grafana (dashboards & visualization)
⚙️ Components
1. Application (platform-app)
Built using Flask
Exposes:
/ → main endpoint
/health → health check
/metrics → Prometheus metrics

Example metric:

http_requests_total
2. Prometheus
Installed using kube-prometheus-stack
Scrapes:
Kubernetes cluster metrics
Node metrics
Application metrics via ServiceMonitor
3. Grafana
Connected to Prometheus as data source
Used for:
Dashboard visualization
Monitoring application behaviour
Observing resource usage
4. ServiceMonitor

Defines how Prometheus discovers and scrapes the application.

Example:

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
🚀 Deployment Flow
CI Pipeline (platform-app repo)
Code pushed to GitHub
Jenkins pipeline triggered
Docker image built
Image pushed to ECR
CD / GitOps (platform-environments repo)
Image tag updated
Argo CD syncs changes
Kubernetes deployment updated
New pods start with updated image
🔍 Verification Steps
1. Check application is running
kubectl get pods -n dev
2. Port-forward service
kubectl port-forward svc/platform-app-dev 8080:80 -n dev
3. Test endpoints
curl http://127.0.0.1:8080/
curl http://127.0.0.1:8080/health
curl http://127.0.0.1:8080/metrics

Expected:

/ → application response
/health → status OK
/metrics → Prometheus metrics
4. Verify Prometheus target
kubectl port-forward svc/monitoring-kube-prometheus-prometheus 9090 -n monitoring

Open:

http://localhost:9090/targets

✔ Application target should be UP

5. Verify Grafana dashboards
kubectl port-forward svc/monitoring-grafana 3000:80 -n monitoring

Open:

http://localhost:3000
Login with admin credentials
View dashboards:
Kubernetes cluster
Pods
Application metrics
