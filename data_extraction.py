import pandas as pd
import requests
import json

class DataExtractor:

    def __init__(self) -> None:
        pass

    #def retrieve_genre_content(self, api_url, genre_id, api_headers):

f = open("lyrics.json")

lyrics = json.load(f)

for x in lyrics:
    print(x["text"])



'''
url = "https://spotify-scraper.p.rapidapi.com/v1/genre/contents"

querystring = {"genreId":"0JQ5DAqbMKFGvOw3O4nLAf"}

headers = {
	"X-RapidAPI-Key": "9326ac5334mshc91f7d388f4fdc4p1cd407jsn5811a52d1ae0",
	"X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

print(response.text)
'''
''''
url = "https://spotify-scraper.p.rapidapi.com/v1/track/lyrics"

querystring = {"trackId":"1cSXzDZt8vzuUp2XREQEJN","format":"json"}

headers = {
	"X-RapidAPI-Key": "9326ac5334mshc91f7d388f4fdc4p1cd407jsn5811a52d1ae0",
	"X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
}

response = requests.request("GET", url, headers=headers, params=querystring)

lyrics = response.json()

with open('lyrics.json', 'w') as f:
    json.dump(lyrics, f)
    '''