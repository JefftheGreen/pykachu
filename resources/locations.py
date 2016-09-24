# /usr/bin/env python
# -*- coding: utf-8 -*-

import resources.common as common
from universal import lazy_property
import resources.utility as utility


class LocationResource(utility.CacheablePropertyResource):

    yaml_tag = '!LocationResource'

    class Meta:
        name = "Location"
        resource_name = "location"
        cache_folder = 'locations/locations/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'region',
            'names',
            'game_indices',
            'areas'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def region(self):
        return common.NamedAPIResource(**self._region)

    @lazy_property
    def game_indices(self):
        return [common.GenerationGameIndex(**kwargs)
                for kwargs in self._game_indices]

    @lazy_property
    def areas(self):
        return [common.NamedAPIResource(**kwargs) for kwargs in self._areas]


class LocationAreaResource(utility.CacheablePropertyResource):

    yaml_tag = '!LocationAreaResource'

    class Meta:
        name = "Location Area"
        resource_name = "location-area"
        cache_folder = 'locations/area/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'game_index',
            'encounter_method_rates',
            'location',
            'pokemon_encounters'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def encounter_method_rates(self):
        return [EncounterMethodRate(**kwargs)
                for kwargs in self._encounter_method_rates]

    @lazy_property
    def location(self):
        return common.NamedAPIResource(**self._location)

    @lazy_property
    def pokemon_encounters(self):
        return [PokemonEncounter(**kwargs)
                for kwargs in self._pokemon_encounters]


class EncounterMethodRate:

    def __init__(self, **kwargs):
        self.encounter_method = common.NamedAPIResource(
            **kwargs['encounter_method'])
        self.version_details = [EncounterVersionDetail(**deet)
                                for deet in kwargs['version_Details']]


class EncounterVersionDetail:

    def __init__(self, **kwargs):
        self.rate = kwargs['rate']
        self.version = common.NamedAPIResource(**kwargs['version'])


class PokemonEncounter:

    def __init__(self, **kwargs):
        self.pokemon = common.NamedAPIResource(**kwargs['pokemon'])
        self.version_details = [common.VersionEncounterDetail(**deet)
                                for deet in kwargs['version_details']]


class PalParkAreaResource(utility.CacheablePropertyResource):

    yaml_tag = '!Pa;ParkAreaResource'

    class Meta:
        name = "Pal Park Area"
        resource_name = "pal-park-area"
        cache_folder = 'locations/pal-park-areas/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'names',
            'pokemon_encounters'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def pokemon_encounters(self):
        return [PalParkEncounterSpecies(**kwargs)
                for kwargs in self._pokemon_encounters]


class PalParkEncounterSpecies:

    def __init__(self, **kwargs):
        self.base_score = kwargs['base_score']
        self.rate = kwargs['rate']
        self.pokemon_species = common.NamedAPIResource(
            **kwargs['pokemon_species'])


class RegionResource(utility.CacheablePropertyResource):

    yaml_tag = '!RegionResource'

    class Meta:
        name = "Region"
        resource_name = "region"
        cache_folder = 'locations/regions/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'locations',
            'main_generation',
            'names',
            'pokedexes',
            'version_groups'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def locations(self):
        return [common.NamedAPIResource(**kwargs) for kwargs in self._locations]

    @lazy_property
    def main_generation(self):
        return common.NamedAPIResource(**self._main_generation)

    @lazy_property
    def pokedexes(self):
        return [common.NamedAPIResource(**kwargs) for kwargs in self._pokedexes]

    @lazy_property
    def version_groups(self):
        return [common.NamedAPIResource(**kwargs)
                for kwargs in self._version_groups]
