# /usr/bin/env python
# -*- coding: utf-8 -*-

from beckett import clients
import os
import yaml
import configparser
import universal
import cache
import tempfile
from datetime import datetime, timedelta
from resources import (AbilityResource, CharacteristicResource,
                       EggGroupResource, GenderResource, GrowthRateResource,
                       NatureResource, PokeathlonStatResource,
                       PokemonColorResource, PokemonFormResource,
                       PokemonHabitatResource, PokemonShapeResource,
                       PokemonSpeciesResource, StatResource, TypeResource,
                       PokemonResource,
                       EncounterResource)

class BeckettClient(clients.BaseClient):
    class Meta:
        name = 'Pokeapi Client'
        base_url = "http://pokeapi.co/api/v2"
        resources = (
            AbilityResource,
            CharacteristicResource,
            EggGroupResource,
            GenderResource,
            GrowthRateResource,
            NatureResource,
            PokeathlonStatResource,
            PokemonColorResource,
            PokemonFormResource,
            PokemonHabitatResource,
            PokemonShapeResource,
            PokemonSpeciesResource,
            StatResource,
            TypeResource,
            PokemonResource,
            EncounterResource
        )


class PokemonClient():


    # Initialize the client.
    #   read_cache (bool):
    #       If true, the client will try to read data from the cache first.
    #       Otherwise, it will only retrieve from Pokeapi.
    #   write_cache (bool):
    #       If true, the client will write any data it retrieves from the api
    #       to the cache. Othrwise it won't.
    def __init__(self, *args, read_cache=True, write_cache=True, **kwargs):
        self.beckett_client = BeckettClient(*args, **kwargs)
        self.read = read_cache
        self.write = write_cache
        if self.read or self.write:
            #TODO: Check and/or set up map files
            if not os.path.isdir(cache.get_cache_dir()):
                os.makedirs(cache.get_cache_dir())
        self.set_attributes()

    def set_attributes(self):
        for resource in self.beckett_client.Meta.resources:
            method_name = 'get_' + resource.Meta.name.lower()
            getter = self.getter_factory(resource, method_name)
            setattr(self, method_name, getter)

    # Creates a getter for a resource
    #   resource (class):
    #       the resource class (subclass of resources.utility.CacheableResource)
    #   method_name (str):
    #       the name the method will have. Should be 'get_' followed by
    #       the resource name in lower case or the same as the method for the
    #       resource in the BeckettClient.
    def getter_factory(self, resource, method_name):
        # Where the cache is located.
        cache_dir = cache.get_cache_dir()
        # Where the resource is cached
        cache_subdir = cache_dir + resource.Meta.cache_folder
        # The method used to get the resource from Pokeapi
        beckett_method = getattr(self.beckett_client, method_name)

        # The method to get a resource.
        #   kwargs:
        #       These are the same as for the normal Beckett client.
        def get(**kwargs):
            # We need the id number, but uid can also be a name for some
            # resources.
            resource_id = self.identifier(uid=kwargs['uid'])
            # Only bother with the cache if the client is set up to read or
            # write to it.
            if self.read or self.write:
                # Make the cache directory if it doesn't exist
                if not os.path.isdir(cache_subdir):
                    os.makedirs(cache_subdir)
                # This is the file that will be read or written to.
                file_name = cache_subdir + str(resource_id)
            # We can'read unless the file actually exists
            if self.read and os.path.isfile(file_name):
                if cache.check_expiration(resource.Meta.name.lower(),
                                         resource_id):
                    os.remove(file_name)
                else:
                    return cache.read_cache(file_name)
            # There's nothing from the cache, so call Pokeapi
            beckett_result = beckett_method(**kwargs)
            # Write to the cache.
            if self.write:
                cache.write_cache(beckett_result, file_name)
                # Set the expiration date for this cached file.
                cache.set_expiration(resource.Meta.name.lower(),
                                     resource_id)
            return beckett_result

        return get

    def identifier(self, resource=None, uid=None):
        if uid:
            return uid

    def alternate_identifiers(self, category=None, id=None, resource=None):
        pass