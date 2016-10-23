# /usr/bin/env python
# -*- coding: utf-8 -*-
import resources.common as common
import resources.utility as utility
from universal import lazy_property


class AbilityResource(utility.CacheablePropertyResource):

    yaml_tag = '!AbilityResource'

    class Meta:
        name = 'Ability'
        resource_name = 'ability'
        cache_folder = 'pokemon/abilities/'
        identifier = 'id'
        attributes = (
            'id',
            'name'
            'is_main_series',
            'generation',
            'names',
            'effect_entries',
            'effect_changes',
            'flavor_text_entries',
            'pokemon'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def generation(self):
        return common.NamedAPIResource(**self._generation)


    @lazy_property
    def effect_entries(self):
        return [common.VerboseEffect(**kwargs)
                for kwargs in self._effect_entries]

    @lazy_property
    def effect_changes(self):
        [common.EffectChange(**kwargs)
         for kwargs in self._effect_changes]

    @lazy_property
    def flavor_text_entries(self):
        return [AbilityFlavorText(**kwargs)
                for kwargs in self._flavor_text_entries]

    @lazy_property
    def pokemon(self):
        return [AbilityPokemon(**kwargs) for kwargs in self._pokemon]

    @property
    def pokemon_ids(self):
        return [pokemon.id for pokemon in self.pokemon]

    @property
    def pokemon_names(self):
        return [pokemon.name for pokemon in self.pokemon]


class AbilityFlavorText:

    def __init__(self, **kwargs):
        self.flavor_text = kwargs['flavor_text']
        self.language = common.NamedAPIResource(**kwargs['language'])
        self.version_group = common.NamedAPIResource(**kwargs['version_group'])


class AbilityPokemon:

    def __init__(self, **kwargs):
        self.is_hidden = kwargs['is_hidden']
        self.slot = kwargs['slot']
        self.pokemon = common.NamedAPIResource(**kwargs['pokemon'])

    @property
    def id(self):
        return self.pokemon.url.split('/')[-2]

    @property
    def name(self):
        return self.pokemon.name

    @property
    def resource(self):
        return self.pokemon.resource


class CharacteristicResource(utility.CacheablePropertyResource):

    yaml_tag = '!CharacteristicResource'

    class Meta:
        name = 'Characteristic'
        resource_name = 'characteristic'
        cache_folder = 'pokemon/characteristics/'
        identifier = 'id'
        attributes = (
            'id',
            'gene_modulo',
            'possible_values',
            'descriptions'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

        @lazy_property
        def descriptions(self):
            return [common.Description(**kwargs)
                    for kwargs in self._descriptions]


class EggGroupResource(utility.CacheablePropertyResource):
    
    yaml_tag = 'PokemonCharacteristicResource'
    
    class Meta:
        name = 'Egg Group'
        resource_name = 'egg-group'
        cache_folder = 'pokemon/egg-groups/'
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
    def pokemon_species(self):
        return [common.NamedAPIResource(**kwargs)
                for kwargs in self._pokemon_species]


class GenderResource(utility.CacheablePropertyResource):

    yaml_tag = '!GenderResource'

    class Meta:
        name = 'Gender'
        resource_name = 'gender'
        cache_folder = 'pokemon/genders/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'pokemon_species_details',
            'required_for_evolution'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def pokemon_species_details(self):
        return [PokemonSpeciesGender(**kwargs)
                for kwargs in self.pokemon_species_details]

    @lazy_property
    def required_for_evolution(self):
        return [common.NamedAPIResource(**kwargs)
                for kwargs in self._required_for_evolution]


class PokemonSpeciesGender:

    def __init__(self, **kwargs):
        self.rate = kwargs['rate']
        self.pokemon_species = common.NamedAPIResource(
            **kwargs['pokemon_species']
        )

    @property
    def decimal_rate(self):
        return self.rate / 8 if self.rate > 0 else 1.0


class GrowthRateResource(utility.CacheablePropertyResource):

    yaml_tag = '!GrowthRateResource'

    class Meta:
        name = 'Growth Rate'
        resource_name = 'growth-rate'
        cache_folder = 'pokemon/growth-rates/'
        identifier = 'id'
        atributes = (
            'id',
            'name',
            'formula',
            'descriptions',
            'levels',
            'pokemon_species'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def descriptions(self):
        [common.Description(**kwargs) for kwargs in self._descriptions]

    @lazy_property
    def levels(self):
        return [GrowthRateExperienceLevel(**kwargs) for kwargs in self._levels]

    @lazy_property
    def pokemon_species(self):
        return [common.NamedAPIResource(**kwargs)
                for kwargs in self._pokemon_species]


class GrowthRateExperienceLevel:

    def __init__(self, **kwargs):
        self.level = kwargs['level']
        self.experience = kwargs['experience']


class NatureResource(utility.CacheablePropertyResource):

    yaml_tag = '!NatureResource'

    class Meta:
        name = 'Nature'
        resource_name = 'nature'
        cache_folder = 'pokemon/natures/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'increased_stat',
            'decreased_stat',
            'hates_flavor',
            'likes_flavor',
            'pokeathlon_stat_changes',
            'move_battle_style_preferences',
            'names'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    def __init__(self):
        self.decreased_stat__cached = None
        self.increased_stat__cached = None
        self.hates_flavor__cached = None
        self.likes_flavor__cached = None
        self.pokeathlon_stat_changes__cached = None
        self.move_battle_style_preferences__cached = None
        self.names__cached = None

    @property
    def decreased_stat(self):
        if not self.decreased_stat__cached:
            self.decreased_stat__cached = common.NamedAPIResource(
                **self._decreased_stat)
        return self.decrease_stat__cached

    @property
    def increased_stat(self):
        if not self.increased_stat__cached:
            self.increased_stat__cached = common.NamedAPIResource(
                **self._increased_stat)
        return self.increase_stat__cached

    @property
    def hates_flavor(self):
        if not self.hates_flavor__cached:
            self.hates_flavor__cached =  common.NamedAPIResource(
                **self._hates_flavor)
        return self.increase_stat__cached

    @property
    def likes_flavor(self):
        if not self.likes_flavor__cached:
            self.likes_flavor__cached = common.NamedAPIResource(
                **self._likes_flavor)
        return self.increase_stat__cached

    @property
    def pokeathlon_stat_changes(self):
        if not self.pokeathlon_stat_changes__cached:
            self.pokeathlon_stat_changes__cached = [NatureStatChange(**kwargs)
                                                for kwargs in
                                                self._pokeathlon_stat_changes]
        return self.pokeathlon_stat_changes__cached

    @property
    def move_battle_style_preferences(self):
        if not self.move_battle_style_preferences__cached:
            m = [MoveBattleStylePreference(**kwargs)
                 for kwargs in self._move_battle_style_preferences]
            self.move_battle_style_preferences__cached = m
        return self.move_battle_style_preferences__cached

    @property
    def names(self):
        if not self.names__cached:
            self.names__cached = [common.Name(**kwargs)
                                  for kwargs in self._names]
        return self.names__cached


class NatureStatChange:

    def __init__(self, **kwargs):
        self.max_change = kwargs['max_change']
        self.pokeathlon_stat = common.NamedAPIResource(
            **kwargs['pokeathlon_stat'])


class MoveBattleStylePreference:

    def __init__(self, kwargs):
        self.low_hp_preference = kwargs['low_hp_preference']
        self.high_hp_preference = kwargs['high_hp_preference']
        self.move_battle_style = common.NamedAPIResource(
            **kwargs['move_battle_style'])


class PokeathlonStatResource(utility.CacheablePropertyResource):
    yaml_tag = '!PokeathlonStatResource'

    class Meta:
        name = 'Pokeathlon Stat'
        resource_name = 'pokeathlon-stat'
        cache_folder = 'pokemon/pokeathlon-stats/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'names',
            'affecting_natures'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )



    @lazy_property
    def affecting_natures(self):
        return  NaturePokeathlonStatAffectSets(**self._affecting_natures)


class NaturePokeathlonStatAffectSets:

    def __init__(self, **kwargs):
        self.increase = [NaturePokeathlonStatAffect(**increase)
                         for increase in kwargs['increase']]
        self.decrease = [NaturePokeathlonStatAffect(**decrease)
                         for decrease in kwargs['decrease']]


class NaturePokeathlonStatAffect:

    def __init__(self, **kwargs):
        self.max_change = kwargs['max_change']
        self.nature = common.NamedAPIResource(**kwargs['nature'])


class PokemonColorResource(utility.CacheablePropertyResource):
    yaml_tag = '!ColorResource'

    class Meta:
        name = 'Pokemon Color'
        resource_name = 'pokemon-color'
        cache_folder = 'pokemon/colors/'
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
    def pokemon_species(self):
        return [common.NamedAPIResource(**kwargs)
                for kwargs in self._pokemon_species]


class PokemonFormResource(utility.CacheablePropertyResource):
    yaml_tag = '!FormResource'

    class Meta:
        name = 'Pokemon Form'
        resource_name = 'pokemon-form'
        cache_folder = 'pokemon/forms/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'order',
            'form_order',
            'is_default',
            'in_battle_only',
            'is_mega',
            'form_name',
            'pokemon',
            'sprites',
            'version_group',
            'names',
            'form_names'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def pokemon(self):
        return common.NamedAPIResource(**self._pokemon)

    @lazy_property
    def sprites(self):
        return PokemonFormSprites(**self._sprites)

    @lazy_property
    def version_group(self):
        return common.NamedAPIResource(**self._version_group)



    @lazy_property
    def form_names(self):
        return [common.Name(**kwargs) for kwargs in self._form_names]


class PokemonFormSprites:

    def __init__(self, **kwargs):
        self.front_default = kwargs['front_default']
        self.front_shiny = kwargs['front_shiny']
        self.back_default = kwargs['back_default']
        self.back_shiny = kwargs['back_shiny']


class PokemonHabitatResource(utility.CacheablePropertyResource):
    yaml_tag = '!HabitatResource'

    class Meta:
        name = 'Pokemon Habitat'
        resource_name = 'pokemon-habitat'
        cache_folder = 'pokemon/habitats/'
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
    def pokemon_species(self):
        return [common.NamedAPIResource(**kwargs)
                for kwargs in self._pokemon_species]


class PokemonShapeResource(utility.CacheablePropertyResource):
    yaml_tag = '!ShapeResource'

    class Meta:
        name = 'Pokemon Shape'
        resource_name = 'pokemon-shape'
        cache_folder = 'pokemon/shapes/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'awesome_names',
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
    def awesome_names(self):
        return [AwesomeName(**kwargs) for kwargs in self._awesome_names]



    @lazy_property
    def pokemon_species(self):
        return [common.NamedAPIResource(**kwargs)
                for kwargs in self._pokemon_species]


class AwesomeName:

    def __init__(self, **kwargs):
        self.awesome_name = kwargs['awesome_name']
        self.language = common.NamedAPIResource(**kwargs['language'])


class PokemonSpeciesResource(utility.CacheablePropertyResource):
    yaml_tag = '!SpeciesResource'

    class Meta:
        name = 'Pokemon Species'
        resource_name = 'pokemon-species'
        cache_folder = 'pokemon/species/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'order',
            'gender_rate',
            'capture_rate',
            'base_happiness',
            'is_baby',
            'hatch_counter',
            'has_gender_differences',
            'forms_switchable',
            'growth_rate',
            'pokedex_numbers',
            'egg_groups',
            'color'
            'shape',
            'evolves_from_species',
            'evolution_chain',
            'habitat',
            'generation',
            'names',
            'pal_park_encounters',
            'flavor_text_entries',
            'form_descriptions',
            'genera',
            'varieties'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def growth_rate(self):
        return common.NamedAPIResource(**self._growth_rate)

    @lazy_property
    def pokedex_numbers(self):
        return [PokemonSpeciesDexEntry(**kwargs)
                for kwargs in self._pokedex_numbers]

    @lazy_property
    def egg_groups(self):
        return [common.NamedAPIResource(**kwargs)
                for kwargs in self._egg_groups]

    @lazy_property
    def color(self):
        return common.NamedAPIResource(**self._color)

    @lazy_property
    def shape(self):
        return common.NamedAPIResource(**self._shape)

    @lazy_property
    def evolves_from_species(self):
        return common.NamedAPIResource(**self._evolves_from_species)

    @lazy_property
    def evolution_chain(self):
        return common.APIResource(**self._evolution_chain)

    @lazy_property
    def habitat(self):
        return common.NamedAPIResource(**self._habitat)

    @lazy_property
    def generation(self):
        return common.NamedAPIResource(**self._generation)



    @lazy_property
    def pal_park_encounters(self):
        return [PalParkEncounterArea(**kwargs)
                for kwargs in self._pal_park_encounters]

    @lazy_property
    def flavor_text_entries(self):
        return [common.FlavorText(**kwargs)
                for kwargs in self._flavor_text_entries]

    @lazy_property
    def form_descriptions(self):
        return [common.Description(**kwargs)
                for kwargs in self._form_descriptions]

    @lazy_property
    def genera(self):
        return [Genus(**kwargs) for kwargs in self._genera]

    @lazy_property
    def varieties(self):
        return [PokemonSpeciesVariety(**kwargs) for kwargs in self._varieties]


class Genus:

    def __init__(self, **kwargs):
        self.genus = kwargs['genus']
        self.language = common.NamedAPIResource(**kwargs['language'])


class PokemonSpeciesDexEntry:

    def __init__(self, **kwargs):
        self.entry_number = kwargs['entry_number']
        self.pokedex = common.NamedAPIResource(**kwargs['pokedex'])


class PalParkEncounterArea:

    def __init__(self, **kwargs):
        self.base_score = kwargs['base_score']
        self.rate = kwargs['rate']
        self.area = common.NamedAPIResource(**kwargs['area'])


class PokemonSpeciesVariety:

    def __init__(self, **kwargs):
        self.is_default = kwargs['is_default']
        self.pokemon = common.NamedAPIResource(**kwargs['pokemon'])


class StatResource(utility.CacheablePropertyResource):
    yaml_tag = '!StatResource'

    class Meta:
        name = 'Stat'
        resource_name = 'stat'
        cache_folder = 'pokemon/stats/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'game_index',
            'is_battle_only',
            'affecting_moves',
            'affecting_natures',
            'characteristics',
            'move_damage_class',
            'names'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def affecting_moves(self):
        return MoveStatAffectSets(self._affecting_moves)

    @lazy_property
    def affecting_natures(self):
        return NatureStatAffectSets(self._affecting_natures)

    @lazy_property
    def characteristics(self):
        return [common.APIResource(**kwargs)
                for kwargs in self._characteristics]

    @lazy_property
    def move_damage_class(self):
        return [common.NamedAPIResource(**kwargs)
                for kwargs in self._move_damage_class]




class MoveStatAffectSets:

    def __init__(self, **kwargs):
        self.increase = [MoveStatAffect(**msa) for msa in kwargs['increase']]
        self.decrease = [MoveStatAffect(**msa) for msa in kwargs['decrease']]


class MoveStatAffect:

    def __init__(self, **kwargs):
        self.change = kwargs['change']
        self.move = common.NamedAPIResource(**kwargs['move'])


class NatureStatAffectSets:

    def __init__(self, **kwargs):
        self.increase = [MoveStatAffect(**msa) for msa in kwargs['increase']]
        self.decrease = [MoveStatAffect(**msa) for msa in kwargs['decrease']]


class TypeResource(utility.CacheablePropertyResource):
    yaml_tag = '!Resource'

    class Meta:
        name = 'Type'
        resource_name = 'type'
        cache_folder = 'pokemon/types/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'damage_relations',
            'game_indices',
            'generation',
            'move_damage_class',
            'names',
            'pokemon',
            'moves'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def damage_relations(self):
        return TypeRelations(self._damage_relations)

    @property
    def no_damage_to(self):
        return self.damage_relations.no_damage_to

    @property
    def half_damage_to(self):
        return self.damage_relations.half_damage_to

    @property
    def double_damage_to(self):
        return self.damage_relations.double_damage_to

    @property
    def no_damage_from(self):
        return self.damage_relations.no_damage_from

    @property
    def half_damage_from(self):
        return self.damage_relations.half_damage_from

    @property
    def double_damage_from(self):
        return self.damage_relations.double_damage_from

    @lazy_property
    def game_indices(self):
        return [common.GenerationGameIndex(**kwargs)
                for kwargs in self._game_indices]

    @lazy_property
    def generation(self):
        return common.NamedAPIResource(self._generation)

    @lazy_property
    def move_damage_class(self):
        return common.NamedAPIResource(self._move_damage_class)



    @lazy_property
    def pokemon(self):
        return [TypePokemon(**kwargs) for kwargs in self._names]

    @lazy_property
    def moves(self):
        return [common.NamedAPIResource(**kwargs) for kwargs in self._moves]


class TypeRelations:

    def __init__(self, **kwargs):
        self.no_damage_to = [common.NamedAPIResource(**t)
                             for t in kwargs['no_damage_to']]
        self.half_damage_to = [common.NamedAPIResource(**t)
                               for t in kwargs['half_damage_to']]
        self.double_damage_to = [common.NamedAPIResource(**t)
                                 for t in kwargs['double_damage_to']]
        self.no_damage_from = [common.NamedAPIResource(**t)
                               for t in kwargs['no_damage_from']]
        self.half_damage_from = [common.NamedAPIResource(**t)
                                 for t in kwargs['half_damage_from']]
        self.double_damage_from = [common.NamedAPIResource(**t)
                                   for t in kwargs['double_damage_from']]


class TypePokemon:

    def __init__(self, **kwargs):
        self.slot = kwargs['slot']
        self.pokemon = common.NamedAPIResource(**kwargs['pokemon'])


class PokemonResource(utility.CacheablePropertyResource):

    yaml_tag = '!PokemonResource'

    class Meta:
        name = 'Pokemon'
        resource_name = 'pokemon'
        cache_folder = 'pokemon/pokemon/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'base_experience',
            'height',
            'is_default',
            'order',
            'weight',
            'abilities',
            'forms',
            'game_indices',
            'held_items',
            'location_area_encounters',
            'moves',
            'sprites',
            'species',
            'stats',
            'types'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def abilities(self):
        print('retrieving abilities for {}'.format(id(self)))
        abilities = [PokemonAbility(**ability) for ability in self._abilities]
        abilities.sort(key=lambda a: a.slot)
        return abilities

    @lazy_property
    def forms(self):
        return [common.NamedAPIResource(**kwargs) for kwargs in self._forms]

    @lazy_property
    def game_indices(self):
        return [common.VersionGameIndex(**kwargs)
                for kwargs in self._game_indices]

    @lazy_property
    def types(self):
        types = [PokemonType(**type) for type in self._types]
        types.sort(key=lambda t: t.slot)
        return types

    @lazy_property
    def held_items(self):
        return [PokemonHeldItem(**item) for item in self._held_items]

    @lazy_property
    def moves(self):
        return [PokemonMove(**move) for move in self._moves]

    @lazy_property
    def sprites(self):
        return PokemonSprites(**self._sprites)

    @lazy_property
    def species(self):
        return common.NamedAPIResource(**self._species)

    @property
    def stats(self):
        return [PokemonStat(**stat) for stat in self._stats]

    @lazy_property
    def stats_dict(self):
        stats = {}
        for stat in self.stats:
            stats[stat.name] = stat
            stats[stat.id] = stat
        return stats

    @property
    def attack(self):
        return self.stats_dict['attack']

    @property
    def defense(self):
        return self.stats_dict['defense']

    @property
    def special_attack(self):
        return self.stats_dict['special-attack']

    @property
    def special_defense(self):
        return self.stats_dict['specialdefense']

    @property
    def speed(self):
        return self.stats_dict['speed']

    @property
    def hp(self):
        return self.stats_dict['hp']

    @lazy_property
    def location_area_encounters(self):
        url = 'http://pokeapi.co' + self._location_area_encounters
        return common.APIResource(url=url, resource_type='encounters')

    @staticmethod
    def get_url(url, **kwargs):
        if 'from_url' in kwargs:
            return kwargs['from_url']
        return '{}/{}/'.format(url, kwargs.get('uid'))


class PokemonAbility:

    def __init__(self, **kwargs):
        self.ability = common.NamedAPIResource(**kwargs['ability'])
        self.slot = kwargs['slot']
        self.is_hidden = kwargs['is_hidden']

    @property
    def name(self):
        return self.ability.name

    @property
    def id(self):
        return self.stat.id

    @property
    def url(self):
        return self.ability.url

    @property
    def resource(self):
        return self.ability.resource


class PokemonType:

    def __init__(self, **kwargs):
        self.type = common.NamedAPIResource(**kwargs['type'])
        self.slot = kwargs.get('slot')

    @property
    def name(self):
        return self.type.name

    @property
    def url(self):
        return self.type.url

    @property
    def id(self):
        return self.stat.id

    @property
    def resource(self):
        return self.type.resource


class PokemonHeldItemVersion:

    def __init__(self, **kwargs):
        self.version = common.NamedAPIResource(**kwargs['version'])
        self.rarity = kwargs['rarity']

    @property
    def name(self):
        return self.version.name

    @property
    def id(self):
        return self.version.id

    @property
    def url(self):
        return self.version.url


class PokemonHeldItem:

    def __init__(self, **kwargs):
        self.item = common.NamedAPIResource(**kwargs['item'])
        self.version_details = [PokemonHeldItemVersion(**d)
                                for d in kwargs['version_details']]
        self.version_dict = {}
        for v in self.version_details:
            self.version_dict[v.name] = v
            self.version_dict[v.id] = v

    @property
    def name(self):
        return self.item.name

    @property
    def url(self):
        return self.item.url

    @property
    def id(self):
        return self.item.id

    @property
    def resource(self):
        return self.item.resource

    def for_version(self, version):
        return self.version_dict[version]

    def rarity_in(self, version):
        return self.for_version(version).rarity


class PokemonMoveVersion:

    def __init__(self, **kwargs):
        self.move_learn_method = common.NamedAPIResource(
            **kwargs['move_learn_method']
        )
        self.version_group = common.NamedAPIResource(**kwargs['version_group'])
        self.level_learned_at = kwargs['level_learned_at']

    @property
    def name(self):
        return self.version_group.name

    @property
    def url(self):
        return self.version_group.url


class PokemonMove:

    def __init__(self, **kwargs):
        self.move = common.NamedAPIResource(**kwargs['move'])
        self.version_group_details = [PokemonMoveVersion(**v) for v in
                                      kwargs['version_group_details']]

    @property
    def name(self):
        return self.move.name

    @property
    def id(self):
        return self.move.id

    @property
    def url(self):
        return self.move.url


class PokemonStat:

    def __init__(self, **kwargs):
        self.stat = common.NamedAPIResource(**kwargs['stat'])
        self.effort = kwargs['effort']
        self.base_stat = kwargs['base_stat']

    @property
    def name(self):
        return self.stat.name

    @property
    def id(self):
        return self.stat.id

    @property
    def url(self):
        return self.stat.url


class PokemonSprites:

    def __init__(self, **kwargs):
        self.front_default = kwargs['front_default']
        self.front_shiny = kwargs['front_default']
        self.front_female = kwargs['front_default']
        self.front_shiny_female = kwargs['front_default']
        self.back_default = kwargs['back_default']
        self.back_shiny = kwargs['back_default']
        self.back_female = kwargs['back_default']
        self.back_shiny_female = kwargs['back_default']


class LocationAreaEncounter:

    def __init__(self, **kwargs):
        self.location_area = common.NamedAPIResource(**kwargs['location_area'])
        self.version_details = [common.VersionEncounterDetail(**deet)
                                for deet in kwargs['version_details']]