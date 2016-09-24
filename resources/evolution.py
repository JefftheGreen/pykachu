# /usr/bin/env python
# -*- coding: utf-8 -*-
import resources.common
from universal import lazy_property
import resources.utility as utility

class EvolutionChainResource(utility.CacheablePropertyResource):

    yaml_tag = '!EvolutionChainResource'

    class Meta:
        name = "Evolution Chain"
        resource_name = "evolution-chain"
        cache_folder = 'evolution/chains/'
        identifier = 'id'
        attributes = (
            'id',
            'baby_trigger_item',
            'chain'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def baby_trigger_item(self):
        return None if self._baby_trigger_item is None \
            else resources.common.NamedAPIResource(**self._baby_trigger_item)

    @lazy_property
    def chain(self):
        return ChainLink(**self._chain)


class ChainLink:

    def __init__(self, **kwargs):
        self.is_baby = kwargs['is_baby']
        self.species = resources.common.NamedAPIResource(**kwargs['species'])
        self.evolution_details = [EvolutionDetail(**deet)
                                  for deet in kwargs['evolution_details']]
        self.evolves_to = [resources.common.NamedAPIResource(**evol)
                           for evol in kwargs['evolves_to']]


class EvolutionDetail:

    def __init__(self, **kwargs):
        self.item = None if kwargs['item'] is None \
            else resources.common.NamedAPIResource(**kwargs['item'])
        self.trigger = resources.common.NamedAPIResource(**kwargs['trigger'])
        self.gender = kwargs['gender']
        self.held_item = None if kwargs['held_item'] is None \
            else resources.common.NamedAPIResource(**kwargs['held_item'])
        self.known_move = None if kwargs['known_move'] is None \
            else resources.common.NamedAPIResource(**kwargs['known_move'])
        self.known_move_type = None if kwargs['known_move_type'] is None \
            else resources.common.NamedAPIResource(**kwargs['known_move_type'])
        self.location = None if kwargs['location'] is None \
            else resources.common.NamedAPIResource(**kwargs['location'])
        self.min_level = kwargs['min_level']
        self.min_happiness = kwargs['min_happiness']
        self.min_beauty = kwargs['min_beauty']
        self.min_affection = kwargs['min_affection']
        self.needs_overworld_rain = kwargs['needs_overworld_rain']
        self.party_species = None if kwargs['party_species'] is None \
            else resources.common.NamedAPIResource(**kwargs['party_species'])
        self.party_type = None if kwargs['party_type'] is None \
            else resources.common.NamedAPIResource(**kwargs['party_type'])
        self.relative_physical_stats = kwargs['relative_physical_stats']
        self.time_of_day = kwargs['time_of_day']
        self.trade_species = None if kwargs['trade_species'] is None \
            else resources.common.NamedAPIResource(**kwargs['trade_species'])
        self.turn_upside_down = kwargs['turn_upside_down']


class EvolutionTriggerResource(utility.CacheablePropertyResource):

    yaml_tag = '!EvolutionTriggerResource'

    class Meta:
        name = "Evolution Trigger"
        resource_name = "evolution-trigger"
        cache_folder = 'evolution/triggers/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'names',
            'pokemon_species'
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
    def pokemon_species(self):
        return [resources.common.NamedAPIResource(**kwargs)
                for kwargs in self._pokemon_species]