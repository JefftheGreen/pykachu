# /usr/bin/env python
# -*- coding: utf-8 -*-

import resources.common as common
from universal import lazy_property
import resources.utility as utility
import collections


class ItemResource(utility.UtilityResource):
    """
    A resource representing an item.

    An item is an object in the games which the player can pick up, keep in
    their bag, and use in some manner. They have various uses, including
    healing, powering up, helping catch Pokémon, or to access a new area.

        Fields:
            id (int)
                The identifier for this item resource
            name (str)
                The name for this item resource
            cost (int)
                The price of this item in stores
            fling (int)
                The power of the move Fling when used with this item.
            fling_effect (NamedAPIResource -> ItemFlingEffectResource)
                The effect of the move Fling when used with this item
            attributes (list of NamedAPIResource -> ItemAttributeResource)
                A list of attributes this item has
            category (NamedAPIResource -> ItemCategoryResource)
                The category of items this item falls into
            effect_entries (list of VerboseEffect)
                The effect of this ability listed in different languages
            flavor_text_entries (list of VersionGroupFlavorText)
                The flavor text of this ability listed in different languages
            game_indices (list of GenerationGameIndex)
                A list of game indices relevent to this item by generation
            names (list of Name)
                The name of this item listed in different languages
            sprites (list of ItemSprites)
                A set of sprites used to depict this item in the game
            held_by_pokemon (list of ItemHolderPokemon)
                A list of Pokémon that might be found in the wild holding this
                item
            baby_trigger_for (APIResource -> EvolutionChainResource)
                An evolution chain this item requires to produce a bay during
                mating
            machines (list of MachineVersionDetail)
                A list of the machines related to this item
    """

    yaml_tag = '!ItemResource'

    class Meta:
        name = "Item"
        resource_name = "item"
        cache_folder = 'items/items/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'cost',
            'fling_power',
            'fling_effect',
            'attributes',
            'category',
            'effect_entries',
            'flavor_text_entries',
            'game_indices',
            'names',
            'sprites',
            'held_by_pokemon',
            'baby_trigger_for',
            'machines'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def fling_effect(self):
        return common.NamedAPIResource(**self._fling_effect)

    @lazy_property
    def attributes(self):
        return [common.NamedAPIResource(**kwargs)
                for kwargs in self._attributes]

    @lazy_property
    def category(self):
        return common.NamedAPIResource(**self._category)

    @lazy_property
    def effect_entries(self):
        return [common.VerboseEffect(**kwargs)
                for kwargs in self._effect_entries]

    @lazy_property
    def flavor_text_entries(self):
        return [common.VersionGroupFlavorText(**kwargs)
                for kwargs in self._flavor_text_entries]

    @lazy_property
    def game_indicies(self):
        return [common.GenerationGameIndex(**kwargs) 
                for kwargs in self._game_indices]


    @lazy_property
    def sprites(self):
        return ItemSprites(**self._sprites)

    @lazy_property
    def held_by_pokemon(self):
        return [ItemHolderPokemon(**kwargs) for kwargs in self._held_by_pokemon]

    @lazy_property
    def held_by_pokemon_by_version(self):
        by_version = collections.defaultdict(lambda: [])
        for pokemon in self._held_by_pokemon:
            by_version[pokemon.version_details.version.name].append(pokemon)
        return by_version

    @lazy_property
    def baby_trigger_for(self):
        return common.APIResource(**self._baby_trigger_for)

    @lazy_property
    def machines(self):
        return [common.MachineVersionDetail(**kwargs)
                for kwargs in self._machines]


class ItemSprites:
    """
    An object representing an item sprite.

        Fields:
            default (str)
                The default depiction of this item. (A url to an image.)
    """

    def __init__(self, **kwargs):
        self.default = kwargs['default']


class ItemHolderPokemon:
    """
    An object representing a pokemon that could be holding an item in the wild.

        Fields:
            pokemon (NamedAPIResource -> PokemonResource)
                The Pokémon that holds this item
            version_details (list of ItemHolderPokemonVersionDetail)
                The details for the version that this item is held in by the
                Pokémon
    """

    def __init__(self, **kwargs):
        self.pokemon = common.NamedAPIResource(**kwargs['pokemon'])
        self.version_details = ItemHolderPokemonVersionDetail(
            **kwargs['version_details'])


class ItemHolderPokemonVersionDetail:
    """
    An object representing details about when a pokemon might be found holding
    an item

        Fields:
            rarity (int)
                How often this Pokémon holds this item in this version
            version (NamedAPIResource -> VersionResource)
                The version that this item is held in by the Pokémon
    """

    def __init__(self, **kwargs):
        self.rarity = kwargs['rarity']
        self.version = common.NamedAPIResource(**kwargs['version'])


class ItemAttributeResource(utility.UtilityResource):
    """
    A resource representing an item attribute.

    Item attributes define particular aspects of items, e.g. "usable in battle"
    or "consumable".

        Fields:
            id (int)
                The identifier for this item attribute resource
            name (str)
                The name for this item attribute resource
            items (list of NamedAPIResource -> ItemResource)
                A list of items that have this attribute
            names (list of Name)
                The name of this item attribute listed in different languages
            descriptions (list of Description)
                The description of this item attribute listed in different languages

    """

    yaml_tag = '!ItemAttributeResource'

    class Meta:
        name = "Item Attribute"
        resource_name = "item-attribute"
        cache_folder = 'items/attributes/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'items',
            'names',
            'descriptions'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def items(self):
        return [common.NamedAPIResource(**kwargs) for kwargs in self._items]

    @lazy_property
    def descriptions(self):
        return [common.Description(**kwargs) for kwargs in self._descriptions]


class ItemCategoryResource(utility.UtilityResource):
    """
    A resource representing an item category.

    Item categories determine where items will be placed in the players bag.

        Fields:
            id (int)
                The identifier for this item category resource
            name (str)
                The name for this item category resource
            items (list of NamedAPIResource -> ItemResource)
                A list of items that are a part of this category
            names (list of Name)
                The name of this item category listed in different languages
            pocket (NamedAPIResource -> ItemPocketResource)
                The pocket items in this category would be put in
    """

    yaml_tag = '!ItemCategoryResource'

    class Meta:
        name = "Item Category"
        resource_name = "item-category"
        cache_folder = 'items/categories/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'items',
            'names',
            'pocket'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def items(self):
        return [common.NamedAPIResource(**kwargs) for kwargs in self._items]



    @lazy_property
    def pocket(self):
        return common.NamedAPIResource(**self._pocket)


class ItemFlingEffectResource(utility.UtilityResource):
    """
    A resource representing an item fling effect.

    The various effects of the move "Fling" when used with different items.

        Fields:
            id (int)
                The identifier for this fling effect resource
            name (str)
                The name for this fling effect resource
            effect_entries (list of Effect)
                The result of this fling effect listed in different languages
            items (list of NamedAPIResource -> ItemResource)
                A list of items that have this fling effect
    """

    yaml_tag = '!ItemFlingEffectResource'

    class Meta:
        name = "Item Fling Effect"
        resource_name = "item-fling-effect"
        cache_folder = 'items/fling-effect/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'effect_entries',
            'items'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def effect_entries(self):
        return [common.Effect(**kwargs) for kwargs in self._effect_entries]

    @lazy_property
    def items(self):
        return [common.NamedAPIResource(**kwargs) for kwargs in self._items]


class ItemPocketResource(utility.UtilityResource):
    """
    A resource representing an item pocket.

    Pockets within the players bag used for storing items by category.

        Fields:
            id (int)
                The identifier for this item pocket resource
            name (str)
                The name for this item pocket resource
            categories (list of NamedAPIResource -> ItemCategoryResource)
                A list of item categories that are relevant to this item pocket
            names (list of Name)
                The name of this item pocket listed in different languages
    """

    yaml_tag = '!ItemPocketResource'

    class Meta:
        name = "Item Pocket"
        resource_name = "item-pocket"
        cache_folder = 'items/pockets/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'categories',
            'names'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def categories(self):
        return [common.NamedAPIResource(**kwargs)
                for kwargs in self._categoriee]


