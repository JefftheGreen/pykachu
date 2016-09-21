# /usr/bin/env python
# -*- coding: utf-8 -*-
import resources.common
from universal import lazy_property
import resources.utility as utility


class GenerationResource(utility.CacheablePropertyResource):

    yaml_tag = '!GenerationResource'

    class Meta:
        name = "Generation"
        resource_name = "generation"
        cache_folder = 'games/generations/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'abilities',
            'names',
            'main_region',
            'moves',
            'pokemon_species',
            'types',
            'version_groups'
        )

    @lazy_property
    def abilities(self):
        return [resources.common.NamedAPIResource(**kwargs)
                for kwargs in self._abilities]

    @lazy_property
    def names(self):
        return [resources.common.Name(**kwargs) for kwargs in self._names]

    @lazy_property
    def main_region(self):
        return resources.common.NamedAPIResource(**self._main_region)

    @lazy_property
    def moves(self):
        return [resources.common.NamedAPIResource(**kwargs) for kwargs in self._moves]

    @lazy_property
    def pokemon_species(self):
        return [resources.common.NamedAPIResource(**kwargs)
                for kwargs in self._pokemon_species]

    @lazy_property
    def types(self):
        return [resources.common.NamedAPIResource(**kwargs) for kwargs in self._types]

    @lazy_property
    def version_groups(self):
        return [resources.common.NamedAPIResource(**kwargs)
                for kwargs in self._version_groups]


class PokedexResource(utility.CacheablePropertyResource):

    yaml_tag = '!PokedexResource'

    class Meta:
        name = "Pokedex"
        resource_name = "pokedex"
        cache_folder = 'games/pokedexes/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'is_main_series',
            'descriptions',
            'names',
            'pokemon_entries',
            'region',
            'version_groups'
        )

    @lazy_property
    def descriptions(self):
        return [resources.common.Description(**kwargs) for kwargs in self._descriptions]

    @lazy_property
    def names(self):
        return [resources.common.Name(**kwargs) for kwargs in self._names]

    @lazy_property
    def pokemon_entries(self):
        return [PokemonEntry(**kwargs) for kwargs in self._pokemon_entries]

    @lazy_property
    def region(self):
        return resources.common.NamedAPIResource(**self._region)

    @lazy_property
    def version_groups(self):
        return [resources.common.NamedAPIResource(**kwargs)
                for kwargs in self._version_groups]


class PokemonEntry:

    def __init__(self, **kwargs):
        self.entry_number = kwargs['entry_number']
        self.pokemon_species = kwargs['pokemon_species']


class VersionResource(utility.CacheablePropertyResource):

    yaml_tag = '!VersionResource'

    class Meta:
        name = "Version"
        resource_name = "version"
        cache_folder = 'games/versions/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'names',
            'version_group'
        )

    @lazy_property
    def names(self):
        return [resources.common.Name(**kwargs) for kwargs in self._names]

    @lazy_property
    def version_group(self):
        return resources.common.NamedAPIResource(self._version_group)


class VersionGroupResource(utility.CacheablePropertyResource):

    yaml_tag = '!VersionGroupResource'

    class Meta:
        name = "Version Group"
        resource_name = "version-group"
        cache_folder = 'games/version-groups/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'order',
            'generation',
            'move_learn_methods',
            'pokedexes',
            'regions',
            'versions'
        )

    @lazy_property
    def generation(self):
        return resources.common.NamedAPIResource(**self._generation)

    @lazy_property
    def move_learn_methods(self):
        return [resources.common.NamedAPIResource(**kwargs)
                for kwargs in self._move_learn_methods]

    @lazy_property
    def pokedexes(self):
        return [resources.common.NamedAPIResource(**kwargs)
                for kwargs in self._pokedexes]

    @lazy_property
    def regions(self):
        return [resources.common.NamedAPIResource(**kwargs) for kwargs in self._regions]

    @lazy_property
    def versions(self):
        return [resources.common.NamedAPIResource(**kwargs) for kwargs in self._versions]
