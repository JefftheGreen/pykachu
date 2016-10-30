# /usr/bin/env python
# -*- coding: utf-8 -*-

import resources.common as common
from universal import lazy_property
import resources.utility as utility


class LocationResource(utility.UtilityResource):
    """
    A resource representing a location.

    Locations that can be visited within the games. Locations make up sizable
    portions of regions, like cities or routes.

        Fields:
            id (int)
                The identifier for this location resource
            name (str)
                 he name for this location resource
            region (NamedAPIResource -> RegionResource)
                The region this location can be found in
            names (list of Name)
                The name of this language listed in different languages
            game_indices (list of GenerationGameIndex)
                A list of game indices relevent to this location by generation
            areas (list of NamedAPIResource -> LocationAreaResource)
                Areas that can be found within this location
    """

    yaml_tag = '!LocationResource'

    class Meta:
        name = "Location"
        resource_name = "location"
        cache_folder = 'locations/locations/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'region',
            'names',
            'game_indices',
            'areas'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def region(self):
        return common.NamedAPIResource(**self._region)

    @lazy_property
    def game_indices(self):
        return [common.GenerationGameIndex(**kwargs)
                for kwargs in self._game_indices]

    @lazy_property
    def areas(self):
        return [common.NamedAPIResource(**kwargs) for kwargs in self._areas]


class LocationAreaResource(utility.UtilityResource):
    """
    A resource representing an area.

    Location areas are sections of areas, such as floors in a building or cave.
    Each area has its own set of possible Pokémon encounters.

        Fields:
            id (int)
                The identifier for this location resource
            name (str)
                The name for this location resource
            game_index (int)
                The internal id of an API resource within game data
            encounter_method_rates (list of EncounterMethodRate)
                A list of methods in which Pokémon may be encountered in this
                area and how likely the method will occur depending on the
                version of the game
            location (NamedAPIResource -> LocationResource)
                The location this area can be found in
            names (list of Name)
                The name of this location area listed in different languages
            pokemon_encounters (list of PokemonEncounter)
                A list of Pokémon that can be encountered in this area along
                with version specific details about the encounter
    """

    yaml_tag = '!LocationAreaResource'

    class Meta:
        name = "Location Area"
        resource_name = "location-area"
        cache_folder = 'locations/area/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'game_index',
            'encounter_method_rates',
            'location',
            'pokemon_encounters'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def encounter_method_rates(self):
        return [EncounterMethodRate(**kwargs)
                for kwargs in self._encounter_method_rates]

    @lazy_property
    def location(self):
        return common.NamedAPIResource(**self._location)

    @lazy_property
    def pokemon_encounters(self):
        return [PokemonEncounter(**kwargs)
                for kwargs in self._pokemon_encounters]


class EncounterMethodRate:
    """
    An object containing information on an encounter method in a particular
    version

        Fields:
            encounter_method (NamedAPIResource -> EncounterMethodResource)
                The method in which Pokémon may be encountered in an area.
            version_details (list of EncounterVersionDetails)
                The chance of the encounter to occur on a version of the game.
    """

    def __init__(self, **kwargs):
        self.encounter_method = common.NamedAPIResource(
            **kwargs['encounter_method'])
        self.version_details = [EncounterVersionDetail(**deet)
                                for deet in kwargs['version_Details']]


class EncounterVersionDetail:
    """
    An object containing information about how often an encounter will occur
    in a particular game version

        Fields:
            rate (int)
                The chance of an encounter to occur.
            version (NamedAPIResource -> VersionResource)
                The version of the game in which the encounter can occur with
                the given chance.
    """

    def __init__(self, **kwargs):
        self.rate = kwargs['rate']
        self.version = common.NamedAPIResource(**kwargs['version'])


class PokemonEncounter:
    """
    An object containing information about which pokemon can occur in a
    particular game version.

        Field:
            pokemon (NamedAPIResource -> PokemonResource)
                The Pokémon being encountered
            version_details (list of VersionEncounterDetail)
                A list of versions and encounters with Pokémon that might happen
                in the referenced location area
    """

    def __init__(self, **kwargs):
        self.pokemon = common.NamedAPIResource(**kwargs['pokemon'])
        self.version_details = [common.VersionEncounterDetail(**deet)
                                for deet in kwargs['version_details']]


class PalParkAreaResource(utility.UtilityResource):
    """
    A resource describing a Pal Park Area.

    Areas used for grouping Pokémon encounters in Pal Park. They're like
    habitats that are specific to Pal Park.

        Fields:
            id (int)
                The identifier for this pal park area resource
            name (str)
                The name for this pal park area resource
            names (list of Name)
                The name of this pal park area listed in different languages
            pokemon_encounters (list of PalParkEncounterSpecies)
    """

    yaml_tag = '!Pa;ParkAreaResource'

    class Meta:
        name = "Pal Park Area"
        resource_name = "pal-park-area"
        cache_folder = 'locations/pal-park-areas/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'names',
            'pokemon_encounters'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def pokemon_encounters(self):
        return [PalParkEncounterSpecies(**kwargs)
                for kwargs in self._pokemon_encounters]


class PalParkEncounterSpecies:
    """
    An object describing a Pal Park Encounter.

        Fields:
            base_score (int)
                The base score given to the player when this Pokémon is caught
                during a pal park run
            rate (int)
                The base rate for encountering this Pokémon in this pal park
                area
            pokemon_species (NamedAPIResource -> PokemonSpeciesResource)
                The Pokémon species being encountered
    """

    def __init__(self, **kwargs):
        self.base_score = kwargs['base_score']
        self.rate = kwargs['rate']
        self.pokemon_species = common.NamedAPIResource(
            **kwargs['pokemon_species'])


class RegionResource(utility.UtilityResource):
    """
    A resource representing a region.

    A region is an organized area of the Pokémon world. Most often, the main
    difference between regions is the species of Pokémon that can be encountered
    within them.

        Fields:
            id (int)
                The identifier for this region resource
            name (str)
                The name for this region resource
            locations (list of NamedAPIResource -> LocationResource)
                A list of locations that can be found in this region
            main_generation (NamedAPIResource -> GenerationResource)
                The generation this region was introduced in
            names (list of Name)
                The name of this region listed in different languages
            pokedexes (list of NamedAPIResource -> PokedexResource)
                A list of pokédexes that catalogue Pokémon in this region
            version_groups (list of NamedAPIResource -> VersionGroupResource)
                A list of version groups where this region can be visited
    """

    yaml_tag = '!RegionResource'

    class Meta:
        name = "Region"
        resource_name = "region"
        cache_folder = 'locations/regions/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'locations',
            'main_generation',
            'names',
            'pokedexes',
            'version_groups'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def locations(self):
        return [common.NamedAPIResource(**kwargs) for kwargs in self._locations]

    @lazy_property
    def main_generation(self):
        return common.NamedAPIResource(**self._main_generation)

    @lazy_property
    def pokedexes(self):
        return [common.NamedAPIResource(**kwargs) for kwargs in self._pokedexes]
