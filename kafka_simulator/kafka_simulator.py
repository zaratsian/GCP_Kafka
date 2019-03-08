
#####################################################################
#
#   Data Simulator for Apache Kafka
#
#   USAGE:
#   kafka_simulator.py --bootstrap_servers localhost:9092 --kafka_topic dztopic1 --time_delay 1 --send_to_kafka 0
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


def simulate_payload():
    
    datetimestamp = datetime.datetime.now()
    pupil_x_angle = random.randint(-90,90)
    pupil_y_angle = random.randint(-90,90)
    pupil_size    = round(random.triangular(1,3,9),2)
    
    payload = {
        'id':           datetimestamp.strftime('%Y%m%d%H%M%S%f'),
        'date':         datetimestamp.strftime('%Y-%m-%d'),
        'timestamp':    datetimestamp.strftime('%H:%M:%S.%f'),
        'leye_x_angle': pupil_x_angle,
        'leye_y_angle': pupil_y_angle,
        'leye_size_mm': pupil_size,
        'reye_x_angle': pupil_x_angle if random.random()<=0.95 else random.randint(-90,90),
        'reye_y_angle': pupil_y_angle if random.random()<=0.95 else random.randint(-90,90),
        'reye_size_mm': pupil_size if random.random()<=0.95 else random.triangular(1,3,9),
        'heart_rate':   int(random.triangular(35,70,175)),
        'blink':        random.randint(0,1)
    }
    
    return payload



if __name__ == "__main__":
    
    # ONLY used for TESTING - Example Arguments
    '''
    args =  {
                "bootstrap_servers": "localhost:9092",
                "kafka_topic":       "dztopic1",
                "time_delay":        1,
                "send_to_kafka":     0
            }
    '''
    
    # Arguments
    ap = argparse.ArgumentParser()
    ap.add_argument("--bootstrap_servers",  required=True,  default='localhost:9092',   help="Apache Kafka Bootstrap Servers")
    ap.add_argument("--kafka_topic",        required=True,                              help="Apache Kafka Topic Name")
    ap.add_argument("--time_delay",         required=False, default=1, type=int,        help="Time delay inbetween simulations (seconds)")
    ap.add_argument("--send_to_kafka",      required=False, default=0, type=int,        help="Send to Kafka (1) or send to console (0)")
    args = vars(ap.parse_args())
    
    try:
        # Setup Kafka Producer
        #producer= KafkaProducer(bootstrap_servers=args['bootstrap_servers'])                                                               # String-based Producer
        producer = KafkaProducer(bootstrap_servers=args['bootstrap_servers'], value_serializer=lambda v: json.dumps(v).encode('utf-8'))     # JSON-based Producer
    except Exception as e:
        print('[ EXCEPTION ] At Kafka Producer Setup - {}'.format(e))
    
    counter = 0
    while True:
        
        counter += 1
        
        payload = simulate_payload()
        
        if args['send_to_kafka']==1:
            try:
                #producer.send(kafka_topic, 'test message {}'.format(counter).encode('utf-8') )     # String-based kafka commit
                producer.send(args['kafka_topic'], value=payload)                                   # JSON-based kafka commit
            except Exception as e:
                print('[ EXCEPTION ] At Kafka Producer Send - {}'.format(e))
        
        print(payload)
        print('\n')
        
        time.sleep(args['time_delay'])



#ZEND
