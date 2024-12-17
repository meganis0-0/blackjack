#!/usr/bin/env python
"""
Все глобальные константы и переменные, используемые в игре в блэкджек.

"""

# Standard imports
# import inspect  # Используется для вывода названия функции в инструкциях журнала
import logging

# Установка уровней логирования
logging.basicConfig(
    # filename='blackjack_debug.log',
    # filemode='w', 
    # level=logging.DEBUG,
    # level=logging.INFO,
    # level=logging.WARNING,
    format="%(asctime)s:%(levelname)s:%(module)s:%(lineno)d:%(message)s"
    )

####################
# Глобальные переменные #
####################

# Пути
IMAGE_PATH = 'images/'
IMAGE_PATH_CARDS = 'images/cards/'
IMAGE_PATH_CHIPS = 'images/casino_chips/'
IMAGE_PATH_BUTTONS = 'images/buttons/'
SOUND_PATH = 'sounds/'
# ранее я использовал IMAGE_PATH = "./images/", который также работает

# Изображение обратной стороны карты, использованное для вывода начальной скрытой карты дилера
CARDBACK_FILENAME = "cardback1.png"

# Изображения-кнопки
PLAY_BUTTON_FILENAME_ON = "play_button_blue.png"
PLAY_BUTTON_FILENAME_OFF = "play_button_blue_fade.png"
HIT_BUTTON_FILENAME_ON = "hit_button_blue.png"
HIT_BUTTON_FILENAME_OFF = "hit_button_blue_fade.png"
STAND_BUTTON_FILENAME_ON = "stand_button_blue.png"
STAND_BUTTON_FILENAME_OFF = "stand_button_blue_fade.png"
SPLIT_BUTTON_FILENAME_ON = "split_button_blue.png"
SPLIT_BUTTON_FILENAME_OFF = "split_button_blue_fade.png"
DOUBLE_DOWN_BUTTON_FILENAME_ON = "doubledown_button_blue.png"
DOUBLE_DOWN_BUTTON_FILENAME_OFF = "doubledown_button_blue_fade.png"
UNDO_BET_BUTTON_FILENAME_ON = "undobet_button_blue.png"
UNDO_BET_BUTTON_FILENAME_OFF = "undobet_button_blue_fade.png"

# Изображения фишек
CHIP_5_FILENAME_ON = "chip_5_w85h85.png"
CHIP_5_FILENAME_OFF = "chip_5_w85h85_fade.png"
CHIP_10_FILENAME_ON = "chip_10_w85h85.png"
CHIP_10_FILENAME_OFF = "chip_10_w85h85_fade.png"
CHIP_50_FILENAME_ON = "chip_50_w85h85.png"
CHIP_50_FILENAME_OFF = "chip_50_w85h85_fade.png"
CHIP_100_FILENAME_ON = "chip_100_w85h85.png"
CHIP_100_FILENAME_OFF = "chip_100_w85h85_fade.png"

# Цвета
GAME_BOARD_COLOR = (34, 139,  34)  # Цвет подхожящий под техасский холдем)
GOLD_COLOR = (255, 215, 0)
BLACK_COLOR = (0, 0, 0)
WHITE_COLOR = (255, 255, 255)
BLUE_COLOR = (0, 0, 255)
GREEN_COLOR = (0, 255, 0)
RED_COLOR = (255, 0, 0)
YELLOW_COLOR = (255, 255, 0)

# Размер, расположение и промежутки между объектами на игровом поле
GAME_BOARD_SIZE = (800, 600)
GAME_BOARD_X_SIZE = GAME_BOARD_SIZE[0]
GAME_BOARD_Y_SIZE = GAME_BOARD_SIZE[1]
PLAYER_CARD_START_POS = (20, 220)
DEALER_CARD_START_POS = (int(GAME_BOARD_X_SIZE * 0.4), 20)
CHIPS_START_POS = (570, 360)
BUTTONS_START_POS = (70, 555)
STATUS_START_POS = (480, 15)
GAP_BETWEEN_CARDS = 20
GAP_BETWEEN_CHIPS = 10
GAP_BETWEEN_BUTTONS = 102
GAP_BETWEEN_SPLIT = 190

# Таймеры в секундах
PAUSE_TIMER1 = 0.5
PAUSE_TIMER2 = 1
PAUSE_TIMER3 = 3

# Разное
NUM_OF_DECKS = 4
LOWEST_BET = 5
DEFAULT_PLAYER_BALANCE = 10000
COUNTING_HELP = True
