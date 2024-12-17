#!/usr/bin/env python
"""
Простая проверка карточной колоды и классов игральных карт

"""
import sys
import os

MAIN_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1, os.path.join(MAIN_DIR, 'includes'))
from carddecks import CardDecks

CARD_RANK = ["Invalid", "Ace", "Two", "Three", "Four", "Five", "Six",
             "Seven", "Eight", "Nine", "Ten", "Jack", "Queen", "King"]
CARD_SUIT = ["Spades", "Clubs", "Diamonds", "Hearts"]

DECK = CardDecks(2)
COUNT = 0
while DECK.length():
    COUNT += 1
    CARD = DECK.pop()
    print(str(COUNT) + ": " + CARD_RANK[CARD.get_rank()] + " of " + CARD_SUIT[CARD.get_suit()])
