Azure Kubernetes Service - AKS -
===

1- Opening & configuring an Azure account

    Opening a Microsoft Azure Account
        - azure.microsoft.com
        - Microsoft account (skype, Github)
        - Provide Name & Address
        - Credit Card Information

    Initalize Tooling
        - Install Azure CLI (require Python3 - if Linux (also installed gcc))
        - login from the CLI to associate it with your account - az login
        - Register namespaces (to create & manage your cluster) - 
            3 required namespaces that are not configured automatically :
                az provider register --namespace Microsoft.Network
                az provider register --namespace Microsoft.Compute
                az provider register --namespace Microsoft.OperationsManagement
            Registering these namespaces first will save you from several error message
        - Choose a location
            az account list locations
        - Create resource group (used to organize and manager related resources for your k8s cluster)
            az group create --name kube-demo --location westus

2- Create a registry

    az acr create 
        --resource-group kube-demo (-g)
        --location  uswest (-l)
        --name mydemoregistry (-n)
        --sky Basic 

3- Create an image 
 
    The image must follow a certain format
        <registry-name>.azurecr.io/<namespace>/<image-name>:<tag>

    Example : docker build -t demoregistry.azurecr.io/examples/demo:1.0 .

4- Push into the Azure registry

    az acr login --name demoregistry
    docker push demoregistry.azurecr.io/examples/demo:1.0

4- Create a cluster

    az aks create
        --resource-group kube-demo (-g)
        --name  demo-cluster (-n)
        --node-vm-size Standard_D1 // what size of VM to use for nodes
        --generate-ssh-keys

5- Create deployment in the cluster

    To do that, we must set before a few permissions
    #get the id from your cluster
    CLIENT_ID=$(az aks show -g kube-demo -n demo-cluster --query "servicePrincipalProfile.clientId" --output tsv ) 
    #get the id for your registry
    ACR_ID=$(az acr show -g kube-demo -n globomanticsdemoregistry --query "id" --output tsv) 
    #Allow cluster pull from your registry
    az role assignment create  \
        --assignee $CLIENT_ID  \
        --role acrpull  \
        --score $ACR_ID
    #get the credential for kubectl to connect to your cluster
    az aks get-credentials -g kube-demo -n demo-cluster
    #enable monitoring for your cluster
    az aks enable-addons -a monitoring -g kube-demo -n demo-cluster
    # Create Deployment & Service
    kubectl create deployment demp-app --image=demoregistry.azurecr.io/examples/demo:1.0
    # Create a LoadBalancer service
    kubectl expose deployment demo-app --type=LoadBalancer --port 5000 --target-port 5000


6- Create image directly in the cloud

7- Destroying your AKS cluster

    # delete the service
    kubectl delete service demo-service
    # delete the cluster
    az aks delete -g kube-demo -n demo-cluster
    # delete the repository
    az acr repository delete -n demoregistry --image examples/demo:2.0
    # delete the entire group
    az group delete -n kube-demo 

