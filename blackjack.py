#!/usr/bin/env python
"""
Это игра в блэкджек на основе графического интерфейса с использованием pygame

"""

# Standard imports
import time

# Local imports
from includes.blackjackfsm import *

# Specialized imports from lib. Add lib to path
# import os
# import sys
# MAIN_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
# sys.path.insert(1, os.path.join(MAIN_DIR, 'lib'))


class BlackJack(object):
    """
    Основной класс игры

    Он содержит основной цикл, и внутри этого цикла вся игра
    состоит из различных состояний конечного автомата.
    Игра будет продолжаться в этом цикле до тех пор, пока у игрока не закончатся деньги
    или пока игрок не закроет главное окно.

    """

    # Initialize pygame hooks
    pygame.init()
    pygame.display.set_caption('Black Jack')
    pygame.font.init()
    clock = pygame.time.Clock()

    # Создаем экземпляр одноэлементных объектов с общей переменной
    common_vars = CommonVariables.get_instance()
    button_status = ButtonStatus.get_instance()
    image_db = ImageDB.get_instance()

    # Заполняем необходимые общие переменные начальными значениями
    common_vars.done = False
    common_vars.screen = pygame.display.set_mode(GAME_BOARD_SIZE)
    common_vars.player_cash = DEFAULT_PLAYER_BALANCE
    common_vars.game_rounds = 0
    common_vars.pause_time = 0
    common_vars.dealer_last_hand = 0
    common_vars.player_hands = []
    common_vars.button_image_width = image_db.get_image(IMAGE_PATH_BUTTONS + HIT_BUTTON_FILENAME_ON).get_width()
    common_vars.button_image_height = image_db.get_image(IMAGE_PATH_BUTTONS + HIT_BUTTON_FILENAME_ON).get_height()
    common_vars.chips_image_width = image_db.get_image(IMAGE_PATH_CHIPS + CHIP_5_FILENAME_ON).get_width()
    common_vars.chips_image_height = image_db.get_image(IMAGE_PATH_CHIPS + CHIP_5_FILENAME_ON).get_height()

    common_vars.text_font = pygame.font.SysFont('Arial', 18)
    value_of_players_hand_font = pygame.font.SysFont('Arial', 16)

    current_state = InitialState()

    # Настройки игры
    while not common_vars.done:
        # Настройки стола
        common_vars.screen.fill(GAME_BOARD_COLOR)
        x_pos = int(GAME_BOARD_X_SIZE * 0.12)
        y_pos = GAME_BOARD_Y_SIZE - 240
        common_vars.screen.blit(image_db.get_image(IMAGE_PATH + 'yellow_box_179_120.png'), (x_pos, y_pos))
        x_pos = int((GAME_BOARD_X_SIZE - image_db.get_image(IMAGE_PATH + "bj_banner_yellow2.png").get_width()) / 2)
        y_pos = GAME_BOARD_Y_SIZE - 500
        common_vars.screen.blit(image_db.get_image(IMAGE_PATH + "bj_banner_yellow2.png"), (x_pos, y_pos))

        if COUNTING_HELP:
            # Отображение числа на руке
            x_pos = 22
            for hand in common_vars.player_hands:
                count = get_value_of_players_hand(hand)
                if count:
                    message = value_of_players_hand_font.render('{0}'.format(count), False, YELLOW_COLOR)
                    common_vars.screen.blit(message, (x_pos, GAME_BOARD_Y_SIZE - 270))
                x_pos += GAP_BETWEEN_SPLIT

        # Отображение текущего состояния игры (количество кредитов, количество сыгранных рук)
        x_pos, y_pos = STATUS_START_POS
        message1 = common_vars.text_font.render('[ Credits: $ {0}]   [Hands played: {1} ]'.format(
            common_vars.player_cash, common_vars.game_rounds), False, YELLOW_COLOR)
        common_vars.screen.blit(message1, (x_pos, y_pos))
        message2 = common_vars.text_font.render('[ Dealers last hand: {0} ]'.format(
            common_vars.dealer_last_hand), False, YELLOW_COLOR)
        common_vars.screen.blit(message2, (x_pos, y_pos + 25))

        # Переход к текущему состоянию
        current_state(common_vars, button_status)

        # Обновление информации на дисплее
        pygame.display.flip()

        # Подключение пузы
        if common_vars.pause_time:
            time.sleep(common_vars.pause_time)
            common_vars.pause_time = 0  # Reset

        # Установка frame-time
        clock.tick(10)


if __name__ == '__main__':
    MY_GAME = BlackJack()
