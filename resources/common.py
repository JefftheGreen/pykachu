# /usr/bin/env python
# -*- coding: utf-8 -*-
import client
from universal import lazy_property


class APIResource:

    def __init__(self, url, resource_type=None):
        self.url = url
        self.resource_type = resource_type if resource_type \
            else self.url.split('/')[-3]
        self.id = self.url.split('/')[-2]

    @lazy_property
    def resource(self):
        poke_client = client.PokemonClient()
        resource =  getattr(poke_client,
                            'get_' + self.resource_type)(uid=self.id)
        return resource


class Description:

    def __init__(self, **kwargs):
        self.description = kwargs['description']
        self.language = NamedAPIResource(**kwargs['language'])


class Effect:

    def __init__(self, **kwargs):
        self.effect = kwargs['effect']
        self.language = NamedAPIResource(**kwargs['language'])


class Encounter:

    def __init__(self, **kwargs):
        self.min_level = kwargs['min_level']
        self.max_level = kwargs['max_level']
        self.condition_values = NamedAPIResource(**kwargs['condition_Values'])
        self.chance = kwargs['chance']
        self.method = NamedAPIResource(**kwargs['method'])


class FlavorText:

    def __init__(self, **kwargs):
        self.flavor_text = kwargs['flavor_text']
        self.language = NamedAPIResource(**kwargs['language'])


class GenerationGameIndex:

    def __init__(self, **kwargs):
        self.index = kwargs['index']
        self.generation = NamedAPIResource(**kwargs['generation'])


class MachineVersionDetail:

    def __init__(self, **kwargs):
        self.machine = APIResource(**kwargs['machine'])
        self.version_group = NamedAPIResource(**kwargs['version_group'])


class Name:

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.language = NamedAPIResource(**kwargs['language'])


class NamedAPIResource(APIResource):

    def __init__(self, name, url, resource_type=None):
        self.name = name
        super().__init__(url, resource_type)


class VerboseEffect:

    def __init__(self, **kwargs):
        self.effect = kwargs['effect']
        self.short_effect = kwargs['short_effect']
        self.language = NamedAPIResource(**kwargs['language'])


class VersionEncounterDetail:

    def __init__(self, **kwargs):
        self.version = NamedAPIResource(**kwargs['version'])
        self.max_chance = kwargs['max_chance']
        self.encounter_details = [Encounter(**encounter)
                                  for encounter in kwargs['encounter_details']]


class VersionGameIndex:

    def __init__(self, **kwargs):
        self.game_index = kwargs['game_index']
        self.version = NamedAPIResource(**kwargs['version'])


class VersionGroupFlavorText:

    def __init__(self, **kwargs):
        self.text = kwargs['text']
        self.language = NamedAPIResource(**kwargs['language'])
        self.version_group = NamedAPIResource(**kwargs['version_group'])


class EffectChange:

    def __init__(self, **kwargs):
        self.effect_entries = [Effect(**entry)
                               for entry in kwargs['effect_entries']]
        self.version_group = NamedAPIResource(**kwargs['version_group'])