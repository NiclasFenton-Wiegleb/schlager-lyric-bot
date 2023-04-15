import requests
import pandas as pd
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from bs4 import BeautifulSoup


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
        secret = "72d7869f54354d1382c568c80d7f3948"

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
    def scrape_lyrics(artist, title):

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

    #test = DataExtractor.clean_song_data("schlager_songs copy.csv")
    # df = DataExtractor.retrieve_artist("schlager_songs.csv")
    df = pd.read_csv("schlager_songs.csv")

    for x in range(10):
        artist = df["artist_name"][x]
        title = df["title"][x]
        lyrics = DataExtractor.scrape_lyrics(artist, title)
        df["lyrics"][x] = lyrics
        print(lyrics)


    print(df)
    print(df.info())