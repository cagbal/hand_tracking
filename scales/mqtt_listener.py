import paho.mqtt.client as mqtt

import time

import json

TOPIC = "/scales/tablet/data"

class Scale(object):
    def __init__(self, ip = "192.168.1.10", port = 1883):
        self.client = mqtt.Client()
        self.ip = ip
        self.port = port 

        self.messages = []
    
    def connect(self):
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect_async(self.ip, self.port)
    
    def on_connect(self, client, userdata, flags, rc):
        print("Connected with result code "+str(rc))

        client.subscribe(TOPIC)

    def on_message(self, client, userdata, msg):
        print(msg.topic+" "+str(msg.payload))

        content = json.loads(msg.payload.decode('utf-8'))

        self.messages.append(content)

    def run_async(self):
        self.client.loop_start()

    def get_last_message(self):
        if len(self.messages) < 1:
            print("No messages received")
            return None 
        return self.messages[-1]

if __name__ == "__main__":
    #Example usage
    scale = Scale() 
    scale.connect()
    scale.run_async()
    
    #showing that it is not blocking anything
    while True:
        print("****")
        msg = scale.get_last_message()
        print("+++++", msg)
        time.sleep(1)