pipeline {
agent any
environment {
    DOCKER_CREDENTIALS_ID = 'roseaw-dockerhub'
    DOCKER_IMAGE = 'cithit/chhetra2'
    IMAGE_TAG = "build-${BUILD_NUMBER}"
    GITHUB_URL = 'https://github.com/chhetra2-ops/225-lab3-6.git'
    KUBECONFIG = credentials('chhetra2-225')
}

stages {
    stage('Checkout') {
        steps {
            checkout([
                $class: 'GitSCM',
                branches: [[name: '*/main']],
                userRemoteConfigs: [[url: "${GITHUB_URL}"]]
            ])
        }
    }

    stage('Lint HTML') {
        steps {
            sh 'npm install htmlhint --save-dev'
            sh 'npx htmlhint *.html'
        }
    }

    stage('Build Docker Image') {
        steps {
            script {
                docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                    docker.build("${DOCKER_IMAGE}:${IMAGE_TAG}", "-f Dockerfile.build .")
                }
            }
        }
    }

    stage('Push Docker Image') {
        steps {
            script {
                docker.withRegistry('https://index.docker.io/v1/', "${DOCKER_CREDENTIALS_ID}") {
                    docker.image("${DOCKER_IMAGE}:${IMAGE_TAG}").push()
                }
            }
        }
    }

    stage('Deploy to Dev Environment') {
        steps {
            sh """
                sed -i 's|cithit/chhetra2:latest|cithit/chhetra2:${IMAGE_TAG}|' deployment-dev.yaml
                kubectl apply -f deployment-dev.yaml
                kubectl rollout status deployment/dev-deployment --timeout=120s
            """
        }
    }

    stage('Inspect Dev Routing') {
        steps {
            sh 'kubectl get ingress -o wide'
            sh 'kubectl get service dev-service -o wide'
            sh 'kubectl get endpoints dev-service -o wide'
        }
    }

    stage('Run Acceptance Tests') {
        steps {
            sh 'docker rm -f qa-tests || true'
            sh 'docker build -t qa-tests -f Dockerfile.test .'
            sh 'docker run --rm qa-tests'
        }
    }

    stage('Deploy to Prod Environment') {
        steps {
            sh """
                sed -i 's|cithit/chhetra2:latest|cithit/chhetra2:${IMAGE_TAG}|' deployment-prod.yaml
                kubectl apply -f deployment-prod.yaml
                kubectl rollout status deployment/prod-deployment --timeout=120s
            """
        }
    }

    stage('Check Kubernetes Cluster') {
        steps {
            sh 'kubectl get all'
            sh 'kubectl get ingress -o wide'
        }
    }
}

post {
    success {
        slackSend(
            color: 'good',
            message: "Build Completed: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        )
    }

    unstable {
        slackSend(
            color: 'warning',
            message: "Build Unstable: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        )
    }

failure {
        slackSend(
            color: 'danger',
            message: "Build Failed: ${env.JOB_NAME} ${env.BUILD_NUMBER}"
        )
    }
}

}
