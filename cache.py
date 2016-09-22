# /usr/bin/env python
# -*- coding: utf-8 -*-

import universal
import tempfile
from datetime import timedelta, datetime
import yaml
import yaml.reader
import configparser
import os
import gzip


def set_up():
    if not os.path.isdir(get_cache_dir()):
        os.makedirs(get_cache_dir())
    # Make the expiration catalog if it doesn't exist
    if not os.path.isfile(get_cache_dir() + 'expiration.cnf'):
        open(get_cache_dir() + 'expiration.cnf', 'a').close()
    # Make the path catalog if it doesn't exist
    if not os.path.isfile(get_cache_dir() + 'paths.cnf'):
        open(get_cache_dir() + 'paths.cnf', 'a').close()


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
        length = timedelta(hours=default_length)
    return length


# Returns the maximum size of the cache. Client and clean() will delete older
# files to reduce the size of the cache to the maximum size or smaller
def get_max_size():
    # If the max_size has been set in the cache file, use that.
    config = universal.get_config()
    try:
        size = int(config['cache']['max_size'])
        assert size > 0
    # Either the cache max size hasn't been set, it's not numeric, or it's
    # <= 0
    except:
        default_size = universal.default_cache_compression
        # Put the default in the config file
        if not 'cache' in config.sections():
            config['cache'] = {}
        config['cache']['compression'] = str(default_size)
        universal.save_config()
        size = default_size
    return size

def get_size():
    return 0
    # TODO: function that gets total size of cache


# Returns whether the cache files should be compressed.
def get_compression():
    # If the max_size has been set in the cache file, use that.
    config = universal.get_config()
    try:
        compression = config['cache']['compression']
        assert compression in ['True', 'False']
        compression = bool(compression)
    # Either the cache max size hasn't been set, it's not numeric, or it's
    # <= 0
    except:
        default_compression = universal.default_cache_compression
        # Put the default in the config file
        if not 'cache' in config.sections():
            config['cache'] = {}
        config['cache']['compression'] = str(default_compression)
        universal.save_config()
        compression = default_compression
    return compression



# Reads a file from the cache
#   category (str):
#       the category (name of resource class) the resource belongs to.
#   id (integer):
#       the id of the cached resource.
#   file_name (str)
#       the file name for the file to read.
# Either category and id or file_name must be provided
# Returns either the contents of the cache file (usually a list of a
# resource type with one member) or, if the file can't be read or doesn't
# exist, None.
def read_cache(category=None, id=None, file_name=None):
    if check_expiration(category, id):
        os.remove(file_name)
        return None
    if not file_name:
        file_name = get_file_path(category, id)
    # if our cache setting is to compress, assume the file is compressed
    if get_compression():
        try:
            with gzip.open(file_name, mode='rb') as file:
                cached = yaml.load(file.read(), Loader=yaml.CSafeLoader)
        except FileNotFoundError:
            return None
        # The file isn't compressed or is corrupted
        except OSError:
            try:
                with open(file_name, mode='r+') as file:
                    cached = yaml.load(file, Loader=yaml.CSafeLoader)
            except yaml.reader.ReaderError:
                return None
    # Our cache setting is to not compress, so assume the file isn't compressed
    else:
        try:
            with open(file_name, mode='r+') as file:
                cached = yaml.load(file, Loader=yaml.CSafeLoader)
        except FileNotFoundError:
            return None
        # The file is either compressed (hopefully) or is corrupted
        except yaml.reader.ReaderError:
            try:
                with gzip.open(file_name, mode='rb') as file:
                    cached = yaml.load(file.read(), Loader=yaml.CSafeLoader)
            except yaml.reader.ReaderError:
                return None
    return cached


# Writes a resource to its cache file
#   category (str):
#       the category (name of resource class) the resource belongs to.
#   id (integer):
#       the id of the cached resource.
#   result (subclass of resources.utility.CacheableResource):
#       The resource that is to be cached.
#   file_name
#       Where in the cache folder to put the resource.
# Either category and id or file_name must be provided. Category and id only
# work if the file already exists and is being rewritten
def write_cache(resource, category=None, id=None, file_name=None):
    if not file_name:
        file_name = get_file_path(category, id)
    # TODO: Make this threaded
    print(file_name)
    cached = yaml.dump_all([resource], Dumper=yaml.CSafeDumper)
    if get_compression():
        with gzip.open(file_name, mode='wb', compresslevel=6) as file:
            file.write(cached.encode())
    else:
        with open(file_name, mode='w+') as file:
            print(cached, file=file)
    if not (category and id):
        category = resource.Meta.name.lower()
        id = resource.id
    set_expiration(category, id)
    # If we've gone over the maximum size, clean the cache to reduce it.
    if get_size() > get_max_size():
        clean()

def get_file_path(category, id):
    # If the path catalog doesn't exist, nothing has a path
    if not os.path.isfile(get_cache_dir() + 'paths.cnf'):
        return None
    # Read the catalog
    parser = configparser.ConfigParser()
    parser.read(get_cache_dir() + 'paths.cnf')
    if category in parser.sections():
        # Check that the file exists in the path catalog.
        if str(id) in parser[category]:
            # Parse the date from a string.
            path = parser[category][str(id)]
            # check that the file actually exists at that path
            if os.path.isfile(path):
                return path
            else:
                return None
    return None

def set_file_path(category, id, path):
    cache_dir = get_cache_dir()
    # Make the path catalog if it doesn't exist
    if not os.path.isfile(get_cache_dir() + 'paths.cnf'):
        open(cache_dir + 'paths.cnf', 'a').close()
    # Load the expiration catalog
    parser = configparser.ConfigParser()
    file_path = cache_dir + 'paths.cnf'
    parser.read(file_path)
    # If the path doesn't include the cache directory, add it on
    if not cache_dir in path:
        path = cache_dir + path
    # Check that the file actually exists
    if not os.path.isfile(path):
        raise AttributeError('File {} cannot be found.'.format(path))
    # Set the path in the catalog
    if category not in parser:
        parser[category] = {}
    parser[category][str(id)] = path
    with open(file_path, 'w+') as expir_file:
        parser.write(expir_file)


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
    expiration = get_expiration(category, id)
    if expiration:
        if datetime.now() > expiration:
            return True
    return False

def get_expiration(category, id):
    # If the expiration catalog doesn't exist, nothing can be expired
    if not os.path.isfile(get_cache_dir() + 'expiration.cnf'):
        None
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
            return expir_date
    return None

def get_file_size(category, id):
    return os.stat(get_file_path(category, id)).st_size

def clean():
    # First, collect all files while removing expired ones
    all_files = []
    paths_parser = configparser.ConfigParser()
    paths_parser.read(get_cache_dir() + 'paths.cnf')
    # Loop through each file stored in the paths category
    for category in paths_parser.sections():
        for id in paths_parser[category]:
            path = paths_parser[category][str(id)]
            # If the file actually exists, add it to the list of files to
            # manage
            if os.path.exists(path):
                # The file is expired, so remove it
                if check_expiration(category, id):
                    remove_file(category, id, path)
                else:
                    size = get_size(category, id)
                    expiration = get_expiration(category, id)
                    all_files.append({'category': category,
                                      'id': id,
                                      'path': path,
                                      'size': size,
                                      'expiration' :expiration})
            # The file doesn't exist, so remove it from the paths catalog
            else:
                paths_parser.remove_option(category, id)
    size = get_size()
    max_size = get_max_size()
    # We've gone over our size limit, so remove in order of expiration date
    # (soonest to latest)
    if size > max_size:
        total_removed = 0
        # Sort by expiration date
        all_files.sort(key=lambda x: x['expiration'])
        target_size = size - max_size
        for file in all_files:
            remove_file(file['category'], file['id'], file['path'])
            total_removed += file['size']
            # We've removed enough files, so no need to continue
            if total_removed >= target_size:
                break
    known_paths = [file['path'] for file in all_files]
    # Now remove uncatalogued files.
    # Loop through all files in cache directory.
    for root, dirs, files in os.walk(get_cache_dir()):
        for file in files:
            file_path = os.path.join(root, file)
            # If the file isn't in the paths catalog we can't find it,
            # so remove it.
            if not file_path in known_paths:
                os.remove(file_path)
    # Finally, remove expiration entries to non-existent files
    if os.path.isfile(get_cache_dir() + 'expiration.cnf'):
        expiration_parser = configparser.ConfigParser()
        # Loop through expiration entries
        for category in expiration_parser.sections():
            if not category in paths_parser.sections():
                expiration_parser.remove_section(category)
            for id in expiration_parser[category]:
                if not id in paths_parser[category]:
                    expiration_parser.remove_option(category, id)


# Removes a file and all references to it in the catalogs.
#   category (str):
#       the category (name of resource class) the resource belongs to.
#   id (integer):
#       the id of the cached resource.
#   path=None (str):
#       the path to the file. If None, the path will be determined from the
#       category and id.
def remove_file(category, id, path=None):
    path_parser = configparser.ConfigParser()
    path_parser.read(get_cache_dir() + 'paths.cnf')
    expiration_parser = configparser.ConfigParser()
    expiration_parser.read(get_cache_dir() + 'expiration.cnf')
    # Get the path from the paths catalog if it wasn't provided
    if not path:
        path = path_parser[category][str(id)]
    # Remove the file from the path catalog
    if category in path_parser.sections():
        path_parser.remove_option(category, str(id))
    # Remove the file from the expiration catalog
    if category in expiration_parser.sections():
        expiration_parser.remove_option(category, str(id))
    # Remove the actual file from the cache
    if os.path.isfile(path):
        os.remove(path)

