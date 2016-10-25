# /usr/bin/env python
# -*- coding: utf-8 -*-
import client
from universal import lazy_property


class APIResource:
    """
    A class that points to a resource that needs to be retrieved from the
    API. 

    Attributes:
        url (str)
            The url of the resource the object points to.
        resource_type (str)
            The type of resource the object points to.
        id (str)
            The id of the resource.
        resource (property)
            When first requested, calls the API for the resource the object points
            to. It is cached and returned.
    """

    def __init__(self, url, resource_type=None):
        self.url = url
        self.resource_type = resource_type if resource_type \
            else self.url.split('/')[-3]
        self.id = self.url.split('/')[-2]

    # The API
    @lazy_property
    def resource(self):
        poke_client = client.PokemonClient()
        resource = getattr(poke_client, 
                           'get_' + self.resource_type)(uid=self.id)
        return resource


class Description:
    """
    A class containing a description of a resource in a given language
        Fields:
            description (str)
                The localized description for an API resource in a specific
                language
            language (NamedAPIResource -> Language)
                The language this name is in
    """

    def __init__(self, **kwargs):
        self.description = kwargs['description']
        self.language = NamedAPIResource(**kwargs['language'])


class Effect:
    """
    A class containing an effect description in a given langauge
        Fields:
            effect (str)
                The localized effect text for an API resource in a specific
                language
            language (NamedAPIResource -> Language)
                The language this effect is in
    """

    def __init__(self, **kwargs):
        self.effect = kwargs['effect']
        self.language = NamedAPIResource(**kwargs['language'])


class Encounter:
    """
    A class describing a possible wild pokemon encounter.
        Fields:
            min_level (int)
                The lowest level the Pokémon could be encountered at
            max_level (int)
                The highest level the Pokémon could be encountered at
            condition_values (list of
            NamedAPIResource -> EncounterConditionValue)
                A list of condition values that must be in effect for this
                encounter to occur
    """

    def __init__(self, **kwargs):
        self.min_level = kwargs['min_level']
        self.max_level = kwargs['max_level']
        self.condition_values = NamedAPIResource(**kwargs['condition_Values'])
        self.chance = kwargs['chance']
        self.method = NamedAPIResource(**kwargs['method'])


class FlavorText:
    """
    A class containing flavor text in a given language
        Fields:
            flavor_text (str)
                The localized flavor text for an API resource in a specific
                language
            language (NamedAPIResource -> Language)
                The language this name is in
    """

    def __init__(self, **kwargs):
        self.flavor_text = kwargs['flavor_text']
        self.language = NamedAPIResource(**kwargs['language'])


class GenerationGameIndex:
    """
    A class
    """

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