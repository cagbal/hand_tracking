from collections.abc import Iterable

from json import dumps
from kafka import KafkaProducer


def count_None(iterable):
    assert isinstance(iterable, Iterable), "Input must be an iterable"

    count = 0

    for x in iterable:
        if isinstance(x, type(None)):
            count += 1

    return count

def convert_path_id_2_json(path_and_id):
    assert isinstance(iterable, Iterable), "Input must be an iterable"


class KafkaClient(object):
    def __init__(self, bootstrap_servers_address='localhost:9092'):
        self.producer = KafkaProducer(bootstrap_servers=[bootstrap_servers_address],
                        value_serializer=lambda x: 
                        dumps(x).encode('utf-8'))

    def publish(self, topic_name, data):
        assert isinstance(topic_name, str), "Topic name must be a string"
        assert isinstance(data, dict), "Data must be a dict"

        self.producer.send('numtest', value=data)


