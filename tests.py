# /usr/bin/env python
# -*- coding: utf-8 -*-

import unittest
import client
import resources
import os
import timeit
from datetime import datetime as dt
import time


class MyTestCase(unittest.TestCase):

    def setUp(self):
        self.client = client.BeckettClient()
        self.pokemon_client = client.PokemonClient()
        self.bulbasaur = self.client.get_pokemon(uid=3)[0]
        self.cached_bulbasaur = self.pokemon_client.get_pokemon(uid=3)[0]

    def test_property_resource(self):
        assert self.cached_bulbasaur.id == 3
        assert not hasattr(self.cached_bulbasaur, '_id')
        for i in range(len(self.cached_bulbasaur.abilities)):
            ability = self.cached_bulbasaur.abilities[i]
            assert isinstance(ability, resources.PokemonAbility)
            assert ability.name in ['chlorophyll', 'overgrow']
            assert ability.slot in [1, 3]
            assert ability.is_hidden in [True, False]
            assert (ability.slot == 1) != ability.is_hidden
            assert isinstance(ability.resource[0], resources.AbilityResource)
        assert [t.name for t in self.bulbasaur.types] == ['grass', 'poison']

    def test_caching(self):
        assert os.path.isfile(os.path.expanduser('~/.PykachuCache/') +
                              'expiration.cnf')
        assert os.path.isfile(os.path.expanduser('~/.PykachuCache/') +
                              'pokemon/pokemon/3')
        assert self.bulbasaur.name == self.cached_bulbasaur.name
        assert ([a.name for a in self.bulbasaur.abilities] ==
                [a.name for a in self.cached_bulbasaur.abilities])
        #[self.pokemon_client.get_pokemon(uid=x) for x in range(1, 10)]


if __name__ == '__main__':
    unittest.main()