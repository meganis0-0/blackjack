#!/usr/bin/env python
"""
Базовый тест для игры в блэкджек.

"""
import unittest
import sys
import os
MAIN_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1, os.path.join(MAIN_DIR, 'includes'))


class UnitTests(unittest.TestCase):

    def test_can_import_playingcard(self):
        # Выдает ошибку импорта, если пакет не может быть импортирован
        from playingcard import PlayingCard

    def test_can_import_carddeck(self):
        # Выдает ошибку импорта, если пакет не может быть импортирован
        from carddecks import CardDecks
        
    def test_invalid_card_rank_type(self):
        # Вызывает SystemExit, если тип ранга не является целым числом (с использованием float)
        from playingcard import PlayingCard
        with self.assertRaises(SystemExit):
            PlayingCard(1.0, 0)
            
    def test_invalid_card_rank_range_low(self):
        # Вызывает SystemExit, если тип ранга ниже 1
        from playingcard import PlayingCard
        with self.assertRaises(SystemExit):
            PlayingCard(0, 0)
            
    def test_invalid_card_rank_range_high(self):
        # Вызывает SystemExit если ранг выше 13
        from playingcard import PlayingCard
        with self.assertRaises(SystemExit):
            PlayingCard(14, 0)
           
    def test_invalid_card_suit_type(self):
        # Вызывает SystemExit если ранг не int (используя string)
        from playingcard import PlayingCard
        with self.assertRaises(SystemExit):
            PlayingCard(1, "Diamonds")
 
    def test_invalid_card_suit_range_low(self):
        # Вызывает SystemExit если ранг ниже 0
        from playingcard import PlayingCard
        with self.assertRaises(SystemExit):
            PlayingCard(1, -1)

    def test_invalid_card_suit_range_high(self):
        # Вызывает SystemExit если тип ранга выше 3
        from playingcard import PlayingCard
        with self.assertRaises(SystemExit):
            PlayingCard(1, 4)

    def test_card_get_rank(self):
        # Подтверджает, если ранг созданного экземпляра не возвращается функцией get_rank()
        from playingcard import PlayingCard
        card = PlayingCard(1, 0)
        self.assertTrue(card.get_rank() == 1)

    def test_card_get_suit(self):
        # Подтверджает, если созданный экземпляр suit не возвращается функцией get_suit() 
        from playingcard import PlayingCard
        card = PlayingCard(1, 0)
        self.assertTrue(card.get_suit() == 0)        
            
    def test_size_of_new_carddeck(self):
        # Проверяет, не превышает ли размер вновь созданной колоды карт по умолчанию 52 карты
        from carddecks import CardDecks
        deck = CardDecks()
        self.assertTrue(deck.length() == 52)

    def test_size_of_new_double_carddeck(self):
        # Проверяет, содержит ли вновь созданная колода карт по умолчанию 104 карты
        from carddecks import CardDecks
        decks = CardDecks(2)
        self.assertTrue(decks.length() == 104)
        
    def test_new_carddeck_pop(self):
        # Подтверждает, что pop не удаляет карту из колоды
        from carddecks import CardDecks
        deck = CardDecks()  # длина 52
        deck.pop()
        self.assertTrue(deck.length() == 51)


if __name__ == "__main__":
    unittest.main()
