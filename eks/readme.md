Elastic Kubernetes Service - EKS -
===

1- Opening & configuring an Azure account

    Opening an Amazon Web Service Account
        - aws.amazon.com
        - Email
        - Provide Name & Address
        - Credit Card Information
        - Mobile number with verification

2- Initalize Tooling
    - Install & configure AWS CLI
        - Python
        - Access Key
        - Secret
    - Install aws-iam-authenticator : Amazon EKS uses IAM to provide authentication to your Kubernetes cluster
        -> curl -o aws-iam-authenticator https://amazon-eks.s3.us-west-2.amazonaws.com/1.18.9/2020-11-02/bin/   darwin/amd64/aws-iam-authenticator
        -> chmod +x ./aws-iam-authenticator
        -> mkdir -p $HOME/bin && cp ./aws-iam-authenticator $HOME/bin/aws-iam-authenticator && export PATH=$PATH:$HOME/bin
        -> aws-iam-authenticator help : to verify the installation
    - eksctl
        -> curl --silent --location "https://github.com/weaveworks/eksctl/releases/latest/download/eksctl_$(uname -s)_amd64.tar.gz" | tar xz -C /tmp
        -> sudo mv /tmp/eksctl /usr/local/bin
        -> eksctl version

3- Create your EKS Cluster

    - Create a repository
        # grap and save the repositoryUri in the output to push docker images
        -> aws ecr create-repository --repository-name demo 
    - Login to the repo
        # output the docker login command
        -> aws ecr get-login --region us-east-1 --no-include-email 
    - Create an image 
        The image must follow a certain format
            <registryId>.dkr.ecr.<region>.amazonaws.com/<image-name>:<tag>

        Examples : 
            -> docker build -t 23454546667.dkr.ecr.us-east-1.amazonaws.com/demo:1.0 .
            -> docker tag 8e232334e4 -t 23454546667.dkr.ecr.us-east-1.amazonaws.com/demo:1.0 .
    - Push the image after being logged in the registry
        -> docker push 23454546667.dkr.ecr.us-east-1.amazonaws.com/demo:1.0
    - Create a cluster
        -> eksctl create cluster 
            --name demo-cluster
            --region use-east-1
            --zones use-east-1a, use-east-1b, use-east-1d [optional flag]
    - Create Deployment & Service
        -> kubectl create deployment demp-app --image=23454546667.dkr.ecr.us-east-1.amazonaws.com/demo:1.0
    - Create a LoadBalancer service
        -> kubectl expose deployment demo-app --type=LoadBalancer --port 5000 --target-port 5000

4- Scaling & updating your EKS Cluster

    - Scale Pods
        -> kubectl scale deployment  demo-app --replicas=3
    - Scale Nodes
        # get the nodegroup
        -> ekstl get nodegroup --cluster=demo-cluster
        # scale nodes
        -> eksctl scale nodegroup --cluster=demo-cluster --nodes=5 --name=ng-e56250ca
    - Update the app
        -> docker build -t 23454546667.dkr.ecr.us-east-1.amazonaws.com/demo:2.0 .
        -> docker push 23454546667.dkr.ecr.us-east-1.amazonaws.com/demo:2.0
        -> kubectl set image deployment/demo-app demo=23454546667.dkr.ecr.us-east-1.amazonaws.com/demo:2.0

5- Serverless option for your k8s Pods by using the AWS Fargate Service
    - No EC2 nodepool to manage
    - Pods rn on Fargate resources
    - Automatically scale

    - create cluster using Aws Fargate
        -> eksctl create cluster 
            --name demo-cluster
            --region use-east-1
            --zones use-east-1a, use-east-1b, use-east-1d [optional flag]
            --fargate
        -> A Fargate Profile is created for your cluster
    -> same commands to deploy / scale your app as before

6- Browsing the AWS Web Console

    - Cluster
        -> EKS : Access your cluster
    - Registry
        -> ECR : Container Registry
        -> EC2 > Running instances : view the underlying instances
    - Monitoring
        - Cloudwatch
    - Billing

7- Deleting your EKS Cluster

    - delete Service
        -> kubectl delete service demo-app
    - delete Cluster
        -> eksctl delete cluster --name demo-cluster
    - delete images
        -> aws ecr list-images --repository-name demo
    - delete a specific images
        -> aws ecr batch-delete-image --repository-name demo --image-id <image-id>
    - delete repository
        -> aws ecr delete-repository --repository-name demo --force