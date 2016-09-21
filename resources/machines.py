# /usr/bin/env python
# -*- coding: utf-8 -*-
import resources.common as common
from universal import lazy_property
import resources.utility as utility


class MachineResource(utility.CacheablePropertyResource):

    yaml_tag = '!MachineResource'

    class Meta:
        name = ""
        resource_name = ""
        cache_folder = 'machines/machines/'
        identifier = 'id'
        attributes = (
            'id',
            'item',
            'move',
            'version_group'
        )

    @lazy_property
    def item(self):
        return common.NamedAPIResource(**self._item)

    @lazy_property
    def move(self):
        return common.NamedAPIResource(**self._move)

    @lazy_property
    def version_group(self):
        return common.NamedAPIResource(**self._version_group)
