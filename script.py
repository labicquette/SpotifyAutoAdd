import spotipy
from spotipy.oauth2 import SpotifyOAuth

"""
    To be able to use this script you need to set your environment variables like so
    export SPOTIPY_CLIENT_ID='your-spotify-client-id'
    export SPOTIPY_CLIENT_SECRET='your-spotify-client-secret'
"""

#variables you need to change :
#targetPlaylistID : ID of the playlist you're modifying 
#sourcePlaylistID : ID of the playlist you're getting the tracks from
targetPlaylistID = "4XsBp3Qs72nKP2zrugOf3P"
sourcePlaylistID = "37i9dQZF1DWVY4eLfA3XFQ"

#spotify's type of authorisation
scope = "playlist-modify-private"

#authentication
sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope,redirect_uri="http://127.0.0.1:9090"))

#(play)list of information on tracks 
targetPlaylist = []
sourcePlaylist = []

#first 100 tracks from user playlist
tracksTarget = sp.playlist_items(targetPlaylistID)
#first 100 tracks from Spotify playlist 
tracksSource = sp.playlist_items(sourcePlaylistID)

#request of tracks after the first 100
targetPlaylist.extend(tracksTarget['items'])
sourcePlaylist.extend(tracksSource['items'])

while tracksTarget['next']:
    tracksTarget = sp.next(tracksTarget)
    targetPlaylist.extend(tracksTarget['items'])

while tracksSource['next']:
    tracksSource = sp.next(tracksSource)
    sourcePlaylist.extend(tracksSource['items'])


#research of original tracks 
originalTracks = []

for item in sourcePlaylist :
    duplicate = False
    for userItem in targetPlaylist:
        if item['track']['id'] == userItem['track']['id']:
            duplicate = True
            break
    if not duplicate :
        originalTracks.append(item['track']['id'])

#addition to user playlist if there are new tracks 
if len(originalTracks) > 0 :
    sp.playlist_add_items(targetPlaylistID, originalTracks)
        