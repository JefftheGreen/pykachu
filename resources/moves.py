# /usr/bin/env python
# -*- coding: utf-8 -*-
import resources.common as common
from universal import lazy_property
import resources.utility as utility


class MoveResource(utility.UtilityResource):
    """
    A resource representing a move.

    Moves are the skills of Pokémon in battle. In battle, a Pokémon uses one
    move each turn. Some moves (including those learned by Hidden Machine) can
    be used outside of battle as well, usually for the purpose of removing
    obstacles or exploring new areas.

        Fields:
            id (int)
                The identifier for this move resource
            name (str)
                The name for this move resource
            accuracy (int)
                The percent value of how likely this move is to be successful
            effect_chance (int)
                The percent value of how likely it is this moves effect will
                happen
            pp (int)
                Power points. The number of times this move can be used
            priority (int)
                A value between -8 and 8. Sets the order in which moves are
                executed during battle. See Bulbapedia for greater detail.
            power (int)
                The base power of this move with a value of 0 if it does not
                have a base power
            contest_combos (list of ContestComboSet)
                A detail of normal and super contest combos that require this
                move
            contest_type (NamedAPIResource -> ContestTypeResource)
                The type of appeal this move gives a Pokémon when used in a
                contest
            contest_effect (NamedAPIResource -> ContestEffectResourc)
                The effect the move has when used in a contest
            damage_class (NamedAPIResource -> MoveDamageClassResource)
                The type of damage the move inflicts on the target, e.g.
                physical
            effect_entries (list of VerboseEffect)
                The effect of this move listed in different languages
            effect_changes (list of AbilityEffectChange)
                The list of previous effects this move has had across version
                groups of the games
            flavor_text_entries (list of MoveFlavorText)
                The flavor text of this move listed in different languages
            generation (NamedAPIResource -> GenerationResource)
                The generation in which this move was introduced
            machines (list of MachineVersionDetail)
                A list of the machines that teach this move
            meta (MoveMetaData)
                Metadata about this move
            names (list of Name)
                The name of this move listed in different languages
            past_values (list of PastMoveStatValues)
                A list of move resource value changes across version groups of
                the game
            stat_changes (list of MoveStatChanges)
                A list of stats this moves effects and how much it effects them
            super_contest_effect (APIResource -> SuperContestEffectResource)
                The effect the move has when used in a super contest
            target (NamedAPIResource -> MoveTarget)
                The type of target that will receive the effects of the attack
            type (NamedAPIResource -> TypeResource)
                The elemental type of this move
    """

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
    """
    An object describing how a move can be combined with others in a contest.

        Fields:
            normal (ContestComboDetail)
                A detail of moves this move can be used before or after,
                granting additional appeal points in contests
            super (ContestComboDetail)
                A detail of moves this move can be used before or after,
                granting additional appeal points in super contests
    """

    def __init__(self, **kwargs):
        self.normal = ContestComboDetail(**kwargs['normal'])
        self.super = ContestComboDetail(**kwargs['super'])


class ContestComboDetail:
    """
    An object describing what moves can be used with a specific other one
    in a contest.

        Fields:
            use_before (list of NamedAPIResource -> MoveResource)
                A list of moves to use before this move
            use_after (list of NamedAPIResource -> Move Resource)
    """

    def __init__(self, **kwargs):
        self.use_before = [common.NamedAPIResource(**u)
                           for u in kwargs['use_before']]
        self.use_after = [common.NamedAPIResource(**u)
                          for u in kwargs['use_after']]


class MoveFlavorText(common.FlavorText):
    """
    An object describing a move's flavor text in a language and particular
    version.

        Fields:
            flavor_text (str)
                The localized flavor text for an api resource in a specific
                language
            language (NamedAPIResource -> LanguageResource)
                The language this name is in
            version_group (NamedAPIResource -> VersionGroupResource)
                The version group that uses this flavor text
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.version_group = common.NamedAPIResource(**kwargs['version_group'])


class MoveMetaData:
    """
    An object containing metadata about a move.

        Fields:
            ailment (NamedAPIResource -> MoveAilmentResource)
                The status ailment this move inflicts on its target
            category (NamedAPIResource -> MoveCategoryResource)
                The category of move this move falls under, e.g. damage or
                ailment
            min_hits (int)
                The minimum number of times this move hits. Null if it always
                only hits once.
            max_hits (int)
                The maximum number of times this move hits. Null if it always
                only hits once.
            min_turns (int)
                The minimum number of turns this move continues to take effect.
                Null if it always only lasts one turn.
            max_turns (int)
                The maximum number of turns this move continues to take effect.
                Null if it always only lasts one turn.
            drain (int)
                HP drain (if positive) or Recoil damage (if negative), in
                percent of damage done
            healing (int)
                The amount of hp gained by the attacking Pokemon, in percent of
                it's maximum HP
            crit_rate (int)
                Critical hit rate bonus
            ailment_chance (int)
                The likelihood this attack will cause an ailment
            flinch_chance (int)
                The likelihood this attack will cause the target Pokémon to
                flinch
            stat_chance (int)
                The likelihood this attack will cause a stat change in the
                target Pokémon
    """

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
    """
    An object describing how a move might change a stat.

        Fields:
            change (int)
                The amount of change
            stat (NamedAPIResource -> StatResource)
                The stat being affected
    """

    def __init__(self, **kwargs):
        self.change = kwargs['chance']
        self.stat = common.NamedAPIResource(**kwargs['stat'])


class PastMoveStatValues:
    """
    An object describing a move in previous versions.

        Fields:
            accuracy (int)
                The percent value of how likely this move is to be successful
            effect_chance (int)
                The percent value of how likely it is this moves effect will
                take effect
            power (int)
                The base power of this move with a value of 0 if it does not
                have a base power
            pp (int)
                Power points. The number of times this move can be used
            effect_entries (list of VerboseEffect)
                The effect of this move listed in different languages
            type (NamedAPIResource -> TypeResource)
                The elemental type of this move
            version_group (NamedAPIResource -> VersionGroupResource)
                The version group in which these move stat values were in effect
    """

    def __init__(self, **kwargs):
        self.accuracy = kwargs['accuracy']
        self.effect_chance = kwargs['effect_chance']
        self.power = kwargs['power']
        self.pp = kwargs['pp']
        self.effect_entries = [common.VerboseEffect(**e)
                               for e in kwargs['effect_entries']]
        self.type = common.NamedAPIResource(**kwargs['type'])
        self.version_group = common.NamedAPIResource(**kwargs['version_group'])


class MoveAilmentResource(utility.UtilityResource):
    """
    A resource describing a status effect.

    Move Ailments are status conditions caused by moves used during battle. See
    Bulbapedia for greater detail.

        Fields:
            id (int)
                The identifier for this move ailment resource
            name (str)
                The name for this move ailment resource
            moves (list of NamedAPIResource -> MoveResource)
                A list of moves that cause this ailment
            names (list of Name)
                The name of this move ailment listed in different languages
    """

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


class MoveBattleStyleResource(utility.UtilityResource):
    """
    A resource describing a move's battle style.

    Styles of moves when used in the Battle Palace. See Bulbapedia for greater
    detail.

        Fields:
            id (int)
                The identifier for this move battle style resource
            name (str)
                The name for this move battle style resource
            names (list of Name)
                The name of this move battle style listed in different languages
    """

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


class MoveCategoryResource(utility.UtilityResource):
    """
    A resource representing a category of moves.

    Very general categories that loosely group move effects.

        Fields:
            id (int)
                The identifier for this move category resource
            name (str)
                The name for this move category resource
            moves (list of NamedAPIResource -> MoveResource)
                A list of moves that fall into this category
            descriptions (list of Description)
                The description of this move ailment listed in different
                languages
    """

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
    def descriptions(self):
        return [common.Description(**kwargs) for kwargs in self._descriptions]


class MoveDamageClassResource(utility.UtilityResource):
    """
    A resource representing a type of damage.

    Damage classes moves can have, e.g. physical, special, or non-damaging.

        Fields:
            id (int)
                The identifier for this move damage class resource
            name (str)
                The name for this move damage class resource
            descriptions (list of Description)
                The description of this move damage class listed in different
                languages
            moves (list of NamedAPIResource -> MoveResource)
                A list of moves that fall into this damage class
            names (list of Name)
                The name of this move damage class listed in different languages
    """

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


class MoveLearnMethodResource(utility.UtilityResource):
    """
    A resource representing a way pokemon can learn a move

    Methods by which Pokémon can learn moves.

        Fields:
            id (int)
                The identifier for this move learn method resource
            name (str)
                The name for this move learn method resource
            descriptions (list of Description)
                The description of this move learn method listed in different
                languages
            names (list of Name)
                The name of this move learn method listed in different languages
            version_groups (list of NamedAPIResource -> VersionGroupResource)
                A list of version groups where moves can be learned through this
                method
    """

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


class MoveTargetsResource(utility.UtilityResource):
    """
    A resource describing how a move is targeted.

    Targets moves can be directed at during battle. Targets can be Pokémon,
    environments or even other moves.

        Fields:
            id (int)
                The identifier for this move target resource
            name (str)
                The name for this move target resource
            descriptions (list of Description)
                The description of this move target listed in different
                languages
            moves (list of NamedAPIResource -> MoveResource)
                A list of moves that that are directed at this target
            names (list of Name)
                The name of this move target listed in different languages
                The name of this move target listed in different languages
    """

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

