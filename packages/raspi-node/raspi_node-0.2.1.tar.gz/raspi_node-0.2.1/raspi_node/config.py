from typing import Any
import os
import json
from uuid import getnode
from string import ascii_letters
from random import choice


# define the main class
class ConfigManager:
    def __init__(self, path: str = './config.json'):
        # set the path
        self.path = path

        # check if it exists
        if not os.path.exists(path):
            ConfigManager.create(path)

        # read the file and load all settings
        conf = self.read()

        # directly set the with super
        for key, value in conf.items():
            super(ConfigManager, self).__setattr__(key, value)
    
    def read(self) -> dict:
        with open(self.path, 'r') as f:
            return json.load(f)
    
    def update(self, **kwargs) -> None:
        # get the conf
        conf = self.read()

        # update
        conf.update(kwargs)

        # save 
        with open(self.path, 'w') as f:
            json.dump(conf, f, indent=4)
    
    def get(self, key: str, default=None):
        if not hasattr(self, key):
            return None
        else:
            return getattr(self, key)
    
    def __setattr__(self, name: str, value: Any) -> None:
        # update - this can be intercepted by validating 
        if name != 'path':
            self.update(**{name: value})
        super(ConfigManager, self).__setattr__(name, value)

    @classmethod
    def from_file(cls, config_path: str) -> 'ConfigManager':
        """Create a new ConfigManager from a config file"""
        Config = ConfigManager(path=config_path)
        return Config

    @classmethod
    def create(cls, config_path: str, **kwargs) -> 'ConfigManager':
        """
        Create a new config file.
        A set of default values will be updated by the
        kwargs and then written to the file
        """
        # set some defaults
        kwargs.setdefault('data_path', os.path.join(os.path.expanduser('~'), '.raspi_data'))
        kwargs.setdefault('MAC', hex(getnode()))

        kwargs.setdefault('wifi_mode', 'ap')
        kwargs.setdefault('wifi_ssid', f"Raspi_Node_{kwargs['MAC'][-4:]}")
        kwargs.setdefault('wifi_password', ''.join([choice(ascii_letters) for _ in range(16)]))

        # create folder and file
        if not os.path.exists(kwargs['data_path']):
            os.makedirs(kwargs['data_path'])

        with open(config_path, 'w') as f:
            json.dump(kwargs, f, indent=4)
        
        return cls.from_file(config_path)


# initialize the default instance
Config = ConfigManager(os.path.abspath(os.path.join(os.path.dirname(__file__), 'config.json')))
