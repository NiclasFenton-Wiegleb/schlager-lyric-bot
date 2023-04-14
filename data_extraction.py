import pandas as pd
import requests
import json

class DataExtractor:

    @classmethod
    def retrieve_playlist_content(cls, playlist_id):

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
    
    @classmethod
    def playlist_to_song_data(cls, playlist_id):
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
    
    @classmethod
    def retrieve_song_lyrics(cls, song_id):
        
        #API request to retrieve playlist data
        url = "https://spotify-scraper.p.rapidapi.com/v1/genre/contents"

        querystring = {"genreId":"0JQ5DAqbMKFGvOw3O4nLAf"}

        headers = {
            "X-RapidAPI-Key": "9326ac5334mshc91f7d388f4fdc4p1cd407jsn5811a52d1ae0",
            "X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        
        try:
            #Try extracting lyrics from song data and save it as
            #.txt file
            song_data = response.json()

            song_lyrics = []

            for x in song_data:
                song_lyrics.append(x["text"])
            
            with open(f"{song_id}_lyrics.txt", "w") as f:
                for line in song_lyrics:
                    f.write(f"{line}\n")
            
            print(song_lyrics)
        
        except:
            #Print response code if there is an error with the API
            print(response.status_code)

        

if __name__ == "__main__":

    #Initialise DataExtractor
    extractor = DataExtractor()

    playlist_id = "6R41RrIjNVNVvPGziXs9F8"

    #Get playlist content using API
    playlist = extractor.retrieve_playlist_content(playlist_id)

    try:
        #Try extracting song data
        df = extractor.playlist_to_song_data(playlist_id)

        df.to_csv("schlager_songs.csv", mode= "a", index= False, header= False)

        songs = pd.read_csv("schlager_songs.csv")

        songs.drop_duplicates(inplace= True)
        print(songs)
        print(songs.info())

    except:
        #Print playlist data if relevant song data can't
        #be extracted
        file = open(f"{playlist_id}_content.json")
        file_content = json.load(file)
        print(file_content)
    