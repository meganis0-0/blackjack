#!/usr/bin/env python
"""

"""
import unittest
import sys
import os
MAIN_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1, os.path.join(MAIN_DIR, 'includes'))
from common import get_value_of_dealers_hand


class DealersHand(unittest.TestCase):

    def test_dealers_hand1(self):
        """
        Начинаем с туза, который должен оставаться на твёрдом (1) тузе, так как вторая
        карта (5) не даёт значения от 17 до 21, даже если туз рассматривается
        как мягкий (11) туз.

        :return: None

        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)
        cards.append(card)
        card = PlayingCard(5, 0)
        cards.append(card)
        self.assertEqual(get_value_of_dealers_hand(cards), 6)

    def test_dealers_hand2(self):
        """
        Начинаем с туза, который должен превратиться в мягкий (11) туз, как только
        появится вторая карта, которая является лицевой (10) картой и должна вернуть 21.

        :return: None

        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)  # Туз
        cards.append(card)
        card = PlayingCard(11, 0)  # Картинка, которая может столкнуться с мягким тузом
        cards.append(card)
        self.assertEqual(get_value_of_dealers_hand(cards), 21)

    def test_dealers_hand3(self):
        """
        Начните с картинки, которая может столкнуться с тузом и второй картой, 
        которая является тузом и должна вернуть 21.

        :return: None

        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(11, 0)  # Картинка, которая может столкнуться с мягким тузом
        cards.append(card)
        card = PlayingCard(1, 0)  # Туз
        cards.append(card)
        self.assertEqual(get_value_of_dealers_hand(cards), 21)

    def test_dealers_hand4(self):
        """
        Начните с туза, за которым следует 4, (получается 5) и еще один туз, который не будет
        в сумме больше 16, если считать его мягким, поэтому придерживайтесь жесткой интерпретации
        которые дают результат 6

        :return: None

        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)  # Туз
        cards.append(card)
        card = PlayingCard(4, 0)
        cards.append(card)
        card = PlayingCard(1, 0)  # Туз
        cards.append(card)
        self.assertEqual(get_value_of_dealers_hand(cards), 6)

    def test_dealers_hand5(self):
        """
        Начните с туза, за которым следует 5 (даёт 6) и ещё один туз, который
        даст больше 16, если рассматривать его как «мягкую» карту, что даёт результат 17

        :return: None

        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)  # Туз
        cards.append(card)
        card = PlayingCard(5, 0)
        cards.append(card)
        card = PlayingCard(1, 0)  # Туз
        cards.append(card)
        self.assertEqual(get_value_of_dealers_hand(cards), 17)

    def test_dealers_hand6(self):
        """
        Начните с туза, за которым следует двойка (даёт 3) и ещё один туз, который
        всё равно будет меньше 17. Затем добавьте четвёрку, которая даст 18, если предыдущий туз станет «мягким».

        :return: None

        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)  # Туз
        cards.append(card)
        card = PlayingCard(2, 0)  # 1 + 2 = 3
        cards.append(card)
        card = PlayingCard(1, 0)  # Туз + 3 = 4
        cards.append(card)
        card = PlayingCard(4, 0)  # Если заменить предыдущий туз на 11, получится (1 + 2 + 11 + 4 = 18)
        cards.append(card)
        self.assertEqual(get_value_of_dealers_hand(cards), 18)

    def test_dealers_hand7(self):
        """
        Начните с туза, за которым следуют двойка и десятка (10), что было бы сбросом (23), если бы
        первый туз считался слабым. Должен остаться сильный туз, и в итоге получится 20.

        :return: None

        """
        from playingcard import PlayingCard
        cards = []
        card = PlayingCard(1, 0)
        cards.append(card)
        card = PlayingCard(2, 0)
        cards.append(card)
        card = PlayingCard(13, 0)
        cards.append(card)
        card = PlayingCard(7, 0)
        cards.append(card)
        self.assertEqual(get_value_of_dealers_hand(cards), 20)


if __name__ == "__main__":
    unittest.main()
