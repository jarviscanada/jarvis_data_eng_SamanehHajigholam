# Cloud, K8S, and DevOps

This project demonstrates a cloud-native deployment workflow using Docker, Kubernetes (AKS), 
Azure Container Registry (ACR), and Jenkins CI/CD pipelines. It showcases how a containerized 
Spring Boot application can be built, pushed, and deployed to a Kubernetes cluster with automated pipelines.

## Architecture

The system is deployed on Azure Kubernetes Service (AKS) and includes:
- A **NodePort** service to expose the trading application externally
- **Multiple Spring Boot pods** (2 replicas) for scalability and high availability
- A **PostgreSQL database pod** with persistent volume storage (10Gi)
- A **ClusterIP** service for internal database communication (not exposed to internet)
- **Kubernetes Secrets** to securely pass database credentials to the app
- **Azure VM Scale Set** nodes (`Standard_DC2s_v3`) to run container workloads

```
Internet
    ↓
NodePort Service (port 80)
    ↓
trading-app pods (x2, port 8080)
    ↓
ClusterIP Service (trading-db:5432)
    ↓
trading-db pod (PostgreSQL)
    ↓
PersistentVolume (10Gi disk)
```

## CI/CD Pipeline

The deployment process is fully automated using Jenkins:

1. Developer pushes code to GitHub
2. Jenkins pipeline is triggered via webhook
3. Jenkins spins up a temporary pod in K8s with Azure CLI and kubectl containers
4. Azure CLI logs in using a service principal (credentials stored securely in Jenkins)
5. Docker image is built using `az acr build` and tagged with the Jenkins build number
6. Image is pushed to Azure Container Registry (ACR)
7. Kubernetes deployment is updated using `kubectl set image`
8. `kubectl rollout status` confirms zero downtime rolling update

## Key Features

- Containerized microservice deployment on Azure AKS
- Automated CI/CD pipeline with Jenkins (dev and prod)
- Kubernetes-based orchestration, scaling, and rolling updates
- Secure credential management using Kubernetes Secrets and Jenkins credentials store
- Persistent storage with PersistentVolumeClaim for database durability
- Separate dev and prod pipelines targeting different AKS clusters

## Summary

This project demonstrates practical experience building and deploying cloud-native applications 
using modern DevOps practices. It covers the full deployment lifecycle, from containerization 
with Docker, to Kubernetes orchestration on AKS, to fully automated CI/CD pipelines with Jenkins, 
reflecting real-world workflows used in production cloud environments.

