import subprocess
class Omx:
    def __init__(self):
        self.now_playing = []

    def play(self, path):
        print "[OMX] trying to play: " + path
        self.now_playing.append(subprocess.Popen(['omxplayer',
            path],stdout=subprocess.PIPE,stdin=subprocess.PIPE))
        print "[OMX] started: " + path
        
    def stop(self):
        print "[OMX] stopping"
        p = self.now_playing[0]
        p.stdin.write('q')
        self.now_playing.remove(p)
   
    def pause(self):
        self.now_playing[0].stdin.write('p')

    def forward(self):
        self.now_playing[0].stdin.write('right')
    def reverse(self):
        pass
    def now_playing(self):
        pass
