#!/usr/bin/env python
"""

"""
import unittest
import sys
import os
MAIN_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1, os.path.join(MAIN_DIR, 'includes'))
from common import get_value_of_players_hand


class PlayersHand(unittest.TestCase):

    def test_players_hand1(self):
        """
        Проверка, что карта-картинка рассматривается со значением 10

        :return:
        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(12, 0)
        cards.append(card)
        self.assertEqual(get_value_of_players_hand(cards), 10)

    def test_players_hand2(self):
        """
        Проверка, что туз рассматривается как мягкий (11)

        :return:
        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)
        cards.append(card)
        self.assertEqual(get_value_of_players_hand(cards), 11)

    def test_players_hand3(self):
        """
        Проверка, что начальный мягкий туз (11) превращается в твёрдый туз (1), 
        когда рука становится пустой.

        :return:
        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)
        cards.append(card)
        self.assertEqual(get_value_of_players_hand(cards), 11)
        card = PlayingCard(5, 0)
        cards.append(card)
        self.assertEqual(get_value_of_players_hand(cards), 16)
        card = PlayingCard(8, 0)
        cards.append(card)
        self.assertEqual(get_value_of_players_hand(cards), 14)

    def test_players_hand4(self):
        """
        Ещё одна проверка, которая показывает, что начальный мягкий туз (11) превращается в твёрдый туз (1), 
        когда рука становится пустой.

        :return:
        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)
        cards.append(card)
        self.assertEqual(get_value_of_players_hand(cards), 11)
        card = PlayingCard(3, 0)
        cards.append(card)
        self.assertEqual(get_value_of_players_hand(cards), 14)
        card = PlayingCard(13, 0)
        cards.append(card)
        self.assertEqual(get_value_of_players_hand(cards), 14)


if __name__ == "__main__":
    unittest.main()
