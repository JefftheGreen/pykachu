# /usr/bin/env python
# -*- coding: utf-8 -*-
import resources.common
from universal import lazy_property
import resources.utility as utility


class EvolutionChainResource(utility.UtilityResource):
    """
    A resource describing an evolution chain.

    Evolution chains are essentially family trees. They start with the lowest
    stage within a family and detail evolution conditions for each as well as
    Pokémon they can evolve into up through the hierarchy.

        Fields:
            id (int)
                The identifier for this evolution chain resource
            baby_trigger_item (NamedAPIResource -> Item)
                The item that a Pokémon would be holding when mating that would
                trigger the egg hatching a baby Pokémon rather than a basic
                Pokémon
            chain (ChainLink)
                The base chain link object. Each link contains evolution details
                for a Pokémon in the chain. Each link references the next
                Pokémon in the natural evolution order.
    """

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
    """
    A class describing a link in an evolutionary chain.

        Fields:
            is_baby (bool)
                Whether or not this link is for a baby Pokémon. This would only
                ever be true on the base link.
            species (NamedAPIResource -> PokemonSpeciesResource)
                The Pokémon species at this point in the evolution chain
            evolution_details (list of EvolutionDetail)
                All details regarding the specific details of the referenced
                Pokémon species evolution
            evolves_to (list of ChainLink)
                A List of chain objects
    """

    def __init__(self, **kwargs):
        self.is_baby = kwargs['is_baby']
        self.species = resources.common.NamedAPIResource(**kwargs['species'])
        self.evolution_details = [EvolutionDetail(**deet)
                                  for deet in kwargs['evolution_details']]
        self.evolves_to = [resources.common.NamedAPIResource(**evol)
                           for evol in kwargs['evolves_to']]


class EvolutionDetail:
    """
    A class representing the details of how a pokemon evolves.

        Fields:
            item (NamedAPIResource -> ItemResource)
                The item required to cause evolution this into Pokémon species
            trigger (NamedAPIResource -> EvolutionTriggerResource)
                The type of event that triggers evolution into this Pokémon
                species
            gender (int)
                The id of the gender of the evolving Pokémon species must be in
                order to evolve into this Pokémon species
            held_item (NamedAPIResource -> ItemResource)
                The item the evolving Pokémon species must be holding during the
                evolution trigger event to evolve into this Pokémon species
            known_move (NamedAPIResource -> MoveResource)
                The move that must be known by the evolving Pokémon species
                during the evolution trigger event in order to evolve into this
                Pokémon species
            known_move_type (NamedAPIResource -> TypeResource)
                The evolving Pokémon species must know a move with this type
                during the evolution trigger event in order to evolve into this
                Pokémon species
            location (NamedAPIResource -> LocationResource)
                The location the evolution must be triggered at.
            min_level (int)
                The minimum required level of the evolving Pokémon species to
                evolve into this Pokémon species
            min_happiness (int)
                The minimum required level of happiness the evolving Pokémon
                species to evolve into this Pokémon species
            min_beauty (int)
                The minimum required level of beauty the evolving Pokémon
                species to evolve into this Pokémon species
            min_affection (int)
                The minimum required level of affection the evolving Pokémon
                species to evolve into this Pokémon species
            needs_overworld_rain (bool)
                Whether or not it must be raining in the overworld to cause
                evolution this Pokémon species
            party_species (NamedAPIResource -> PokemonSpeciesResource)
                The Pokémon species that must be in the players party in order
                for the evolving Pokémon species to evolve into this Pokémon
                species
            party_type (NamedAPIResource -> TypeResource)
                The player must have a Pokémon of this type in their party
                during the evolution trigger event in order for the evolving
                Pokémon species to evolve into this Pokémon species
            relative_physical_stats (int)
                The required relation between the Pokémon's Attack and Defense
                stats. 1 means Attack > Defense. 0 means Attack = Defense.
                -1 means Attack < Defense.
            time_of_day (str)
                The required time of day. Day or night.
            trade_species (NamedAPIResource -> PokemonSpeciesResource)
                Pokémon species for which this one must be traded.
            turn_upside_down (bool)
                Whether or not the 3DS needs to be turned upside-down as this
                Pokémon levels up.
    """

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


class EvolutionTriggerResource(utility.UtilityResource):
    """
    A resource representing an evolution trigger.

    Evolution triggers are the events and conditions that cause a Pokémon to
    evolve. Check out Bulbapedia for greater detail.

        Fields:
            id (int)
                The identifier for this evolution trigger resource
            name (str)
                The name for this evolution trigger resource
            names (list of Name)
                The name of this evolution trigger listed in different languages
            pokemon_species (list of NamedAPIResource -> PokemonSpeciesResource)
                A list of pokemon species that result from this evolution
                trigger
    """

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