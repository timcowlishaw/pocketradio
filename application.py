from flask import Flask, Response
from flask_cors import CORS
import requests
import os
import random


app = Flask(__name__)
CORS(app)

@app.route('/')
def get_podcast_files():
    token = get_token(os.environ["POCKETCASTS_USERNAME"], os.environ["POCKETCASTS_PASSWORD"])
    podcasts = get_podcasts(token)
    random.shuffle(podcasts)
    urls = [get_unlistened_podcast_episode_url(token, p["uuid"]) for p in podcasts[0:100]]
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
	return random.choice(unlistened_urls)

if __name__ == "__main__":
    app.run()


