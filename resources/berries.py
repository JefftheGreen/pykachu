# /usr/bin/env python
# -*- coding: utf-8 -*-
import resources.common
from universal import lazy_property
import resources.utility as utility


'''
A resource object representing a Berry.

Berries are small fruits that can provide HP and status condition restoration,
stat enhancement, and even damage negation when eaten by Pokémon. Check out
Bulbapedia for greater detail.

Fields:
    id (integer)
        The identifier for this berry resource
    name (string)
        The name for this berry resource
    growth_time (integer)
        Time it takes the tree to grow one stage, in hours. Berry trees go
        through four of these growth stages before they can be picked.
    max_harvest (integer)
        The maximum number of these berries that can grow on one tree in
        Generation IV
    natural_gift_power	(integer)
        The power of the move "Natural Gift" when used with this Berry
    size (integer)
        The size of this Berry, in millimeters
    smoothness (integer)
        The smoothness of this Berry, used in making Pokéblocks or Poffins
    soil_dryness (integer)
        The speed at which this Berry dries out the soil as it grows. A higher
        rate means the soil dries more quickly.
    firmness (NamedAPIResource -> BerryFirmness)
        The firmness of this berry, used in making Pokéblocks or Poffins
    flavors (list of BerryFlavorMap)
        A list of references to each flavor a berry can have and the potency of
        each of those flavors in regard to this berry
    item (NamedAPIResource -> Item)
        Berries are actually items. This is a reference to the item specific
        data for this berry.
    natural_gift_type (NamedAPIResource -> Type)
        The Type the move "Natural Gift" has when used with this Berry
'''
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
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
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


'''A class relating a flavor to a berry.
    Fields:
        potency (integer)
            How powerful the referenced flavor is for this berry
        flavor (NamedAPIResource -> BerryFlavor)
            The referenced berry flavor
'''
class BerryFlavorMap:

    def __init__(self, **kwargs):
        self.potency = kwargs['potency']
        self.flavor = resources.common.NamedAPIResource(**kwargs['flavor'])

    # Returns the flavor resource. Equivalent to self.flavor.resource
    @property
    def resource(self):
        return self.flavor.resource


'''A resource object representing berry firmness.
    Fields:
        id (integer)
            The identifier for this berry firmness resource
        name (string)
            The name for this berry firmness resource
        berries (list of NamedAPIResource -> Berry)
            A list of the berries with this firmness
        names (list of Name)
            The name of this berry firmness listed in different languages'''
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
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
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
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
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