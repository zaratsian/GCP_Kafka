# Google Cloud Kafka Deployment


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
git clone https://github.com/zaratsian/Kafka_GCP.git
```

5. Run Kafka Consumer Client for BigQuery (this will stream events from Kafka to Google BigQuery)

```
python kafka_consumer_bigquery.py 
```

**NOTE: Kafka Command Line Consumer**
/opt/kafka/bin/kafka-console-consumer.sh --bootstrap-server kafka-server1-vm:9092 --topic topicz1


## Kafka Client Setup

1. Deploy a GCE instance, which acts as the Kafka Client

```
gcloud ...
```

2. Clone this Github repo

```
git clone https://github.com/zaratsian/Kafka_GCP.git
```

3. Test Run - Simulate 100 Kafka events, which will pass through Kafka and persist in BigQuery

```
xxxx
```

4. Deploy load testing using GKE

```
xxxx
```
