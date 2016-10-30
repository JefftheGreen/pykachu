# /usr/bin/env python
# -*- coding: utf-8 -*-
import resources.common as common
from universal import lazy_property
import resources.utility as utility


class MachineResource(utility.UtilityResource):
    """
    A resource representing a TM or HM.

    Machines are the representation of items that teach moves to Pokémon. They
    vary from version to version, so it is not certain that one specific TM or
    HM corresponds to a single Machine.

        Fields:
            id (int)
                The identifier for this machine resource
            item (NamedAPIResource -> ItemResource)
                The TM or HM item that corresponds to this machine
            move (NamedAPIResource -> MoveResource)
                The move that is taught by this machine
            version_group (NamedAPIResource -> VersionGroupResource)
    """

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
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
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
