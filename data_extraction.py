import pandas as pd
import requests
import json

class DataExtractor:

    def __init__(self) -> None:
        pass

    def retrieve_playlist_content(self, playlist_id):

        #API request to retrieve playlist data
        url = "https://spotify-scraper.p.rapidapi.com/v1/playlist/contents"

        querystring = {"playlistId":f"{playlist_id}"}

        headers = {
            "X-RapidAPI-Key": "9326ac5334mshc91f7d388f4fdc4p1cd407jsn5811a52d1ae0",
            "X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)

        #Save playlist content as json file
        playlist_content = response.json()

        with open(f"{playlist_id}_content.json", "w") as f:
            json.dump(playlist_content, f)
        
    def playlist_to_song_data(self, playlist_id):
        #Note: retrieve_playlist_content() method needs to be run beforehand

        #Open json file with playlist content
        f = open(f"{playlist_id}_content.json")

        playlist_content = json.load(f)

        #Extract relevant song info from playlist content
        url = [x["shareUrl"] for x in playlist_content["contents"]["items"]]
        song_name = [x["name"] for x in playlist_content["contents"]["items"]]
        song_id = [x["id"] for x in playlist_content["contents"]["items"]]
        release_year = [x["album"]["date"] for x in playlist_content["contents"]["items"]]

        #Convert song data to dataframe
        song_dict = {"url": url,
                    "title": song_name,
                    "spotify_id": song_id,
                    "release_year": release_year}

        df = pd.DataFrame(song_dict)
        return df
        


extractor = DataExtractor()

playlist_id = "6R41RrIjNVNVvPGziXs9F8" 

#playlist = extractor.retrieve_playlist_content(playlist_id)

df = extractor.playlist_to_song_data(playlist_id)

#df.to_csv("schlager_songs.csv", mode= "a", index= False, header= False)

songs = pd.read_csv("schlager_songs.csv")

songs.drop_duplicates(inplace= True)
print(songs)
print(songs.info())



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