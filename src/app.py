#!flask/bin/python
from flask import Flask, jsonify, make_response, abort, render_template
import subprocess
import json
import os

app = Flask(__name__)

PATH = '/Volumes/Data/filmer'
FILE_EXT1 = '*.avi'
output = subprocess.check_output(['find', PATH, '-name',
     FILE_EXT1])[0:-1].split(b'\n')

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

@app.route('/raspivideo/movies/play/<int:movie_id>', methods = ['GET'])
def play_movie(movie_id):
    movie = filter(lambda t : t['id'] == movie_id, movies)
    movie_path = movie[0]['title']
    vlc_path = '/Applications/VLC.app/Contents/MacOS/VLC'
    cmd = vlc_path + ' "' + movie_path + '"'
    print cmd
    subprocess.call(cmd, shell=True)
    #os.system('echo ' + movie[0])
    return jsonify( { 'starting movie': movie } )



@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify( { 'error': 'Not found' } ), 404)

if __name__ == '__main__':
    app.run(host='0.0.0.0')
