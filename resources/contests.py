# /usr/bin/env python
# -*- coding: utf-8 -*-

from resources.utility import lazy_property
import resources.utility as utility


class ContestTypeResource(utility.CacheablePropertyResource):

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

    @lazy_property
    def berry_flavor(self):
        return utility.NamedAPIResource(**self._berry_flavor)

    @lazy_property
    def names(self):
        return [ContestName(**kwargs) for kwargs in self._names]


class ContestName:

    def __init__(self, **kwargs):
        self.name = kwargs['name']
        self.color = kwargs['color']
        self.language = utility.NamedAPIResource(**kwargs['language'])


class ContestEffectResource(utility.CacheablePropertyResource):

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

    @lazy_property
    def effect_entries(self):
        return [utility.Effect(**kwargs) for kwargs in self._effect_entries]

    @lazy_property
    def flavor_text_entries(self):
        return [utility.FlavorText(**kwargs)
                for kwargs in self._flavor_text_entries]


class SuperContestEffect(utility.CacheablePropertyResource):

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

    @lazy_property
    def flavor_text_entries(self):
        return [utility.FlavorText(**kwargs)
                for kwargs in self._flavor_text_entries]

    @lazy_property
    def moves(self):
        return [utility.NamedAPIResource(**kwargs) for kwargs in self._moves]
