#!/usr/bin/env python
import flask
import requests
import subprocess
import sys
import omx
import ConfigParser
from app import app
import os


movies = []
omxplayer = omx.Omx()


@app.route('/raspivideo')
def index():
    load_movies()
    return flask.render_template('main.html')


@app.route('/raspivideo/movies', methods=['GET'])
def get_all_movies():
    return flask.jsonify({'movies': movies})


@app.route('/raspivideo/movies/<int:movie_id>', methods=['GET'])
def get_movie(movie_id):
    movie = filter(lambda t: t['id'] == movie_id, movies)
    if len(movie) == 0:
        abort(404)
    return flask.jsonify({'movie': movie[0]})


@app.route('/raspivideo/movies/action/play/<int:movie_id>', methods=['GET'])
def play_movie(movie_id):
    if len(omxplayer.currently_playing()) == 0:
        omxplayer.play(get_moviepath(movie_id))
        return flask.jsonify({'playing': movie_id})
    else:
        print '[APP] unable to start movie, already playing'


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
    parser = ConfigParser.ConfigParser()
    os_path = os.getcwd() + '/app/settings.cfg'
    parser.read(os_path)
    try:
        running_time = parser.getfloat('info', 'running time')
    except ConfigParser.ConfigError, e:
        print '[ERROR] unable to load running time from config'
        print e

    print running_time
    return flask.jsonify({'action': 'resumed'})

@app.route('/raspivideo/movies/path', methods=['POST'])
def setup_path():
    if not request.json or not 'path' in request.json:
        abort(400)
    path = request.json['path']
    init_config(path)
    load_movies()
    return flask.jsonify({'path set': path}), 201


@app.errorhandler(404)
def not_found(error):
    return flask.make_response(jsonify({'error': 'Not found'}), 404)


# helper functions
def get_moviepath(movie_id):
    movie = filter(lambda t: t['id'] == movie_id, movies)
    return movie[0]['path']


def get_title(movie_path):
    movie_title = movie_path.split('/')[-2:-1][0].split('.')[0]
    return movie_title


def load_movies():
    print '[APP] loading movies'
    parser = ConfigParser.ConfigParser()
    os_path = os.getcwd() + '/app/settings.cfg'
    parser.read(os_path)
    try:
        path = parser.get('info', 'path')
    except ConfigParser.ConfigError, e:
        print '[ERROR] unable to load path from config'
        print e
    
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
