"""This script builds the Flask app."""
from datetime import datetime
import spotipy
from flask import Flask, request, render_template, redirect, session, escape
import spotipy.oauth2 as oauth2
from functions import authorize, initializer, get_playlist, logger, get_current_user_saved_tracks
from secret import SCOPE, CLIENT_ID, CLIENT_SECRET, REDIRECT_URI
from azure_functions import get_face_emotion_information
import os
from flask_sqlalchemy import SQLAlchemy
# from . import models

project_dir = os.path.dirname(os.path.abspath(__file__))
database_file = "sqlite:///{}".format(os.path.join(project_dir, "moodify.db"))

app = Flask(__name__, static_folder="static")
APP_ROOT = os.path.dirname(os.path.abspath(__file__))

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_DATABASE_URI'] = database_file
db = SQLAlchemy(app)

class User(db.Model):
    # See http://flask-sqlalchemy.pocoo.org/2.0/models/#simple-example
    # for details on the column types.

    # We always need an id
    id = db.Column(db.Integer, primary_key=True)

    # A dessert has a name, a price and some calories:
    name = db.Column(db.String(100))
    username = db.Column(db.String)
    last_login = db.Column(db.Integer)
    email = db.Column(db.String(120), unique = False, nullable = True)

    def __init__(self, name, username, email):
        self.name = name
        self.username = username
        self.last_login = datetime.now()
        self.email = email

    def get_username(self):
        return self.username

def flask_app():

    @app.route('/', methods=['GET'])
    def index():
        return render_template('index.html')

    @app.route('/click', methods=['GET'])
    def click():
        logger('button', 'click')
        sp_oauth = oauth2.SpotifyOAuth(CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, scope=SCOPE)
        return redirect(sp_oauth.get_authorize_url())

    @app.route('/logout', methods = ['GET'])
    def logout():
        logger('button', 'logout')
        # session.clear()
        # print("SESSION POP  ",session.pop('username', None))
        return render_template('index.html')

    @app.route('/authorization', methods=['GET','POST'])
    def authorization():
        response = request.url
        username = authorize(response)
        logger(username, 'attempt')
        spotify_object = initializer(username)
        print('\n\n\n\n ', spotify_object)
        current_user = spotify_object.current_user()
        email = current_user['email']
        name = current_user['display_name']
        user = User(name, username, email)
        db.session.add(user)
        db.session.commit()
        session['username'] = username
        logger(username, 'success')
        return render_template('upload.html')


    @app.route("/upload", methods=["POST","GET"])
    def upload():
        # username = session.pop('username', None)

        num_of_tracks = 10
        target = os.path.join(APP_ROOT, 'images/')

        if not os.path.isdir(target):
                os.mkdir(target)
        else:
            print("Couldn't create upload directory: {}".format(target))

        print(request.files.getlist("file"))
        for upload in request.files.getlist("file"):
            print(upload)
            print("{} is the file name".format(upload.filename))
            filename = upload.filename
            destination = "".join([target, filename])
            print("Accept incoming file:", filename)
            print("Save it to:", destination)
            upload.save(destination)
            emotion = get_face_emotion_information(destination)
            username = session.get('username', None)
            spotify_object = initializer(username)
            get_playlist(spotify_object, emotion, num_of_tracks)
        # return send_from_directory("images", filename, as_attachment=True)
        return render_template("complete.html", file_path=destination)


    @app.route('/upload/<file_path>')
    def send_image(file_path):
        return True
    #send_from_directory("images", filename)
    #end of upload

    return app


if __name__ == '__main__':
    print("Creating MOODIFY database...")
    db.create_all()
    print("MOODIFY database successfully created!")
    APP = flask_app()
    APP.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
    APP.run(debug=True)
