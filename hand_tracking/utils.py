from collections.abc import Iterable

from json import dumps
from kafka import KafkaProducer

import json
from datetime import datetime


def count_None(iterable):
    assert isinstance(iterable, Iterable), "Input must be an iterable"

    count = 0

    for x in iterable:
        if isinstance(x, type(None)):
            count += 1

    return count

def convert_path_id_2_json(path_and_id):
    assert isinstance(iterable, Iterable), "Input must be an iterable"

def create_json_message( 
      event_type, 
      object_position,
      probability,
      object_id,
      object_type
      ):
    """
    Sample Message format
    {
    "timestamp": 1600953683.2281373,
    "event_type": "object-out",
    "object_info": {
        "position": "left",
        "probability": 0.7006784439086914,
        "object_id": "Not valid",
        "object_type": "peanuts"
    }
    }
    """

    now = datetime.now()

    timestamp = datetime.timestamp(now)

    message = {
        "timestamp" : timestamp,
        "event_type": event_type,
        "object_info": 
        {
            "position": object_position,
            "probability": probability,
            "object_id": object_id,
            "object_type": object_type
        }
    }
    
    # write it to a file
    save_json_message(message)

    return message

def save_json_message(message):
    assert isinstance(message, dict), "Message must be a dict"
    
    with open("data/"+str(message["timestamp"])+'.json', 'w', encoding='utf-8') as f:
        json.dump(message, f, ensure_ascii=False, indent=4)

    return 


class KafkaClient(object):
    def __init__(self, bootstrap_servers_address='localhost:9092'):
        self.producer = KafkaProducer(bootstrap_servers=[bootstrap_servers_address],
                        value_serializer=lambda x: 
                        dumps(x).encode('utf-8'))

    def publish(self, topic_name, data):
        assert isinstance(topic_name, str), "Topic name must be a string"
        assert isinstance(data, dict), "Data must be a dict"

        self.producer.send(topic_name, value=data)


