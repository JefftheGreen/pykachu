# /usr/bin/env python
# -*- coding: utf-8 -*-

import universal
import tempfile
from datetime import timedelta, datetime
import yaml
import configparser
import os


# Returns the cache directory as a string.
def get_cache_dir():
    # if the cache directory has been set in the config file, use that.
    config = universal.get_config()
    try:
        path = config['cache']['path']
        tempfile.TemporaryFile(dir=path).close()
        return path
    # Either the cache directory wasn't set or we can't write to it, so use
    # the default
    except:
        default_path = universal.default_cache_path
        if not 'cache' in config.sections():
            config['cache'] = {}
        config['cache']['path'] = default_path
        universal.save_config()
        return default_path


# Returns the time after which a cache resource should expire.
def get_expiration_length():
    # If the cache expiration length has been set in the cache file,
    # use that.
    config = universal.get_config()
    try:
        length = config['cache']['expiration_length']
        length = timedelta(**length)
    # Eiter the cache expiration length hasn't been set or it's in an
    # inappropriate format, so use default
    except:
        default_length = universal.default_expiration_length
        # Put the default in the config file
        if not 'cache' in config.sections():
            config['cache'] = {}
        config['cache']['expiration_length'] = str(default_length)
        universal.save_config()
        return timedelta(hours=default_length)


# Reads a file from the cache
#   file_name (str)
#       the file name for the file to read.
def read_cache(file_name):
    with open(file_name, mode='r+') as file:
        cached = yaml.load(file, Loader=yaml.CSafeLoader)
    return cached


# Writes a resource to its cache file
#   result (subclass of resources.utility.CacheableResource):
#       The resource that is to be cached.
#   file_name
#       Where in the cache folder to put the resource.
def write_cache(result, file_name):
    # TODO: Make this threaded
    cached = yaml.dump_all([result], Dumper=yaml.CSafeDumper)
    with open(file_name, mode='w+') as file:
        print(cached, file=file)


# Set the expiration date for a cached resource.
#   category (str):
#       the category (name of resource class) the resource belongs to.
#   id (integer):
#       the id of the cached resource.
def set_expiration(category, id):
    # Make the expiration catalog if it doesn't exist
    if not os.path.isfile(get_cache_dir() + 'expiration.cnf'):
        open(get_cache_dir() + 'expiration.cnf', 'a').close()
    # Load the expiration catalog
    parser = configparser.ConfigParser()
    file_path = get_cache_dir() + 'expiration.cnf'
    parser.read(file_path)
    # The expiration date is a fixed distance into the future.
    date = datetime.now() + get_expiration_length()
    # Set the date in the catalog
    if category not in parser:
        parser[category] = {}
    parser[category][str(id)] = datetime.isoformat(date, sep=':')
    with open(file_path, 'w+') as expir_file:
        parser.write(expir_file)


# Finds whether cached resource is expired
#   category (str):
#       the category (name of resource class) the resource belongs to.
#   id (integer):
#       the id of the cached resource.
def check_expiration(category, id):
    # If the expiration catalog doesn't exist, nothing can be expired
    if not os.path.isfile(get_cache_dir() + 'expiration.cnf'):
        return False
    # Read the catalo
    parser = configparser.ConfigParser()
    parser.read(get_cache_dir() + 'expiration.cnf')
    if category in parser.sections():
        # The resource has to be in the catalog to be expired.
        if str(id) in parser[category]:
            # Parse the date from a string.
            expir_date = parser[category][str(id)]
            expir_date = datetime.strptime(expir_date,
                                           '%Y-%m-%d:%H:%M:%S.%f')
            # It's expired if the current date is after the expiration date
            if datetime.now() > expir_date:
                return True
    return False