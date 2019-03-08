
#####################################################################
#
#   Kafka Consumer - Stream data to Google BigQuery
#
#   USAGE: python kafka_consumer_bigquery.py --bootstrap_servers kafka-server1-vm:9092 --kafka_topic topicz1 --bq_dataset_id kafka_ds --bq_table_id kafka_table1 &
#
#   Requirements:
#       pip install kafka-python
#       pip install --upgrade google-cloud-bigquery
#
#####################################################################

import os
import time, datetime
import json
import argparse
import threading
import multiprocessing
from kafka import KafkaConsumer, KafkaProducer
from google.cloud import bigquery

os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "{}/kafka-to-bigquery.json".format( os.environ['HOME'] )  # Service Acct


#####################################################################
#
#   Functions
#
#####################################################################

def bg_streaming_insert(rows_to_insert, bq_dataset_id, bq_table_id):
    ''' 
    BigQuery Streaming Insert - Insert python list into BQ
    '''
    
    # Note: The table must already exist and have a defined schema
    # rows_to_insert is a list of variables (i.e. (id, date, value1, value2, etc.))
    client    = bigquery.Client()
    table_ref = client.dataset(bq_dataset_id).table(bq_table_id)
    table     = client.get_table(table_ref)
    errors    = client.insert_rows(table, rows_to_insert)
    if errors == []:
        print('[ Success ] {} Streaming Insert into BigQuery Complete'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))
    else:
        print('[ WARNING ] {} Issue inserting into BigQuery'.format(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')))


def kafka_consumer_to_bigquery(args):
    
    stop_event = multiprocessing.Event()
    
    # https://kafka-python.readthedocs.io/en/master/apidoc/kafka.html#kafka.KafkaConsumer
    consumer = KafkaConsumer(bootstrap_servers=args['bootstrap_servers'], auto_offset_reset='latest', consumer_timeout_ms=1000)
    
    consumer.subscribe([args['kafka_topic']])
    
    # Initialize Rows
    rows_to_insert = []
    
    while not stop_event.is_set():
        for i, message in enumerate(consumer):
            
            if (i % args['bulk_load_count'])!=0:
                rows_to_insert.append( json.loads(message.value) )
            else:
                rows_to_insert.append( json.loads(message.value) )
                bg_streaming_insert(rows_to_insert, args['bq_dataset_id'], args['bq_table_id'])
                # Reset rows
                rows_to_insert = []
            
            if stop_event.is_set():
                break
    
    consumer.close()


#####################################################################
#
#   Main
#
#####################################################################

if __name__ == "__main__":
    
    # ONLY used for TESTING - Example Arguments
    '''
    args =  {
        'bootstrap_servers' : 'kafka-server1-vm:9092',
        'kafka_topic'       : 'topicz1',
        'bq_dataset_id'     : 'kafka_ds',
        'bq_table_id'       : 'kafka_table1',
        'bulk_load_count'   : 1000
        }
    '''
    
    # Arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("--bootstrap_servers",  required=True,  help="Kafka Bootstrap Server(s)")
    ap.add_argument("--kafka_topic",        required=True,  help="Kafka Topic Name")
    ap.add_argument("--bq_dataset_id",      required=True,  help="Google BigQuery Dataset ID")
    ap.add_argument("--bq_table_id",        required=True,  help="Google BigQuery Table ID")
    ap.add_argument("--bulk_load_count",    required=False, default=1000, help="Bulk Load Count")
    args = vars(ap.parse_args())
    
    # Kafka Consumer to BigQuery
    kafka_consumer_to_bigquery(args)



#ZEND
