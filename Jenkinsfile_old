pipeline {
    agent any

    environment {
        REGISTRY = "docker.io"
        IMAGE_NAME = "khaira23/message-app"
        IMAGE_TAG = "build-${BUILD_NUMBER}"  // unique tag per build
        DEPLOYMENT_FILE = "k8s/deployment.yaml"
        KUBE_DEPLOYMENT = "flask-deployment"
        KUBE_NAMESPACE = "default"
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
                withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'DOCKER_PASSWORD', usernameVariable: 'DOCKER_USERNAME')]) {
                    sh '''
                        echo $DOCKER_PASSWORD | docker login -u $DOCKER_USERNAME --password-stdin
                        docker push ${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}
                    '''
                }
            }
        }

        stage('Deploy to Kubernetes') {
            steps {
                withKubeConfig([credentialsId: 'k8s-credential']) {
                    sh '''
                    echo "🚀 Deploying application to Kubernetes..."
                    
                    # Replace the image placeholder dynamically
                    sed -i "s|IMAGE_PLACEHOLDER|${REGISTRY}/${IMAGE_NAME}:${IMAGE_TAG}|g" ${DEPLOYMENT_FILE}

                    # Apply deployment
                    kubectl apply -f ${DEPLOYMENT_FILE}
                    kubectl rollout status deployment/${KUBE_DEPLOYMENT} -n ${KUBE_NAMESPACE}
                    '''
                }
            }
        }
    }

    post {
        always {
            echo "✅ Pipeline completed. Build number: ${BUILD_NUMBER}"
        }
    }
}

