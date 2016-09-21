# /usr/bin/env python
# -*- coding: utf-8 -*-
import resources.common
from universal import lazy_property
import resources.utility as utility


class BerryResource(utility.CacheablePropertyResource):

    yaml_tag = '!BerryResource'

    class Meta:
        name = "Berry"
        resource_name = "berry"
        cache_folder = 'berries/berries/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'growth_time',
            'max_harvest',
            'natural_gift_power',
            'size',
            'smoothness',
            'soil_dryness',
            'firmness',
            'flavors',
            'item',
            'natural_gift_type'
        )

    @lazy_property
    def firmness(self):
        return resources.common.NamedAPIResource(**self._firmness)

    @lazy_property
    def flavors(self):
        return BerryFlavorMap(**self._flavors)

    @lazy_property
    def item(self):
        return resources.common.NamedAPIResource(**self._item)

    @lazy_property
    def natural_gift_type(self):
        return resources.common.NamedAPIResource(**self._natural_gift_type)


class BerryFlavorMap:

    def __init__(self, **kwargs):
        self.potency = kwargs['potency']
        self.flavor = resources.common.NamedAPIResource(**kwargs['flavor'])

    @property
    def resource(self):
        return self.flavor.resource


class BerryFirmnessResource(utility.CacheablePropertyResource):

    yaml_tag = '!BerryFirmnessResource'

    class Meta:
        name = "Berry Firmness"
        resource_name = "berry-firmness"
        cache_folder = 'berries/firmnesses/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'berries',
            'names'
        )

    @lazy_property
    def berries(self):
        return [resources.common.NamedAPIResource(**kwargs) for kwargs in self._berries]

    @lazy_property
    def names(self):
        return [resources.common.Name(**kwargs) for kwargs in self._names]


class BerryFlavorResource(utility.CacheablePropertyResource):

    yaml_tag = '!BerryFlavorResource'

    class Meta:
        name = "Berry Flavor"
        resource_name = "berry-flavor"
        cache_folder = 'berries/flavors/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'berries',
            'contest_type',
            'names'
        )

    @lazy_property
    def berries(self):
        return [FlavorBerryMap(**kwargs) for kwargs in self._berries]

    @lazy_property
    def contest_type(self):
        return resources.common.NamedAPIResource(**self._contest_type)

    @lazy_property
    def names(self):
        return [resources.common.Name(**kwargs) for kwargs in self._names]


class FlavorBerryMap:

    def __init__(self, kwargs):
        self.potency = kwargs['potency']
        self.berry = resources.common.NamedAPIResource(**kwargs['berry'])

    @property
    def resource(self):
        return self.berry.resource