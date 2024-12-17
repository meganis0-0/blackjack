#!/usr/bin/env python
"""
Конечная машина состояний (FSM), используемая в игре «Блэк Джек».

"""

# Standard imports
import sys
import os

# Local imports
MAIN_DIR = (os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
sys.path.insert(1, os.path.join(MAIN_DIR, 'includes'))
from common import *
from carddecks import CardDecks  # , TestingCardDeck


class State(object):
    """
    Базовый класс конечных автоматов (FSM).

    """
    def next_state(self, state):
        """

        :param state:
        :return: None

        """
        self.__class__ = state

    def get_state(self):
        """

        :return: Имя текущего состояния как строка.

        """
        temp = str(self.__class__).strip('\'>').split('.')
        return temp[2]


class InitialState(State):
    """
    Инициализируем и сбросываем все необходимые переменные, которые будут использоваться в каждом раунде.

    """
    def __call__(self, common_vars, button_status):
        """

        :param common_vars:
        :param button_status:
        :return: None

        """
        logging.info(type(self).__name__ + ': Credits: {0}'.format(common_vars.player_cash))

        common_vars.hands_status = {'first_hand_blackjack': False,
                                    'first_hand_win': False,
                                    'first_hand_push': False,
                                    'first_hand_loose': False,
                                    'first_hand_busted': False,
                                    'second_hand_blackjack': False,
                                    'second_hand_win': False,
                                    'second_hand_push': False,
                                    'second_hand_loose': False,
                                    'second_hand_busted': False}
        common_vars.player_hands = []
        hand_instance = []
        common_vars.player_hands.append(hand_instance)
        common_vars.player_bets = []
        common_vars.bets_pos = []  # [(x,y), (x,y), ...]
        common_vars.game_rounds += 1
        common_vars.double_downs = [False, False]  # Флаг для каждой возможной раздачи
        common_vars.first_card_hidden = True
        button_status.reset()
        self.next_state(BettingState)


class BettingState(State):
    """
    Добавляет или удаляет ставки до тех пор, пока игрок не нажмёт на кнопку,
    или выйдет в «FinalState», если войдёт в это состояние без
    денег, достаточных для размещения ставки.
    """

    # Статические переменные класса
    _current_bet = []
    _chips_visible = True

    def __call__(self, common_vars, button_status):
        """

        :param common_vars:
        :param button_status:
        :return: None

        """
        logging.debug(type(self).__name__ + ':' + 'enter')

        if common_vars.player_cash >= LOWEST_BET or sum(self._current_bet) > 0:
            plot_chips(common_vars.screen,
                       common_vars.player_cash,
                       common_vars.chips_image_width,
                       self._chips_visible)

            if sum(self._current_bet) > 0:
                button_status.play = True
                button_status.undo_bet = True
            else:
                button_status.play = False
                button_status.undo_bet = False
            plot_buttons(common_vars.screen, button_status)

            # Создаем видимые области для кнопок и фишек, используемых при щелчке мыши.
            button_collide_instance = ButtonCollideArea.get_instance(common_vars)
            chips_collide_instance = ChipsCollideArea.get_instance(common_vars)

            sound_db = SoundDB.get_instance()
            chip_sound = sound_db.get_sound(SOUND_PATH + 'chipsstack.wav')

            temp_bet_list = []
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    common_vars.done = True
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_position = pygame.mouse.get_pos()  # returns (x, y) in a tuple
                    if button_collide_instance.play_button_area.collidepoint(mouse_position[0], mouse_position[1])\
                            and sum(self._current_bet) > 0:
                        # Time to play
                        logging.info(type(self).__name__ + ': [Play] pressed')
                        logging.info(type(self).__name__ + ': Current bet is {0}'.format(self._current_bet))
                        logging.info(type(self).__name__ + ': Remaining credits {0}'.format(common_vars.player_cash))
                        # Инициализируем все необходимые переменные для следующего состояния
                        common_vars.player_bets.append(self._current_bet)
                        common_vars.dealer_cards = []
                        common_vars.first_card_hidden = True
                        common_vars.player_deal = False
                        common_vars.player_hit = False
                        button_status.play = False
                        button_status.undo_bet = False
                        # Сброс локальных статических переменных состояния
                        self._current_bet = []
                        self._chips_visible = True
                        self.next_state(DealingState)
                    elif button_collide_instance.undo_bet_button_area.\
                            collidepoint(mouse_position[0], mouse_position[1])\
                            and sum(self._current_bet) > 0:
                        chip_sound.play()
                        common_vars.player_cash += self._current_bet.pop()
                        logging.info(type(self).__name__ + ': [Undo bet] pressed, remaining credits {0}'.
                                     format(common_vars.player_cash))

                    if len(self._current_bet) < 20:
                        self._chips_visible = True
                        if chips_collide_instance.chip_5_area.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash >= 5:
                            chip_sound.play()
                            self._current_bet.append(5)
                            common_vars.player_cash -= 5
                        elif chips_collide_instance.chip_10_area.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash >= 10:
                            chip_sound.play()
                            self._current_bet.append(10)
                            common_vars.player_cash -= 10
                        elif chips_collide_instance.chip_50_area.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash >= 50:
                            chip_sound.play()
                            self._current_bet.append(50)
                            common_vars.player_cash -= 50
                        elif chips_collide_instance.chip_100_area.collidepoint(mouse_position[0], mouse_position[1]) \
                                and common_vars.player_cash >= 100:
                            chip_sound.play()
                            self._current_bet.append(100)
                            common_vars.player_cash -= 100
                    else:
                        self._chips_visible = False

            temp_bet_list.append(self._current_bet)
            plot_bets(common_vars.screen, temp_bet_list)
        else:
            # У вас закончились наличные, заканчиваем игру
            self.next_state(FinalState)


class DealingState(State):
    """
    Сдаем первые две карты дилеру и игроку.

    Первые четыре итерации при входе в это состояние будут включать
    1. Карту для игрока + пауза,
    2. Карту для дилера + пауза,
    3. Вторую карту для игрока + пауза,
    4. Вторую карту для дилера + пауза,
    5. Проверяем, есть ли у игрока блэкджек, и если нет,
    дожидаемя, пока игрок нажмёт «hit», «stand» или, возможно, «split».

    """
    def __call__(self, common_vars, button_status):
        """

        :param common_vars:
        :param button_status:
        :return: None

        """
        logging.debug(type(self).__name__ + ':' + 'enter')

        if is_cut_passed(common_vars.shoe_of_decks):
            logging.info(type(self).__name__ + ': Cut passed, create new shoe with {0} decks'.format(NUM_OF_DECKS))
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)
            # common_vars.shoe_of_decks = TestingCardDeck()

        plot_chips(common_vars.screen, common_vars.player_cash, common_vars.chips_image_width, False)

        sound_db = SoundDB.get_instance()
        card_sound = sound_db.get_sound(SOUND_PATH + 'cardslide.wav')

        first_hand = 0  # У нас есть только одна рука для игрока в этом состоянии
        if len(common_vars.dealer_cards) < 2:
            # Создаем короткую паузу между раздачей первых двух карт
            common_vars.pause_time = PAUSE_TIMER1

            if not common_vars.player_hands[first_hand]:
                # С пустой рукой берем первую карту для игрока.
                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands[first_hand].append(card)

            elif not common_vars.dealer_cards:
                # С пустой рукой берем первую карту для дилера.
                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.dealer_cards.append(card)

            elif len(common_vars.player_hands[first_hand]) == 1:
                # Берем вторую карту для игрока
                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands[first_hand].append(card)

            elif len(common_vars.dealer_cards) == 1:
                # Берем вторую карту для дилера
                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.dealer_cards.append(card)
        elif not button_status.hit:
            # Выбраны две карты для игрока и дилера, давайте оценим, есть ли
            # блэкджек, ничья или возможный сплит.
            logging.info(type(self).__name__ + ': Two cards dealt, first evaluation')
            common_vars.pause_time = 0
            value_of_dealers_hand = get_value_of_dealers_hand(common_vars.dealer_cards)
            for hand in common_vars.player_hands:
                value_of_players_hand = get_value_of_players_hand(hand)
                if value_of_players_hand == 21 and len(common_vars.player_hands) != 2:  # Не сплит
                    # Давайте оценим и сравним с дилером.
                    common_vars.first_card_hidden = False
                    if value_of_dealers_hand == 21:
                        # Ничья, ставки возвращаются игроку.
                        logging.info(type(self).__name__ + ':' + 'Push')
                        common_vars.pause_time = PAUSE_TIMER3
                        plot_results(common_vars.screen, common_vars.text_font, 'Push')
                        common_vars.hands_status['first_hand_push'] = True
                        common_vars.player_cash += sum(common_vars.player_bets[0])
                    else:
                        # BlackJack, выплата 3/2 (1.5)
                        logging.info(type(self).__name__ + ':' + 'Black Jack!!!')
                        common_vars.pause_time = PAUSE_TIMER3
                        plot_results(common_vars.screen, common_vars.text_font, 'Black Jack!!!')
                        common_vars.hands_status['first_hand_blackjack'] = True
                        common_vars.player_cash += sum(common_vars.player_bets[0])  # Сначала вернем свою ставку
                        common_vars.player_cash += int(sum(common_vars.player_bets[0]) * 1.5)

                    common_vars.dealer_last_hand = value_of_dealers_hand
                    # Сделаем короткую паузу, чтобы представить результат раздачи
                    common_vars.pause_time = PAUSE_TIMER3
                    button_status.reset()
                    self.next_state(InitialState)
                elif len(common_vars.player_hands) != 2 and is_possible_split(hand):
                    # Уже не в сплите и две равные карты
                    button_status.split = can_double_bet(common_vars.player_bets, common_vars.player_cash)
                    button_status.hit = True
                else:
                    button_status.hit = True
        else:
            button_status.hit = True
            button_status.stand = True
            button_status.double_down = can_double_bet(common_vars.player_bets, common_vars.player_cash)

        # Создаем видимые области для кнопок, используемых при нажатии мыши.
        button_collide_instance = ButtonCollideArea.get_instance(common_vars)

        plot_buttons(common_vars.screen, button_status)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common_vars.done = True
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_position = pygame.mouse.get_pos()  # returns (x, y) in a tuple
                if button_status.hit and button_collide_instance.hit_button_area.\
                        collidepoint(mouse_position[0], mouse_position[1]):
                    logging.info(type(self).__name__ + ': [Hit] pressed')
                    card_sound.play()
                    card = common_vars.shoe_of_decks.pop()
                    common_vars.player_hands[first_hand].append(card)
                    button_status.split = False
                    button_status.double_down = False
                    self.next_state(PlayerHitState)
                elif button_status.stand and button_collide_instance.stand_button_area.\
                        collidepoint(mouse_position[0], mouse_position[1]):
                    logging.info(type(self).__name__ + ': [Stand] pressed')
                    self.next_state(DealerInitState)
                elif button_status.double_down and button_collide_instance.double_down_button_area.\
                        collidepoint(mouse_position[0], mouse_position[1]):
                    logging.info(type(self).__name__ + ': [Double down] pressed')
                    # Удваиваем ставку перед тем, как перейти в раздел "Состояние дилера".
                    common_vars.player_cash -= sum(common_vars.player_bets[0])
                    common_vars.player_bets.append(common_vars.player_bets[0])
                    logging.info(type(self).__name__ + ': Remaining credits {0}'.format(common_vars.player_cash))
                    card_sound.play()
                    card = common_vars.shoe_of_decks.pop()
                    common_vars.player_hands[first_hand].append(card)  # Выдается третья карта
                    common_vars.double_downs[first_hand] = True
                    button_status.double_down = False
                    self.next_state(DealerInitState)
                elif button_status.split and button_collide_instance.split_button_area.\
                        collidepoint(mouse_position[0], mouse_position[1]):
                    # Удвоение ставки, прежде чем перейти в разделенное состояние.
                    logging.info(type(self).__name__ + ': [Split] pressed')
                    common_vars.player_cash -= sum(common_vars.player_bets[0])
                    common_vars.player_bets.append(common_vars.player_bets[0])
                    button_status.reset()
                    logging.info(type(self).__name__ + ': Remaining credits {0}'.format(common_vars.player_cash))
                    self.next_state(SplitState)

        plot_bets(common_vars.screen, common_vars.player_bets)

        plot_buttons(common_vars.screen, button_status)

        plot_players_hands(common_vars.screen,
                           PLAYER_CARD_START_POS,
                           common_vars.player_hands,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)


class SplitState(State):
    """
    Разделяем первые две карты игрока на две руки.
    Берем по новой карте в каждую руку, и если игроку повезёт
    и он получит 21 в обеих руках, оцениваем это как удвоенный блэкджек или ничью.
    В противном случае переходим к следующему состоянию 'PlayerHitState'.

    """
    def __call__(self, common_vars, button_status):
        """

        :param common_vars:
        :param button_status:
        :return: None

        """
        logging.debug(type(self).__name__ + ':' + 'enter')

        if is_cut_passed(common_vars.shoe_of_decks):
            logging.info(type(self).__name__ + ': Cut passed, create new shoe with {0} decks'.format(NUM_OF_DECKS))
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)

        plot_chips(common_vars.screen, common_vars.player_cash, common_vars.chips_image_width, False)
        plot_buttons(common_vars.screen, button_status)

        sound_db = SoundDB.get_instance()
        card_sound = sound_db.get_sound(SOUND_PATH + 'cardslide.wav')

        first_hand = 0
        second_hand = 1
        if len(common_vars.player_hands) == 1:
            hand_instance = []
            common_vars.player_hands.append(hand_instance)
            common_vars.player_hands[second_hand].append(common_vars.player_hands[first_hand].pop())

        logging.info(type(self).__name__ + ': {0}:{1}'.
                     format(len(common_vars.player_hands[first_hand]),
                            len(common_vars.player_hands[second_hand])))

        if len(common_vars.player_hands[second_hand]) != 2:
            # Пополняем каждую раздачу одной дополнительной картой.
            common_vars.pause_time = PAUSE_TIMER1
            if len(common_vars.player_hands[first_hand]) < 2:
                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands[first_hand].append(card)
            elif len(common_vars.player_hands[second_hand]) < 2:
                card_sound.play()
                card = common_vars.shoe_of_decks.pop()
                common_vars.player_hands[second_hand].append(card)
        else:
            # Теперь у обеих рук по две карты, давайте оценим
            value_of_players_hands = 0
            for hand in common_vars.player_hands:
                value_of_players_hands += get_value_of_players_hand(hand)
            if value_of_players_hands != 42:
                # Не два раза по 21 или ответ на вопрос о смысле жизни, переходим к следующему состоянию
                button_status.hit = True
                button_status.stand = True
                button_status.double_down = can_double_bet(common_vars.player_bets, common_vars.player_cash)
                self.next_state(PlayerHitState)
            else:
                # У игрока две пары по 21, шанс на это приблизительно 0,00715356%
                value_of_dealers_hand = get_value_of_dealers_hand(common_vars.dealer_cards)
                common_vars.dealer_last_hand = value_of_dealers_hand
                sum_of_bets = 0
                for bet in common_vars.player_bets:
                    sum_of_bets += sum(bet)
                logging.info(type(self).__name__ + ':' + 'sum_of_bets = {0}'.format(sum_of_bets))
                if value_of_dealers_hand == 21:
                    # Ничья, ставки возвращаются игроку.
                    logging.info(type(self).__name__ + ':' + 'Push')
                    plot_results(common_vars.screen, common_vars.text_font, 'Push')
                    common_vars.player_hands['first_hand_push'] = True
                    common_vars.player_hands['second_hand_push'] = True
                    common_vars.player_cash += sum_of_bets
                else:
                    # Double BlackJack, выплата 3/2 (1.5)
                    logging.info(type(self).__name__ + ':' + 'Double BlackJack!!!')
                    plot_results(common_vars.screen, common_vars.text_font, 'Double Black Jack!!!')
                    common_vars.player_hands['first_hand_blackjack'] = True
                    common_vars.player_hands['second_hand_blackjack'] = True
                    common_vars.player_cash += sum_of_bets
                    common_vars.player_cash += int(sum_of_bets * 1.5)

                # Сделаем короткую паузу, чтобы представить результат раздачи
                common_vars.pause_time = PAUSE_TIMER3
                button_status.reset()
                self.next_state(InitialState)

        plot_bets(common_vars.screen, common_vars.player_bets)

        plot_players_hands(common_vars.screen,
                           PLAYER_CARD_START_POS,
                           common_vars.player_hands,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)


class PlayerHitState(State):
    """
    Остаемся в этом состоянии до тех пор, пока игрок не будет удовлетворен (stand) или не проиграет.

    Вытаскиваем карты, если игрок нажимает "hit", проверяем результаты, возвращаемся к игре.
    "Начальное состояние", если игрок попался, или переходим в следующее состояние, если
    игрок нажимает кнопку "stand".

    Правила игры в Блэкджек:
    Номинал карт со второй по десятую равен их очковому значению (от 2 до 10).
    Все старшие карты (валет, дама и король) стоят десять очков.
    Тузы могут стоить одно или одиннадцать очков.
    Как и в обычных правилах казино, в этой игре нельзя получить 5-Чарли или 7-Чарли.

    Правило Чарли в блэкджеке (Charlie Rule) — это правило, согласно которому игрок, 
    имеющий в одной руке определённое количество карт, автоматически выигрывает.
    Это довольно редкое правило, встречающееся лишь в некоторых версиях блэкджека. 
    Оно известно в разных вариациях: пятикарточный Чарли, шестикарточный Чарли и так далее. 
    Чем меньше карт нужно для активации данного правила, тем выгоднее оно для игрока.
    Например, по правилу пятикарточного Чарли если игрок достигает пятикарточной руки без провала, он выигрывает.

    """

    # Статические переменные класса
    _current_hand = 0

    def __call__(self, common_vars, button_status):
        """

        :param common_vars:
        :param button_status:
        :return: None

        """
        logging.debug(type(self).__name__ + ':' + 'enter')

        if is_cut_passed(common_vars.shoe_of_decks):
            logging.info(type(self).__name__ + ': Cut passed, create new shoe with {0} decks'.format(NUM_OF_DECKS))
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)

        plot_chips(common_vars.screen, common_vars.player_cash, common_vars.chips_image_width, False)

        sound_db = SoundDB.get_instance()
        card_sound = sound_db.get_sound(SOUND_PATH + 'cardslide.wav')

        num_of_hands = len(common_vars.player_hands)
        if num_of_hands == 2:
            image_db = ImageDB.get_instance()
            if self._current_hand == 0:
                common_vars.screen.blit(image_db.get_image(IMAGE_PATH + 'hand.png'), (100, 315))
            else:
                common_vars.screen.blit(image_db.get_image(IMAGE_PATH + 'hand.png'), (100 + GAP_BETWEEN_SPLIT, 315))

        value_of_players_hand = get_value_of_players_hand(common_vars.player_hands[self._current_hand])
        if value_of_players_hand > 21:
            logging.info(type(self).__name__ + ': Player is busted {0}'.format(value_of_players_hand))
            common_vars.pause_time = PAUSE_TIMER3
            plot_results(common_vars.screen, common_vars.text_font,
                         'Player is busted {0}'.format(value_of_players_hand))
            if num_of_hands == 1:
                common_vars.hands_status['first_hand_busted'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            elif self._current_hand == 0:
                # Split и в первой руке проигрыш
                common_vars.hands_status['first_hand_busted'] = True
                button_status.double_down = True
                self._current_hand += 1
            elif self._current_hand == 1 and common_vars.hands_status['first_hand_busted']:
                # Split и обе руки проиграны
                common_vars.hands_status['second_hand_busted'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # Split и во второй руке проигрыш
                common_vars.hands_status['second_hand_busted'] = True
                self._current_hand = 0
                self.next_state(DealerInitState)
        elif value_of_players_hand == 21:
            if num_of_hands == 2 and self._current_hand == 0:
                logging.info(type(self).__name__ + ': first hand has ' + '21, save this hand for later evaluation')
                self._current_hand += 1
            else:
                logging.info(type(self).__name__ + ': second hand has ' + '21, lets see what the dealer has')
                self._current_hand = 0
                self.next_state(DealerInitState)
        else:
            # Создаем видимые области для кнопок, используемых при нажатии мыши.
            button_collide_instance = ButtonCollideArea.get_instance(common_vars)
            plot_buttons(common_vars.screen, button_status)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    common_vars.done = True
                if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    mouse_position = pygame.mouse.get_pos()  # returns (x, y) in a tuple
                    if button_collide_instance.hit_button_area.collidepoint(mouse_position[0], mouse_position[1]):
                        logging.info(type(self).__name__ + ': [Hit] pressed')
                        card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands[self._current_hand].append(card)
                        button_status.double_down = False
                    elif button_status.double_down and button_collide_instance.double_down_button_area.\
                            collidepoint(mouse_position[0], mouse_position[1]):
                        logging.info(type(self).__name__ + ': [Double down] pressed')
                        common_vars.double_downs[self._current_hand] = True
                        common_vars.player_cash -= sum(common_vars.player_bets[0])
                        common_vars.player_bets.append(common_vars.player_bets[0])
                        logging.info(type(self).__name__ + ': Remaining credits {0}'.format(common_vars.player_cash))
                        card_sound.play()
                        card = common_vars.shoe_of_decks.pop()
                        common_vars.player_hands[self._current_hand].append(card)
                        if num_of_hands == 2 and self._current_hand == 0:
                            # Одна рука осталась для управления
                            self._current_hand += 1
                        else:
                            self._current_hand = 0
                            button_status.double_down = False
                            self.next_state(DealerInitState)
                    elif button_collide_instance.stand_button_area.collidepoint(mouse_position[0], mouse_position[1]):
                        logging.info(type(self).__name__ + ': [Stands] pressed, player has {0}'.
                                     format(value_of_players_hand))
                        if num_of_hands == 2 and self._current_hand == 0:
                            # Одна рука осталась для управления
                            self._current_hand += 1
                            button_status.double_down = True
                        else:
                            self._current_hand = 0
                            self.next_state(DealerInitState)

        plot_bets(common_vars.screen, common_vars.player_bets)

        plot_buttons(common_vars.screen, button_status)

        plot_players_hands(common_vars.screen,
                           PLAYER_CARD_START_POS,
                           common_vars.player_hands,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)


class DealerInitState(State):
    """
    На основе двух вытянутых карт для дилера и карт, которые были вытянуты для игрока в предыдущих состояниях,
    проверяем, выиграл ли дилер какую-либо раздачу или у нас есть ничья.
    Если нет, переходим к следующему состоянию «DealerHitState».

    """

    # Статические переменные класса
    _current_hand = 0

    def __call__(self, common_vars, button_status):
        """

        :param common_vars:
        :param button_status:
        :return: None

        """
        logging.debug(type(self).__name__ + ':' + 'enter')

        if is_cut_passed(common_vars.shoe_of_decks):
            logging.info(type(self).__name__ + ': Cut passed, create new shoe with {0} decks'.format(NUM_OF_DECKS))
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)

        plot_chips(common_vars.screen, common_vars.player_cash, common_vars.chips_image_width, False)

        common_vars.first_card_hidden = False  # Показываем вторую карту дилера
        num_of_hands = len(common_vars.player_hands)
        value_of_dealer_hand = get_value_of_dealers_hand(common_vars.dealer_cards)
        common_vars.dealer_last_hand = value_of_dealer_hand
        value_of_player_hand = get_value_of_players_hand(common_vars.player_hands[self._current_hand])

        if value_of_dealer_hand == 21:
            logging.info(type(self).__name__ +
                         ': Dealer has {0}, Player has {1}'.format(value_of_dealer_hand, value_of_player_hand))
            if value_of_player_hand < 21:
                # Текущая рука игрока, проигранная против дилера
                common_vars.pause_time = PAUSE_TIMER3
                plot_results(common_vars.screen, common_vars.text_font,
                             'Dealer has {0}, Player has {1}'.format(value_of_dealer_hand, value_of_player_hand))
                if num_of_hands == 1:
                    # Только одна рука игрока
                    common_vars.hands_status['first_hand_loose'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                elif num_of_hands == 2 and self._current_hand == 0:
                    # Собераем ставки у игрока, который проиграл
                    common_vars.player_bets.pop()
                    # Первая рука в раздельном режиме, переход к следующей 
                    self._current_hand += 1
                    common_vars.hands_status['first_hand_loose'] = True
                else:
                    # Вторая рука в раздельном режиме
                    common_vars.hands_status['second_hand_loose'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
            else:
                logging.info(type(self).__name__ + ': Both dealer and player has 21, a push')
                common_vars.pause_time = PAUSE_TIMER3
                plot_results(common_vars.screen, common_vars.text_font,
                             'Both dealer and player has 21, a push')
                # Выплата ставки игроку обратно
                common_vars.player_cash += sum(common_vars.player_bets.pop())
                if num_of_hands == 1 or self._current_hand == 1:
                    # Оценивалась только первая рука игрока или последняя рука в раздельном режиме
                    common_vars.hands_status['first_hand_push'] = True
                    self._current_hand = 0
                    button_status.reset()
                    self.next_state(InitialState)
                else:
                    # Первая рука в раздельном режиме, переход к следующей 
                    self._current_hand += 1
                    common_vars.hands_status['first_hand_push'] = True
        elif value_of_dealer_hand > 15 and value_of_dealer_hand > value_of_player_hand:
            # У дилера на руках не менее 16 очков, и он выигрывает
            logging.info(type(self).__name__ +
                         ': Dealer wins with {0} over player {1}'.
                         format(value_of_dealer_hand, value_of_player_hand))
            common_vars.pause_time = PAUSE_TIMER3
            plot_results(common_vars.screen, common_vars.text_font,
                         'Dealer wins with {0} over player {1}'.
                         format(value_of_dealer_hand, value_of_player_hand))
            if num_of_hands == 1 or self._current_hand == 1:
                # Оценивалась только первая рука игрока или последняя рука в раздельном режиме
                common_vars.hands_status['first_hand_loose'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # Первая рука в раздельном режиме, переход к следующей раздаче
                self._current_hand += 1
                common_vars.hands_status['first_hand_loose'] = True
        elif value_of_player_hand > 21:
            # Игрок выведен из предыдущего состояния (возможно, с удвоенным коэффициентом).
            logging.info(type(self).__name__ +
                         ': Player is busted with {0}'.format(value_of_player_hand))
            common_vars.pause_time = PAUSE_TIMER3
            plot_results(common_vars.screen, common_vars.text_font,
                         'Player is busted with {0}'.format(value_of_player_hand))
            if num_of_hands == 1 or self._current_hand == 1:
                # Только одна рука
                common_vars.hands_status['first_hand_busted'] = True
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # Первая рука в раздельном режиме, переход к следующей раздаче
                self._current_hand += 1
                common_vars.hands_status['first_hand_busted'] = True
        else:
            self._current_hand = 0
            self.next_state(DealerHitState)

        plot_bets(common_vars.screen, common_vars.player_bets)

        plot_buttons(common_vars.screen, button_status)

        plot_players_hands(common_vars.screen,
                           PLAYER_CARD_START_POS,
                           common_vars.player_hands,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)


class DealerHitState(State):
    """
    Игрок готов со своей рукой (руками), а две первые карты дилера
    не побили карты игрока в предыдущем состоянии «DealerInitState».
    Дилер может брать карты, пока не выиграет или не проиграет,
    согласно правилам 16 и 17.

    """

    # Статичные переменные класса
    _current_hand = 0

    def __call__(self, common_vars, button_status):
        """

        :param common_vars:
        :param button_status:
        :return: None

        """
        logging.debug(type(self).__name__ + ':' + 'enter')

        if is_cut_passed(common_vars.shoe_of_decks):
            logging.info(type(self).__name__ + ': Cut passed, create new shoe with {0} decks'.format(NUM_OF_DECKS))
            common_vars.shoe_of_decks = CardDecks(NUM_OF_DECKS)

        plot_chips(common_vars.screen, common_vars.player_cash, common_vars.chips_image_width, False)

        sound_db = SoundDB.get_instance()
        card_sound = sound_db.get_sound(SOUND_PATH + 'cardslide.wav')

        num_of_hands = len(common_vars.player_hands)
        value_of_dealer_hand = get_value_of_dealers_hand(common_vars.dealer_cards)
        common_vars.dealer_last_hand = value_of_dealer_hand
        value_of_player_hand = get_value_of_players_hand(common_vars.player_hands[self._current_hand])

        if value_of_dealer_hand < 16:
            # Дилер обязан ходить до 16, независимо от того, какая у игрока комбинация
            card_sound.play()
            card = common_vars.shoe_of_decks.pop()
            common_vars.dealer_cards.append(card)
            common_vars.pause_time = 1.0
        elif value_of_dealer_hand < 17 and value_of_dealer_hand < value_of_player_hand:
            # У дилера меньше 17 очков и это меньше, чем текущая комбинация игрока.
            card_sound.play()
            card = common_vars.shoe_of_decks.pop()
            common_vars.dealer_cards.append(card)
            common_vars.pause_time = 1.0
        elif value_of_player_hand > 21 or 22 > value_of_dealer_hand > value_of_player_hand:
            # Дилер выиграл раздачу
            common_vars.pause_time = PAUSE_TIMER3
            if value_of_player_hand > 21:
                logging.info(type(self).__name__ +
                             ': Player is busted {0}'.format(value_of_player_hand))
                plot_results(common_vars.screen, common_vars.text_font,
                             'Player is busted {0}'.format(value_of_player_hand))
                if self._current_hand == 0:
                    common_vars.hands_status['first_hand_busted'] = True
                else:
                    common_vars.hands_status['second_hand_busted'] = True
            else:
                logging.info(type(self).__name__ +
                             ': Dealer wins with {0} over player {1}'.
                             format(value_of_dealer_hand, value_of_player_hand))
                plot_results(common_vars.screen, common_vars.text_font,
                             'Dealer wins with {0} over player {1}'.
                             format(value_of_dealer_hand, value_of_player_hand))
                if self._current_hand == 0:
                    common_vars.hands_status['first_hand_loose'] = True
                else:
                    common_vars.hands_status['second_hand_loose'] = True
            # Забираем ставку игрока после проигрыша
            common_vars.player_bets.pop()
            if common_vars.double_downs[self._current_hand]:
                # Забираем вторую ставку игрока после проигрыша (если было удвоение)
                common_vars.player_bets.pop()
            common_vars.pause_time = PAUSE_TIMER3
            if num_of_hands == 1 or self._current_hand == 1:
                # Мы закончили, если у игрока только одна рука или вторая рука была оценена
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # Первая рука в разделенном режиме была рассчитана, переходим ко второй
                self._current_hand += 1
        elif value_of_dealer_hand == value_of_player_hand:
            # Одинаковое значение у игрока и дилера - ничья
            common_vars.pause_time = PAUSE_TIMER3
            logging.info(type(self).__name__ +
                         ': A push, dealer has {0}, player has {1}'.
                         format(value_of_dealer_hand, value_of_player_hand))
            plot_results(common_vars.screen, common_vars.text_font,
                         'A push dealer has {0}, player has {1}'.
                         format(value_of_dealer_hand, value_of_player_hand))
            if self._current_hand == 0:
                common_vars.hands_status['first_hand_push'] = True
            else:
                common_vars.hands_status['second_hand_push'] = True

            if num_of_hands == 1 or self._current_hand == 1:
                # Мы закончили, если у игрока только одна рука или вторая рука была оценена
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # Первая рука в разделенном режиме была рассчитана, переходим ко второй
                self._current_hand += 1

            # Выплата ставки игроку
            common_vars.player_cash += sum(common_vars.player_bets.pop())
            if common_vars.double_downs[self._current_hand]:
                # Выплата второй ставки если было удвоение
                common_vars.player_cash += sum(common_vars.player_bets.pop())

        else:
            # Игрок выиграл руку
            if self._current_hand == 0:
                common_vars.hands_status['first_hand_win'] = True
            else:
                common_vars.hands_status['second_hand_win'] = True
            logging.info(type(self).__name__ +
                         ': Player wins with {0} over dealer {1}, bet is {2}'.
                         format(value_of_player_hand, value_of_dealer_hand, common_vars.player_bets[0]))
            common_vars.pause_time = PAUSE_TIMER3
            plot_results(common_vars.screen, common_vars.text_font,
                         "Player wins with {0} over dealer {1}".format(value_of_player_hand, value_of_dealer_hand))
            common_vars.player_cash += sum(common_vars.player_bets.pop()) * 2
            if common_vars.double_downs[self._current_hand]:
                # Выигрыш после удвоения (добавляем дополнительную победу)
                logging.info(type(self).__name__ +
                             ': Double down, add additional win {0}'.
                             format(common_vars.player_bets[0]))
                common_vars.player_cash += sum(common_vars.player_bets.pop()) * 2
            common_vars.dealer_last_hand = value_of_dealer_hand
            if num_of_hands == 1 or self._current_hand == 1:
                # Мы закончили, если у игрока только одна рука или вторая рука была оценена
                self._current_hand = 0
                button_status.reset()
                self.next_state(InitialState)
            else:
                # Первая рука в разделенном режиме была рассчитана, переходим ко второй
                self._current_hand += 1

        plot_bets(common_vars.screen, common_vars.player_bets)

        plot_buttons(common_vars.screen, button_status)

        plot_players_hands(common_vars.screen,
                           PLAYER_CARD_START_POS,
                           common_vars.player_hands,
                           common_vars.double_downs,
                           common_vars.hands_status)

        plot_dealers_hand(common_vars.screen,
                          DEALER_CARD_START_POS,
                          common_vars.dealer_cards,
                          common_vars.first_card_hidden)


class FinalState(State):
    """
    У игрока закончились деньги.
    Остаемся в этом состоянии, пока он не нажмёт кнопку выхода [x].

    """
    def __call__(self, common_vars, button_status):
        """

        :param common_vars:
        :param button_status:
        :return: None

        """
        logging.debug(type(self).__name__ + ':' + 'enter')

        # Plot the players current account value
        account_text = common_vars.text_font.render("Game Over, you're out of money", False, GOLD_COLOR)
        common_vars.screen.blit(account_text, (5, GAME_BOARD_Y_SIZE - 30))

        # React on mouse click on [x]
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                common_vars.done = True
