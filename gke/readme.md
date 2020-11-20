Google Kubernetes Engine - GKE -
===

1- Opening & configuring a Google account
- cloud.google.com
- Google Account (Gmail or G Suite)
- Provide Name & Address
- Credit Card Information

2- Initalize Tooling

- Enable Kubernetes Engine Api
    * From the web-based console

- Install Google Cloud SDK
    * Make sure Python is installed in your machine
    
        ```bash
        $> curl -O https://dl.google.com/dl/cloudsdk/channels/rapid/downloads/google-cloud-sdk-319.0.0-linux-x86.tar.gz
        $> tar zxvf google-cloud-sdk-319.0.0-linux-x86
        $> ./google-cloud-sdk/install.sh
        $> ./google-cloud-sdk/install.sh --help
        ```
    * Some new commands

        ```bash
        $> gcloud init
        $> gcloud projects list
        $> export PROJECT_ID=PROJECT_ID_VALUE
        ```

    * Configure gcloud to match account / project / region to use  


3- Create your GKE Cluster

    - Create an image
        <hostname>/<project-id>/<image-name>:<tag>
            <hostname> : host for Google Container Registry that will store the image
        Examples : 
            -> docker build -t gcr.io/demo-project-123/demo:1.0 .
            -> docker tag 8e2324345 gcr.io/demo-project-123/demo:1.0 .
    - Login 
        -> gcloud auth configure-docker
    - Push the image
        -> docker push gcr.io/demo-project-123/demo:1.0
    - Create a cluster
        -> gcloud container cluster create demo-cluster --num-nodes=3
    - Create Deployment & Service
        -> kubectl create deployment demp-app --image=gcr.io/demo-project-123/demo:1.0
    - Create a LoadBalancer service
        -> kubectl expose deployment demo-app --type=LoadBalancer --port 5000 --target-port 5000

4- Scaling & updating your GKE Cluster

    - Scale Pods
        -> kubectl scale deployment  demo-app --replicas=3
    - Scale Nodes
        -> gcloud container clusters resize demo-cluster --num-nodes 5
    - Update the app
        -> docker build -t gcr.io/demo-project-123/demo:2.0 .
        -> docker push gcr.io/demo-project-123/demo:2.0
        -> kubectl set image deployment/demo-app demo=gcr.io/demo-project-123/demo:2.0

6- Browsing the GKE Web Console

    - Monitoring
        - Monitoring > Stackdriver
            -> resources > Kuberenetes Engine
        - Compute > Kubernetes Engine
    - Cluster
    - Registry
        - Container Registry Menu
    - Billing

7- Deleting your GKE Cluster

    - delete Service
        -> kubectl delete service demo-app
    - delete Cluster
        -> gcloud container clusters delete demo-cluster
    - delete a specific images
        -> gcloud container images delete gcr.io/demo-project-123/demo:1.0
        -> gcloud container images delete gcr.io/demo-project-123/demo:2.0
