# /usr/bin/env python
# -*- coding: utf-8 -*-

import yaml
try:
    from yaml import CSafeLoader as YAMLLoader
    from yaml import CSafeDumper as YAMLDumper
except ImportError:
    print("Can't find yaml.CSafeLoader. Libyaml is probably not installed. " +
          "Using pure Python loader and dumper.")
    from yaml import SafeLoader as YAMLLoader
    from yaml import SafeDumper as YAMLDumper
from beckett import resources
from resources.common import lazy_property
import resources.common as common
import collections


class CacheableResource(resources.BaseResource, yaml.YAMLObject):

    yaml_loader = YAMLLoader
    yaml_dumper = YAMLDumper

    @staticmethod
    def get_url(url, **kwargs):
        if 'from_url' in kwargs:
            return kwargs['from_url']
        return '{}/{}/'.format(url, kwargs.get('uid'))


class PropertyResource(resources.BaseResource):

    @staticmethod
    def get_method_name(resource, method_type):
        """
        Generate a method name for this resource based on the method type.

        The Beckett BaseResource class doesn't handle spaces in resource names.
        This fixes that.
        """
        return resources.BaseResource.get_method_name(resource,
                                                      method_type).replace(' ',
                                                                           '_')

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


class ResourceWithCommonMethods(resources.BaseResource):

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

    @lazy_property
    def pokemon_species_by_name(self):
        if hasattr(self, 'pokemon_species'):
            return {species.name: species for species in self.pokemon_species}
        else:
            raise AttributeError(
                "'{}' object has no attribute 'pokemon_species_by_name'".format(
                    type(self))
            )

    @lazy_property
    def pokemon_species_by_id(self):
        if hasattr(self, 'pokemon_species'):
            return {species.id: species for species in self.pokemon_species}
        else:
            raise AttributeError(
                "'{}' object has no attribute 'pokemon_species_by_name'".format(
                    type(self))
            )

    @lazy_property
    def version_groups(self):
        if hasattr(self, '_version_groups'):
            return [common.NamedAPIResource(**kwargs)
                for kwargs in self._version_groups]
        else:
            raise AttributeError(
                "'{}' object has no attribute 'version_groups'".format(
                    type(self))
            )

    @lazy_property
    def moves(self):
        if hasattr(self, '_moves'):
            return [common.NamedAPIResource(**kwargs) for kwargs in self._moves]
        else:
            raise AttributeError(
                "'{}' object has no attribute 'moves'".format(type(self))
            )


class UtilityResource(PropertyResource, CacheableResource,
                      ResourceWithCommonMethods):

    pass


class LanguageResource(CacheableResource):
    yaml_tag = '!LanguageResource'

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