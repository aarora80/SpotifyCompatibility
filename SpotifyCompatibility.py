import requests
import urllib.parse
import json
import math

from datetime import datetime, timedelta
from flask import Flask, redirect, request, jsonify, session, render_template
from types import SimpleNamespace



# USER_ID = ''
# USER_NAME = ''

user_hashmap = {}
class User:
    def __init__(self, userid, name):
        self.id = userid
        self.name = name
        self.artists = []
        self.tracks = []

    
    def add_artist(self, artist):
        self.artists.append(artist)


    def add_track(self, track):
        self.tracks.append(track)

    def __str__(self):
        return f"User ID: {self.id}\nUser Name: {self.name}\n\nArtists:\n{', '.join([str(artist) for artist in self.artists])}\n\nTracks:\n{', '.join([str(track) for track in self.tracks])}"



class SpotifyAlbum:
    def __init__(self, album_data):
        self.album_id = album_data.get('id')
        self.album_name = album_data.get('name')
        self.release_date = album_data.get('release_date')

        # Extract album artists
        self.album_artists = [SpotifyArtist(artist) for artist in album_data.get('artists', [])]

    def __str__(self):
        return f"Album ID: {self.album_id}, Name: {self.album_name}, Release Date: {self.release_date}\n" \
               f"Album Artists: {', '.join([str(artist) for artist in self.album_artists])}"
class SpotifyArtist:
    def __init__(self, artist_data):
        self.artist_id = artist_data.get('id')
        self.name = artist_data.get('name')
        self.genres = artist_data.get('genres', [])
        self.popularity = artist_data.get('popularity')

    def __str__(self):
        return f"Artist ID: {self.artist_id}, Name: {self.name}, Genres: {self.genres}, Popularity: {self.popularity}"

class SpotifyTrack:
    def __init__(self, track_data):
        # Album information
        album_data = track_data.get('album', {})
        self.album = SpotifyAlbum(album_data)

        # Track information
        self.track_id = track_data.get('id')
        self.track_name = track_data.get('name')
        self.explicit = track_data.get('explicit', False)
        self.popularity = track_data.get('popularity')

        # Extract track artists
        self.track_artists = [SpotifyArtist(artist) for artist in track_data.get('artists', [])]

    def __str__(self):
        return f"Track ID: {self.track_id}, Name: {self.track_name}, Popularity: {self.popularity}, Explicit: {self.explicit}\n" \
               f"{self.album}\n" \
               f"Track Artists: {', '.join([str(artist) for artist in self.track_artists])}"





app = Flask(__name__)
app.secret_key = "88fhr8fh8r-8rhf8rfh8r-frhrfhrifh"

CLIENT_ID='153275bcfe0a442e9fd192f8f77ba795'
CLIENT_SECRET='81e5284135c2421880752de90dc45272'
REDIRECT_URI='http://localhost:5000/callback'

AUTH_URL = 'https://accounts.spotify.com/authorize'
TOKEN_URL = 'https://accounts.spotify.com/api/token'
API_BASE_URL = 'https://api.spotify.com/v1/'

@app.route('/')
def index():
    return render_template("index.html")
    #return "Welcome to my Spotify app <a href ='/login'>Login with Spotify</a>"

@app.route('/login')
def login():
    scope = 'user-top-read user-library-read user-read-private user-read-email'

    params = {
        'client_id': CLIENT_ID,
        'response_type':'code',
        'scope':scope,
        'redirect_uri':REDIRECT_URI,
        'show_dialog':True
    }

    auth_url=f"{AUTH_URL}?{urllib.parse.urlencode(params)}"

    return redirect(auth_url)

@app.route('/callback')

def callback():
    if 'error' in request.args:
        return jsonify({"error": request.args['error']})

    if 'code' in request.args:
        req_body={
            'code': request.args['code'],
            'grant_type': 'authorization_code',
            'redirect_uri': REDIRECT_URI,
            'client_id': CLIENT_ID,
            'client_secret':CLIENT_SECRET
        }

        response = requests.post(TOKEN_URL, data=req_body)
        token_info = response.json()
        #print(token_info)
        session['access_token'] = token_info['access_token']
        session['refresh_token'] = token_info['refresh_token']
        session['expires_at'] = datetime.now().timestamp() + token_info['expires_in']

        return redirect('/searchPage')

@app.route('/searchPage')

def searchPage():
    #global USER_ID, USER_NAME
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }
    response = requests.get(API_BASE_URL + 'me', headers=headers)
    #print(response)
    user = response.json()
    session['user_id'] = user.get('id')
    session['user_name'] = user.get('display_name')

    #print(f"USER_ID: {USER_ID}, USER_NAME: {USER_NAME}")
    # User.id = UserId
    # User.name = Name
    #print(UserId)
    #print(Name)
    
    #print(user_hashmap)
    #return render_template("search.html") 
    return redirect('/artists')
    #return jsonify(user)
def create_user(userid, name):
    return User(userid=userid, name=name)
@app.route('/artists')

# def get_tracks():
#     if 'access_token' not in session:
#         return redirect('/login')

#     if datetime.now().timestamp() > session['expires_at']:
#         return redirect('/refresh-token')

#     headers = {
#         'Authorization': f"Bearer {session['access_token']}"
#     }

#     response = requests.get(API_BASE_URL + 'me/tracks?limit=50', headers=headers)
#     tracks = response.json()
    
#     return jsonify(tracks)

# def get_playlists():
#     if 'access_token' not in session:
#         return redirect('/login')

#     if datetime.now().timestamp() > session['expires_at']:
#         return redirect('/refresh-token')

#     headers = {
#         'Authorization': f"Bearer {session['access_token']}"
#     }

#     response = requests.get(API_BASE_URL + 'me/playlists', headers=headers)
#     playlists = response.json()

#     playlist_ids = [item['id'] for item in playlists['items']]
#     print(playlist_ids)
    
#     tracks = []
#     for playlist_id in playlist_ids:
#         tracks.append(get_playlist_tracks(playlist_id))
    
#     return tracks


# def get_playlist_tracks(playlistID):
    
#     headers = {
#         'Authorization': f"Bearer {session['access_token']}"
#     }


#     response = requests.get(API_BASE_URL + 'playlists/' + playlistID + '/tracks', headers=headers)
#     tracks = response.json()
#     return tracks
#---------------------------
def get_user_top_artists():
    global user_hashmap
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = requests.get(API_BASE_URL + 'me/top/artists?limit=15', headers=headers)
    artists = response.json()
#Initialize a list to store instances of SpotifyArtist
    
    spotify_artists = []
# Accessing artists
    if 'items' in artists and artists['items']:
        # Assuming items is a list, you might need to adjust accordingly
        for artist_data in artists['items']:
            # Use a dictionary with default values to handle missing fields
            artist_info = {
                'id': artist_data.get('id'),
                'name': artist_data.get('name'),
                'genres': artist_data.get('genres', []),
                'popularity': artist_data.get('popularity')
            }

            # Create an instance of SpotifyArtist
            artist = SpotifyArtist(artist_info)

            # Append the artist instance to the list
            spotify_artists.append(artist)

    # Retrieve user information from the session
    user_id = session.get('user_id')
    user_name = session.get('user_name')

    if user_name in user_hashmap:
        # If the user exists, update the existing instance
        current_user = user_hashmap[user_name]
    else:
        # If the user does not exist, create a new instance
        current_user = create_user(userid=user_id, name=user_name)
        user_hashmap[user_name] = current_user

    for artist in spotify_artists:
        current_user.add_artist(artist)
    return redirect('/tracks')   

@app.route('/tracks')
def get_user_top_tracks():
    global user_hashmap
    if 'access_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp() > session['expires_at']:
        return redirect('/refresh-token')

    headers = {
        'Authorization': f"Bearer {session['access_token']}"
    }

    response = requests.get(API_BASE_URL + 'me/top/tracks?limit=50', headers=headers)
    tracks_data = response.json()

    # Initialize a list to store instances of SpotifyTrack
    spotify_tracks = []
    if 'items' in tracks_data and tracks_data['items']:
        for track_data in tracks_data['items']:
            # Create an instance of SpotifyTrack
            track = SpotifyTrack(track_data)

            # Append the track instance to the list
            spotify_tracks.append(track)

    
    user_id = session.get('user_id')
    user_name = session.get('user_name')

    if user_name in user_hashmap:
        # If the user exists, update the existing instance
        current_user = user_hashmap[user_name]
    else:
        # If the user does not exist, create a new instance
        current_user = create_user(userid=user_id, name=user_name)
        user_hashmap[user_name] = current_user

    for track in spotify_tracks:
        current_user.add_track(track)
    return redirect('/content')


#def scoreAlgorithm():



@app.route('/refresh-token')
def refresh_token():
    if 'refresh_token' not in session:
        return redirect('/login')

    if datetime.now().timestamp()>session['expires_at']:
        req_body = {
            'grant_type': 'refresh_token',
            'refresh_token': session['refresh_token'],
            'client_id': CLIENT_ID,
            'client_secret':CLIENT_SECRET

        }

        response = requests.post(TOKEN_URL, data=req_body)
        new_token_info = response.json()

        session['access_token'] = new_token_info['access_token']
        session['expires_at'] = datetime.now().timestamp() + new_token_info['expires_in']

        return redirect('/searchPage')

@app.route('/content', methods=['GET'])



def content():
    if 'access_token' in session:
        # Retrieve user information from the session
        user_name = session.get('user_name')

        # Check if the user_id already exists in the user_hashmap
        if user_name in user_hashmap:
            # If the user exists, retrieve the user instance from the hashmap
            current_user = user_hashmap[user_name]
        else:
            # If the user does not exist, handle this case based on your application's logic
            return 'User not found in user_hashmap'

        print(user_hashmap)
        # Print information about the User
        print(current_user)

    return render_template("search.html")

@app.route('/match', methods=['POST'])
def matchPage():
    searched_name = request.form.get('user_name')

    # Assuming the current user is stored in the session
    if 'user_name' in session:
        current_user_name = session['user_name']

        # Check if the searched_name exists in the user_hashmap
        if searched_name in user_hashmap:
            # Retrieve the user instances from the hashmap
            current_user = user_hashmap.get(current_user_name)
            searched_user = user_hashmap.get(searched_name)

            # Perform your matching algorithm using current_user and searched_user
            compatibility_percentage = calculate_compatibility(current_user, searched_user)

            # Pass both users and the compatibility percentage to the template
            return render_template("match.html", current_user=current_user, searched_user=searched_user, compatibility_percentage=compatibility_percentage)

        else:
            # If the searched_name does not exist in the user_hashmap, handle this case based on your application's logic
            return render_template("match.html", match_result="User not found")
    else:
        # If the current user is not in the session, handle this case based on your application's logic
        return render_template("match.html", match_result="Current user not found in session")

# In your match.html template, you can access the passed values like {{ current_user.name }}, {{ searched_user.name }}, {{ compatibility_percentage }}


def calculate_compatibility_for_pair(user1, user2):
    # Initialize separate percentage calculators
    artist_match_percentage = 0.0
    genre_exact_match_percentage = 0.0
    genre_partial_match_percentage = 0.0
    popularity_match_percentage = 0.0
    track_match_percentage = 0.0
    popularity_track_match_percentage = 0.0
    album_match_percentage = 0.0
    release_date_match_percentage = 0.0
    track_artist_match_percentage = 0.0
    track_artist_partial_match_percentage = 0.0
    explicit_match_percentage = 0.0

    # Check artist objects
    for artist1 in user1.artists:
        for artist2 in user2.artists:
            # If artist IDs match
            if artist1.artist_id == artist2.artist_id:
                artist_match_percentage += 0.9
                print(f'Artist Match: {artist_match_percentage}')

            # If genres are not empty and match exactly
            if artist1.genres and artist2.genres and set(artist1.genres) == set(artist2.genres):
                genre_exact_match_percentage += 0.8
                print(f'Genre Match (Exact): {genre_exact_match_percentage}')
            # If genres are not empty and some match
            elif artist1.genres and artist2.genres and set(artist1.genres) & set(artist2.genres):
                genre_partial_match_percentage += 0.5
                print(f'Genre Match (Partial): {genre_partial_match_percentage}')

            # If the difference in popularity is < 10 and both popularity values are not None
            if artist1.popularity is not None and artist2.popularity is not None and abs(artist1.popularity - artist2.popularity) < 10:
                popularity_match_percentage += 0.9
                print(f'Popularity Match: {popularity_match_percentage}')

    # Check track objects
    for track1 in user1.tracks:
        for track2 in user2.tracks:
            # If track IDs match
            if track1.track_id == track2.track_id:
                track_match_percentage += 1.0
                #print(f'Track Match: {track_match_percentage}')

            # If the difference in popularity is < 10 and both popularity values are not None
            if track1.popularity is not None and track2.popularity is not None and abs(track1.popularity - track2.popularity) < 10:
                popularity_track_match_percentage += 0.5
                #print(f'Popularity Track Match: {popularity_track_match_percentage}')

            # If album IDs match
            if track1.album.album_id == track2.album.album_id:
                album_match_percentage += 0.8
                #print(f'Album Match: {album_match_percentage}')

            # If the difference in the year of the release date is < 5
            if track1.album.release_date and track2.album.release_date and abs(int(track1.album.release_date[:4]) - int(track2.album.release_date[:4])) < 5:
                release_date_match_percentage += 0.7
                #print(f'Release Date Match: {release_date_match_percentage}')

            # If artist IDs match
            if set(artist.artist_id for artist in track1.track_artists) == set(artist.artist_id for artist in track2.track_artists):
                track_artist_match_percentage += 0.9
                #print(f'Track Artist Match: {track_artist_match_percentage}')

            # If track artist IDs match
            if set(artist.artist_id for artist in track1.track_artists) & set(artist.artist_id for artist in track2.track_artists):
                track_artist_partial_match_percentage += 0.8
                #print(f'Track Artist Match (Partial): {track_artist_partial_match_percentage}')

            # If explicit values are both 'yes' or both 'no'
            if track1.explicit is not None and track2.explicit is not None and track1.explicit == track2.explicit:
                explicit_match_percentage += 0.7
                #print(f'Explicit Match: {explicit_match_percentage}')

    # Combine separate percentages using a weighted sum
    artist_total_percentage = (artist_match_percentage * 0.2) + (popularity_match_percentage * 0.1) + ((genre_exact_match_percentage + genre_partial_match_percentage) * 0.3)
    track_total_percentage = (track_match_percentage * 0.7) + ((popularity_track_match_percentage + album_match_percentage + release_date_match_percentage + track_artist_match_percentage + track_artist_partial_match_percentage + explicit_match_percentage) * 0.3)

    # Combine artist and track percentages using a weighted sum
    total_percentage = ((artist_total_percentage/100) * 0.8) + ((track_total_percentage/1000) * 0.5)

    # Print the final compatibility percentages
    print(f'Final Artist Compatibility: {artist_total_percentage * 100}%')
    print(f'Final Track Compatibility: {track_total_percentage * 100}%')

    # Return the final compatibility percentage
    return round(total_percentage * 100, 2)

def calculate_compatibility(user1, user2):
    # Reset compatibility percentages for a new calculation
    session.pop('artist_match_percentage', None)
    session.pop('genre_exact_match_percentage', None)
    session.pop('genre_partial_match_percentage', None)
    session.pop('popularity_match_percentage', None)
    session.pop('track_match_percentage', None)
    session.pop('popularity_track_match_percentage', None)
    session.pop('album_match_percentage', None)
    session.pop('release_date_match_percentage', None)
    session.pop('track_artist_match_percentage', None)
    session.pop('track_artist_partial_match_percentage', None)
    session.pop('explicit_match_percentage', None)

    # Calculate compatibility for user1 to user2
    compatibility_user1_to_user2 = calculate_compatibility_for_pair(user1, user2)

    # Calculate compatibility for user2 to user1
    compatibility_user2_to_user1 = calculate_compatibility_for_pair(user2, user1)

    # Average the compatibility scores
    average_compatibility = (compatibility_user1_to_user2 + compatibility_user2_to_user1) / 2.0

    return average_compatibility




if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
