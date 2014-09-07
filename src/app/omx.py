import subprocess
import time
import ConfigParser
import os
import config


STOP = 'q'
PAUSE = 'p'
FWD = 'right'
REV = 'left'

class Omx:
    def __init__(self):
        self.now_playing = []
        self.start_time = None
        self.stop_time = None
        self.config = config.Config()


    def play(self, movie_id, path):
        if len(self.now_playing) == 0:
            movie_id = str(movie_id)
            self.start_time = time.time()
            if self.config.get('last played') != movie_id:
                self.now_playing.append(subprocess.Popen(['omxplayer', '-o', 'local',
                    '-b', path], stdout=subprocess.PIPE,
                    stdin=subprocess.PIPE))
                print "[OMX] playing. id: %s, path: %s" % (movie_id, path)
                self.config.add('last played', movie_id)
            else:
                running_time = float(self.config.get('running time'))
                self.now_playing.append(subprocess.Popen(['omxplayer', '-o',
                    'local', '-b', path, '-l', str(running_time)], stdout=subprocess.PIPE, stdin=subprocess.PIPE))
                print "[OMX] resuming at: %d. id: %s, path: %s" % (running_time, movie_id, path)
        else:
            print '[OMX] already playing'


    def stop(self):
        if len(self.now_playing) != 0:
            p = self.now_playing.pop()
            running_time = time.time() - self.start_time
            print '[OMX] stopped, running time: %ds' % running_time
            p.stdin.write(STOP)
            self.config.add('running time', str(running_time))


    def pause(self):
        if self.now_playing[0]:
            self.now_playing[0].stdin.write(PAUSE)


    def forward(self):
        if self.now_playing[0]:
            self.now_playing[0].stdin.write(FWD)


    def reverse(self):
        if self.now_playing[0]:
            self.now_playing[0].stdin.write(REV)


    def resume(self):
        pass
        # if self.now_playing[0]:
            # self.now_playing[0].stdin.write(RESUME + ' ' +
            #         str(self.start_time))


    def currently_playing(self):
        return self.now_playing
