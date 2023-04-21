import pandas as pd

class DataCleaner:

    @classmethod
    def open_text_data(cls, song_id):

        try:
            #Open .txt file containing the lyrics corresponding to the song_id
            save_path = "./lyrics_text"
            
            with open(f"{save_path}/{song_id}_lyrics.txt", "r") as f:
                    lyrics_text = f.read()
            
            if lyrics_text == '{"status":false,"reason":"Lyrics not found."}':
                 
                return None
            else:
                 
                return lyrics_text
        
        except:
             pass
        
    @classmethod
    def remove_square_brackets(cls, string):
        #remove brackets from string or continue in case of an error (e.g. string == NoneType)
        try:
            new_string = string.replace('[', '').replace(']', ' ')
            return new_string
        
        except:
            pass
        
    @classmethod
    def clean_lyrics_data(cls, dataframe):
         
        df = dataframe
         #Take the dataframe and clean the data
         #Dropping unnecessary columns
        try:
            df.drop("Unnamed: 0.1", axis= 1, inplace= True)
        except:
            pass
        
        try:
            df.drop("Unnamed: 0", axis= 1, inplace= True)
        except:
            pass

        # Drop unnecessary substrings
        df["lyrics"] = df["lyrics"].str.replace("[\d\d:\d\d.\d\d]", "", regex= True)
        df["lyrics"] = df["lyrics"].apply(lambda x: DataCleaner.remove_square_brackets(x))

        return df
    
    @classmethod
    def df_to_txt(cls, dataframe):
        df = dataframe

        #Extract clean lyrics from data frame and save as .txt
        for lyrics in df["lyrics"]:
            try:
                row = df[df["lyrics"] == lyrics]
                song_id = df["spotify_id"][row.index]
                save_path = "./lyrics"
                
                if lyrics != None:
                    with open(f"{save_path}/{song_id}_lyrics.txt", "w") as f:
                            f.write(f"{lyrics}")
                    print(song_id)
                else:
                    continue
            except:
                continue


if __name__ == "__main__":

    df = pd.read_csv("schlager_songs.csv")

    # for x in df["spotify_id"]:
    #     lyrics = DataCleaner.open_text_data(x)
    #     lyrics_ls.append(lyrics)

    # df = DataCleaner.clean_lyrics_data(df)

    # df.to_csv("schlager_songs.csv", mode= "w")

    DataCleaner.df_to_txt(df)


 

