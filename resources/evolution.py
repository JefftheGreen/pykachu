# /usr/bin/env python
# -*- coding: utf-8 -*-

from resources.utility import lazy_property
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

    @lazy_property
    def baby_trigger_item(self):
        return None if self._baby_trigger_item is None \
            else utility.NamedAPIResource(**self._baby_trigger_item)

    @lazy_property
    def chain(self):
        return ChainLink(**self._chain)


class ChainLink:

    def __init__(self, **kwargs):
        self.is_baby = kwargs['is_baby']
        self.species = utility.NamedAPIResource(**kwargs['species'])
        self.evolution_details = [EvolutionDetail(**deet)
                                  for deet in kwargs['evolution_details']]
        self.evolves_to = [utility.NamedAPIResource(**evol)
                           for evol in kwargs['evolves_to']]


class EvolutionDetail:

    def __init__(self, **kwargs):
        self.item = None if kwargs['item'] is None \
            else utility.NamedAPIResource(**kwargs['item'])
        self.trigger = utility.NamedAPIResource(**kwargs['trigger'])
        self.gender = kwargs['gender']
        self.held_item = None if kwargs['held_item'] is None \
            else utility.NamedAPIResource(**kwargs['held_item'])
        self.known_move = None if kwargs['known_move'] is None \
            else utility.NamedAPIResource(**kwargs['known_move'])
        self.known_move_type = None if kwargs['known_move_type'] is None \
            else utility.NamedAPIResource(**kwargs['known_move_type'])
        self.location = None if kwargs['location'] is None \
            else utility.NamedAPIResource(**kwargs['location'])
        self.min_level = kwargs['min_level']
        self.min_happiness = kwargs['min_happiness']
        self.min_beauty = kwargs['min_beauty']
        self.min_affection = kwargs['min_affection']
        self.needs_overworld_rain = kwargs['needs_overworld_rain']
        self.party_species = None if kwargs['party_species'] is None \
            else utility.NamedAPIResource(**kwargs['party_species'])
        self.party_type = None if kwargs['party_type'] is None \
            else utility.NamedAPIResource(**kwargs['party_type'])
        self.relative_physical_stats = kwargs['relative_physical_stats']
        self.time_of_day = kwargs['time_of_day']
        self.trade_species = None if kwargs['trade_species'] is None \
            else utility.NamedAPIResource(**kwargs['trade_species'])
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

    @lazy_property
    def names(self):
        return [utility.Name(**kwargs) for kwargs in self._names]

    @lazy_property
    def pokemon_species(self):
        return [utility.NamedAPIResource(**kwargs)
                for kwargs in self._pokemon_species]