# Aselsan-Devops-Junior-Task
## Table of Contents
- [Prerequisites](#prerequisites)
- [Step 1](#step1)
- [Step 2](#step2)
- [Step 3](#step3)

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
Once the image is built and pushed to DockerHub, you can run the Docker container. `your_dockerhub_username/binance` this specifies the Docker image to use. This command will start the container, running the binanceAPI.py script, which fetches and logs BTCUSDT exchange rates at 5-minute intervals.

## Step2
In this step, we set up a cron job to monitor the system's load average at specific times and log the information to a file. The cron job is scheduled to run at 3:00 AM on the 5th, 10th, 15th, 20th, 25th, and 30th of each month.

- **Creating the Script**
```
nano script.sh
```
First, we create a shell script named **script.sh** that captures the system's load average and saves it to a timestamped log file. You can copy directly **script.sh** file.

``` 
chmod +x /path/to/script.sh
```
Making the script executable. Replace `/path/to/script.sh` with the actual path to your script.

```
crontab -e
```
Edit the crontab file. We add the script to the cron jobs list to automate its execution.

```
0 3 5,10,15,20,25,30 * * /path/to/script.sh
```
`0 3`: Specifies that the job runs at 3:00 AM.

`5,10,15,20,25,30`: Specifies the days of the month the job runs.

`*`: Any month.

`*`: Any day of the week.

 `/path/to/script.sh`: The full path to the shell script.
 







