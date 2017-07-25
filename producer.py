import threading, time

from kafka import KafkaProducer


class Producer(threading.Thread):

    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='192.168.26.152:9092')

    def send_message(self, topic, message):
        self.producer.send(topic,message.encode('utf-8'))
        print("Sent - "+message)
        time.sleep(.1)