# 🚀 Platform Apps (DevOps CI/CD Pipeline)

This repository contains the application code and CI pipeline used to build, scan, and deploy a containerised application using modern DevOps practices.

---

## 🧩 Overview

This project demonstrates a **production-style CI pipeline** that integrates:

* Docker image build
* Security scanning (Trivy)
* AWS ECR image registry
* GitOps-based deployment (ArgoCD)
* Promotion workflow (Dev → Prod)

---

## ⚙️ CI/CD Pipeline Flow

```
Code Push (GitHub)
        ↓
Jenkins Pipeline
        ↓
Build Docker Image (Git SHA tag)
        ↓
Trivy Security Scan (fail on critical)
        ↓
Push Image to AWS ECR
        ↓
Update GitOps Repo (Dev)
        ↓
ArgoCD Deploys to Dev
        ↓
⏸ Manual Approval
        ↓
Promote to Production
        ↓
ArgoCD Deploys to Prod
```

---

## 🔐 Security (DevSecOps)

* Integrated **Trivy vulnerability scanning**
* Pipeline fails on **CRITICAL vulnerabilities**
* Ensures only secure images are promoted

```
--severity CRITICAL --exit-code 1
```

---

## 🏷 Image Tagging Strategy

* Uses **Git commit SHA** for immutability
* Example:

```
devops-app:10c206a
```

Benefits:

* Traceability
* Rollback capability
* Consistent deployments

---

## 🧪 Reliability Practices

* Health endpoints exposed (`/health`)
* Readiness & Liveness probes configured in Kubernetes
* Immutable deployments using image tags

---

## 🛠 Tech Stack

* Jenkins (CI)
* Docker
* Trivy (Security)
* AWS ECR
* GitHub

---

## 📦 Repository Structure

```
.
├── app/
├── Dockerfile
├── Jenkinsfile
└── README.md
```

---

## 🎯 Key Learnings

* End-to-end CI pipeline design
* DevSecOps integration
* GitOps deployment trigger mechanism
* Production promotion workflow

---
