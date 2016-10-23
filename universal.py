# /usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import os
import functools

config_parser = configparser.ConfigParser()
if os.name == 'nt':
    dir = 'PykachuCache'
else:
    dir = '.PykachuCache'
default_cache_path = os.path.expanduser(
    os.path.join('~', dir)
)
default_expiration_length = 7*24 # Seven days
default_cache_size = float('inf')
default_cache_compression = True


# Returns a ConfigParser with the config file loaded
def get_config():
    config_parser.read(config_path())
    return config_parser


# Returns the path of the config file.
def config_path():
    return os.path.join(os.path.dirname(os.path.realpath(__file__)),
                        'configure',
                        'config.cnf')


# Saves the config file.
def save_config():
    with open(config_path(), 'w+') as file:
        config_parser.write(file)


# A property that caches the result to avoid querying the api more than needed.
def lazy_property(func):
    return property(functools.lru_cache()(func))