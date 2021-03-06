def current_user_playlist_tracks(spotify, playlist_id=None, fields=None, limit=100, offset=0, market=None):
    plid = spotify._get_id('playlist', playlist_id)
    return spotify._get("playlists/%s/tracks" % plid, limit=limit, offset=offset, fields=fields, market=market)


def current_user_playlist_create(spotify, playlist_name, public=True):
        data = {'name': playlist_name, 'public': public, 'description': 'New playlist with name {}'.format(playlist_name)}
        return spotify._post("me/playlists", payload=data)


def current_user_playlist_add_tracks(spotify, playlist_id, tracks, position=None):
    plid = spotify._get_id('playlist', playlist_id)
    ftracks = [spotify._get_uri('track', tid) for tid in tracks]
    return spotify._post("playlists/%s/tracks" % plid, payload=ftracks, position=position)


def sad_mood(sp, tracks):
    saved_tracks = []
    for track in tracks:
        features = sp.audio_features(track)
        danceability = features[0]["danceability"]
        energy = features[0]["energy"]
        valence = features[0]["valence"]
        if valence <= 0.25:
            saved_tracks.append(track)
        elif energy <= 0.25 :
            saved_tracks.append(track)
        elif danceability <= 0.25:
            saved_tracks.append(track)
    return saved_tracks


def angry_mood(sp, tracks):
    saved_tracks = []
    for track in tracks:
        features = sp.audio_features(track)
        energy = features[0]["energy"]
        tempo=features[0]["tempo"]
        if energy >= 0.8 :
            saved_tracks.append(track)
        elif tempo >= 80 and tempo <= 120:
            saved_tracks.append(track)
    return saved_tracks


def happy_mood(sp, tracks):
    saved_tracks = []
    for track in tracks:
        features = sp.audio_features(track)
        energy = features[0]["energy"]
        valence = features[0]["valence"]
        if valence >= 0.75:
            saved_tracks.append(track)
        elif energy <= 0.75 :
            saved_tracks.append(track)
    return saved_tracks


def neutral_mood(sp, tracks):
    saved_tracks = []
    for track in tracks:
        features = sp.audio_features(track)
        energy = features[0]["energy"]
        valence = features[0]["valence"]
        tempo=features[0]["tempo"]
        if valence <= 0.8 and valence >= 0.35:
            saved_tracks.append(track)
        elif energy >= 0.2 and energy <= 0.9:
            saved_tracks.append(track)
        elif tempo>=60 and tempo <= 110:
            saved_tracks.append(track)
    return saved_tracks


def fear_mood(sp, tracks):
    saved_tracks = []
    for track in tracks:
        features = sp.audio_features(track)
        energy = features[0]["energy"]
        valence = features[0]["valence"]
        if valence <= 0.5:
            saved_tracks.append(track)
        elif energy >= 0.2 and energy <= 0.9:
            saved_tracks.append(track)
    return saved_tracks



