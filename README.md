# Google Cloud Kafka Deployment

## Kafka Server Setup

1. Click [here](https://console.cloud.google.com/marketplace/details/click-to-deploy-images/kafka?q=kafka&id=f19a0f63-fc57-47fd-9d94-8d5ca6af935e) to deploy Apache Kafka using Google Cloud Marketplace

  * **Deployment Name:** kafka-server1
  * **Zone:** us-central1-f
  * **Machine Type:** 4vCPUs, 15GB Memory
  * **Boot Disk Type** SSD Persistent Disk
  * **BOot Disk Size** 50GB

2. SSH into kafka-server1

3. Create Kafka Topic

```
/opt/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic topicz1 
```

4. Clone this github repo

```
git clone xxxx
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

2. Clone this github repo

```
git clone xxxx
```

3. Test Run - Simulate 100 Kafka events, which will pass through Kafka and persist in BigQuery

```
xxxx
```

4. Deploy load testing using GKE

```
xxxx
```
