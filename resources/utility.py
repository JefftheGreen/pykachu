# /usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
from beckett import resources
import functools


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