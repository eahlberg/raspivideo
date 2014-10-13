import os
import os.path
import ConfigParser


class Config:
    """
    Class for persisting settings such as path, last played movie, running time.
    """
    def __init__(self):
        self.path = os.getcwd() + '/app'
        self.cfg_path = self.path + '/settings.cfg'
        self.last_played = 'none'
        self.running_time = 'none'
        if not os.path.isfile(self.cfg_path):
            print '[APP] no config found, creating settings.cfg'
            parser = ConfigParser.SafeConfigParser()
            parser.add_section('info')
            parser.set('info', 'path', self.path)
            parser.set('info', 'config path', self.cfg_path)
            parser.set('info', 'last played', self.last_played)
            parser.set('info', 'running time', self.running_time)
            with open(self.cfg_path, 'wb') as file:
                parser.write(file)

    def get(self, item):
        """
        Returns the value of a certain item in the config.
        """
        parser = ConfigParser.SafeConfigParser()
        parser.read(self.cfg_path)
        try:
            value = parser.get('info', item)
            return value
        except ConfigParser.NoOptionError as e:
            print e
            return None

    def add(self, item, value):
        """
        Adds a value to the config.
        """
        parser = ConfigParser.SafeConfigParser()
        parser.read(self.cfg_path)
        try:
            parser.set('info', item, value)
        except ConfigParser.NoSectionError as e:
            print e
        with open(self.cfg_path, 'wb') as file:
            parser.write(file)
