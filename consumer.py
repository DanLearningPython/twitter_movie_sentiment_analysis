from kafka import KafkaConsumer
from predict import Predict
from config import *
import json
import pymongo


class Consumer:

    daemon = True

    def __init__(self):
        self.consumer = KafkaConsumer(bootstrap_servers=kafka_host, auto_offset_reset='earliest')
        self.predict = Predict()
        self.mongo_client = pymongo.MongoClient("mongodb://"+mongo_host)
        self.mongo_db = self.mongo_client.twitter

    def subscribe(self, tag='test'):
        self.consumer.subscribe([tag])

        for message in self.consumer:
            value = message.value
            prepared_tweets = self.predict.prepare([str(value)])
            if prepared_tweets is None:
                print("Error")
            else:
                result = self.get_result(message)
                sentiment = self.predict.classify(prepared_tweets)
                result['sentiment'] = sentiment[0]
                db_result = self.save_result_to_db(result)
                print(db_result)
                print(result)

    def get_result(self, message):
        result = {}
        result['topic'] = message.topic
        result['tweet'] = message.value.decode('utf-8') #convert byte to string
        result['checksum'] = message.checksum
        result['timestamp'] = message.timestamp

        return result

    def save_result_to_db(self, result):
        try:
            db_result = self.mongo_db.movies.insert_one(result)
            return db_result
        except pymongo.errors.DuplicateKeyError:
            return None

    def save_result_to_file(self, result):
        file_name = result['topic']+".txt"
        with open(file_name, 'w') as f:
            json.dump(result, f, ensure_ascii=True)

consumer = Consumer()
consumer.subscribe()