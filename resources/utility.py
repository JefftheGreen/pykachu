# /usr/bin/env python
# -*- coding: utf-8 -*-

from beckett import resources
import client
import yaml
from universal import lazy_property

class CacheableResource(resources.BaseResource, yaml.YAMLObject):

    yaml_loader = yaml.CSafeLoader
    yaml_dumper = yaml.CSafeDumper

    @staticmethod
    def get_url(url, **kwargs):
        if 'from_url' in kwargs:
            return kwargs['from_url']
        return '{}/{}/'.format(url, kwargs.get('uid'))


class PropertyResource(resources.BaseResource):

    def set_attributes(self, **kwargs):
        """
        Set the resource attributes from the kwargs.
        Only sets items in the `self.Meta.attributes` white list.
        Subclass this method to customise attributes.
        Args:
            kwargs: Keyword arguements passed into the init of this class
        """
        if self._subresource_map:
            self.set_subresources(**kwargs)
            for key in self._subresource_map.keys():
                # Don't let these attributes be overridden later
                kwargs.pop(key, None)
        for field, value in kwargs.items():
            if field in self.Meta.attributes:
                if field in dir(self):
                    setattr(self, "_" + field, value)
                    setattr(self, field + "__cached", None)
                else:
                    setattr(self, field, value)


class CacheablePropertyResource(PropertyResource, CacheableResource):

    pass


class LanguageResource(CacheableResource):
    yaml_tag = '!PokemonResource'

    class Meta:
        name = 'Language'
        resource_name = 'language'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'official',
            'iso639',
            'iso3166',
            'names'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )


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


class NamedAPIResource(APIResource):

    def __init__(self, name, url, resource_type=None):
        self.name = name
        super().__init__(url, resource_type)


class VersionEncounterDetail:
    pass


class VersionGameIndex:

    def __init__(self, **kwargs):
        self.game_index = kwargs['game_index']
        self.version = NamedAPIResource(**kwargs['version'])


class Name:

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.language = NamedAPIResource(**kwargs['language'])


class Effect:

    def __init__(self, **kwargs):
        self.effect = kwargs['effect']
        self.language = NamedAPIResource(**kwargs['language'])


class VerboseEffect:

    def __init__(self, **kwargs):
        self.effect = kwargs['effect']
        self.short_effect = kwargs['short_effect']
        self.language = NamedAPIResource(**kwargs['language'])


class Description:

    def __init__(self, **kwargs):
        self.description = kwargs['description']
        self.language = NamedAPIResource(**kwargs['language'])


class GenerationGameIndex:

    def __init__(self, **kwargs):
        self.index = kwargs['index']
        self.generation = NamedAPIResource(**kwargs['generation'])


class FlavorText:

    def __init__(self, **kwargs):
        self.flavor_text = kwargs['flavor_text']
        self.language = NamedAPIResource(**kwargs['language'])