#!/usr/bin/env python
from flask import Flask, jsonify, make_response, abort, render_template
import subprocess
import json
import os

app = Flask(__name__)

#PATH = '/Volumes/Data/filmer'
PATH = '/home/pi/timecapsule/filmer'
OMX_PATH = 'omxplayer -o local '
FILE_EXT1 = '*.avi'
FILE_EXT2 = '*.AVI'
FILE_EXT3 = '*.mkv'
FILE_EXT4 = '*.mp4'

output = subprocess.check_output(['find', PATH, '-name', FILE_EXT1, '-o',
	'-name', FILE_EXT2, '-o', '-name', FILE_EXT3, '-o', '-name', FILE_EXT4])[0:-1].split(b'\n')

movies = []
for i in xrange(0, len(output)):
    movie_title = output[i].decode('utf-8')
    movie = {
            'id': i,
            'title': movie_title
    }
    movies.append(movie)


@app.route('/raspivideo')
def index():
    return render_template('main.html')

@app.route('/raspivideo/movies', methods = ['GET'])
def get_all_movies():
    return jsonify( { 'movies': movies } )

@app.route('/raspivideo/movies/<int:movie_id>', methods = ['GET'])
def get_movie(movie_id):
    movie = filter(lambda t: t['id'] == movie_id, movies)
    if len(movie) == 0:
        abort(404)
    return jsonify( { 'movie': movie[0] } )

@app.route('/raspivideo/movies/action/play/<int:movie_id>', methods = ['GET'])
def play_movie(movie_id):
    cmd_pi = OMX_PATH + '"' + get_moviepath(movie_id) + '"'
    #print cmd_pi
    os.system(cmd_pi) 

@app.route('/raspivideo/movies/action/pause', methods = ['GET'])
def pause_movie(movie_id):
    print "in pause"
    os.system('p')

@app.route('/raspivideo/movies/action/stop', methods = ['GET'])
def stop_movie(movie_id):
    print "in stop"
    os.system('q')

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

def get_moviepath(movie_id):
    movie = filter(lambda t : t['id'] == movie_id, movies)
    return movie[0]['title']

if __name__ == '__main__':
    app.run(host='0.0.0.0')
