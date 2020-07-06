#!/usr/bin/python3.8
# blackjack.py
'''
A simple player vs dealer blackjack game
'''

from time import sleep
import random

CARD_VALUES = {'Two':2, 'Three':3, 'Four':4,
               'Five':5, 'Six':6, 'Seven':7, 'Eight':8,
               'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10,
               'King':10, 'Ace':11
              }
CARD_SUITS = ('Clubs', 'Spades', 'Hearts', 'Diamonds')
CARD_RANKS = ('Two', 'Three', 'Four', 'Five',
              'Six', 'Seven', 'Eight', 'Nine', 'Ten',
              'Jack', 'Queen', 'King', 'Ace'
             )

STARTING_CHIPS = 500
MINIMUM_BET = 5


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
        self.suit = suit
        self.rank = rank
        self.value = CARD_VALUES[rank]
    def __str__(self):
        return self.rank + " of " + self.suit
    def details(self):
        '''
        Print details for the card
        '''
        print('{} of {}\n----------------\nSuit:\t{}\nRank\t{}\nValue\t{}\n'
              .format(self.rank, self.suit, self.suit, self.rank, self.value)
             )


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

def display_board(dealer_hand, player_hand, bet, chipstack, hidden=0):
    '''
    Display the current hands and current bets with a number of cards of dealers hand hidden
    '''
    pline = '-'*30
    print('\033c') #clear the screen
    print('Dealer Hand\n{}'.format(pline))
    for _ in range(hidden):
        print('????? of ??????')
    dealer_total = 0
    for card in dealer_hand.hand[hidden:]:
        print(card)
        dealer_total += card.value
    if hidden > 0:
        print('Dealer Total: {}?'.format(dealer_total))
    else:
        print('Dealer Total: {}'.format(dealer_hand.total()))
    print('\n\n')
    print('Player Hand\n{}'.format(pline))
    for card in player_hand.hand:
        print(card)
    print('Player Total: {}'.format(player_hand.total()))
    print('\n{}'.format(pline))
    print('Current bet: ${:>30}'.format(bet))
    print('Chips Remaining: ${:>30}'.format(chipstack.chips - bet))
    print('{}\n'.format(pline))



if __name__ == '__main__':
    # Setup game
    # Create ChipStack
    CHIPS = ChipStack(STARTING_CHIPS)
    # Create Deck
    DECK = Deck()
    DECK.shuffle()
    print('Dealer is shuffling the deck...')
    sleep(3)
    # Main while loop
    PLAYING = True
    while PLAYING:
        # If player chipstack < minimum bet, exit game
        if CHIPS.chips < MINIMUM_BET:
            PLAYING = False
            print('I am sorry, you do not have enough chips to continue.  Goodbye.')
            break
        # Player places bet or quits
        BET = 0
        while BET < MINIMUM_BET:
            BET = MINIMUM_BET
            try:
                BET = float(input('Place your bet! (minimum {}) '.format(MINIMUM_BET)))
            except:
                print('')
            else:
                BET = MINIMUM_BET
        # Shuffle Deck
        if len(DECK) < 16:
            DECK = Deck()
            DECK.shuffle()
            print('Dealer is shuffling the deck...')
            sleep(3)
        # Deal hands
        DEALER_HAND = Hand()
        PLAYER_HAND = Hand()
        PLAYER_HAND.recv_card(DECK.deal())
        display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 2)
        sleep(1)
        DEALER_HAND.recv_card(DECK.deal())
        display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 2)
        sleep(1)
        PLAYER_HAND.recv_card(DECK.deal())
        display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 2)
        sleep(1)
        DEALER_HAND.recv_card(DECK.deal())
        display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 2)
        sleep(1)
        # Display both cards in dealer hand and player hand
        display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 1)
        sleep(1)

        # If dealer and player both have 21, push and break Round loop
        if DEALER_HAND.total() == PLAYER_HAND.total() == 21:
            display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 0)
            print('Both dealer and player start with blackjack.  PUSH!')
        # If dealer has 21 and player doesn't, dealer wins and break Round loop
        elif DEALER_HAND.total() == 21:
            display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 0)
            print('Dealer got Black Jack.  Sorry. You lost ${}'.format(BET))
            CHIPS.rem_chips(BET)
        # If HAND.total() == 21, player wins, and BLACKJACK
        elif PLAYER_HAND.total() == 21:
            display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 0)
            print('Player got a Black Jack!! You win ${}!'.format(BET * 3 / 2))
            CHIPS.add_chips(BET * 3 / 2)
        else:
            # Player Choice while loop
            PLAYER_BUST = False
            PLAYER_STAY = False
            while not PLAYER_BUST and not PLAYER_STAY:
                # If HAND.total() > 21, player busts
                if PLAYER_HAND.total() > 21:
                    PLAYER_BUST = True
                    break
                # Player option: fold, stay, hit, double-down?, split?
                PLAYER_OPTIONS = ['fold', 'stay', 'hit']
                SELECTION = ''
                while SELECTION not in PLAYER_OPTIONS:
                    display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 1)
                    SELECTION = (input('What would you like to do? {} '.format(PLAYER_OPTIONS)))
                # If stay, break Player Choice while loop
                if SELECTION == 'stay':
                    PLAYER_STAY = True
                    break
                # If hit, add card to hand and continue
                if SELECTION == 'hit':
                    PLAYER_HAND.recv_card(DECK.deal())
                    display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 1)
                    sleep(1)
                # TODO If double-down, double bet and hit once, then break Player Choice while loop
                # TODO Split
            # If player busted remove bet from chipstack
            if PLAYER_BUST:
                display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 0)
                print('Player busts.  You lose ${}'.format(BET))
                CHIPS.rem_chips(BET)
            else:
                # Dealer while loop, only initiate if player not busted out
                display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 0)
                sleep(1)
                while DEALER_HAND.total() < 17:
                    # If dealer hand > 21, dealer busts, player wins, break Dealer loop
                    # If dealer hand >= 17, dealer stays, break Dealer loop
                    # If dealer hand < 17, dealer hits
                    DEALER_HAND.recv_card(DECK.deal())
                    display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 0)
                    sleep(1)
                # if dealer busted add bet to chipstack
                if DEALER_HAND.total() > 21:
                    display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 0)
                    print('Dealer busts.  You win ${}!'.format(BET))
                    CHIPS.add_chips(BET)
                # elif dealer hand == player_hand, push, no chipstack change
                elif DEALER_HAND.total() == PLAYER_HAND.total():
                    display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 0)
                    print('Both dealer and player scored {}.  Push!'.format(DEALER_HAND.total()))
                # elif dealer hand > player hand, dealer wins, remove bet from chipstack
                elif DEALER_HAND.total() > PLAYER_HAND.total():
                    display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 0)
                    print('Dealer\'s {} beats player\'s {}.\nDealer wins. You lose ${}.'
                          .format(DEALER_HAND.total(),
                                  PLAYER_HAND.total(),
                                  BET)
                         )
                # elif player hand > dealer hand, player wins, add bet to chipstack
                elif DEALER_HAND.total() < PLAYER_HAND.total():
                    display_board(DEALER_HAND, PLAYER_HAND, BET, CHIPS, 0)
                    print('Player\'s {} beats dealer\'s {}!!!\n Player wins ${}!'
                          .format(PLAYER_HAND.total(),
                                  DEALER_HAND.total(),
                                  BET)
                         )
        # Check if player wants to continue playing.
        CONFIRM_CONTINUE = input('Keep playing? [y/n] ')
        if CONFIRM_CONTINUE == 'n':
            PLAYING = False
            print('You walked away with ${}.  Goodbye!'.format(CHIPS.chips))
    print('Quitting...')