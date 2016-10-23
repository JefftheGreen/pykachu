# /usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
from beckett import resources
from resources.common import lazy_property
import resources.common as common
import collections


class CacheableResource(resources.BaseResource, yaml.YAMLObject):

    yaml_loader = yaml.CSafeLoader
    yaml_dumper = yaml.CSafeDumper

    @staticmethod
    def get_url(url, **kwargs):
        if 'from_url' in kwargs:
            return kwargs['from_url']
        return '{}/{}/'.format(url, kwargs.get('uid'))


class PropertyResource(resources.BaseResource):

    attr_docs = collections.defaultdict(lambda: 'My docstring.')

    def set_attributes(self, **kwargs):
        """
        Set the resource attributes from the kwargs.
        Only sets items in the `self.Meta.attributes` white list.
        Subclass this method to customise attributes.
        Args:
            kwargs: Keyword arguments passed into the init of this class
        """
        if self._subresource_map:
            self.set_subresources(**kwargs)
            for key in self._subresource_map.keys():
                # Don't let these attributes be overridden later
                kwargs.pop(key, None)
        for field, value in kwargs.items():
            if field in self.Meta.attributes:
                if field in dir(self):
                    field_name = "_" + field
                else:
                    field_name = field
                setattr(self, field_name, value)



class CacheablePropertyResource(PropertyResource, CacheableResource):

    @lazy_property
    def names(self):
        if hasattr(self, '_names'):
            return [common.Name(**kwargs) for kwargs in self._names]
        else:
            raise AttributeError(
                "'{}' object has no attribute 'names'".format(type(self))
            )

    @lazy_property
    def descriptions(self):
        if hasattr(self, '_descriptions'):
            return [common.Description(**kwargs)
                    for kwargs in self._descriptions]
        else:
            raise AttributeError(
                "'{}' object has no attribute 'descriptions'".format(type(self))
            )


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