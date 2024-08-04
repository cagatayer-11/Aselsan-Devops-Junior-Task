# Aselsan-Devops-Junior-Task
## Table of Contents
- [Prerequisites](#prerequisites)
- [Step 1](#step1)

## Prerequisites
- [Docker](https://docs.docker.com/engine/install/)
- [Kubernetes (minikube, kubectl)](https://kubernetes.io/docs/setup/)
- [Python 3.9 or higher](https://www.python.org/downloads/)
- Access to a Linux environment

## Step1
- **Docker**

First, Docker needs to be installed on the Linux machine refer to the official [Docker](https://docs.docker.com/engine/install/) installation guide.

- **Dockerize the Python Script**

A Dockerfile defines the environment and dependencies required to run the application. You can use "Dockerfile" in BinanceAPI folder.
```
docker build -t your_dockerhub_username/binance .
```
Use the Docker CLI to build the Docker image from the Dockerfile.
  ```
docker login -u "your_user_name" -p "your_password"
docker push your_dockerhub_username/binance
```
Push the image to DockerHub for centralized storage and distribution.
```
 docker run your_user_name/binance
```
Once the image is built and pushed to DockerHub, you can run the Docker container. `your_dockerhub_username/binance` this specifies the Docker image to use.











