# /usr/bin/env python
# -*- coding: utf-8 -*-
import resources.common as common
from universal import lazy_property
import resources.utility as utility


class MoveResource(utility.CacheablePropertyResource):

    yaml_tag = '!MoveResource'

    class Meta:
        name = "Move"
        resource_name = "move"
        cache_folder = 'moves/moves/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'accuracy',
            'effect_chance',
            'pp',
            'priority',
            'power',
            'contest_combos',
            'contest_type',
            'contest_effect',
            'damage_class',
            'effect_entries',
            'effect_changes',
            'generation',
            'machines',
            'meta',
            'names',
            'past_values',
            'stat_changes',
            'super_contest_effect',
            'target',
            'type'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def contest_combos(self):
        return ContestComboSets(**self._contest_combos)

    @lazy_property
    def contest_type(self):
        return common.NamedAPIResource(**self._contest_type)

    @lazy_property
    def contest_effect(self):
        return common.APIResource(**self._contest_effect)

    @lazy_property
    def damage_class(self):
        return common.NamedAPIResource(**self._damage_class)

    @lazy_property
    def effect_entries(self):
        return [common.VerboseEffect(**kwargs)
                for kwargs in self._effect_entries]

    @lazy_property
    def effect_changes(self):
        return [common.EffectChange(**kwargs)
                for kwargs in self._effect_changes]

    @lazy_property
    def flavor_text_entries(self):
        return [MoveFlavorText(**kwargs) for kwargs in self._flavor_text_entries]

    @lazy_property
    def generation(self):
        return common.NamedAPIResource(**self._generation)

    @lazy_property
    def machines(self):
        return [common.MachineVersionDetail(**kwargs)
                for kwargs in self._machines]

    @lazy_property
    def meta(self):
        return MoveMetaData(**self._meta)


    @lazy_property
    def past_values(self):
        return [PastMoveStatValues(**kwargs) for kwargs in self._past_values]

    @lazy_property
    def stat_changes(self):
        return [MoveStatChange(**kwargs) for kwargs in self._stat_changes]

    @lazy_property
    def super_contest_effect(self):
        return common.APIResource(**self._super_contest_effect)

    @lazy_property
    def target(self):
        return common.NamedAPIResource(**self._target)

    @lazy_property
    def type(self):
        return common.NamedAPIResource(**self._type)


class ContestComboSets:

    def __init__(self, **kwargs):
        self.normal = ContestComboDetail(**kwargs['normal'])
        self.super = ContestComboDetail(**kwargs['super'])


class ContestComboDetail:

    def __init__(self, **kwargs):
        self.use_before = [common.NamedAPIResource(**u)
                           for u in kwargs['use_before']]
        self.use_after = [common.NamedAPIResource(**u)
                          for u in kwargs['use_after']]


class MoveFlavorText(common.FlavorText):

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.version_group = common.NamedAPIResource(**kwargs['version_group'])


class MoveMetaData:

    def __init__(self, **kwargs):
        self.ailment = common.NamedAPIResource(**kwargs['ailment'])
        self.category = common.NamedAPIResource(**kwargs['category'])
        self.min_hits = kwargs['min_hits']
        self.max_hits = kwargs['max_hits']
        self.min_turns = kwargs['min_turns']
        self.max_turns = kwargs['max_turns']
        self.drain = kwargs['drain']
        self.healing = kwargs['healing']
        self.crit_rate = kwargs['hit_rate']
        self.ailment_chance = kwargs['ailment_chance']
        self.flinch_chance = kwargs['flinch_chance']
        self.stat_chance = kwargs['stat_chance']


class MoveStatChange:

    def __init__(self, **kwargs):
        self.change = kwargs['chance']
        self.stat = common.NamedAPIResource(**kwargs['stat'])


class PastMoveStatValues:

    def __init__(self, **kwargs):
        self.accuracy = kwargs['accuracy']
        self.effect_chance = kwargs['effect_chance']
        self.power = kwargs['power']
        self.pp = kwargs['pp']
        self.effect_entries = [common.VerboseEffect(**e)
                               for e in kwargs['effect_entries']]
        self.type = common.NamedAPIResource(**kwargs['type'])
        self.version_group = common.NamedAPIResource(**kwargs['version_group'])


class MoveAilmentResource(utility.CacheablePropertyResource):

    yaml_tag = '!MoveAilmentResource'

    class Meta:
        name = "Move Ailment"
        resource_name = "move-ailment"
        cache_folder = 'moves/ailment/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'moves',
            'names'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def moves(self):
        return [common.NamedAPIResource(**kwargs) for kwargs in self._moves]


class MoveBattleStyleResource(utility.CacheablePropertyResource):

    yaml_tag = '!MoveBattleStyleResource'

    class Meta:
        name = "MoveBattleStyle"
        resource_name = "move-battle-style"
        cache_folder = 'moves/battle-style/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'names'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )


class MoveCategoryResource(utility.CacheablePropertyResource):

    yaml_tag = '!MoveCategoryResource'

    class Meta:
        name = "Move Category"
        resource_name = "move-category"
        cache_folder = 'moves/categories/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'moves',
            'descriptions'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def moves(self):
        return [common.NamedAPIResource(**kwargs) for kwargs in self._moves]

    @lazy_property
    def descriptions(self):
        return [common.Description(**kwargs) for kwargs in self._descriptions]


class MoveDamageClassResource(utility.CacheablePropertyResource):

    yaml_tag = '!MoveDamageClassResource'

    class Meta:
        name = "Move Damage Class"
        resource_name = "move-damage-class"
        cache_folder = 'moves/damage-class/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'descriptions',
            'moves',
            'names'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def descriptions(self):
        return [common.Description(**kwargs) for kwargs in self._descriptions]

    @lazy_property
    def moves(self):
        return [common.NamedAPIResource(**kwargs) for kwargs in self._moves]


class MoveLearnMethodResource(utility.CacheablePropertyResource):

    yaml_tag = '!MoveLearnMethodResource'

    class Meta:
        name = "Move Learn Method"
        resource_name = "move-learn-method"
        cache_folder = 'moves/learn-method/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'descriptions',
            'names',
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
        return [common.Description(**kwargs) for kwargs in self._descriptions]



    @lazy_property
    def version_groups(self):
        return [common.NamedAPIResource(**kwargs)
                for kwargs in self._version_groups]


class MoveTargetsResource(utility.CacheablePropertyResource):

    yaml_tag = '!MoveTargetsResource'

    class Meta:
        name = "Move Targets"
        resource_name = "move-targets"
        cache_folder = 'moves/targets/'
        identifier = 'id'
        attributes = (
            'id',
            'name',
            'descriptions',
            'moves',
            'names'
        )
        valid_status_codes = (
            200,
        )
        methods = (
            'get',
        )

    @lazy_property
    def descriptions(self):
        return [common.Description(**kwargs) for kwargs in self._descriptions]

    @lazy_property
    def moves(self):
        return [common.NamedAPIResource(**kwargs) for kwargs in self._moves]

