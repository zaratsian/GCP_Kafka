
#############################################################################
#
#   Variables
#
#############################################################################
gke_cluster_name=gke-cluster-z1
gke_app_name=gke-app-z1
gke_app_image=gcr.io/ml-healthcare-poc-201901/kafka_simulator_threaded
number_of_nodes=10
number_of_replicas=$((number_of_nodes * 2))
gke_compute_zone=us-central1-b


#############################################################################
#
#   Deployment
#
#############################################################################

# Create a GKE Cluster
#gcloud config set compute/zone $$gke_compute_zone
gcloud container clusters create $gke_cluster_name \
    --num-nodes $number_of_nodes \
    --machine-type n1-standard-1 \
    --zone $gke_compute_zone


# Get authentication credentials for the cluster
# After creating the cluster, you need to get authentication credentials to interact with the cluster
gcloud container clusters get-credentials $gke_cluster_name --zone $gke_compute_zone


# Deploy an application to the cluster
kubectl run $gke_app_name --image $gke_app_image


# Exposing the Deployment
# After deploying the application, you need to expose it so that users can access it.
# You can expose your application by creating a Service, a Kubernetes resource that exposes your application to external traffic.
# --port initializes public port 80 to the Internet and
# --target-port routes the traffic to port 8080 of the application
#kubectl expose deployment $gke_app_name --type LoadBalancer --port 80 --target-port 8080


# Scaling Deployment (Manual)
# https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#scale
kubectl scale deployment $gke_app_name --replicas $number_of_replicas

# Scaling Deployment (Autoscale)
# https://kubernetes.io/docs/reference/generated/kubectl/kubectl-commands#autoscale
#kubectl autoscale deployment $gke_app_name --max 6 --min 4 --cpu-percent 50


#############################################################################
#
#   Upgrade
#
#############################################################################

#kubectl edit deployment $gke_app_name


#############################################################################
#
#   Status
#
#############################################################################

# Get Services
kubectl get services

# Inspect the app
#kubectl get service $gke_app_name

# Get Deployments
kubectl get deployments

# Get Pods
kubectl get pods

# Cluster Info
#kubectl cluster-info

# Configs
#kubectl config view


#############################################################################
#
#   Troubleshooting
#
#############################################################################

# Get Events
#kubectl get events

# Pod Logs
#kubectl logs <pod-name>


#############################################################################
#
#   Cleanup
#
#############################################################################

# Delete a service
#kubectl delete service $gke_app_name

# Delete a Deployment
#kubectl delete deployment $gke_app_name

# Delete GKE Cluster
#gcloud container clusters delete $gke_cluster_name --zone $gke_compute_zone



#ZEND
