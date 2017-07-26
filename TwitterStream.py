from tweepy import OAuthHandler
from tweepy import Stream
from tweepy.streaming import StreamListener

from TextProcessor import TextProcessor
from config import *
from kafka.producer import Producer


class StdOutListener(StreamListener):
    """ A listener handles tweets that are received from the stream.
    This is a basic listener that just prints received tweets to stdout.
    """

    def on_status(self, data):
        text = data.text
        text = TextProcessor.clean(text)
        if len(text) > 0:
            print(text)
            producer.send_message('test',text)
        return True

    def on_error(self, status):
        print(status)

if __name__ == '__main__':
    listener = StdOutListener()
    auth = OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)
    producer = Producer()
    TextProcessor = TextProcessor()
    stream = Stream(auth, listener)
    stream.filter(track=['valerian'])
