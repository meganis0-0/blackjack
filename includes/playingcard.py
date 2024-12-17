#!/usr/bin/env python
"""
Класс «Игральная карта»

Этот класс создаёт экземпляр игральной карты с допустимым значением ранга от 1 до 13 и масти от 0 до 3.

"""
import sys
import traceback


class PlayingCard(object):
    """
    Класс представляющий игральную карту
    """
    def __init__(self, rank, suit):
        try:
            if not isinstance(rank, int):
                raise ValueError("Error: rank has to be integer: "
                                 + str(rank))
            elif rank < 1 or rank > 13:
                raise ValueError("Error: rank out of range (1-13): "
                                 + str(rank))
            else:
                self.__rank = rank
        except ValueError:
            traceback.print_exc()
            sys.exit()

        try:
            if not isinstance(suit, int):
                raise ValueError("Error: suit has to be integer: "
                                 + str(suit))
            elif suit < 0 or suit > 3:
                raise ValueError("Error: suit out of range (0-3): "
                                 + str(suit))
            else:
                self.__suit = suit
        except ValueError:
            traceback.print_exc()
            sys.exit()

    def get_rank(self):
        """
        :return: Ранг этого экземпляра.

        """
        return self.__rank

    def get_suit(self):
        """
        :return: Масть этого экземпляра.

        """
        return self.__suit
