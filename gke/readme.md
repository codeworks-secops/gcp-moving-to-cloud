# <center>Google Kubernetes Engine - GKE -</center>

0- Architecture
===

[Open the Architecture Diagram](https://app.diagrams.net/#G1_vhCo7SYZB3ZF2k-rKy4Un1OUcK6o3gF)

1- Opening & configuring a Google account
===

- cloud.google.com
- Google Account (Gmail or G Suite)
- Provide Name & Address
- Credit Card Information

2- Create new GCP Project
===

```bash
# Get billing accounts list
$> gcloud alpha billing accounts list
# Get the Organisation ID
ORGANISATION_ID=$(gcloud organizations describe codeworks.fr --format=json | jq '.name' | cut -f 2 -d '/' | sed 's/"//g')
# Export a new environment variable named `PROJECT_NAME`
$> export PROJECT_NAME=codeday-gke-demo
# Create a new project
$> gcloud projects create ${PROJECT_NAME} --organization=${ORGANISATON_ID}
# Grab the project number
$> PROJECT_NUMBER=$(gcloud projects list --format=json | jq -c '.[] | select(.name == env.PROJECT_NAME) | .projectNumber' | sed 's/"//g')
# Link the project to the billing account
$> gcloud alpha billing accounts projects link ${PROJECT_NUMBER} --account-id=0150EE-171E17-3E357F
# Check the console if you want !!!
```

3- Initialize Tooling
===

- Enable Kubernetes Engine API (if it's not yes done)
    
    * From the web-based console

- Install Google Cloud SDK
    
    * Make sure that Python is installed in your machine
    
        ```bash
        $> curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-319.0.0-linux-x86.tar.gz
        $> tar zxvf google-cloud-sdk-319.0.0-linux-x86
        $> ./google-cloud-sdk/install.sh
        $> ./google-cloud-sdk/install.sh --help
        ```
    * Some new commands

        ```bash
        # Configure gcloud to match account / project / zone to use from scratch
        $> gcloud init
        # Display zones list
        $> gcloud compute zones list
        # Checl all of the configuration
        $> gcloud config list
        ```

4- Google Container Registry
===

- Create the Docker Image
 
    The tag must follow a certain format : **HOST_NAME/PROJECT_NAME/IMAGE_NAME:TAG**
    
    **HOST_NAME** : host for Google Container Registry that will store the image
    
    **PROJECT_NAME** : Project Id on GCP

    **IMAGE_NAME** : Desired Docker Image Name
    
    **TAG** : Tag Number
        
    ```bash 
    # Build new image 
    $> docker build -t gcr.io/${PROJECT_NAME}/greeting-app:1.0.0 .
    # [FROM TAG] Build new image
    $> docker tag 8e2324345 gcr.io/${PROJECT_NAME}/greeting-app:1.0.0 .
    ```
- Launch the Docker image

    ```bash
    # command to launch the docker image
    docker run --publish 5000:5000 --detach --name greeting_app gcr.io/${PROJECT_NAME}/greeting-app:1.0.0
    # visit the logs
    docker logs <CONTAINER_ID> -f
    ```

- Login

    ```bash
    # set up a credential helper
    $> gcloud auth configure-docker
    ```

- Push the image
    
    ```bash
    $> docker push gcr.io/${PROJECT_NAME}/greeting-app:1.0.0
    ```

5- Create and interact with your GKE Cluster
===

- Create a cluster
    
    ```bash
    # I'm going to start with 2 nodes
    $> gcloud container clusters create codeday-cluster --num-nodes=2
    ```

- Some Kubectl commands

    ```bash
    # Check nodes in the Cluster
    $> kubectl get nodes
    # Check Pods
    $> kubectl get pods
    ```
- Create Deployment & Service
    
    ```bash
    $> kubectl create deployment greeting-app --image=gcr.io/${PROJECT_NAME}/greeting-app:1.0.0
    ```

- Create a LoadBalancer service

    ```bash
    $> kubectl expose deployment greeting-app --type=LoadBalancer --port 5000 --target-port 5000
    ```

6- Scaling & updating your GKE Cluster
===

- Scale Pods

    ```bash
    $> kubectl scale deployment  greeting-app --replicas=3
    ```
   
- Scale Nodes
    
    ```bash
    $> gcloud container clusters resize codeday-cluster --num-nodes 1
    ```

- Updating our application
    
    ```bash
    $> docker build -t gcr.io/${PROJECT_NAME}/greeting-app:2.0.0 .
    $> docker push gcr.io/${PROJECT_NAME}/greeting-app:2.0.0
    $> kubectl set image deployment/greeting-app greeting-app=gcr.io/${PROJECT_NAME}/greeting-app:2.0.0
    ```

7- Browsing the GKE Web Console
===

- Monitoring
    - Monitoring -> Dashboards -> GKE

- Cluster
    - Compute -> Kubernetes Engine

- Registry
    - Container Registry Menu

- Billing
    - Reports

8- Deleting your GKE Cluster
===

- delete Service
    
    ```bash
    $> kubectl delete service greeting-app
    ```

- delete Cluster
    
    ```bash
    $> gcloud container clusters delete codeday-cluster
    ```

- delete a specific images

    ```bash
    $> gcloud container images delete gcr.io/${PROJECT_NAME}/greeting-app:1.0.0
    $> gcloud container images delete gcr.io/${PROJECT_NAME}/greeting-app:2.0.0
    ```

9- Some useful gcloud commands
===

```bash
# Configure your current gcp environment
$> gcloud init
# Display projets list
$> gcloud projects list
# Set up a credential helper
$> gcloud auth configure-docker
# Display regions list
$> gcloud compute regions list
# Display zones list
$> gcloud compute zones list
# Display clusters list
$> gcloud container clusters list
# Display images list
$> gcloud container images list
```
