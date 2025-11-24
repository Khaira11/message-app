pipeline {
    agent any

    environment {
        REGISTRY = "docker.io"
        IMAGE_NAME = "khaira23/message-app"
        IMAGE_TAG = "build-${BUILD_NUMBER}"  // unique tag per build
        CONTAINER_NAME = "message-app-container"
        APP_PORT = "5000"
        K8S_NAMESPACE = "default"
        K8S_DEPLOYMENT_NAME = "message-app"
        K8S_CONTAINER_PORT = "5000"
    }

    stages {
        stage('Checkout Code') {
            steps {
                git branch: 'main', url: 'https://github.com/Khaira11/message-app.git'
            }
        }

        stage('Build Docker Image') {
            steps {
                sh '''
                echo "🏗️ Building Docker image..."
                docker build -t ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG} .
                '''
            }
        }

        stage('Login & Push to DockerHub') {
            steps {
                echo '🔐 Logging in to DockerHub'
                withCredentials([usernamePassword(credentialsId: 'dockerhub-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    sh '''
                        echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                        docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Run Docker Container (Test)') {
            steps {
                sh '''
                echo "🚀 Starting container from the built image for testing..."

                # Stop and remove any previous container with same name
                if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
                    docker rm -f ${CONTAINER_NAME} || true
                fi

                # Run new container
                docker run -d --name ${CONTAINER_NAME} -p ${APP_PORT}:${APP_PORT} ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}

                echo "✅ Container '${CONTAINER_NAME}' is running on port ${APP_PORT}"
                docker ps | grep ${CONTAINER_NAME}
                '''
            }
        }

        stage('Kubernetes Deployment') {
            steps {
                echo '🚀 Deploying to Kubernetes...'
                sh '''
                # Create Kubernetes deployment YAML
                cat > k8s-deployment.yaml <<EOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: ${K8S_DEPLOYMENT_NAME}
  namespace: ${K8S_NAMESPACE}
  labels:
    app: message-app
spec:
  replicas: 2
  selector:
    matchLabels:
      app: message-app
  template:
    metadata:
      labels:
        app: message-app
    spec:
      containers:
      - name: message-app
        image: ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
        ports:
        - containerPort: ${K8S_CONTAINER_PORT}
        env:
        - name: PORT
          value: "${K8S_CONTAINER_PORT}"
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
---
apiVersion: v1
kind: Service
metadata:
  name: ${K8S_DEPLOYMENT_NAME}-service
  namespace: ${K8S_NAMESPACE}
spec:
  selector:
    app: message-app
  ports:
    - protocol: TCP
      port: 80
      targetPort: ${K8S_CONTAINER_PORT}
  type: LoadBalancer
EOF

                # Apply Kubernetes deployment
                kubectl apply -f k8s-deployment.yaml
                '''
            }
        }

        stage('Verify Kubernetes Deployment') {
            steps {
                sh '''
                echo "📊 Checking deployment status..."
                kubectl rollout status deployment/${K8S_DEPLOYMENT_NAME} -n ${K8S_NAMESPACE} --timeout=300s
                
                echo "🔍 Checking pods..."
                kubectl get pods -n ${K8S_NAMESPACE} -l app=message-app
                
                echo "🌐 Checking services..."
                kubectl get svc -n ${K8S_NAMESPACE} | grep ${K8S_DEPLOYMENT_NAME}
                '''
            }
        }
    }

    post {
        always {
            echo "✅ Pipeline completed. Build number: ${BUILD_NUMBER}"
            sh '''
            # Clean up local Docker container
            if [ "$(docker ps -aq -f name=${CONTAINER_NAME})" ]; then
                docker rm -f ${CONTAINER_NAME} || true
            fi
            docker system prune -af
            '''
        }
        success {
            echo "🎉 Deployment successful! Application is running in Kubernetes."
            sh '''
            echo "📋 Final deployment status:"
            kubectl get deployment ${K8S_DEPLOYMENT_NAME} -n ${K8S_NAMESPACE}
            '''
        }
        failure {
            echo "❌ Deployment failed. Check logs for details."
            sh '''
            # Get deployment logs for debugging
            kubectl describe deployment ${K8S_DEPLOYMENT_NAME} -n ${K8S_NAMESPACE} || true
            kubectl logs -l app=message-app -n ${K8S_NAMESPACE} --tail=50 || true
            '''
        }
    }
}
