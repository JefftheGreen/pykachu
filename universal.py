# /usr/bin/env python
# -*- coding: utf-8 -*-

import configparser
import os

config_parser = configparser.ConfigParser()
default_cache_path = os.path.expanduser('~/.PykachuCache/')
default_expiration_length = 7*24 # Seven days
import functools

def get_config():
    config_parser.read(config_path())
    return config_parser

def config_path():
    return os.path.dirname(os.path.realpath(__file__)) + '/configure/config.cnf'

def save_config():
    with open(config_path(), 'w+') as file:
        config_parser.write(file)

def lazy_property(func):
    return property(functools.lru_cache()(func))