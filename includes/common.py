#!/usr/bin/env python
"""
Все распространенные вспомогательные функции и классы, используемые в игре в блэкджек

"""

# Standard imports
import sys
import os
import pygame
import inspect 

# Local imports
MAIN_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1, os.path.join(MAIN_DIR, 'includes'))
from globals import *
from playingcard import PlayingCard

#############################
#  Вспомогательные функции  #
#############################


def plot_players_hands(screen,
                       player_pos_start,
                       player_hands,
                       double_downs,
                       hands_status):
    """
    Выкладываем все карты игроков на игровой стол.

    :param screen:
    :param player_pos_start:
    :param player_hands:
    :param double_downs:
    :param hands_status:
    :return: None

    """
    logging.debug(inspect.stack()[0][3] + ': enter')

    player_x_pos, player_y_pos = player_pos_start
    image_db = ImageDB.get_instance()
    for index_x, hand in enumerate(player_hands):
        for index_y, card in enumerate(hand):
            image = BlackJackCardFormatter.get_instance(IMAGE_PATH_CARDS).get_string(card)

            if index_y == 2 and len(hand) == 3 and double_downs[index_x]:
                # Выдаем третью карту, если в текущей раздаче у нас есть удвоение.
                screen.blit(pygame.transform.rotate(image_db.get_image(image), 90),
                            (player_x_pos, player_y_pos))
            else:
                screen.blit(image_db.get_image(image), (player_x_pos, player_y_pos))
            player_x_pos += GAP_BETWEEN_CARDS
            player_y_pos -= 14

        x_offset = -50
        y_offset = -40
        if index_x == 0:
            hand = 'first_hand_'
        else:
            hand = 'second_hand_'

        if hands_status[hand + 'blackjack']:
            screen.blit(image_db.get_image(IMAGE_PATH + "blackjack.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status[hand + 'win']:
            screen.blit(image_db.get_image(IMAGE_PATH + "you_win.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status[hand + 'push']:
            screen.blit(image_db.get_image(IMAGE_PATH + "push.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status[hand + 'loose']:
            screen.blit(image_db.get_image(IMAGE_PATH + "you_loose.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        elif hands_status[hand + 'busted']:
            screen.blit(image_db.get_image(IMAGE_PATH + "busted.png"),
                        (player_x_pos + x_offset, player_y_pos + y_offset))
        player_x_pos, player_y_pos = player_pos_start
        player_x_pos += GAP_BETWEEN_SPLIT


def plot_dealers_hand(screen,
                      dealer_card_start_pos,
                      dealer_cards,
                      first_card_hidden):
    """
    Выкладываем все карты дилера на игровой стол, и если первая карта
    должна быть скрыта, положите карту обратно.

    :param screen:
    :param dealer_card_start_pos:
    :param dealer_cards:
    :param first_card_hidden:
    :return: None

    """
    logging.debug(inspect.stack()[0][3] + ': enter')

    dealer_x_pos, dealer_y_pos = dealer_card_start_pos
    image_db = ImageDB.get_instance()
    for card in dealer_cards:
        if first_card_hidden is True:
            # Первая карта дилера скрыта
            screen.blit(image_db.get_image(IMAGE_PATH_CARDS + CARDBACK_FILENAME),
                        (dealer_x_pos, dealer_y_pos))
        else:
            image = BlackJackCardFormatter.get_instance(IMAGE_PATH_CARDS).get_string(card)
            screen.blit(image_db.get_image(image), (dealer_x_pos, dealer_y_pos))
        first_card_hidden = False
        dealer_x_pos += GAP_BETWEEN_CARDS
        dealer_y_pos += 14


def plot_chips(screen,
               player_cash,
               chips_image_width,
               visible):
    """
    Помещаем фишки на игровое поле, чтобы игрок мог нажимать на них и делать ставки.

    :param screen:
    :param player_cash:
    :param chips_image_width:
    :param visible: True если активно и False если неактивно.
    :return: None

    """
    logging.debug(inspect.stack()[0][3] + ': enter')
    chips_x_pos, chips_y_pos = CHIPS_START_POS
    gap = chips_image_width + GAP_BETWEEN_CHIPS
    image_db = ImageDB.get_instance()
    if visible:
        if player_cash >= 5:
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_5_FILENAME_ON),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 10:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_10_FILENAME_ON),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 50:
            chips_x_pos -= gap
            chips_y_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_50_FILENAME_ON),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 100:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_100_FILENAME_ON),
                        (chips_x_pos, chips_y_pos))
    else:
        if player_cash >= 5:
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_5_FILENAME_OFF),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 10:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_10_FILENAME_OFF),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 50:
            chips_x_pos -= gap
            chips_y_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_50_FILENAME_OFF),
                        (chips_x_pos, chips_y_pos))
        if player_cash >= 100:
            chips_x_pos += gap
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + CHIP_100_FILENAME_OFF),
                        (chips_x_pos, chips_y_pos))


def plot_bets(screen, player_bets):
    """
    Выстраиваем все «стопки» ставок, которые доступны в стеке ставок игрока.
    Их может быть от одной до четырёх в зависимости от того, было ли разделение или
    количество удвоений.

    :param screen:
    :param player_bets:
    :return: None

    """
    logging.debug(inspect.stack()[0][3] + ': enter')
    image_db = ImageDB.get_instance()
    chip_x_pos = 30
    chip_y_pos = 360
    for bet in player_bets:
        for chip in bet:
            screen.blit(image_db.get_image(IMAGE_PATH_CHIPS + 'chip_{0}_w85h85.png'.format(chip)),
                        (chip_x_pos, chip_y_pos))
            chip_y_pos += 8
        chip_y_pos = 360
        chip_x_pos += 50


def plot_buttons(screen, button_status):
    """
    Выстраиваем все кнопки на игровом поле и в зависимости от состояния кнопки 
    выстраиваем их как видимые и кликабельные или затенённые/выцветшие, указывающие на то, что они не кликабельные.

    :param screen:
    :param button_status: True если активно и False если неактивно (затемнено).
    :return: None

    """
    logging.debug(inspect.stack()[0][3] + ': enter')
    button_x_pos, button_y_pos = BUTTONS_START_POS
    image_db = ImageDB.get_instance()
    if button_status.play is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + PLAY_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + PLAY_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    if button_status.undo_bet is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + UNDO_BET_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + UNDO_BET_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    if button_status.hit is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + HIT_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + HIT_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    if button_status.stand is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + STAND_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + STAND_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    if button_status.split is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + SPLIT_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + SPLIT_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS

    if button_status.double_down is True:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + DOUBLE_DOWN_BUTTON_FILENAME_ON),
                    (button_x_pos, button_y_pos))
    else:
        screen.blit(image_db.get_image(IMAGE_PATH_BUTTONS + DOUBLE_DOWN_BUTTON_FILENAME_OFF),
                    (button_x_pos, button_y_pos))
    button_x_pos += GAP_BETWEEN_BUTTONS


def plot_results(screen, text_font, message):
    """
    Отображаем текстовое сообщение в строке состояния в том же месте,
    где отображаются кнопки.
    Чтобы их увидеть, нужно сделать паузу, иначе
    сообщение будет мгновенно перекрыто кнопками.

    :param screen:
    :param text_font:
    :param message:
    :return: None

    """
    logging.debug(inspect.stack()[0][3] + ': enter')

    assert isinstance(message, str)
    text_to_plot = text_font.render(message, False, GOLD_COLOR)
    x_pos, y_pos = STATUS_START_POS
    screen.blit(text_to_plot, (x_pos, y_pos + 50))


def get_value_of_players_hand(hand):
    """
    Расчет стоимость комбинации игроков в соответствии с правилами. 
    Прежде всего, считаем, что все открытые карты равны 10.
    Если у игрока на руках туз, а остаток
    комбинации равен или меньше 10, туз будет считаться
    "Слабым тузом" со значением 11. Если у игрока на руках туз и он получает карты на значения в сумме больше 10,
    тузы будут заменены на твердые тузы со значением 1 по одному.

    :param hand: A list of :meth:`lib.playingcard.PlayingCard` objects.
    :return: Конечное значение руки как integer.

    """
    logging.debug(inspect.stack()[0][3] + ': enter')
    assert isinstance(hand, list)
    summary = 0
    num_of_soft_aces = 0
    for card in hand:
        assert isinstance(card, PlayingCard)
        rank = card.get_rank()
        if rank > 10:
            # Рассматриваем все открытые карты как 10
            summary += 10
            logging.debug(inspect.stack()[0][3] + ': face')
        elif rank == 1 and summary <= 10:
            # Если выпал туз, начинаем считать мягкую комбинацию "старшим тузом".
            summary += 11
            num_of_soft_aces += 1
            logging.debug(inspect.stack()[0][3] + ': soft ace')
        else:
            summary += rank
            logging.debug(inspect.stack()[0][3] + ': add rank {0} to summary givs {1}'.format(rank, summary))

        if num_of_soft_aces and summary > 21:
            # превращаем мягкий туз в твёрдый, уменьшаем на 10, так как мы уже учли 11
            summary -= 10
            num_of_soft_aces -= 1
            logging.debug(inspect.stack()[0][3] + ': busted, toggle soft to hard ace')

    return summary


def get_value_of_dealers_hand(hand):
    """
    Рассчитываем стоимость раздачи дилера в соответствии с правилами. 
    Прежде всего, считаем, что все открытые карты равны 10.
    Если карта - туз и если общая сумма текущей раздачи
    составит 17 или более, но меньше 21, дилер должен засчитать туза
    как "мягкого" туза.

    :param hand: A list of :meth:`lib.playingcard.PlayingCard` objects.
    :return: Конечное значение руки как integer.

    """
    logging.debug(inspect.stack()[0][3] + ': enter')
    assert isinstance(hand, list)
    summary = 0
    hard_ace = 0
    for card in hand:
        assert isinstance(card, PlayingCard)
        rank = card.get_rank()
        if rank > 10:
            # Рассматриваем все открытые карты как 10
            summary += 10
            logging.debug(inspect.stack()[0][3] + ': face')
        elif rank == 1:
            # Если карта является тузом и если общая сумма текущей раздачи составит 17 или более
            # но менее 21, дилер должен считать туз «мягким» тузом.
            if 17 <= (summary + 11) < 22:
                summary += 11
                logging.debug(inspect.stack()[0][3] + ': soft ace')
            else:
                # Сохраняем туза для последующей оценки, когда в сводку будут добавлены новые карты.
                hard_ace = 1
                summary += 1
                logging.debug(inspect.stack()[0][3] + ': hard ace')
                continue
        else:
            summary += rank
            logging.debug(inspect.stack()[0][3] + ': add rank {0} to summary givs {1}'.format(rank, summary))

        if hard_ace and 17 <= (summary + hard_ace * 10) < 22:
            # Превращаем твёрдую карту в мягкую, прибавьте 10, так как 1 уже есть в сумме, итого 11
            summary += 10
            logging.debug(inspect.stack()[0][3] + ': toggle hard to soft ace')

    return summary


def is_cut_passed(shoe_of_decks):
    """
    Проверяем, что мы не прошли «порог» в колоде карт, где
    порог должен составлять примерно 18% от общего размера колоды.

    :param shoe_of_decks:
    :return: True если порог пройден, иначе False.

    """
    logging.debug(inspect.stack()[0][3] + ': enter')

    status = False
    if shoe_of_decks is None or shoe_of_decks.length() < (NUM_OF_DECKS * 52 * 0.18):
        logging.debug(inspect.stack()[0][3] + 'Passed the "cut" in the shoe')
        status = True
    return status


def is_possible_split(player_cards):
    """
    Сравниваем первую и вторую карты в руке игрока, 
    и если ранги обеих карт совпадают, вернем значение True, иначе вернем значение False.

    :param player_cards:
    :return: True or False

    """
    logging.debug(inspect.stack()[0][3] + ': enter')

    if len(player_cards) != 2:
        return False
    if player_cards[0].get_rank() != player_cards[1].get_rank():
        return False
    else:
        return True


def can_double_bet(player_bets, player_cash):
    """
    Если у игрока есть хотя бы сумма, равная первой ставке, 
    вернем значение True, иначе вернем значение False

    :param player_bets:
    :param player_cash:
    :return: True or False

    """
    if player_cash < sum(player_bets[0]):
        return False
    else:
        return True


##########################
# Общие классы поддержки #
##########################


class ImageDB:
    """
    При создании экземпляра этого класса в виде объекта будет создан одноэлементный объект,
    который содержит библиотеку (словарь), хранящую изображения при загрузке.
    Это позволит избежать перезагрузки изображения при каждом вызове функции
    в основном игровом цикле.
    Использование:
    instance = ImageDB.get_instance()
    image = instance.get_image(path)
    Или:
    image = ImageDB.get_instance().get_image(path)

    """
    instance = None

    @classmethod
    def get_instance(cls):
        """
        Если экземпляр равен None, создаем экземпляр этого класса
        и вернем его, в противном случае вернем существующий экземпляр.

        :return: Экземпляр ImageDB.

        """
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        logging.info(inspect.stack()[0][3] + ':' + 'ImageDb instance created')
        self.image_library = {}

    def get_image(self, path):
        """
        Если изображение есть в словаре, оно будет возвращено.
        Если изображение не найдено в словаре, оно будет загружено из
        файловой системы или вызовет исключение, если не будет найдено.

        :param path: <string>  содержащая абсолютный путь к каталогу \
        , в котором находится ожидаемое изображение.
        :return: Изображение в формате объекта pygame Surface.

        """
        logging.debug(inspect.stack()[0][3] + ':' + 'enter')

        image = self.image_library.get(path)
        if image is None:
            logging.info(inspect.stack()[0][3] + ':' + path)
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            image = pygame.image.load(canonicalized_path)
            self.image_library[path] = image
        return image


class SoundDB:
    """
    При создании экземпляра этого класса в виде объекта будет создан одноэлементный объект,
    который содержит библиотеку (словарь), хранящую звуки при загрузке.
    Это позволит избежать перезагрузки звука при каждом вызове функции
    в основном игровом цикле.
    Использование:
    instance = SoundDB.get_instance()
    sound = instance.get_sound(path)
    Или:
    sound = SoundDB.get_instance().get_sound(path)

    """
    instance = None

    @classmethod
    def get_instance(cls):
        """
        Если экземпляр равен None, создаем экземпляр этого класса
        и вернем его, в противном случае вернем существующий экземпляр.

        :return: Экземпляр SoundDB.

        """
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        logging.info(inspect.stack()[0][3] + ':' + 'SoundDb instance created')
        self.sound_library = {}

    def get_sound(self, path):
        """
        Если звук есть в словаре, он будет возвращён.
        Если звук не найден в словаре, он будет загружен из
        файловой системы или вызовет исключение, если не будет найден.

        :param path: <string>  содержащая абсолютный путь к каталогу \
        , в котором находится ожидаемый звук.
        :return: Звук в формате объекта pygame Surface.

        """
        logging.debug(inspect.stack()[0][3] + ':' + 'enter')

        sound = self.sound_library.get(path)
        if sound is None:
            logging.info(inspect.stack()[0][3] + ':' + path)
            canonicalized_path = path.replace('/', os.sep).replace('\\', os.sep)
            sound = pygame.mixer.Sound(canonicalized_path)
            self.sound_library[path] = sound
        return sound


class BlackJackCardFormatter:
    """
    Класс, который объединяет общие методы, 
    позволяющие управлять данными объекта PlayingCard, используемого в игре «Блэк Джек».

    """
    instance = None

    @classmethod
    def get_instance(cls, path=''):
        """
        Если экземпляр равен None, создаем экземпляр этого класса
        и вернем его, в противном случае вернем существующий экземпляр.

        :param path: Дополнительный путь к месту хранения изображения будет
        добавлен к имени изображения, если он указан.
        :return: Экземпляр BlackJackCardFormatter.

        """
        if cls.instance is None:
            cls.instance = cls(path)
        return cls.instance

    def __init__(self, path):
        """
        Создаем экземпляр одноэлементного объекта и атрибуты ранга и масти
        , которые содержат сопоставление между целочисленными значениями и соответствующими
        строками в виде чисел или названий.

        :param path:
        """
        logging.info(inspect.stack()[0][3] + ':' + 'BlackJackCardFormatter instance created')
        self.path = path
        self.card_rank = ["Invalid", "ace", "2", "3", "4", "5", "6", "7",
                          "8", "9", "10", "jack", "queen", "king"]
        self.card_suit = ["spades", "clubs", "diamonds", "hearts"]

    def get_string(self, card):
        """
        Преобразуем целочисленные значения карт для ранга и масти в строку в формате <rank>_of_<suit>.png.
        Если для создания этого экземпляра был указан путь, 
        он будет добавлен к имени изображения в формате <path>/<rank>_of_<suit>.png.

        :param card: of type :meth:`lib.playingcard.PlayingCard`
        :return: <string>

        """
        logging.debug(inspect.stack()[0][3] + ':' + 'enter')

        image = self.path + self.card_rank[card.get_rank()] + "_of_" \
            + self.card_suit[card.get_suit()] + ".png"
        return image


class ButtonCollideArea:
    """
    При создании экземпляра этого класса в виде объекта будет создан одноэлементный объект,
    содержащий заданные области столкновения для всех кнопок. 
    Поскольку это будет вызываться для каждого круга в основном игровом цикле, мы
    сведём к минимуму количество повторных объявлений.

    """
    instance = None

    @classmethod
    def get_instance(cls, common_vars):
        """
        Если экземпляр равен None, создаем экземпляр этого класса
        и вернем его, в противном случае вернем существующий экземпляр.

        :param common_vars:
        :return: Экземпляр ButtonCollideArea.

        """
        if cls.instance is None:
            cls.instance = cls(common_vars)
        return cls.instance

    def __init__(self, common_vars):
        """
        Создаем экземпляр одноэлементного объекта и объекты области Pygame Rect
        для всех кнопок, чтобы можно было определить, когда мышь нажимается в любой из этих областей.

        :param common_vars:
        """
        logging.info(inspect.stack()[0][3] + ':' + 'ButtonCollideArea instance created')
        button_x_pos, button_y_pos = BUTTONS_START_POS

        self.play_button_area = pygame.Rect(button_x_pos,
                                            button_y_pos,
                                            common_vars.button_image_width,
                                            common_vars.button_image_height)
        button_x_pos += GAP_BETWEEN_BUTTONS
        self.undo_bet_button_area = pygame.Rect(button_x_pos,
                                                button_y_pos,
                                                common_vars.button_image_width,
                                                common_vars.button_image_height)
        button_x_pos += GAP_BETWEEN_BUTTONS
        self.hit_button_area = pygame.Rect(button_x_pos,
                                           button_y_pos,
                                           common_vars.button_image_width,
                                           common_vars.button_image_height)
        button_x_pos += GAP_BETWEEN_BUTTONS
        self.stand_button_area = pygame.Rect(button_x_pos,
                                             button_y_pos,
                                             common_vars.button_image_width,
                                             common_vars.button_image_height)
        button_x_pos += GAP_BETWEEN_BUTTONS
        self.split_button_area = pygame.Rect(button_x_pos,
                                             button_y_pos,
                                             common_vars.button_image_width,
                                             common_vars.button_image_height)
        button_x_pos += GAP_BETWEEN_BUTTONS
        self.double_down_button_area = pygame.Rect(button_x_pos,
                                                   button_y_pos,
                                                   common_vars.button_image_width,
                                                   common_vars.button_image_height)


class ChipsCollideArea:
    """
    При создании экземпляра этого класса в виде объекта будет создан одноэлементный объект,
    содержащий заданные области столкновения для всех фишек.
    Поскольку это будет вызываться для каждого круга в основном игровом цикле, мы
    сведём к минимуму количество повторных объявлений.

    """
    instance = None

    @classmethod
    def get_instance(cls, common_vars):
        """
        Если экземпляр равен None, создаем экземпляр этого класса
        и вернем его, в противном случае вернем существующий экземпляр.

        :param common_vars:
        :return: Экземпляр ChipsCollideArea.

        """
        if cls.instance is None:
            cls.instance = cls(common_vars)
        return cls.instance

    def __init__(self, common_vars):
        """
        Создаем экземпляр одноэлементного объекта и объекты-прямоугольники Pygame
        для всех фишек, чтобы можно было определить, когда мышь нажимается в любой из этих областей.

        :param common_vars:
        """
        logging.info(inspect.stack()[0][3] + ':' + 'ChipsCollideArea instance created')
        chips_x_pos, chips_y_pos = CHIPS_START_POS
        gap = common_vars.chips_image_width + GAP_BETWEEN_CHIPS
        self.chip_5_area = pygame.Rect(chips_x_pos,
                                       chips_y_pos,
                                       common_vars.chips_image_width,
                                       common_vars.chips_image_height)
        chips_x_pos += gap
        self.chip_10_area = pygame.Rect(chips_x_pos,
                                        chips_y_pos,
                                        common_vars.chips_image_width,
                                        common_vars.chips_image_height)
        chips_x_pos -= gap
        chips_y_pos += gap
        self.chip_50_area = pygame.Rect(chips_x_pos,
                                        chips_y_pos,
                                        common_vars.chips_image_width,
                                        common_vars.chips_image_height)
        chips_x_pos += gap
        self.chip_100_area = pygame.Rect(chips_x_pos,
                                        chips_y_pos,
                                        common_vars.chips_image_width,
                                        common_vars.chips_image_height)


class CommonVariables:
    """
    При создании экземпляра этого класса в виде объекта будет создан одноэлементный объект
    , содержащий все общие переменные, которые будут передаваться по ссылке
    между основным игровым циклом и различными состояниями конечного автомата.

    """
    instance = None

    @classmethod
    def get_instance(cls):
        """
        Если экземпляр равен None, создаем экземпляр этого класса
        и вернем его, в противном случае вернем существующий экземпляр.

        :return: Экземпляр CommonVariables.

        """
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        """
        Создаем экземпляр одноэлементного объекта со всеми атрибутами, установленными в значение None.
        Заполняется вызывающей стороной.

        """
        self.done = None
        self.screen = None
        self.shoe_of_decks = None
        self.player_hands = None
        self.hands_status = None
        self.double_downs = None
        self.dealer_cards = None
        self.dealer_last_hand = None
        self.player_deal = None
        self.player_hit = None
        self.player_cash = None
        self.player_bets = None
        self.bets_pos = None
        self.game_rounds = None
        self.text_font = None
        self.first_card_hidden = None
        self.pause_time = None
        self.button_image_width = None
        self.button_image_height = None
        self.chips_image_width = None
        self.chips_image_height = None


class ButtonStatus:
    """
    При создании экземпляра этого класса в виде объекта будет создан одноэлементный объект
    с атрибутом bool для каждой кнопки, который указывает, 
    должна ли она отображаться, быть видимой или затенённой/затушеванной, чтобы показать, можно ли на неё нажать.

    """
    instance = None

    @classmethod
    def get_instance(cls):
        """
        Если экземпляр равен None, создаем экземпляр этого класса
        и вернем его, в противном случае вернем существующий экземпляр.

        :return: Экземпляр ButtonStatus.

        """
        if cls.instance is None:
            cls.instance = cls()
        return cls.instance

    def __init__(self):
        """
        Создаем экземпляр одноэлементного объекта со всеми атрибутами, установленными в значение False.

        """
        self.play = False
        self.undo_bet = False
        self.hit = False
        self.stand = False
        self.split = False
        self.double_down = False

    def reset(self):
        """
        Устанавливаем все атрибуты в значение False.

        :return: None

        """
        self.play = False
        self.undo_bet = False
        self.hit = False
        self.stand = False
        self.split = False
        self.double_down = False
