import requests
from bs4 import BeautifulSoup
import spotipy
from spotipy.oauth2 import SpotifyOAuth

sp = spotipy.Spotify(
    auth_manager=SpotifyOAuth(
        scope="playlist-modify-private",
        redirect_uri="http://example.com",
        client_id="ENTER YOUR CLIENT_ID",
        client_secret="ENTER YOUR SECRET KEY",
        show_dialog=True,
        cache_path="token.txt"
    )
)
user_id = sp.current_user()["id"]
user_name = sp.current_user()["display_name"]
print(user_id, user_name)

# User inputs the date
input_date = input("Which year do you want to travel to? Type the date in this format YYYY-MM-DD: ")

# URL for the Billboard Hot 100 chart
URL = f"https://www.billboard.com/charts/hot-100/{input_date}/"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36"
}

# Fetch the webpage
response = requests.get(URL, headers=headers)
response.raise_for_status()
billboard_website = response.text

# Parse the HTML content
soup = BeautifulSoup(billboard_website, "html.parser")

# Locate song titles
titles = soup.select("li.o-chart-results-list__item h3.c-title")

# Extract and clean the titles
song_names = [title.get_text(strip=True) for title in titles]

# Search song in Spotify
song_URIS = []
year = input_date[0:4]
for song in song_names:
    result = sp.search(q=f"track:{song} year:{year}", type="track")
    print(result)
    try:
        uri = result["tracks"]["items"][0]["uri"]
        song_URIS.append(uri)
    except IndexError:
        print(f"{song} doesn't exist in Spotify. Skipped.")

playlist = sp.user_playlist_create(user_id, f"{input_date} Billboard 100", public=False, description= f"{input_date}'s Top 100 Billboard list")
sp.playlist_add_items(playlist_id=playlist["id"], items=song_URIS)

# Print the result
print(song_names)