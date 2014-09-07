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
    load_movies()
    print '[APP] movies loaded'
    return flask.render_template('main.html')


@app.route('/raspivideo/movies', methods=['GET'])
def get_all_movies():
    return flask.jsonify({'movies': [e.__dict__ for e in movies]})


@app.route('/raspivideo/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = None
    for elem in movies:
        if elem.id == movie_id:
            movie = elem
    if not Movie:
        abort(404)
    return flask.jsonify({'movie': movie.__dict__})


@app.route('/raspivideo/movies/action/play/<int:movie_id>', methods=['GET'])
def play_movie(movie_id):
# movie out currently playing logic
    omxplayer.play(movie_id, get_moviepath(movie_id))
    return flask.jsonify({'playing': movie_id})


@app.route('/raspivideo/movies/action/stop', methods=['GET'])
def stop_movie():
    omxplayer.stop()
    return flask.jsonify({'action': 'stopped'})


@app.route('/raspivideo/movies/action/play_pause', methods=['GET'])
def pause_movie():
    omxplayer.pause()
    return flask.jsonify({'action': 'play/pause'})


@app.route('/raspivideo/movies/action/resume', methods=['GET'])
def resume_movie():
    print config.get('running time')
    return flask.jsonify({'action': 'resumed'})

@app.route('/raspivideo/movies/path', methods=['POST'])
def setup_path():
    if not request.json or not 'path' in request.json:
        abort(400)
    movie_path = request.json['path']
    config.add('movie path', movie_path)
    return flask.jsonify({'path set': movie_path}), 201


@app.errorhandler(404)
def not_found(error):
    return flask.make_response(jsonify({'error': 'Not found'}), 404)


# helper functions
def get_moviepath(movie_id):
    for m in movies:
        if m.id == movie_id:
            return m.path
    return None


def get_title(movie_path):
    movie_title = movie_path.split('/')[-2:-1][0].split('.')[0]
    return movie_title


def load_movies():
    print '[APP] loading movies'
    movie_path = config.get('movie path')

    output = subprocess.check_output(['find', movie_path, '-name', FILE_EXT1, '-o',
                                     '-name', FILE_EXT2, '-o', '-name',
                                     FILE_EXT3, '-o', '-name',
                                     FILE_EXT4])[0:-1].split(b'\n')
    for i in xrange(0, len(output)):
        path = output[i].decode('utf-8')
        title = get_title(path)
        m = movie.Movie(i, title, path)
        movies.append(m)


