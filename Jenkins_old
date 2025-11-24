pipeline {
    agent any

    environment {
        REGISTRY = "docker.io"
        IMAGE_NAME = "khaira23/message-app"
        IMAGE_TAG = "build-${BUILD_NUMBER}"  // unique tag per build
        CONTAINER_NAME = "message-app-container"
        APP_PORT = "5000"
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

        stage('Run Docker Container') {
            steps {
                sh '''
                echo "🚀 Starting container from the built image..."

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
    }

    post {
        always {
            echo "✅ Pipeline completed. Build number: ${BUILD_NUMBER}"
            sh 'docker system prune -af'
        }
    }
}

