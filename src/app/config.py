import os
import os.path
import ConfigParser


class Config:
    def __init__(self):
        self.path = os.getcwd() + '/app'
        self.cfg_path = self.path + '/settings.cfg'
        self.movie_path = '/mnt/time_capsule/filmer'
        self.last_played = 'none'
        self.running_time = 'none'
        if not os.path.isfile(self.cfg_path):
            parser = ConfigParser.SafeConfigParser()
            parser.add_section('info')
            parser.set('info', 'path', self.path)
            parser.set('info', 'config path', self.cfg_path)
            parser.set('info', 'movie path', self.movie_path)
            parser.set('info', 'last played', self.last_played)
            parser.set('info', 'running time', self.running_time)
            with open(self.cfg_path, 'wb') as file:
                parser.write(file)


    def get(self, item):
        parser = ConfigParser.SafeConfigParser()
        parser.read(self.cfg_path)
        return parser.get('info', item)

    def add(self, item, value):
        parser = ConfigParser.SafeConfigParser()
        parser.read(self.cfg_path)
        try:
            parser.set('info', item, value)
        except ConfigParser.NoSectionError as e:
            print e
        with open(self.cfg_path, 'wb') as file:
            parser.write(file)



