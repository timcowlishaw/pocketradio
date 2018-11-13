from flask import Flask
from pocketcasts import Pocketcasts
import os
import random
app = Flask(__name__)
pocket = Pocketcasts(os.environ["POCKETCASTS_USERNAME"], password=os.environ["POCKETCASTS_PASSWORD"])
@app.route('/')
def get_podcast_files():
    return 
# A very simple Flask Hello World app for you to get started with...

from flask import Flask

app = Flask(__name__)

@app.route('/')
def hello_world():
    podcasts = [e.url for p in pocketcasts.get_subscribed_podcasts() for e in pocketcasts.get_podcast_episodes(p)]
    random.shuffle(podcasts)
    return ("\n").join(podcasts)


