# shows a user's playlists (need to be authenticated via oauth)

import sys
import spotipy
import spotipy.util as util


def show_tracks(tracks):

    for i, item in enumerate(tracks['items']):
        track = item['track']
        print ("   %d   %s" % (i, track['artists'][0]['name'],))
        add_tracks(track['artists'][0]['id'])

def add_tracks(artistid):
    response = sp.artist_top_tracks(artistid)
    tracklist = list()

    for newtrack in response['tracks']:
        tracklist.append(newtrack['uri'])

    newresults = sp.user_playlist_add_tracks(username, newplaylist['id'],
    tracklist)

if __name__ == '__main__':

    if len(sys.argv) > 2:
        newplaylistname = sys.argv[2]
    else:
        newplaylistname = 'New Playlist'

    if len(sys.argv) < 2:
        print (sys.argv[0], 'Username(Required), Playlist Name(Optional)')
        sys.exit()
    else:
        username = sys.argv[1]

    scope = 'playlist-modify-public'
    token = util.prompt_for_user_token(username,scope)

    if token:
        sp = spotipy.Spotify(auth=token)
        playlists = sp.user_playlists(username)
        newplaylist = sp.user_playlist_create(username, newplaylistname)

        for playlist in playlists['items']:
            if playlist['owner']['id'] == username:

                if playlist['name'] == 'Artists':
                    print (playlist['name'])
                    print ('  total artists count', playlist['tracks']['total'])
                    results = sp.user_playlist(username, playlist['id'],
                        fields="tracks,next")
                    tracks = results['tracks']
                    show_tracks(tracks)
                    while tracks['next']:
                        tracks = sp.next(tracks)
                        show_tracks(tracks)
    else:
        print ("Can't get token for", username)
