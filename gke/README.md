# <center>Google Kubernetes Engine - GKE -</center>

1- Architecture
===

[Architecture Diagram](https://app.diagrams.net/#G1_vhCo7SYZB3ZF2k-rKy4Un1OUcK6o3gF)

2- Opening & configuring a Google account
===

- cloud.google.com
- Google Account (Gmail or G Suite)
- Provide Name & Address
- Credit Card Information

3- Create a new GCP Project
===

- Get billing accounts list
    ```bash
    gcloud alpha billing accounts list
    ```

- Get the Organisation ID
    ```bash
    ORGANISATION_ID=$(gcloud organizations describe codeworks.fr --format=json | jq '.name' | cut -f 2 -d '/' | sed 's/"//g')
    ```

- Export a new environment variable named `PROJECT_NAME`
    ```bash
    PROJECT_NAME=codeday-gke-demo
    ```

- Create a new project
    ```bash
    gcloud projects create ${PROJECT_NAME} --organization=${ORGANISATON_ID}
    ```

- Grab the project number
    ```bash
    PROJECT_NUMBER=$(gcloud projects list --format=json | jq -c '.[] | select(.name == env.PROJECT_NAME) | .projectNumber' | sed 's/"//g')
    ```

- Link the project to the billing account
    ```bash
    gcloud alpha billing accounts projects link ${PROJECT_NUMBER} --account-id=0150EE-171E17-3E357F
    ```

- Check the console if you want !!!

4- Initialize Tooling
===

- Enable Kubernetes Engine API (if it's not yes done)
    
    * From the web-based console

- Install Google Cloud SDK
    
    * Make sure that Python is installed in your machine
    
        ```bash
        curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-319.0.0-linux-x86.tar.gz
        
        tar zxvf google-cloud-sdk-319.0.0-linux-x86
        
        ./google-cloud-sdk/install.sh
        
        ./google-cloud-sdk/install.sh --help
        ```
    * Some new commands

        ```bash
        # Configure gcloud to match account / project / zone to use from scratch
        gcloud init
        
        # Display zones list
        gcloud compute zones list
        
        gcloud init

        # Check all of the configuration
        gcloud config list
        ```

5- Google Container Registry
===

- Create the Docker Image
 
    The tag must follow a certain format : **HOST_NAME/PROJECT_NAME/IMAGE_NAME:TAG**
    
    **HOST_NAME** : host for Google Container Registry that will store the image
    
    **PROJECT_NAME** : Project Id on GCP

    **IMAGE_NAME** : Desired Docker Image Name
    
    **TAG** : Tag Number
        
    - Build a new image
    
        ```bash 
        docker build -t gcr.io/${PROJECT_NAME}/greeting-app:1.0.0 .
        ```

    - [FROM TAG] Build new image
        ```bash
        docker tag 8e2324345 gcr.io/${PROJECT_NAME}/greeting-app:1.0.0 .
        ```
- Launch the Docker image

    - Command to launch the docker image
        ```bash
        docker run --publish 5000:5000 --detach --name greeting_app gcr.io/${PROJECT_NAME}/greeting-app:1.0.0
        ```
    
    - visit the logs if you want
        ```bash
        docker logs <CONTAINER_ID> -f
        ```

- Login and setup a credential helper

    ```bash
    gcloud auth configure-docker
    ```

- Push the Docker image to the GCR
    
    ```bash
    docker push gcr.io/${PROJECT_NAME}/greeting-app:1.0.0
    ```

6- Create and interact with your GKE Cluster
===

- Create a cluster : I'm going to start with 2 nodes
    
    ```bash
    gcloud container clusters create codeday-cluster --num-nodes=2
    ```

- Some Kubectl commands

    - Check nodes in the Cluster
        ```bash
        kubectl get nodes
        ```
    
    - get all Pods
        ```bash
        kubectl get pods
        ```

- Create Deployment & Service
    
    ```bash
    kubectl create deployment greeting-app --image=gcr.io/${PROJECT_NAME}/greeting-app:1.0.0
    ```

- Create a LoadBalancer service

    ```bash
    kubectl expose deployment greeting-app --type=LoadBalancer --port 5000 --target-port 5000
    ```

- Access your application using the external IP address of the LB service

7- Scaling & updating your GKE Cluster
===

- Scale Pods

    ```bash
    kubectl scale deployment  greeting-app --replicas=3
    ```
   
- Scale Nodes
    
    ```bash
    gcloud container clusters resize codeday-cluster --num-nodes 1
    ```

- Updating our application
    
    ```bash
    docker build -t gcr.io/${PROJECT_NAME}/greeting-app:2.0.0 .
    
    docker push gcr.io/${PROJECT_NAME}/greeting-app:2.0.0
    
    kubectl set image deployment/greeting-app greeting-app=gcr.io/${PROJECT_NAME}/greeting-app:2.0.0
    ```

8- Browsing the GKE Web Console
===

- Monitoring
    - Monitoring -> Dashboards -> GKE

- Cluster
    - Compute -> Kubernetes Engine

- Registry
    - Container Registry Menu

- Billing
    - Reports

9- Deleting your GKE Cluster
===

- delete Service
    
    ```bash
    kubectl delete service greeting-app
    ```

- delete Cluster
    
    ```bash
    gcloud container clusters delete codeday-cluster
    ```

- delete a specific images

    ```bash
    gcloud container images delete gcr.io/${PROJECT_NAME}/greeting-app:1.0.0
    
    gcloud container images delete gcr.io/${PROJECT_NAME}/greeting-app:2.0.0
    ```

10- Some useful gcloud commands
===
    
- Configure your current gcp environment
    ```bash
    gcloud init
    ```

-  Display projets list
    ```bash
    gcloud projects list
    ```

- Set up a credential helper
    ```bash
    gcloud auth configure-docker
    ```

- Display regions list
    ```bash
    gcloud compute regions list
    ```

- Display zones list
    ```bash
    gcloud compute zones list
    ```

- Display clusters list
    ```bash
    gcloud container clusters list
    ```

- Display images list
    ```bash
    gcloud container images list
    ```
