#!/usr/bin/env python
# -*- coding:utf-8 -*-
#
# ----------------------------------------------------------------------
# ccGains - Create capital gains reports for cryptocurrency trading.
# Copyright (C) 2017 Jürgen Probst
#
# This file is part of ccGains.
#
# ccGains is free software: you can redistribute it and/or modify it
# under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# ccGains is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public
# License along with ccGains. If not, see <http://www.gnu.org/licenses/>.
# ----------------------------------------------------------------------
#
# Get the latest version at: https://github.com/probstj/ccGains
#

from __future__ import division

import unittest

from ccgains import relations
from ccgains.relations import CurrencyPair, RecipeStep, Recipe


class TestCurrencyRelation(unittest.TestCase):
    def setUp(self):
        self.rel = relations.CurrencyRelation()

    def test_update_pairs_one(self):
        # Create dummy pairs:
        pairs = [("A", "B")]
        # Expected result:
        d = {("A", "B"): (1, [("A", "B", False)]), ("B", "A"): (1, [("A", "B", True)])}

        # Make dummy historic data dict:
        for p in pairs:
            self.rel.historic_prices[p] = None
        self.rel.update_available_pairs()

        self.assertDictEqual(self.rel.recipes, d)

    def test_update_pairs_two_separate(self):
        # Create dummy pairs:
        pairs = [("A", "B"), ("C", "D")]
        # Expected result:
        d = {
            ("A", "B"): (1, [("A", "B", False)]),
            ("B", "A"): (1, [("A", "B", True)]),
            ("C", "D"): (1, [("C", "D", False)]),
            ("D", "C"): (1, [("C", "D", True)]),
        }

        # Make dummy historic data dict:
        for p in pairs:
            self.rel.historic_prices[p] = None
        self.rel.update_available_pairs()

        self.assertDictEqual(self.rel.recipes, d)

    def test_update_pairs_two_joined(self):
        # Create dummy pairs:
        pairs = [("A", "B"), ("B", "C")]
        # Expected result:
        d = {
            ("A", "B"): (1, [("A", "B", False)]),
            ("B", "A"): (1, [("A", "B", True)]),
            ("B", "C"): (1, [("B", "C", False)]),
            ("C", "B"): (1, [("B", "C", True)]),
            ("A", "C"): (2, [("A", "B", False), ("B", "C", False)]),
            ("C", "A"): (2, [("B", "C", True), ("A", "B", True)]),
        }

        # Make dummy historic data dict:
        for p in pairs:
            self.rel.historic_prices[p] = None
        self.rel.update_available_pairs()

        self.assertDictEqual(self.rel.recipes, d)

    def test_update_pairs_two_joinedreverse(self):
        # Create dummy pairs:
        pairs = [("A", "B"), ("C", "B")]
        # Expected result:
        d = {
            ("A", "B"): (1, [("A", "B", False)]),
            ("B", "A"): (1, [("A", "B", True)]),
            ("C", "B"): (1, [("C", "B", False)]),
            ("B", "C"): (1, [("C", "B", True)]),
            ("A", "C"): (2, [("A", "B", False), ("C", "B", True)]),
            ("C", "A"): (2, [("C", "B", False), ("A", "B", True)]),
        }

        # Make dummy historic data dict:
        for p in pairs:
            self.rel.historic_prices[p] = None
        self.rel.update_available_pairs()

        self.assertDictEqual(self.rel.recipes, d)

    def test_update_pairs_two_separate_then_joined(self):
        # Diff for this test case might be long. Disable length constraint:
        oldmaxDiff = self.maxDiff
        self.maxDiff = None

        # Create dummy pairs:
        pairs = [("A", "B"), ("C", "D")]
        pair_extra = ("B", "C")
        # Expected result:
        d = {
            ("A", "B"): (1, [("A", "B", False)]),
            ("B", "A"): (1, [("A", "B", True)]),
            ("C", "D"): (1, [("C", "D", False)]),
            ("D", "C"): (1, [("C", "D", True)]),
        }
        d_extra = {
            ("B", "C"): (1, [("B", "C", False)]),
            ("C", "B"): (1, [("B", "C", True)]),
            ("A", "C"): (2, [("A", "B", False), ("B", "C", False)]),
            ("C", "A"): (2, [("B", "C", True), ("A", "B", True)]),
            ("B", "D"): (2, [("B", "C", False), ("C", "D", False)]),
            ("D", "B"): (2, [("C", "D", True), ("B", "C", True)]),
            ("A", "D"): (3, [("A", "B", False), ("B", "C", False), ("C", "D", False)]),
            ("D", "A"): (3, [("C", "D", True), ("B", "C", True), ("A", "B", True)]),
        }

        # Make dummy historic data dict:
        for p in pairs:
            self.rel.historic_prices[p] = None
        self.rel.update_available_pairs()

        self.assertDictEqual(self.rel.recipes, d)

        # make this a dummy HistoricData object:
        self.cfrom, self.cto = pair_extra
        self.rel.add_historic_data(self)

        d.update(d_extra)
        self.assertDictEqual(self.rel.recipes, d)

        # If everything went well, reset maxDiff:
        self.maxDiff = oldmaxDiff

    def test_update_pairs_two_separate_then_joinedreverse(self):
        # Diff for this test case might be long. Disable length constraint:
        oldmaxDiff = self.maxDiff
        self.maxDiff = None

        # Create dummy pairs:
        pairs = [("A", "B"), ("C", "D")]
        pair_extra = ("C", "B")
        # Expected result:
        d = {
            ("A", "B"): (1, [("A", "B", False)]),
            ("B", "A"): (1, [("A", "B", True)]),
            ("C", "D"): (1, [("C", "D", False)]),
            ("D", "C"): (1, [("C", "D", True)]),
        }
        d_extra = {
            ("B", "C"): (1, [("C", "B", True)]),
            ("C", "B"): (1, [("C", "B", False)]),
            ("A", "C"): (2, [("A", "B", False), ("C", "B", True)]),
            ("C", "A"): (2, [("C", "B", False), ("A", "B", True)]),
            ("B", "D"): (2, [("C", "B", True), ("C", "D", False)]),
            ("D", "B"): (2, [("C", "D", True), ("C", "B", False)]),
            ("A", "D"): (3, [("A", "B", False), ("C", "B", True), ("C", "D", False)]),
            ("D", "A"): (3, [("C", "D", True), ("C", "B", False), ("A", "B", True)]),
        }

        # Make dummy historic data dict:
        for p in pairs:
            self.rel.historic_prices[p] = None
        self.rel.update_available_pairs()

        self.assertDictEqual(self.rel.recipes, d)

        # make this a dummy HistoricData object:
        self.cfrom, self.cto = pair_extra
        self.rel.add_historic_data(self)

        d.update(d_extra)
        self.assertDictEqual(self.rel.recipes, d)

        # If everything went well, reset maxDiff:
        self.maxDiff = oldmaxDiff

    def test_update_pairs_two_separate_then_joined_then_optimized(self):
        # Create dummy pairs:
        pairs = [("A", "B"), ("C", "D")]
        pair_extra = ("B", "C")

        # Make dummy historic data dict:
        for p in pairs:
            self.rel.historic_prices[p] = None
        self.rel.update_available_pairs()

        # make this a dummy HistoricData object:
        self.cfrom, self.cto = pair_extra
        self.rel.add_historic_data(self)

        # add pair with direct exchange rate data:
        direct_pair = ("A", "D")
        self.cfrom, self.cto = direct_pair
        self.rel.add_historic_data(self)

        self.assertEqual(self.rel.recipes[direct_pair], (1, [("A", "D", False)]))
        self.assertEqual(self.rel.recipes[direct_pair[::-1]], (1, [("A", "D", True)]))


class TestRelationCustomTypes(unittest.TestCase):
    def test_currency_pair_reverse(self):
        """Test reversing a CurrencyPair results in base and quote swapped"""
        pair = CurrencyPair("BTC", "USD")
        expected_reversed_pair = CurrencyPair("USD", "BTC")

        self.assertEqual(pair.reversed(), expected_reversed_pair)

    def test_currency_pair_add(self):
        """Test that adding one CurrencyPair to another results in a CurrencyPair
        with (first.base, second.quote)
        """
        first = CurrencyPair("XRP", "BTC")
        second = CurrencyPair("BTC", "USD")
        expected_pair = CurrencyPair("XRP", "USD")
        self.assertEqual(first + second, expected_pair)

    def test_currency_pair_immutable_and_hashable(self):
        """CurrencyPairs are used as dictionary keys, so must be hashable
        and immutable. Hashes of two equal CurrencyPairs must be equal
        """
        pair = CurrencyPair("XRP", "BTC")
        second_pair = CurrencyPair("XRP", "BTC")
        first_hash = hash(pair)

        with self.assertRaises(AttributeError):
            pair.base = "ETH"

        self.assertEqual(hash(pair), first_hash)

        self.assertEqual(pair, second_pair)

        self.assertEqual(hash(pair), hash(second_pair))

    def test_recipe_step_to_recipe(self):
        """Test that a RecipeStep can be turned into a correct Recipe"""
        step = RecipeStep("XLM", "ETH", False)
        recipe = step.as_recipe()
        expected_recipe = Recipe(1, [RecipeStep("XLM", "ETH", False)])

        self.assertEqual(recipe, expected_recipe)

    def test_recipe_step_reversal(self):
        """Reversing a RecipeStep should invert the reciprocal and leave currency
        ordering intact
        """

        step = RecipeStep("ZEC", "BNB", False)
        expected_reversed = RecipeStep("ZEC", "BNB", True)
        self.assertEqual(step.reversed(), expected_reversed)

    def test_add_recipe_steps(self):
        """Adding two recipe steps should result in a Recipe with correct order"""
        step_one = RecipeStep("ZEC", "BNB", False)
        step_two = RecipeStep("BNB", "BTC", False)
        expected_recipe = Recipe(
            2, [RecipeStep("ZEC", "BNB", False), RecipeStep("BNB", "BTC", False)]
        )

        self.assertEqual(step_one + step_two, expected_recipe)

    def test_add_recipe_step_to_recipe(self):
        """Adding a RecipeStep to a Recipe should put the step in the correct location
        and increment the number of steps
        """

        step = RecipeStep("ZEC", "BNB", False)
        recipe = Recipe(
            2, [RecipeStep("BNB", "BTC", False), RecipeStep("BTC", "USD", False)]
        )

        # RecipeStep + Recipe
        expected_add_right = Recipe(
            3,
            [
                RecipeStep("ZEC", "BNB", False),
                RecipeStep("BNB", "BTC", False),
                RecipeStep("BTC", "USD", False),
            ],
        )

        # Recipe + RecipeStep
        expected_add_left = Recipe(
            3,
            [
                RecipeStep("BNB", "BTC", False),
                RecipeStep("BTC", "USD", False),
                RecipeStep("ZEC", "BNB", False),
            ],
        )

        self.assertEqual(step + recipe, expected_add_right)
        self.assertEqual(recipe + step, expected_add_left)

    def test_recipe_comparisons(self):
        """Test comparison operators on Recipes. GT/LT are based on number of steps.
        Equality requires same number of steps and same list (including ordering) of
        each step
        """

        smaller_recipe = Recipe(
            2, [RecipeStep("BNB", "BTC", False), RecipeStep("BTC", "USD", False)]
        )

        bigger_recipe = Recipe(
            3,
            [
                RecipeStep("BNB", "BTC", False),
                RecipeStep("BTC", "USD", False),
                RecipeStep("ZEC", "BNB", False),
            ],
        )
        bigger_recipe_different_order = Recipe(
            3,
            [
                RecipeStep("BTC", "USD", False),
                RecipeStep("BNB", "BTC", False),
                RecipeStep("ZEC", "BNB", False),
            ],
        )

        self.assertLess(smaller_recipe, bigger_recipe)
        self.assertGreater(bigger_recipe, smaller_recipe)
        self.assertNotEqual(bigger_recipe, bigger_recipe_different_order)

    def test_add_recipe_to_recipe(self):
        """Recipe + Recipe should give a new recipe with steps in order"""
        recipe_one = Recipe(
            2, [RecipeStep("BNB", "BTC", False), RecipeStep("BTC", "USD", False)]
        )
        recipe_two = Recipe(
            3,
            [
                RecipeStep("BNB", "BTC", False),
                RecipeStep("BTC", "USD", False),
                RecipeStep("ZEC", "BNB", False),
            ],
        )

        # one + two
        expected_add_right = Recipe(
            5,
            [
                RecipeStep("BNB", "BTC", False),  # recipe_one
                RecipeStep("BTC", "USD", False),  # recipe_one
                RecipeStep("BNB", "BTC", False),  # recipe_two
                RecipeStep("BTC", "USD", False),  # recipe_two
                RecipeStep("ZEC", "BNB", False),  # recipe_two
            ],
        )

        # two + one
        expected_add_left = Recipe(
            5,
            [
                RecipeStep("BNB", "BTC", False),  # recipe_two
                RecipeStep("BTC", "USD", False),  # recipe_two
                RecipeStep("ZEC", "BNB", False),  # recipe_two
                RecipeStep("BNB", "BTC", False),  # recipe_one
                RecipeStep("BTC", "USD", False),  # recipe_one
            ],
        )

        self.assertEqual(recipe_one + recipe_two, expected_add_right)
        self.assertEqual(recipe_two + recipe_one, expected_add_left)


if __name__ == "__main__":
    unittest.main()
