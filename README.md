# Repository Structure

week3-app-ci/
├── Dockerfile
└── app/
    ├── app.py
    └── requirements.txt

- app.py

```bash
from flask import Flask, jsonify
import os

app = Flask(__name__)

@app.get("/health")
def health():
    return jsonify(app="week3-app", status="ok", version=os.getenv("APP_VERSION", "dev"))

@app.get("/")
def root():
    return "week3-app is running\n"

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
```

- requirements.txt

```bash
Flask==3.0.2
```

- Dockerfile

```bash
docker build -t app:test .
docker ps -a
docker run -d -p 5000:5000 app:test
curl http://localhost:5000/health
 
docker stop {container-id}
docker ps -a
```

```bash
FROM python:3.10-slim

WORKDIR /app

COPY app/requirements.txt /app/requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ /app/

EXPOSE 5000

CMD ["python", "app.py"]
```

- Jenkinsfile

```bash
pipeline {
  agent any

  environment {
    AWS_REGION   = "ap-southeast-2"
    AWS_ACCOUNT  = "421869852482"
    ECR_REPO     = "devops-app"
    ECR_REGISTRY = "${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"

    GITOPS_REPO  = "techngi/platform-environments"
    GITOPS_DIR   = "platform-environments"
    VALUES_FILE  = "envs/dev/values.yaml"
  }

  stages {

    stage("Checkout CI repo") {
      steps {
        checkout scm
      }
    }

    stage("Build Docker Image") {
      steps {
        script {
          env.IMAGE_TAG = sh(script: "git rev-parse --short HEAD", returnStdout: true).trim()

          sh """
            set -euxo pipefail
            docker build -t ${ECR_REPO}:${IMAGE_TAG} .
            docker tag ${ECR_REPO}:${IMAGE_TAG} ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}
          """
        }
      }
    }

stage("Push Image to ECR") {
  steps {
    withCredentials([[$class: 'AmazonWebServicesCredentialsBinding', credentialsId: 'aws-creds']]) {
      sh """
        set -euxo pipefail

        aws sts get-caller-identity

        aws ecr get-login-password --region ${AWS_REGION} | \
          docker login --username AWS --password-stdin ${ECR_REGISTRY}

        docker push ${ECR_REGISTRY}/${ECR_REPO}:${IMAGE_TAG}
      """
    }
  }
}

    stage("Update GitOps Repo (CD Trigger)") {
      steps {
        withCredentials([string(credentialsId: 'github_token', variable: 'GITHUB_TOKEN')]) {
          sh """
            set -euxo pipefail
            rm -rf ${GITOPS_DIR}
            git clone https://${GITHUB_TOKEN}@github.com/${GITOPS_REPO}.git ${GITOPS_DIR}
            cd ${GITOPS_DIR}

            # Update the tag in the file ArgoCD uses
            sed -i -E 's/^( *tag:).*/\\1 "'"${IMAGE_TAG}"'"/' ${VALUES_FILE}

            git config user.email "jenkins@local"
            git config user.name "jenkins"

            git add ${VALUES_FILE}
            git diff --cached --quiet || git commit -m "Update image tag to ${IMAGE_TAG}"
            git push origin master
          """
        }
      }
    }

  } // end stages
}   // end pipeline
```


