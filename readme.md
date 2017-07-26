# Movie sentiment classifier - WIP

Application takes in streaming Twitter data, cleans it, then feeds it into Kafka through producer.py.
Then, consumer.py ingests the streaming data and runs it through the sentiment classifier. Finally, the result is saved
in mongodb to be served through a RESTful interface (other project - Flask)

Classifier - random forest with bag of words.

1. Ensure both Kafka server and Zookeeper are running
2. Start the kafka consumer
~~~
python kafka/consumer.py
~~~
3. Start the Twitter stream
~~~
python kafka/TwitterStream.py
~~~

Mongo - setup (todo)
~~~
db.movies.createIndex( { "checksum": 1 }, { unique: true } )
~~~

Output format (sentiment: [negative, positive]):
~~~
{'topic': 'test', 'tweet': "Wow, this is the worst movie I've ever seen.", 'checksum': -459854744, 'timestamp': 1501095796914, 'sentiment': [0.91, 0.09], '_id': ObjectId('5978e7768048f877a9c56bbf')}
~~~