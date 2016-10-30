# /usr/bin/env python
# -*- coding: utf-8 -*-
import resources.common
from universal import lazy_property
import resources.utility as utility


class GenerationResource(utility.UtilityResource):
    """
    A resource representing a game generation.

    A generation is a grouping of the Pokémon games that separates them based on
    the Pokémon they include. In each generation, a new set of Pokémon, Moves,
    Abilities and Types that did not exist in the previous generation are
    released.

        Fields:
            id (int)
                The identifier for this generation resource
            name (str)
                The name for this generation resource
            abilities (list of NamedAPIResource -> AbilityResource)
                A list of abilities that were introduced in this generation
            names (list of Name)
                The name of this generation listed in different languages
            main_region (NamedAPIResource -> RegionResource)
                The main region travelled in this generation
            moves (list of NamedAPIResource -> MoveResource)
                A list of moves that were introduced in this generation
            pokemon_species (list of NamedAPIResourec -> PokemonSpeciesResource)
                A list of Pokémon species that were introduced in this
                generation
            types (list of NamedAPIResource -> TypeResource)
                A list of types that were introduced in this generation
            version_groups (list of NamedAPIResource -> VersionGroupResource)
                A list of version groups that were introduced in this generation
    """

    yaml_tag = '!GenerationResource'

    class Meta:
        name = "Generation"
        resource_name = "generation"
        cache_folder = 'games/generations/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'abilities',
            'names',
            'main_region',
            'moves',
            'pokemon_species',
            'types',
            'version_groups'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def abilities(self):
        return [resources.common.NamedAPIResource(**kwargs)
                for kwargs in self._abilities]

    @lazy_property
    def names(self):
        return [resources.common.Name(**kwargs) for kwargs in self._names]

    @lazy_property
    def main_region(self):
        return resources.common.NamedAPIResource(**self._main_region)

    @lazy_property
    def pokemon_species(self):
        return [resources.common.NamedAPIResource(**kwargs)
                for kwargs in self._pokemon_species]

    @lazy_property
    def types(self):
        return [resources.common.NamedAPIResource(**kwargs) for kwargs in self._types]

    @lazy_property
    def version_groups(self):
        return [resources.common.NamedAPIResource(**kwargs)
                for kwargs in self._version_groups]


class PokedexResource(utility.UtilityResource):
    """
    A resource representing a pokedex version.

    A Pokédex is a handheld electronic encyclopedia device; one which is capable
    of recording and retaining information of the various Pokémon in a given
    region with the exception of the national dex and some smaller dexes related
    to portions of a region. See Bulbapedia for greater detail.

        Fields:
            id (int)
                The identifier for this Pokédex resource
            name (str)
                The name for this Pokédex resource
            is_main_series (bool)
                Whether or not this Pokédex originated in the main series of the
                video games
            descriptions (list of Description)
                The description of this Pokédex listed in different languages
            names (list of Name)
                The name of this Pokédex listed in different languages
            pokemon_entries (list of PokemonEntry)
                A list of Pokémon catalogued in this Pokédex and their indexes
            region (NamedAPIResource -> RegionResource)
                The region this Pokédex catalogues Pokémon for
            version_groups (list of NamedAPIResource -> VersionGroupResource)
                A list of version groups this Pokédex is relevant to
    """

    yaml_tag = '!PokedexResource'

    class Meta:
        name = "Pokedex"
        resource_name = "pokedex"
        cache_folder = 'games/pokedexes/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'is_main_series',
            'descriptions',
            'names',
            'pokemon_entries',
            'region',
            'version_groups'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def descriptions(self):
        return [resources.common.Description(**kwargs) for kwargs in self._descriptions]

    @lazy_property
    def names(self):
        return [resources.common.Name(**kwargs) for kwargs in self._names]

    @lazy_property
    def pokemon_entries(self):
        return [PokemonEntry(**kwargs) for kwargs in self._pokemon_entries]

    @lazy_property
    def region(self):
        return resources.common.NamedAPIResource(**self._region)


class PokemonEntry:
    """
    A class representing an entry of a Pokemon species in a pokedex.

        Fields:
            entry_number (int)
                The index of this Pokémon species entry within the Pokédex
            pokemon_species (NamedAPIResource -> PokemonSpeciesResource)
                The Pokémon species being encountered
    """

    def __init__(self, **kwargs):
        self.entry_number = kwargs['entry_number']
        self.pokemon_species = kwargs['pokemon_species']


class VersionResource(utility.UtilityResource):
    """
    A resource representing a version of the games.

    Versions of the games, e.g., Red, Blue or Yellow.

        Fields:
            id (int)
                The identifier for this version resource
            name (str)
                The name for this version resource
            names (list of Name)
                The name of this version listed in different languages
            version_group (NamedAPIResource -> VersionGroupResource)
                The version group this version belongs to
    """

    yaml_tag = '!VersionResource'

    class Meta:
        name = "Version"
        resource_name = "version"
        cache_folder = 'games/versions/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'names',
            'version_group'
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


class VersionGroupResource(utility.UtilityResource):
    """
    A resource representing a version group.

    Version groups categorize highly similar versions of the games.

        Fields:
            id (int)
                The identifier for this version group resource
            name (str)
                The name for this version group resource
            order (int)
                Order for sorting. Almost by date of release, except similar
                versions are grouped together.
            generation (NamedAPIResource -> GenerationResource)
                The generation this version was introduced in
            move_learn_methods (list of NamedAPIResource ->
            MoveLearnMethodResource)
                A list of methods in which Pokémon can learn moves in this
                version group
            pokedexes (list of NamedAPIResource -> PokedexResource)
                A list of Pokédexes introduces in this version group
            regions (list of NamedAPIResource -> RegionResource)
                A list of regions that can be visited in this version group
            versions (list of NamedAPIResource -> VersionResource)
                The versions this version group owns
    """

    yaml_tag = '!VersionGroupResource'

    class Meta:
        name = "Version Group"
        resource_name = "version-group"
        cache_folder = 'games/version-groups/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'order',
            'generation',
            'move_learn_methods',
            'pokedexes',
            'regions',
            'versions'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def generation(self):
        return resources.common.NamedAPIResource(**self._generation)

    @lazy_property
    def move_learn_methods(self):
        return [resources.common.NamedAPIResource(**kwargs)
                for kwargs in self._move_learn_methods]

    @lazy_property
    def pokedexes(self):
        return [resources.common.NamedAPIResource(**kwargs)
                for kwargs in self._pokedexes]

    @lazy_property
    def regions(self):
        return [resources.common.NamedAPIResource(**kwargs)
                for kwargs in self._regions]

    @lazy_property
    def versions(self):
        return [resources.common.NamedAPIResource(**kwargs)
                for kwargs in self._versions]
