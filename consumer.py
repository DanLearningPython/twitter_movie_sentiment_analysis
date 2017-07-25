from kafka import KafkaConsumer
from predict import Predict


class Consumer:

    daemon = True

    def __init__(self):
        self.consumer = KafkaConsumer(bootstrap_servers='192.168.26.152:9092',auto_offset_reset='earliest')
        self.predict = Predict()

    def subscribe(self, tag='test'):
        self.consumer.subscribe([tag])

        for message in self.consumer:
            topic = message.topic
            timestamp = message.timestamp
            value = message.value
            print(value)
            prepared_tweets = self.predict.prepare([str(value)])
            if prepared_tweets is None:
                print("Error")
            else:
                print(self.predict.classify(prepared_tweets))
                #tweet = self.predict.clean_tweets(value)
                #print(tweet)

#tweets = list(['Congratulations to the cast and crew of @dunkirkmovie. The film has received the #criticschoice seal of distinction. #dunkirk #DunkirkMovie', 'Yes great movie here.'])
#prepared_tweets = predict.prepare(tweets)
#print(predict.classify(prepared_tweets))

consumer = Consumer()
consumer.subscribe()