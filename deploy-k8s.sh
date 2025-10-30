#!/bin/bash

echo "Deploying to Kubernetes..."

# Apply Kubernetes manifests
kubectl apply -f k8s/configmap.yaml
kubectl apply -f k8s/deployment.yaml
kubectl apply -f k8s/service.yaml

# Optional: Apply ingress if you have one
# kubectl apply -f k8s/ingress.yaml

echo "Waiting for pods to be ready..."
kubectl wait --for=condition=ready pod -l app=webhook-test-app --timeout=60s

echo "Deployment complete!"
echo "Service URL:"
kubectl get service webhook-test-service
