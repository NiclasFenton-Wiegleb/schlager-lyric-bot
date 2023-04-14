import requests


class DataExtractor:

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