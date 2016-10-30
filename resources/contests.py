# /usr/bin/env python
# -*- coding: utf-8 -*-

import resources.common
from universal import lazy_property
import resources.utility as utility


class ContestTypeResource(utility.UtilityResource):
    """
    A resource representing a contest type.

    Contest types are categories judges used to weigh a Pokémon's condition in
    Pokémon contests. Check out Bulbapedia for greater detail.

        Fields:
            id (int)
                The identifier for this contest type resource
            name (str)
                The name for this contest type resource
            berry_flavor (NamedAPIResource -> BerryFlavorResource)
                The berry flavor that correlates with this contest type
            names (list of ContestName)
                The name of this contest type listed in different languages
    """

    yaml_tag = '!ContestTypeResource'

    class Meta:
        name = "Contest Type"
        resource_name = "contest-type"
        cache_folder = 'contest/types/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'berry_flavor',
            'names'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def berry_flavor(self):
        return resources.common.NamedAPIResource(**self._berry_flavor)

    @lazy_property
    def names(self):
        return [ContestName(**kwargs) for kwargs in self._names]


class ContestName:
    """
    A class describing a contest type name.

        Fields:
            name (str)
                The name for this contest
            color (str)
                The color associated with this contest's name
            language (NamedAPIResource -> LanguageResource)
                The language that this name is in
    """

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.color = kwargs['color']
        self.language = resources.common.NamedAPIResource(**kwargs['language'])


class ContestEffectResource(utility.UtilityResource):
    """
    A resource representing a contest effect.

    Contest effects refer to the effects of moves when used in contests.

        Fields:
            id (int)
                The identifier for this contest type resource
            appeal (int)
                The base number of hearts the user of this move gets
            jam (int)
                The base number of hearts the user's opponent loses
            effect_entries (list of Effect)
                The result of this contest effect listed in different languages
            flavor_text_entries (list of FlavorText)
                The flavor text of this contest effect listed in different
                languages
    """

    yaml_tag = '!ContestEffectResource'

    class Meta:
        name = "Contest Effect"
        resource_name = "contest-effect"
        cache_folder = 'contest/effects/'
        identifier = 'id'
        attributes = (
            'id',
            'appeal',
            'jam',
            'effect_entries',
            'flavor_text_entries'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def effect_entries(self):
        return [resources.common.Effect(**kwargs) for kwargs in self._effect_entries]

    @lazy_property
    def flavor_text_entries(self):
        return [resources.common.FlavorText(**kwargs)
                for kwargs in self._flavor_text_entries]


class SuperContestEffectResource(utility.UtilityResource):
    """
    A resource describing a super contest effect.

    Super contest effects refer to the effects of moves when used in super
    contests.

        Fields:
            id (int)
                The identifier for this super contest effect resource
            appeal (int)
                The level of appeal this super contest effect has
            flavor_text_entries (list of FlavorText)
                The flavor text of this super contest effect listed in different
                languages
            moves (list of NamedAPIResource -> MoveResource)
                A list of moves that have the effect when used in super contests
    """

    yaml_tag = '!SuperContestEffectResource'

    class Meta:
        name = "Super Contest Effect"
        resource_name = "super-contest-effect"
        cache_folder = 'contest/super-effects/'
        identifier = 'id'
        attributes = (
            'id',
            'appeal',
            'flavor_text_entries',
            'moves'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def flavor_text_entries(self):
        return [resources.common.FlavorText(**kwargs)
                for kwargs in self._flavor_text_entries]
