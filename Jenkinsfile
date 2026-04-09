pipeline {
  agent any

  environment {
    AWS_REGION   = "ap-southeast-2"
    AWS_ACCOUNT  = "914339264187"
    ECR_REPO     = "devops-app"
    ECR_REGISTRY = "${AWS_ACCOUNT}.dkr.ecr.${AWS_REGION}.amazonaws.com"
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

    stage("Trivy Scan") {
      steps {
        sh """
          set -euxo pipefail
          docker run --rm \
            -v /var/run/docker.sock:/var/run/docker.sock \
            ghcr.io/aquasecurity/trivy:latest \
            image --scanners vuln \
            --severity CRITICAL \
            --exit-code 1 \
            --no-progress \
            ${ECR_REPO}:${IMAGE_TAG}
        """
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

    stage("Update Dev GitOps Repo") {
      steps {
        withCredentials([string(credentialsId: 'github_token', variable: 'GITHUB_TOKEN')]) {
          sh '''
            set -euxo pipefail
            rm -rf platform-environments
            git clone https://${GITHUB_TOKEN}@github.com/techngi/platform-environments.git platform-environments
            cd platform-environments

            sed -i -E "s/^( *tag:).*/\\1 \\"${IMAGE_TAG}\\"/" envs/dev/values.yaml

            git config user.email "jenkins@local"
            git config user.name "jenkins"

            git add envs/dev/values.yaml
            git diff --cached --quiet || git commit -m "Update dev image tag to ${IMAGE_TAG}"
            git push origin master
          '''
        }
      }
    }

stage('Debug Branch') {
  steps {
    sh '''
      echo "BRANCH_NAME=${BRANCH_NAME}"
      echo "GIT_BRANCH=${GIT_BRANCH}"
    '''
  }
}

    stage('Approve Production Deployment') {
	when {
	  expression {
            return env.GIT_BRANCH == 'origin/master' || env.BRANCH_NAME == 'master'
         }
        }

      steps {
        timeout(time: 10, unit: 'MINUTES') {
          input message: "Deploy to PRODUCTION?", ok: "Deploy"
        }
      }
    }

    stage('Promote to Production') {
      when {
        expression {
          return env.GIT_BRANCH == 'origin/master' || env.BRANCH_NAME == 'master'
         }  
       }
      steps {
        withCredentials([string(credentialsId: 'github_token', variable: 'GITHUB_TOKEN')]) {
          sh '''
            set -euxo pipefail

            rm -rf platform-environments
            git clone https://${GITHUB_TOKEN}@github.com/techngi/platform-environments.git platform-environments
            cd platform-environments

            sed -i -E "s/^( *tag:).*/\\1 \\"${IMAGE_TAG}\\"/" envs/prod/values.yaml

            git config user.email "jenkins@local"
            git config user.name "jenkins"

            git add envs/prod/values.yaml
            git diff --cached --quiet || git commit -m "Promote image ${IMAGE_TAG} to prod"
            git push origin master
          '''
        }
      }
    }
  }
}
