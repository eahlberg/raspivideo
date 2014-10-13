"""
RESTful user interface that provides handlers for the different URLs. See
http://en.wikipedia.org/wiki/Representational_state_transfer for more info about
REST.
"""
#!/usr/bin/env python
import flask
import requests
import subprocess
import sys
import omx
import config
import movie
import ConfigParser
from app import app
import os
import os.path


movies = []
omxplayer = omx.Omx()
config = config.Config()

FILE_EXT1 = '*.avi'
FILE_EXT2 = '*.AVI'
FILE_EXT3 = '*.mkv'
FILE_EXT4 = '*.mp4'


@app.route('/raspivideo')
def index():
    """
    Handler for the root url. Loads all movies and renders the first page.
    """
    if path_set():
        load_movies()
    return flask.render_template('main.html')


@app.route('/raspivideo/movies', methods=['GET'])
def get_all_movies():
    """
    Returns a json file of all movies.
    """
    if path_set():
        load_movies()
    return flask.jsonify({'movies': [e.__dict__ for e in movies]})


@app.route('/raspivideo/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    """
    Returns a json file of a specific movie.
    """
    movie = None
    for elem in movies:
        if elem.id == movie_id:
            movie = elem
    if not Movie:
        abort(404)
    return flask.jsonify({'movie': movie.__dict__})


@app.route('/raspivideo/movies/action/play/<int:movie_id>', methods=['GET'])
def play_movie(movie_id):
    """
    Plays the movie with the specified movie id.
    """
    omxplayer.play(movie_id, get_moviepath(movie_id))
    return flask.jsonify({'playing': movie_id})


@app.route('/raspivideo/movies/action/stop', methods=['GET'])
def stop_movie():
    """
    Stops the movie with the specified movie id.
    """
    omxplayer.stop()
    return flask.jsonify({'action': 'stopped'})


@app.route('/raspivideo/movies/action/play_pause', methods=['GET'])
def pause_movie():
    """
    Pauses the movie with the specified movie id.
    """
    omxplayer.pause()
    return flask.jsonify({'action': 'play/pause'})


@app.route('/raspivideo/movies/action/resume', methods=['GET'])
def resume_movie():
    """
    Resumes the movie with the specified movie id.
    """
    return flask.jsonify({'action': 'resumed'})


@app.route('/raspivideo/movies/path', methods=['POST'])
def setup_path():
    """
    Handles a POST request containing the path of the video files.
    """
    if 'path' not in flask.request.json:
        abort(400)
    movie_path = flask.request.json['path']
    config.add('movie path', movie_path)
    print '[APP] path set'
    return flask.jsonify({'path set': movie_path}), 201


@app.errorhandler(404)
def not_found(error):
    """
    Standard error handler.
    """
    return flask.make_response(flask.jsonify({'error': 'Not found'}), 404)


# helper functions
def get_moviepath(movie_id):
    """
    Returns the path for a movie given an id.
    """
    for m in movies:
        if m.id == movie_id:
            return m.path
    return None


def get_title(movie_path):
    """
    Returns the title of a given movie given a path.
    """
    movie_title = movie_path.split('/')[-2:-1][0].split('.')[0]
    return movie_title


def load_movies():
    """
    Loads all movies specified in the path. Assumes the path is accessible (i.e.
    already mounted).
    """
    print '[APP] loading movies'
    movie_path = config.get('movie path')

    output = subprocess.check_output(
        ['find', movie_path, '-name', FILE_EXT1, '-o', '-name', FILE_EXT2,
         '-o', '-name', FILE_EXT3, '-o', '-name',
         FILE_EXT4])[0:-1].split(b'\n')
    for i in xrange(0, len(output)):
        path = output[i].decode('utf-8')
        title = get_title(path)
        m = movie.Movie(i, title, path)
        movies.append(m)
    print '[APP] movies loaded'

def path_set():
    """
    Checks if the path is set in the config.
    """
    path = config.get('movie path')
    if path:
        return True
    return False
