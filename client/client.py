# /usr/bin/env python
# -*- coding: utf-8 -*-

from beckett import clients
import os
import cache
from resources import (
    AbilityResource,
    BerryResource,
    BerryFirmnessResource,
    BerryFlavorResource,
    CharacteristicResource,
    ContestTypeResource,
    ContestEffectResource,
    EggGroupResource,
    EncounterMethodResource,
    EncounterConditionResource,
    EncounterConditionValueResource,
    EvolutionChainResource,
    EvolutionTriggerResource,
    GenderResource,
    GenerationResource,
    GrowthRateResource,
    ItemResource,
    ItemAttributeResource,
    ItemCategoryResource,
    ItemFlingEffectResource,
    ItemPocketResource,
    LocationResource,
    LocationAreaResource,
    MachineResource,
    MoveResource,
    MoveAilmentResource,
    MoveBattleStyleResource,
    MoveCategoryResource,
    MoveDamageClassResource,
    MoveLearnMethodResource,
    MoveTargetsResource,
    NatureResource,
    PalParkAreaResource,
    PokeathlonStatResource,
    PokedexResource,
    PokemonResource,
    PokemonColorResource,
    PokemonFormResource,
    PokemonHabitatResource,
    PokemonShapeResource,
    PokemonSpeciesResource,
    RegionResource,
    StatResource,
    SuperContestEffectResource,
    TypeResource,
    VersionResource,
    VersionGroupResource
)


class BeckettClient(clients.BaseClient):
    class Meta:
        name = 'Pokeapi Client'
        base_url = "http://pokeapi.co/api/v2"
        resources = (
            AbilityResource,
            BerryResource,
            BerryFirmnessResource,
            BerryFlavorResource,
            CharacteristicResource,
            ContestTypeResource,
            ContestEffectResource,
            EggGroupResource,
            EncounterMethodResource,
            EncounterConditionResource,
            EncounterConditionValueResource,
            EvolutionChainResource,
            EvolutionTriggerResource,
            GenderResource,
            GenerationResource,
            GrowthRateResource,
            ItemResource,
            ItemAttributeResource,
            ItemCategoryResource,
            ItemFlingEffectResource,
            ItemPocketResource,
            LocationResource,
            LocationAreaResource,
            MachineResource,
            MoveResource,
            MoveAilmentResource,
            MoveBattleStyleResource,
            MoveCategoryResource,
            MoveDamageClassResource,
            MoveLearnMethodResource,
            MoveTargetsResource,
            NatureResource,
            PalParkAreaResource,
            PokeathlonStatResource,
            PokedexResource,
            PokemonResource,
            PokemonColorResource,
            PokemonFormResource,
            PokemonHabitatResource,
            PokemonShapeResource,
            PokemonSpeciesResource,
            RegionResource,
            StatResource,
            SuperContestEffectResource,
            TypeResource,
            VersionResource,
            VersionGroupResource
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
            cache.set_up()
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
                read_result = cache.read_cache(
                    category=resource.Meta.name.lower(),
                    id=resource_id, file_name=file_name)
                if read_result:
                    return read_result
            # There's nothing from the cache, so call Pokeapi
            beckett_result = beckett_method(**kwargs)
            # Write to the cache.
            if self.write:
                cache.write_cache(beckett_result,
                                  category=resource.Meta.name.lower(),
                                  id=resource_id,
                                  file_name=file_name)
            return beckett_result

        return get

    def identifier(self, resource=None, uid=None):
        if uid:
            return uid

    def alternate_identifiers(self, category=None, id=None, resource=None):
        pass