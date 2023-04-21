import requests
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup
from ratelimit import limits, sleep_and_retry
import config


class DataExtractor:

    @classmethod
    def clean_song_data(cls, csv_file):

        #Open csv file and drop duplicates
        df = pd.read_csv(f"{csv_file}")
        df.drop_duplicates(inplace= True)

        #Add empty columns to be completed with data later
        artist_name = [None for x in enumerate(df["title"])]
        lyrics = [None for x in enumerate(df["title"])]

        df["artist_name"] = artist_name
        df["lyrics"] = lyrics

        #Overwrite existing file with updated one
        df.to_csv(f"{csv_file}", mode= "w")

        return df

    @classmethod
    def retrieve_artist(cls, csv_file):

        #Establishing connection to Spotify API
        cid = "ed9e37ea51574c2b9bd6e4809e185d7a"
        secret = config.spotify_secret

        client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
        sp = spotipy.Spotify(client_credentials_manager = client_credentials_manager)

        #Get artist name based on song id and add to dataframe
        df = pd.read_csv(f"{csv_file}")


        for x in df["spotify_id"]:
            song_data = sp.track(x)
            artist_data = song_data["artists"]
            for y in artist_data:
                artist = y["name"]
                row = df[df["spotify_id"] == x]
                df["artist_name"][row.index] = artist
                print(artist)

        
        #Overwrite existing file with updated one
        df.to_csv(f"{csv_file}", mode= "w")

        return df
    
    @classmethod
    def scrape_lyrics(cls, artist, title):

        #format artist and title and retrieve lyrics from genius.com
        artist2 = str(artist.replace(' ','-')) if ' ' in artist else str(artist)
        title2 = str(title.replace(' ','-')) if ' ' in title else str(title)
        page = requests.get('https://genius.com/'+ artist2 + '-' + title2 + '-' + 'lyrics')
        html = BeautifulSoup(page.text, 'html.parser')
        lyrics1 = html.find("div", class_="lyrics")
        lyrics2 = html.find("div", class_="Lyrics__Container-sc-1ynbvzw-2 jgQsqn")
        if lyrics1:
            lyrics = lyrics1.get_text()
        elif lyrics2:
            lyrics = lyrics2.get_text()
        elif lyrics1 == lyrics2 == None:
            lyrics = None

        return lyrics

    @classmethod
    @sleep_and_retry
    @limits(calls= 1, period= 2)
    def rapidapi_spotify_lyrics(cls, song_id):
        
        #API request to retrieve playlist data
        url = "https://spotify-scraper.p.rapidapi.com/v1/track/lyrics"

        querystring = {"trackId":f"{song_id}"}

        headers = {
            "X-RapidAPI-Key": config.lyrics_api_key,
            "X-RapidAPI-Host": "spotify-scraper.p.rapidapi.com"
        }

        response = requests.request("GET", url, headers=headers, params=querystring)
        
        try:
            #Try extracting lyrics from song data and save it as
            #.txt file
            song_lyrics = response.text

            save_path = "./lyrics_text"
        
            with open(f"{save_path}/{song_id}_lyrics.txt", "w") as f:
                    f.write(f"{song_lyrics}")
            
            return song_lyrics
        
        except:
            #Print response code if there is an error with the API
            print(response.status_code)

        

if __name__ == "__main__":

    df = pd.read_csv("schlager_songs.csv")

    df_empty = df[df["lyrics"].isnull() == True]

    for x in df_empty["spotify_id"]:
        lyrics = DataExtractor.rapidapi_spotify_lyrics(x)
        print(x)
