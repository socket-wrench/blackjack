#!/usr/bin/python3.8
# blackjack.py
'''
A simple player vs dealer blackjack game
'''

from time import sleep
import random

GAME_DELAY = 0.5

CARD_RANKS = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine',
              'Ten', 'Jack', 'Queen', 'King', 'Ace')
CARD_VALUES = {
    'Two': 2,
    'Three': 3,
    'Four': 4,
    'Five': 5,
    'Six': 6,
    'Seven': 7,
    'Eight': 8,
    'Nine': 9,
    'Ten': 10,
    'Jack': 10,
    'Queen': 10,
    'King': 10,
    'Ace': 11
}
CARD_SUITS = ('Clubs', 'Spades', 'Hearts', 'Diamonds')
SUIT_SYMBOLS = {'Spades':'\u2660',
                'Clubs':'\u2663',
                'Hearts':'\u2661',
                'Diamonds':'\u2662'}

STARTING_CHIPS = 1000.0
MINIMUM_BET = 100.0

CARD_IMAGE = ('\u250c'+'\u2500'*9+'\u2510''\n'
              '\u2502'+'{}'+' '*7+'\u2502''\n'
              '\u2502'+' '*9+'\u2502''\n'
              '\u2502'+' '*9+'\u2502''\n'
              '\u2502'+' '*3+'{}'+' '*4+'\u2502''\n'
              '\u2502'+' '*9+'\u2502''\n'
              '\u2502'+' '*9+'\u2502''\n'
              '\u2502'+' '*7+'{}'+'\u2502''\n'
              '\u2514'+'\u2500'*9+'\u2518'
             ).format('{rank: <2}', '{suit: <2}', '{rank: >2}')
BLANK_CARD_IMAGE = ('\u250c'+'\u2500'*9+'\u2510''\n'
                    '\u2502'+'\u2591'*9+'\u2502''\n'
                    '\u2502'+'\u2591'*9+'\u2502''\n'
                    '\u2502'+'\u2591'*9+'\u2502''\n'
                    '\u2502'+'\u2591'*9+'\u2502''\n'
                    '\u2502'+'\u2591'*9+'\u2502''\n'
                    '\u2502'+'\u2591'*9+'\u2502''\n'
                    '\u2502'+'\u2591'*9+'\u2502''\n'
                    '\u2514'+'\u2500'*9+'\u2518'
                    )

class Hand():
    '''
    The current hand for player
    '''

    def __init__(self):
        self.hand = []

    def recv_card(self, new_cards):
        '''
        Add card(s) to player hand
        '''
        if isinstance(new_cards, list):
            # Add list of multiple cards
            self.hand.extend(new_cards)
        else:
            # Add single card
            self.hand.append(new_cards)

    def total(self):
        '''
        Calculate the total value for current hand
        '''
        total = 0
        aces = 0
        for card in self.hand:
            total += card.value
            if card.rank in 'Ace':
                aces += 1
            while total > 21 and aces > 0:
                total -= 10
                aces -= 1
        return total

    def prt_hand(self):
        '''
        Show current hand
        '''
        for card in self.hand:
            print(card)
        print('Total: {}'.format(self.total()))


class ChipStack():
    '''
    Stack of chips
    '''

    def __init__(self, chips):
        self.chips = chips

    def add_chips(self, chips):
        '''
        Add chips to stack
        '''
        self.chips += chips

    def rem_chips(self, chips):
        '''
        Remove chips from stack
        '''
        self.chips -= chips

    def __str__(self):
        return '${}'.format(self.chips)

    def __len__(self):
        return self.chips

class Card():
    '''
    Class for each card
    '''

    def __init__(self, suit, rank):
        self.suit = suit.capitalize()
        self.rank = rank.capitalize()
        self.value = CARD_VALUES[rank]
        if self.rank in ('Jack', 'Queen', 'King', 'Ace'):
            self.card_char = self.rank[0]
        else:
            self.card_char = self.value
        self.image = CARD_IMAGE.format(rank=self.card_char,
                                       suit=SUIT_SYMBOLS[self.suit])

    def __str__(self):
        return self.rank + " of " + self.suit

class Deck():
    '''
    Class for the deck of cards
    '''

    def __init__(self):
        self.all_cards = []
        for suit in CARD_SUITS:
            for rank in CARD_RANKS:
                created_card = Card(suit, rank)
                self.all_cards.append(created_card)

    def __len__(self):
        return len(self.all_cards)

    def __str__(self):
        deck_comp = ''
        for card in self.all_cards:
            deck_comp += '\n  ' + card.__str__()
        return 'The deck has:' + deck_comp

    def shuffle(self):
        '''
        Shuffle the deck
        '''
        random.shuffle(self.all_cards)

    def deal(self):
        '''
        Pull a card off the deck and deal return that card
        '''
        return self.all_cards.pop()

def join_lines(strings):
    '''
    Takes a series of items cards printed individually and prints
    them together horizontally.
    e.g.
    [],[],[]
    becomes:
    [][][]
    '''
    liness = [string.splitlines() for string in strings]
    return '\n'.join(''.join(lines) for lines in zip(*liness))

def hand_image(hand, hidden_cards=0):
    '''
    Prints image of a hand horizontally
    :param hand: the specific Hand class object to be displayed
    :param hidden_cards: how many of the cards should be hidden (default 0)
    '''
    images = []
    for _ in range(0, hidden_cards):
        images.append(BLANK_CARD_IMAGE)
    for card in hand.hand[hidden_cards:]:
        images.append(card.image)
    return join_lines(images)

def display_board(dealer_hand, player_hand, bet, chipstack, hidden=0):
    '''
    Display the current hands and current bets with a number of cards of dealers hand hidden
    '''
    pline = '-' * 30
    print('\033c')  # clear the screen
    print('Dealer Hand\n{}'.format(pline))
    print(hand_image(dealer_hand, hidden))
    dealer_total = 0
    for card in dealer_hand.hand[hidden:]:
        dealer_total += card.value
    if hidden > 0:
        print('Dealer Total: {}?'.format(dealer_total))
    else:
        print('Dealer Total: {}'.format(dealer_hand.total()))
    print('\n\n')
    print('Player Hand\n{}'.format(pline))
    print(hand_image(player_hand))
    print('Player Total: {}'.format(player_hand.total()))
    print('\n{}'.format(pline))
    print('Current bet:     {:>5}{}'.format('$', bet))
    print('Chips Remaining: {:>5}{}'.format('$', chipstack.chips - bet))
    print('{}\n'.format(pline))


if __name__ == '__main__':
    # Setup game
    # Create ChipStack
    CHIPS = ChipStack(STARTING_CHIPS)
    # Create Deck
    DECK = Deck()
    DECK.shuffle()
    print('Dealer is shuffling the deck...')
    sleep(3 * GAME_DELAY)
    # Main while loop
    PLAYING = True
    while PLAYING:
        # If player chipstack < minimum bet, exit game
        if CHIPS.chips < MINIMUM_BET:
            PLAYING = False
            print(
                'I am sorry, you do not have enough chips to continue.  Goodbye.'
            )
            break
        # Player places bet or quits
        BET = 0
        while BET < MINIMUM_BET:
            BET = MINIMUM_BET
            try:
                BET = input('Bank roll:  ${}\n'
                            'Minimum Bet:  ${}.\n'
                            'Press enter to bet the minimum or enter a number to raise the bet. '
                            .format(CHIPS.chips, MINIMUM_BET))
                if BET == '':
                    BET = MINIMUM_BET
                else:
                    BET = float(BET)
            except ValueError:
                print('{} is not a valid bet.  Must be a number.'.format(BET))
                BET = 0
            if BET > CHIPS.chips:
                print('You have bet more than you have,')
                print('please bet beneath your current bank roll of ${}'
                      .format(CHIPS.chips))
                BET = 0
        # Shuffle Deck
        if len(DECK) < 16:
            DECK = Deck()
            DECK.shuffle()
            print('Dealer is shuffling the deck...')
            sleep(3 * GAME_DELAY)
        # Deal hands
        DEALER_HAND = Hand()
        PLAYER_HAND = Hand()
        PLAYER_HAND.recv_card(DECK.deal())
        display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 2)
        sleep(GAME_DELAY)
        DEALER_HAND.recv_card(DECK.deal())
        display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 2)
        sleep(GAME_DELAY)
        PLAYER_HAND.recv_card(DECK.deal())
        display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 2)
        sleep(GAME_DELAY)
        DEALER_HAND.recv_card(DECK.deal())
        display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 2)
        sleep(GAME_DELAY)
        # Display both cards in dealer hand and player hand
        display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 1)
        sleep(GAME_DELAY)

        # If dealer and player both have 21, push and break Round loop
        if DEALER_HAND.total() == PLAYER_HAND.total() == 21:
            display_board(DEALER_HAND, PLAYER_HAND, 0.0, CHIPS, 0)
            print('Both dealer and player start with blackjack.  PUSH!')
            sleep(2 * GAME_DELAY)
        # If dealer has 21 and player doesn't, dealer wins and break Round loop
        elif DEALER_HAND.total() == 21:
            CHIPS.rem_chips(BET)
            display_board(DEALER_HAND, PLAYER_HAND, 0.0, CHIPS, 0)
            print('Dealer got Black Jack.  Sorry. You lost ${}'.format(BET))
            sleep(2 * GAME_DELAY)
        # If HAND.total() == 21, player wins, and BLACKJACK
        elif PLAYER_HAND.total() == 21:
            CHIPS.add_chips(BET * 3 / 2)
            display_board(DEALER_HAND, PLAYER_HAND, 0.0, CHIPS, 0)
            print('Player got a Black Jack!! You win ${}!'.format(BET * 3 / 2))
            sleep(2 * GAME_DELAY)
        else:
            # Player Choice while loop
            PLAYER_BUST = False
            PLAYER_STAY = False
            while not PLAYER_BUST and not PLAYER_STAY:
                # If HAND.total() > 21, player busts
                if PLAYER_HAND.total() > 21:
                    PLAYER_BUST = True
                    break
                # Player option: fold, stay, hit, double-down, split?
                SELECTION = ''
                if len(PLAYER_HAND.hand) == 2 and CHIPS.chips >= BET * 2:
                    PLAYER_OPTIONS = ('s', 'h', 'd')
                    while SELECTION.lower() not in PLAYER_OPTIONS:
                        display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 1)
                        SELECTION = (input('What would you like to do? \n'
                                           '[s]tay, [h]it, or [d]ouble-down '))
                else:
                    PLAYER_OPTIONS = ('s', 'h')
                    while SELECTION.lower() not in PLAYER_OPTIONS:
                        display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 1)
                        SELECTION = (input('What would you like to do? [s]tay or [h]it '))
                # If stay, break Player Choice while loop
                if SELECTION == 's':
                    PLAYER_STAY = True
                    break
                # If hit, add card to hand and continue
                if SELECTION == 'h':
                    PLAYER_HAND.recv_card(DECK.deal())
                    display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 1)
                    sleep(GAME_DELAY)
                if SELECTION == 'd':
                    PLAYER_HAND.recv_card(DECK.deal())
                    BET += BET
                    display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 1)
                    sleep(GAME_DELAY)
                    PLAYER_STAY = True
                    break
                # TODO Split
            # If player busted remove bet from chipstack
            if PLAYER_BUST:
                display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 0)
                print('Player busts.  You lose ${}'.format(BET))
                CHIPS.rem_chips(BET)
            else:
                # Dealer while loop, only initiate if player not busted out
                display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 0)
                sleep(GAME_DELAY)
                while DEALER_HAND.total() < 17:
                    # If dealer hand > 21, dealer busts, player wins, break Dealer loop
                    # If dealer hand >= 17, dealer stays, break Dealer loop
                    # If dealer hand < 17, dealer hits
                    DEALER_HAND.recv_card(DECK.deal())
                    display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 0)
                    sleep(GAME_DELAY)
                # if dealer busted add bet to chipstack
                if DEALER_HAND.total() > 21:
                    CHIPS.add_chips(BET)
                    display_board(DEALER_HAND, PLAYER_HAND, 0, CHIPS, 0)
                    print('Dealer busts.  You win ${}!'.format(BET))
                # elif dealer hand == player_hand, push, no chipstack change
                elif DEALER_HAND.total() == PLAYER_HAND.total():
                    display_board(DEALER_HAND, PLAYER_HAND, 0, CHIPS, 0)
                    print('Both dealer and player scored {}.  Push!'.format(
                        DEALER_HAND.total()))
                # elif dealer hand > player hand, dealer wins, remove bet from chipstack
                elif DEALER_HAND.total() > PLAYER_HAND.total():
                    CHIPS.rem_chips(BET)
                    display_board(DEALER_HAND, PLAYER_HAND, 0, CHIPS, 0)
                    print(
                        'Dealer\'s {} beats player\'s {}.\nDealer wins. You lose ${}.'
                        .format(DEALER_HAND.total(), PLAYER_HAND.total(), BET))
                # elif player hand > dealer hand, player wins, add bet to chipstack
                elif DEALER_HAND.total() < PLAYER_HAND.total():
                    CHIPS.add_chips(BET)
                    display_board(DEALER_HAND, PLAYER_HAND, 0, CHIPS, 0)
                    print(
                        'Player\'s {} beats dealer\'s {}!!!\n Player wins ${}!'
                        .format(PLAYER_HAND.total(), DEALER_HAND.total(), BET))
        # Check if player wants to continue playing.
        display_board(DEALER_HAND, PLAYER_HAND, 0, CHIPS, 0)
        if CHIPS.chips >= MINIMUM_BET:
            CONFIRM_CONTINUE = input('Keep playing? [y/n] ')
        else:
            CONFIRM_CONTINUE = 'y'
        if CONFIRM_CONTINUE.lower() == 'n':
            PLAYING = False
            print('You walked away with ${}.  Goodbye!'.format(CHIPS.chips))
    print('Quitting...')
