#!/usr/bin/env python

from flask import Flask, Response
from flask_cors import CORS
import requests
import os
import random
import json

app = Flask(__name__)
CORS(app)

N_PODCASTS = 20
N_STARRED = 10

@app.route('/')
def get_podcast_files():
    token = get_token(os.environ["POCKETCASTS_USERNAME"], os.environ["POCKETCASTS_PASSWORD"])
    starred_eps = get_starred_episodes(token)
    random.shuffle(starred_eps)
    starred_eps = starred_eps[0:N_STARRED]
    podcasts = get_podcasts(token)
    random.shuffle(podcasts)
    urls = [ep["url"] for ep in starred_eps] + [get_unlistened_podcast_episode_url(token, p["uuid"]) for p in podcasts[0:N_PODCASTS]]
    random.shuffle(urls)
    return Response(("\n").join(urls), mimetype="audio/x-mpegurl")


def get_token(username, password):
    response = requests.post("https://api.pocketcasts.com/user/login", json={
        "email": username,
        "password": password,
        "scope": "webplayer"
    }, headers={
        "Accept": "application/json"
    })
    return response.json()["token"]

def get_podcasts(token):
    response = requests.post("https://api.pocketcasts.com/user/podcast/list", json={
        "v": 1
    }, headers={
        "Authorization": "Bearer %s" % token,
        "Accept": "application/json"
    })
    return response.json()["podcasts"]

def get_starred_episodes(token):
    response = requests.post("https://api.pocketcasts.com/user/starred", json={
        "v": 1
    }, headers={
        "Authorization": "Bearer %s" % token,
        "Accept": "application/json"
    })
    return response.json()["episodes"]

def get_unlistened_podcast_episode_url(token, uuid):
    cache_response = requests.get("https://cache.pocketcasts.com/podcast/full/%s/0/3/1000" % uuid, headers={
        "Authorization": "Bearer %s" % token,
        "Accept": "application/json"
    })
    api_response = requests.post("https://api.pocketcasts.com/user/podcast/episodes", json={
        "uuid": uuid
    }, headers={
        "Authorization": "Bearer %s" % token,
        "Accept": "application/json"
    })
    listened_uuids = set(e["uuid"] for e in api_response.json()["episodes"] if e["playingStatus"] != 0 and e["playedUpTo"] > 0)
    unlistened_urls = [e["url"] for e in cache_response.json()["podcast"]["episodes"] if e["uuid"] not in listened_uuids]
    return unlistened_urls[0]

if __name__ == "__main__":
    app.run()


