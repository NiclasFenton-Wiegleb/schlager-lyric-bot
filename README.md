# schlager-lyric-bot

This project sets out to fine-tune an LLM that can generate lyrics to Schlager songs (a genre of music popular in German speaking countries) based on a verse as input.

Technologies:

- Transformers
- QLorA
- PyTorch
- Python
- API
- Pandas

## Data Collection

To effectively fine-tune an LLM, we first need to build a dataset to train on. In this case, as the resulting model is supposed to generate lyrics to Schlager songs, retrieving and storing lyrics for existing Schlager songs is a good place to start.

Using Spotify's own API the playlist_data_extraction.py retrieves the metadata for a playlist, by providing the corresponding song ID. These can easily be obtained by searching for Schlager playlists on the Spotify app itself. The data is stored in JSON files (see schlager_playlist_data folder). We can then create a CSV file the stores the relevant song data, including url, artist, title and Spotify id - this is done using the `playlist_to_song_data` method.

The `song_lyrics_extraction.py` script uses a Spotify scraper from RapidAPI to retrieve the lyrics text for each song in the schlager_songs.csv file based on the Spotify ID. the lyrics are added to the `schlager_songs_v2.csv` file.

Finally, the `text_data_cleaning.py` script cleans and saves the lyrics text data that can easily be loaded into a dataframe.

## Training Baseline Model

Initially, we need to fine-tune a baseline model against which future models can be measured. This is covered in the `Baseline_Schlager_bot.ipynb` notebook.

Base model: 
malteos/bloom-1b5-clp-german

## Training 7b Model

To build on the baseline model, we now try to beat it by fine-tuning another version on a more powerful 7b Llama 2 model already fine-tuned for German language use. This also uses QLorA methods to allow for the more efficient use of resources during training. This is documented in `7b_Schlager_bot.ipynb` notebook.

Base model:
LeoLM/leo-hessianai-7b

## Text Generation

To use the 7b model, please access the corresponding app in this huggingface space: https://huggingface.co/spaces/niclasfw/schlager-bot-4

## Sources

- Schlager song lyrics: Spotify
- Baseline model: https://huggingface.co/docs/peft/task_guides/clm-prompt-tuning
- 7b model: https://www.philschmid.de/instruction-tune-llama-2
