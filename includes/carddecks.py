#!/usr/bin/env python
"""
Создает колоду игральных карт (обычную колоду из 52 карт) или виртуальную «обувную» колоду из
карт, если определено более одной колоды.
При создании одной или нескольких колод они будут перемешаны.

"""
from random import shuffle
from playingcard import PlayingCard


class CardDecks(object):
    """
    При создании экземпляра содержит список
    :meth:`lib.playingcard.PlayingCard` объекты в рандомном порядке.

    """

    def __init__(self, num_of_decks=1):
        """
        Создаем одну или несколько колод игральных карт и перемешиваем их все
        вместе в списке.

        """
        self.__card_decks = []
        for num in range(0, num_of_decks):
            for suit in range(0, 4):
                for rank in range(1, 14):
                    instance = PlayingCard(rank, suit)
                    self.__card_decks.append(instance)
        self.shuffle()

    def shuffle(self):
        """
        Перетасовываем все карты в этом списке экземпляров.

        :return: None

        """
        shuffle(self.__card_decks)

    def pop(self):
        """
        Достаем последнюю карту из списка.

        :return: A :meth:`lib.playingcard.PlayingCard` object.

        """
        return self.__card_decks.pop()

    def length(self):
        """
        :return: Длина (количество оставшихся карт) в списке.

        """
        return len(self.__card_decks)


class TestingCardDeck(object):
    """
    Используется для создания предварительно определенной колоды для тестирования

    """

    def __init__(self):
        """
        Создайем экземпляр колоды, содержащей
        :meth:`lib.playingcard.PlayingCard` объекты,
        которые имеют заранее заданные значения для тестирования конкретных
        сценариев в игре «Блэк Джек»

        """
        self.__card_decks = []

        for x in range(1, 52):  # Заполнение колоды 52-мя картами
            instance = PlayingCard(7, 1)
            self.__card_decks.append(instance)

        # Оставляем на 19 (туз + 8), и дилер получит два туза 1+1+4+(общее значение в колоде выше)
        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(1, 0))
        self.__card_decks.append(PlayingCard(8, 3))
        self.__card_decks.append(PlayingCard(1, 3))
        self.__card_decks.append(PlayingCard(1, 2))

        # Две десятки игроку, чтобы использовать их для разделения, а затем два туза, чтобы посмотреть, как
        # разыгрывается двойной блэкджек.
        self.__card_decks.append(PlayingCard(6, 2))
        self.__card_decks.append(PlayingCard(8, 1))
        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(10, 0))

        # Первая раздача для игрока - это блэкджек
        self.__card_decks.append(PlayingCard(6, 2))
        self.__card_decks.append(PlayingCard(10, 1))
        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(1, 0))

        # Начинаем с низкой руки, чтобы игрок мог протестировать удвоение
        self.__card_decks.append(PlayingCard(6, 2))
        self.__card_decks.append(PlayingCard(2, 1))
        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(2, 0))

        # Создаем сплит, первая рука в порядке, а вторая проигрыш
        self.__card_decks.append(PlayingCard(12, 1))
        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(2, 0))
        self.__card_decks.append(PlayingCard(6, 2))
        self.__card_decks.append(PlayingCard(8, 1))
        self.__card_decks.append(PlayingCard(4, 1))
        self.__card_decks.append(PlayingCard(8, 0))

    def pop(self):
        """
        Удаляет последний элемент из списка и возвращает его.

        :return: A :meth:`lib.playingcard.PlayingCard` object.

        """
        return self.__card_decks.pop()

    def length(self):
        """
        :return: Длину оставшейся колоды.

        """
        return len(self.__card_decks)
