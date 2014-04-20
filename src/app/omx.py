import subprocess
import time
import ConfigParser
import os


STOP = 'q'
PAUSE = 'p'
FWD = 'right'

class Omx:
    def __init__(self):
        self.now_playing = []
        self.start_time = None
        self.stop_time = None

    def play(self, path):
        print "[OMX] trying to play: " + path
        self.now_playing.append(subprocess.Popen(['omxplayer', '-o', 'local',
                                '-b', path], stdout=subprocess.PIPE,
                                stdin=subprocess.PIPE))
        self.start_time = time.time()
        print "[OMX] started: " + path
        print "[OMX] time: " + str(self.start_time)

    def stop(self):
        self.stop_time = time.time()
        print "[OMX] stopping"
        print "[OMX] stop time: " + str(self.stop_time)
        running_time = self.stop_time - self.start_time
        print "[OMX] running time: " + str(running_time)
        p = self.now_playing[0]
        p.stdin.write(STOP)
        self.now_playing.remove(p)
        
        config = ConfigParser.ConfigParser()
        config.read('settings.cfg')
        path = os.getcwd() + '/app/settings.cfg'
        config.read(path)
        config.set('info', 'running time', str(running_time))

        with open(path, 'wb') as config_file:
            config.write(config_file)

    def pause(self):
        self.now_playing[0].stdin.write(PAUSE)

    def forward(self):
        self.now_playing[0].stdin.write(FWD)

    def reverse(self):
        pass

    def now_playing(self):
        pass
