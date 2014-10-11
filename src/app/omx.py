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
    """
    Class for handling the Raspberry Pi's built in Omxplayer. Saves some
    information in a config file, for example last played video and running
    time.
    """
    def __init__(self):
        self.now_playing = []
        self.start_time = None
        self.stop_time = None
        self.config = config.Config()

    def play(self, movie_id, path):
        """
        Starts a video given an id and a path.
        """
        if len(self.now_playing) == 0:
            movie_id = str(movie_id)
            self.start_time = time.time()
            if self.config.get('last played') != movie_id:
                self.now_playing.append(
                    subprocess.Popen(['omxplayer', '-o', 'local', '-b', path],
                                     stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE))
                print "[OMX] playing. id: %s, path: %s" % (movie_id, path)
                self.config.add('last played', movie_id)
            else:
                running_time = float(self.config.get('running time'))
                self.now_playing.append(
                    subprocess.Popen(['omxplayer', '-o', 'local', '-b', path,
                                      '-l', str(running_time)],
                                     stdout=subprocess.PIPE,
                                     stdin=subprocess.PIPE))
                print "[OMX] resuming at: %d. id: %s, path: %s" % (
                    running_time, movie_id, path)
        else:
            print '[OMX] already playing'

    def stop(self):
        """
        Stops the running video.
        """
        if len(self.now_playing) != 0:
            p = self.now_playing.pop()
            running_time = time.time() - self.start_time
            print '[OMX] stopped, running time: %ds' % running_time
            p.stdin.write(STOP)
            self.config.add('running time', str(running_time))

    def pause(self):
        """
        Pauses the running video.
        """
        if self.now_playing[0]:
            self.now_playing[0].stdin.write(PAUSE)

    def forward(self):
        """
        Forwards 30 seconds in the currently playing video.
        """
        if self.now_playing[0]:
            self.now_playing[0].stdin.write(FWD)

    def reverse(self):
        """
        Reverses 30 seconds in the currently playing video.
        """
        if self.now_playing[0]:
            self.now_playing[0].stdin.write(REV)

    def currently_playing(self):
        """
        Returns the movie object that is currently playing.
        """
        return self.now_playing
