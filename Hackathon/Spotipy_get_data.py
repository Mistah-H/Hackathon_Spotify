import spotipy
import csv
import pandas as pd

# Authentication
token = spotipy.oauth2.SpotifyClientCredentials(client_id='ID', client_secret='client_secret')
cache_token = token.get_access_token()
spotify = spotipy.Spotify(cache_token)

## Playlist Track Data
# Purpose: Given a Spotify Playlist, get detailed track information for every song

results = spotify.playlist_tracks('spotify:playlist:6VZtYgEhGS6JMYNvJV3XfU', offset=0)

# Store results in a tracks array
tracks = results['items']

# Continue paginating through until all results are returned
while results['next']:
    results = spotify.next(results)
    tracks.extend(results['items'])

# Open and configure output csv
with open('playlist_track_data.csv', mode='w') as employee_file:
    spotify_writer = csv.writer(employee_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    # Write csv headers
    spotify_writer.writerow(['Index', 'Artist Name', 'Track Name', 'Release Date','Danceability','Energy','Key','Loudness','Mode','Speechiness','Accousticness','Instrumentalness','Liveness','Valence','Tempo','Duration MS','Time Signature'])

    # index
    i = 0

    # for each track in the playlist, gather more information and write to csv
    for item in (tracks):
        i = i + 1
        track = item['track']

        # if the track is a local file, skip it
        if "local" in track['uri']:
            continue

        # Two more API calls to get more track-related information
        audio_features = spotify.audio_features(track['uri'])[0]
        release_date = spotify.track(track['uri'])['album']['release_date']

        # print to console for debugging
        print("   %d %32.32s %s %s" % (i, track['artists'][0]['name'], track['name'],release_date))

        # write to csv
        spotify_writer.writerow([i, track['artists'][0]['name'], track['name'], release_date
                                , audio_features['danceability']
                                , audio_features['energy']
                                , audio_features['key']
                                , audio_features['loudness']
                                , audio_features['mode']
                                , audio_features['speechiness']
                                , audio_features['acousticness']
                                , audio_features['instrumentalness']
                                , audio_features['liveness']
                                , audio_features['valence']
                                , audio_features['tempo']
                                , audio_features['duration_ms']
                                , audio_features['time_signature']]
                                )

# COnvert to Pickle format 
df = pd.read_csv('playlist_track_data.csv', encoding='latin-1')
df.to_pickle('./Spotify_track_data.pkl')
