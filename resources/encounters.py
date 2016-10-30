# /usr/bin/env python
# -*- coding: utf-8 -*

import resources.common
import resources.utility as utility
from universal import lazy_property


class EncounterMethodResource(utility.UtilityResource):
    """
    A resource describing an encounter method.

    Methods by which the player might can encounter Pokémon in the wild, e.g.,
    walking in tall grass. Check out Bulbapedia for greater detail.

        Fields:
            id (int)
                The identifier for this encounter method resource
            name (str)
                The name for this encounter method resource
            order (int)
                A good value for sorting
            names (list of Name)
                The name of this encounter method listed in different languages
    """

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
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def names(self):
        return [resources.common.Name(**kwargs) for kwargs in self._names]


class EncounterConditionResource(utility.UtilityResource):
    """
    A resource describing an encounter condition.

    Conditions which affect what pokemon might appear in the wild, e.g., day or
    night.

        Fields:
            id (int)
                The identifier for this encounter condition resource
            name (str)
                The name for this encounter condition resource
            names (list of Name)
                The name of this encounter method listed in different languages
            values (list of NamedAPIResource -> EncounterConditionValueResource)
                A list of possible values for this encounter condition
    """

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
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def names(self):
        return [resources.common.Name(**kwargs) for kwargs in self._names]

    @lazy_property
    def values(self):
        return [utility.NamedAPIResource(**kwargs) for kwargs in self._values]


class EncounterConditionValueResource(utility.UtilityResource):
    """
    A resource describing a value of an encounter condition.

    Encounter condition values are the various states that an encounter
    condition can have, i.e., time of day can be either day or night.

        Fields:
            id (int)
                The identifier for this encounter condition value resource
            name (str)
                The name for this encounter condition value resource
            condition (list of NamedAPIResource -> EncounterCondiitonResource)
                The condition this encounter condition value pertains to
            names (list of Name)
                The condition this encounter condition value pertains to
    """

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
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def names(self):
        return [resources.common.Name(**kwargs) for kwargs in self._names]

    @lazy_property
    def condition(self):
        return [resources.common.NamedAPIResource(**kwargs)
                for kwargs in self._condition]