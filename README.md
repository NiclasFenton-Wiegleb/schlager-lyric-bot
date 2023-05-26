# **WIP**

# schlager-lyric-bot

Technologies:

- Transformers
- PyTorch
- Python
- API
- Pandas

## Milestone 1 - Collecting the Dataset

To create a good ML model, we first need to build a database to train the algorithm. In this case, as the resulting model is supposed to generate lyrics to Schlager songs, retrieving and storing lyrics for existing Schlager songs is a good place to start.

Using Spotify's own API the playlist_data_extraction.py retrieves the metadata for a playlist, by providing the corresponding id. These can easily be obtained by searching for Schlager playlists on the Spotify app itself. The data is stored in JSON files (see schlager_playlist_data folder). We can then create a CSV file the stores the relevant song data, including url, artist, title and Spotify id - this is done using the playlist_to_song_data method.

Once this is done, the song_lyrics_extraction.py script uses a Spotify scraper from RapidAPI to retrieve the lyrics text for each song in the schlager_songs.csv file based on the Spotify id. the lyrics are added to the CSV file and also stored as .txt files in a specified directory.

Finally, the text_data_cleaning.py script cleans the lyrics text data and saves it in its clean form. To enrich the dataset and give the model a better understanding of german vocabulary and grammar, a chunk of text data is added from a general dataset used for NLP model training and available online (see source below).

## Milestone 2 - Training the Model

## Milestone 3 - Text Generation


## Sources

- General German language dataset: https://github.com/German-NLP-Group/german-transformer-training

- Schlager song lyrics: Spotify

- run_lungauage_modeling.py script for training NLP model from scratch: https://github.com/huggingface/transformers/blob/main/examples/legacy/run_language_modeling.py
