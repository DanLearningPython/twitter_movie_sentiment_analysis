import threading, time
from config import *
from kafka import KafkaProducer


class Producer(threading.Thread):

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers=host)

    def send_message(self, topic, message):
        self.producer.send(topic,message.encode('utf-8'))
        print("Sent - "+message)
        time.sleep(.1)