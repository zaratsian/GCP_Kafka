# Kafka Simulation on Google Cloud

**Index:**

1. Configure [Google BigQuery](https://cloud.google.com/bigquery/)
2. Create Service Account within GCP
3. Install and configure Kafka Server
4. Install and configure Kafka Client - With containerized simulator, scaled with [GKE](https://cloud.google.com/kubernetes-engine/)


## Google BigQuery Setup

1. Launch Google Cloud Shell from the GCP Console

2. Create BigQuery Dataset

```
# Variables
project_id=$GOOGLE_CLOUD_PROJECT
dataset_id=kafka_ds
table_id=kafka_table1

# Create BigQuery Dataset
bq mk --description "Kafka Dataset" $dataset_id

# Create BigQuery Table
bq mk --table --description "Kafka Table" $project_id:$dataset_id.$table_id id:STRING,date:STRING,timestamp:STRING,flag:INTEGER,value:FLOAT

echo "[ INFO ] List all BigQuery tables within $dataset_id"
bq ls $dataset_id
```

## Create Service Account (so Kafka can write to BigQuery)

```
# Service Account Name
sa_name=kafka-to-bigquery

# Create Service Account
gcloud iam service-accounts create $sa_name --display-name $sa_name

# Add Roles (specifically for BigQuery)
gcloud projects add-iam-policy-binding $GOOGLE_CLOUD_PROJECT \
  --member serviceAccount:$sa_name@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com \
  --role roles/bigquery.dataEditor

# List the Service Account Keys for the specified SA
gcloud iam service-accounts keys list \
  --iam-account $sa_name@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com

# Create the SA Key
gcloud iam service-accounts keys create /tmp/$sa_name.json \
  --iam-account $sa_name@$GOOGLE_CLOUD_PROJECT.iam.gserviceaccount.com

# Move to Google Cloud Storage
gsutil mb gs://$GOOGLE_CLOUD_PROJECT-kafka
gsutil cp /tmp/$sa_name.json gs://$GOOGLE_CLOUD_PROJECT-kafka
```

## Kafka Server Setup

1. Click [here](https://console.cloud.google.com/marketplace/details/click-to-deploy-images/kafka?q=kafka) to deploy Apache Kafka using Google Cloud Marketplace

  * **Deployment Name:** kafka-server1
  * **Zone:** us-central1-f
  * **Machine Type:** 4vCPUs, 15GB Memory
  * **Boot Disk Type** SSD Persistent Disk
  * **BOot Disk Size** 50GB

2. SSH into kafka-server1-vm

3. Create Kafka Topic

```
/opt/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic topicz1 
```

4. Clone this Github repo

```
sudo apt install git -y
git clone https://github.com/zaratsian/GCP_Kafka.git
```

5. Install Python Libraries

```
sudo apt install python-pip -y
sudo pip install kafka-python==1.4.4
sudo pip install google-cloud-bigquery==1.9.0
```

6. Copy SA into GCE instance

```
cd ~
export GOOGLE_CLOUD_PROJECT="$(curl 'http://metadata.google.internal/computeMetadata/v1/project/project-id' -H 'Metadata-Flavor: Google')"
gsutil cp gs://$GOOGLE_CLOUD_PROJECT-kafka/kafka-to-bigquery.json .
```

7. Run Kafka Consumer Client for BigQuery (this is used to stream events from Kafka to BigQuery)

```
python ./GCP_Kafka/kafka_consumer_bigquery.py --bootstrap_servers kafka-server1-vm:9092 --kafka_topic topicz1 --bq_dataset_id kafka_ds --bq_table_id kafka_table1 &
```

**NOTE: Kafka Command Line Consumer**

/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka-server1-vm:9092 --topic topicz1


## Kafka Client Setup

1. Launch Google Cloud Shell from the GCP Console

2. Deploy a GCE instance, which acts as the Kafka Client

```
project_id=$GOOGLE_CLOUD_PROJECT
gce_instance_name=kafka-client1

gcloud compute --project=$project_id instances create $gce_instance_name --zone=us-east1-b --machine-type=n1-standard-4 --subnet=default --network-tier=PREMIUM --maintenance-policy=MIGRATE --scopes=https://www.googleapis.com/auth/cloud-platform --image=debian-9-drawfork-v20181101 --image-project=eip-images --boot-disk-size=20GB --boot-disk-type=pd-standard --boot-disk-device-name=$gce_instance_name
```

3. SSH into this GCE Instance (which is the Kafka Client)

4. Install Python Libraries

```
sudo apt install python-pip -y
sudo pip install kafka-python==1.4.4
```

5. Clone this Github repo

```
sudo apt install git -y
git clone https://github.com/zaratsian/GCP_Kafka.git
```

6. Test Run - Simulate 100 Kafka events, which will pass through Kafka and persist in BigQuery

```
python ./GCP_Kafka/kafka_simulator/kafka_simulator.py --bootstrap_servers kafka-server1-vm:9092 --kafka_topic topicz1 --time_delay 5 --send_to_kafka 1
```

7. Deploy load testing using GKE (execute from Google Cloud Shell)

```
# NOTE: Execute these commands from the Google Cloud Shell

# Install Docker (if not already installed)
#sudo apt update
#sudo apt install -y apt-transport-https ca-certificates curl software-properties-common
#curl -fsSL https://download.docker.com/linux/ubuntu/gpg | sudo apt-key add -
#sudo add-apt-repository "deb [arch=amd64] https://download.docker.com/linux/ubuntu bionic stable"
#sudo apt update
#apt-cache policy docker-ce
#sudo apt install -y docker-ce
#sudo usermod -aG docker ${USER}

# Clone Git Repo
git clone https://github.com/zaratsian/GCP_Kafka.git

# Navigate to dir
cd GCP_Kafka/kafka_simulator_threaded/

# Build Docker container
sudo ./01_build.sh

# Setup Container Registry
sudo ./02_setup_container_registry.sh

# Deploy GKE to execute the Kafka Simulation
# NOTE: This will create the GKE Cluster, which takes a few minutes to spin up.
sudo ./04_deploy_gke.sh
```

8. GKE Cluster can be cleanup / shut down by using the following commands:

```
gke_cluster_name=gke-cluster-z1
gke_app_name=gke-app-z1
gke_compute_zone=us-central1-b

# Delete a service
#kubectl delete service $gke_app_name

# Delete a Deployment
#kubectl delete deployment $gke_app_name

# Delete GKE Cluster
#gcloud container clusters delete $gke_cluster_name --zone $gke_compute_zone
```
