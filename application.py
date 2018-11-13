from flask import Flask, Response
from pocketcasts import Pocketcasts
import os
import random


app = Flask(__name__)

@app.route('/')
def get_podcast_files():
    pocketcasts = Pocketcasts(os.environ["POCKETCASTS_USERNAME"], password=os.environ["POCKETCASTS_PASSWORD"])
    podcasts = [e.url for p in pocketcasts.get_subscribed_podcasts() for e in pocketcasts.get_podcast_episodes(p)]
    random.shuffle(podcasts)
    return Response(("\n").join(podcasts), mimetype="audio/x-mpegurl")

if __name__ == "__main__":
    app.run()

