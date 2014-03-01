#!/usr/bin/env python
from flask import (abort,
                   Flask,
                   jsonify,
                   make_response,
                   render_template,
                   request
                   )
import requests
import subprocess
import sys
import omx
import ConfigParser
from app import app

movies = []
now_playing = []
omxplayer = omx.Omx()


# handlers
@app.route('/raspivideo')
def index():
    load_movies()
    return render_template('main.html')


@app.route('/raspivideo/movies', methods=['GET'])
def get_all_movies():
    return jsonify({'movies': movies})


@app.route('/raspivideo/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = filter(lambda t: t['id'] == movie_id, movies)
    if len(movie) == 0:
        abort(404)
    return jsonify({'movie': movie[0]})


@app.route('/raspivideo/movies/action/play/<int:movie_id>', methods=['GET'])
def play_movie(movie_id):
    omxplayer.play(get_moviepath(movie_id))
    return jsonify({'playing': movie_id})


@app.route('/raspivideo/movies/action/stop', methods=['GET'])
def stop_movie():
    omxplayer.stop()
    return jsonify({'action': 'stopped'})


@app.route('/raspivideo/movies/action/play_pause', methods=['GET'])
def pause_movie():
    omxplayer.pause()
    return jsonify({'action': 'play/pause'})


@app.route('/raspivideo/movies/path', methods=['POST'])
def setup_path():
    if not request.json or not 'path' in request.json:
        abort(400)
    path = request.json['path']
    init_config(path)
    load_movies()
    return jsonify({'path set': path}), 201


@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)


# helper functions
def get_moviepath(movie_id):
    movie = filter(lambda t: t['id'] == movie_id, movies)
    return movie[0]['path']


def get_title(movie_path):
    movie_title = movie_path.split('/')[-2:-1][0].split('.')[0]
    return movie_title


def get_data(movie_title, data):
    r = requests.get('http://www.omdbapi.com/?t=%s' % movie_title)
    return r.json()[data]


def load_movies():
    print '[APP] loading movies'
    config = ConfigParser.RawConfigParser()
    config.read('app/settings.cfg')
    path = config.get('info', 'path')
    print path
    file_ext1 = '*.avi'
    file_ext2 = '*.AVI'
    file_ext3 = '*.mkv'
    file_ext4 = '*.mp4'

    output = subprocess.check_output(['find', path, '-name', file_ext1, '-o',
                                     '-name', file_ext2, '-o', '-name',
                                     file_ext3, '-o', '-name',
                                     file_ext4])[0:-1].split(b'\n')
    for i in xrange(0, len(output)):
        movie_path = output[i].decode('utf-8')
        movie_title = get_title(movie_path)
        movie = {'id': i,
                 'title': movie_title,
                 'path': movie_path}
        movies.append(movie)


def init_config(path):
    print '[APP] initializing path: ' + path
    config = ConfigParser.RawConfigParser()
    config.add_section('info')
    config.set('info', 'path', path)
    with open('settings.cfg', 'wb') as configfile:
        config.write(configfile)
