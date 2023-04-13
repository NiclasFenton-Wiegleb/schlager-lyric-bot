import pandas as pd
import requests
import json

class DataExtractor:

    def __init__(self) -> None:
        pass

    def retrieve_playlist_content(self, playlist_id):
        url = "https://spotify-scraper.p.rapidapi.com/v1/playlist/contents"

        querystring = {"playlistId":f"{playlist_id}"}

        headers = {
            "X-RapidAPI-Key": "9326ac5334mshc91f7d388f4fdc4p1cd407jsn5811a52d1ae0",
            "X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        playlist_content = response.json()

        with open(f"{playlist_id}_content.json", "w") as f:
            json.dump(playlist_content, f)
        


#extractor = DataExtractor()

playlist_id = "2dCNbxILFEJnnEb8h6L4eV"

#playlist = extractor.retrieve_playlist_content(playlist_id)


f = open(f"{playlist_id}_content.json")

playlist_content = json.load(f)

playlist_song_ids = [x["id"] for x in playlist_content["contents"]["items"]]

print(playlist_song_ids)

#for x in playlist_content:
    #playlist_song_ids.append()



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