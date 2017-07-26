from kafka import KafkaConsumer
from predict import Predict
from config import *
import json

class Consumer:

    daemon = True

    def __init__(self):
        self.consumer = KafkaConsumer(bootstrap_servers=host, auto_offset_reset='earliest')
        self.predict = Predict()

    def subscribe(self, tag='test'):
        self.consumer.subscribe([tag])

        for message in self.consumer:
            value = message.value
            print(value)
            prepared_tweets = self.predict.prepare([str(value)])
            if prepared_tweets is None:
                print("Error")
            else:
                result = self.get_result(message)
                sentiment = self.predict.classify(prepared_tweets)
                result['sentiment'] = sentiment
                print(result)
                #self.save_result(result)
                #print(sentiment)

    def get_result(self, message):
        results = {}
        results['topic'] = message.topic
        results['timestamp'] = message.timestamp
        results['tweet'] = message.value

        return results

    def save_result(self, result):
        file_name = result.topic+".txt"
        with open(file_name, 'w') as f:
            json.dump(result, f, ensure_ascii=True)

consumer = Consumer()
consumer.subscribe()