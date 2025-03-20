import os
from dotenv import load_dotenv
from supabase import create_client, Client
from colorama import Fore, init
import yt_dlp as youtube_dl
import re

load_dotenv()
init(autoreset=True)

supabase_url: str = os.environ.get("SUPABASE_URL")
supabase_key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(supabase_url, supabase_key)

DOWNLOAD_FOLDER = "temp_downloads/audio"
os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)

def add_music_to_supabase(song: str, artist: str, url: str, color: str):
    data = {
        "song_name": song,
        "artist_name": artist,
        "url": url,
        "color": f"#{color}",
        "download_audio": True,
        "crop_image": True
    }
    try:
        response = supabase.table("song_info").insert(data).execute()
        if response.data:
            print(f'{Fore.GREEN}✅ Added song "{song}" by {artist} to Supabase.')
        else:
            print(f'{Fore.YELLOW}⚠️ Failed to add song "{song}" by {artist}". Response: {response}')
    except Exception as e:
        print(f'{Fore.RED}❌ Error adding song "{song}" by {artist}: {str(e)}')


def fetch_songs_to_download():
    response = (
        supabase.table("song_info")
        .select("song_name, artist_name, url, download_audio")
        .or_("download_audio.eq.true")
        .execute()
    )

    if not response.data:
        print(f"{Fore.GREEN}✅ No songs need downloading.")
        return []

    song_download_queue = response.data
    print(f"{Fore.BLUE}🎧 Found {len(response.data)} song(s) to download.")

    for index, song in enumerate(song_download_queue, start=1):
        print(f"{Fore.CYAN}{index}. {song['song_name']} by {song['artist_name']}")

    return song_download_queue


def download_audio_files(song_download_queue):
    for songs in song_download_queue:
        song_no_format = songs['song_name']
        artist_no_format = songs['artist_name']
        url = songs['url']
        download_audio = songs['download_audio']

        # Format song name and artist into "song-name-by-artist"
        song = re.sub(r'[^a-zA-Z0-9]+', '-', songs['song_name'].strip().lower())
        artist = re.sub(r'[^a-zA-Z0-9]+', '-', songs['artist_name'].strip().lower())
        formatted_filename = f"{song}-by-{artist}"

        if download_audio:
            print(f"{Fore.GREEN}🎧 Downloading audio for {song_no_format} by {artist_no_format}")
            try:
                ydl_opts = {
                    'format': 'bestaudio/best',
                    'outtmpl': f"{DOWNLOAD_FOLDER}/{formatted_filename}.%(ext)s",
                    'quiet': False,
                    'noplaylist': True,
                    'cookiefile': 'cookies.txt'
                }

                with youtube_dl.YoutubeDL(ydl_opts) as ydl:
                    ydl.download([url])

                print(f"{Fore.GREEN}✅ Audio downloaded successfully for {song_no_format} by {artist_no_format}.")

                # Mark download_audio as False in Supabase to avoid redownloading
                supabase.table("song_info").update({"download_audio": False}).eq("url", url).execute()

            except Exception as e:
                print(f"{Fore.RED}❌ Failed to download audio for {song} by {artist}: {str(e)}")



def main_script():
    n = int(input('Enter the number of songs you want to add: '))

    if n != 0:
        print('Please enter the following details for each song: ')
        for i in range(n):
            song = input('Enter the name of the song: ')
            artist = input('Enter the name of the artist: ')
            url = input('Enter the URL of the song: ')
            color = input('Enter the color of the song (hex code): ')

            add_music_to_supabase(song, artist, url, color)

    song_download_queue = fetch_songs_to_download()
    download_audio_files(song_download_queue)


if __name__ == '__main__':
    main_script()
