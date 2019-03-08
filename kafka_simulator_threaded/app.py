
#####################################################################
#
#   Data Simulator for Apache Kafka
#
#   Deployed as a container (scaled with Kubernetes, GKE)
#
#   Test with python 3.7
#   https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
#
#   Prereqs:
#   pip install kafka-python
#
#####################################################################


from kafka import KafkaProducer
import json
import re
import datetime, time
import random
import argparse
import threading
import params


def simulate_payload():
    
    datetimestamp = datetime.datetime.now()
    
    payload = {
        'id':           datetimestamp.strftime('%Y%m%d%H%M%S%f'),
        'datetimestamp':datetimestamp.strftime('%Y-%m-%d %H:%M:%S.%f'),
        'heart_rate':   int(random.triangular(35,70,175))
    }
    
    return payload



def initialize_kafka_producer(params):
    try:
        producer = KafkaProducer(bootstrap_servers=params['bootstrap_servers'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))     # JSON-based Producer
    except Exception as e:
        print('[ EXCEPTION ] Could not connect to Kafka bootstrap server - {}'.format(e))
    
    return producer



def publish_kafka_event(params, producer, counter):
    
    while True:
        
        payload = simulate_payload()
        payload['counter'] = counter
        
        if params['send_to_kafka']==1:
            try:
                producer.send(params['kafka_topic'], value=payload)   # JSON-based kafka commit
            except Exception as e:
                print('[ EXCEPTION ] Failure sending JSON payload to Kafka producer - {}'.format(e))
        else:
            print('{}\n'.format(payload))
        
        time.sleep(params['time_delay'])



if __name__ == "__main__":
    
    params = {
        'bootstrap_servers'   : '35.184.69.2:9092',
        'send_to_kafka'       : 1,
        'kafka_topic'         : 'eye_tracking',
        'time_delay'          : 5,
        'number_of_threads'   : 100
    }
    
    producer = initialize_kafka_producer(params)
    
    threads = []
    for i in range(params['number_of_threads']):
        threads.append(threading.Thread(target=publish_kafka_event, args=(params, producer, i,)))
    
    for thread in threads:
        thread.start()



#ZEND
