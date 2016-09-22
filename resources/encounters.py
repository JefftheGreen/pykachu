# /usr/bin/env python
# -*- coding: utf-8 -*

import resources.common
import resources.utility as utility
from universal import lazy_property


class EncounterMethodResource(utility.CacheablePropertyResource):
    yaml_tag = '!EncounterMethodResource'

    class Meta:
        name = 'Encounter Method'
        resource_name = 'encounter-method'
        cache_folder = 'encounters/encounter-methods/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'order',
            'names'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def names(self):
        return [resources.common.Name(**kwargs) for kwargs in self._names]


class EncounterConditionResource(utility.CacheablePropertyResource):

    yaml_tag = '!EncounterConditionResource'

    class Meta:
        name = 'Encounter Condition'
        resource_name = 'encounter-condition'
        cache_folder = 'encounters/encounter-conditions/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'names',
            'values'
        )

    @lazy_property
    def names(self):
        return [resources.common.Name(**kwargs) for kwargs in self._names]

    @lazy_property
    def values(self):
        return [utility.NamedAPIResource(**kwargs) for kwargs in self._values]


class EncounterConditionValueResource(utility.CacheablePropertyResource):

    yaml_tag = '!EncounterConditionValueResource'

    class Meta:
        name = 'Encounter Condition Value'
        resource_name = 'encounter-condition-value'
        cache_folder = 'encounters/encounter-condition-values/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'names',
            'condition'
        )

    @lazy_property
    def names(self):
        return [resources.common.Name(**kwargs) for kwargs in self._names]

    @lazy_property
    def condition(self):
        return [resources.common.NamedAPIResource(**kwargs)
                for kwargs in self._condition]