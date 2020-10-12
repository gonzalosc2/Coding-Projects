
####################################
# author: Gonzalo Salazar
# course: 2020 Complete Python Bootcamps: From Zero to Hero in Python
# purpose: milestone project 2 - create a Blackjack game (w/o splitting and
#          doubling down)
# description: Classes and Functions definition
# other: N/A
####################################

#recall: to set working directory
#cd ..
#cd Coding-Projects/Blackjack

### MODULES ###
import random

### GLOBAL VARIABLES ###
suits = ('Clubs', 'Diamonds', 'Hearts', 'Spades')
ranks = ('Two','Three','Four','Five','Six','Seven','Eight','Nine','Ten', \
         'Jack','Queen','King','Ace')
values = {'Two':2,'Three':3,'Four':4,'Five':5,'Six':6,'Seven':7,'Eight':8, \
          'Nine':9,'Ten':10,'Jack':10,'Queen':10,'King':10,'Ace':11}
playing = True

### CLASSESS ###
class Card:
    "Creates a Card object with a suit and a rank"

    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[self.rank]

    def __str__(self):
        return self.rank + ' of ' + self.suit

class Deck:
    "Holds all 52 Card objects, which can be shuffled"

    def __init__(self):
        self.deck = []  # start with an empty list

        for suit in suits:
            for rank in ranks:
                card = Card(suit,rank)
                self.deck.append(card)

    def __str__(self):
        deck_in_string = ''

        for card in self.deck:
            deck_in_string += '\n' + card.__str__()

        return 'Actual Deck: \n' + deck_in_string

    def __len__(self):
        count = 0

        for card in self.deck:
            count += 1

        return count

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        return self.deck.pop()

class Hand:
    "Holds those Cards that have been dealt to each player from the Deck"

    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def __str__(self):
        hand_in_string = ''

        if self.cards == []:
            return 'Empty Hand'
        else:
            for card in self.cards:
                hand_in_string += '\n' + card.__str__()

            return 'Actual Hand: \n' + hand_in_string

    def add_card(self,card):
        if card.rank == "Ace":
            self.aces += 1

        self.value += card.value
        self.cards.append(card)

    def adjust_for_ace(self):
        while self.aces > 0 and self.value > 21:
            self.value -= 10
            self.aces -= 1

class Chips:
    "Keeps track of a Player's starting chips, bets, and ongoing winnings"

    def __init__(self,total = 100):
        self.total = total  # default is 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

class BalanceError(Exception):
    "Used when bet amount is larger than the available balance"
    pass

### FUNCTIONS ###
def take_bet(chips):
    "Asks the user for an integer value and checks that a Player's bet can be"
    "covered by their available chips."

    while True:
        try:
            chips.bet = int(input('How much do you want to bet?: '))

            if chips.total < chips.bet:
                raise BalanceError('Bet amount is larger than the available balance.')

            return bet

        except ValueError:
            print('The value entered is wrong. Please use interger values.')

        except BalanceError:
            print('Bet amount is larger than the available balance.' + \
                  '\nPlease bet an amount less than or equal to your available balance: ' + \
                  str(chips.total))

def hit(deck,hand):
    "Deals one card off the deck and add it to the Hand. As well as checks for"
    "aces in the event that a player's hand exceeds 21."

    deal = deck.deal()
    hand.add_card(deal)
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    "Controls the behavior of the while loop associated with the player's turn."

    global playing  # to control an upcoming while loop
    hit_values = ('H','HIT')
    stand_values = ('S','STAND')

    while True:
        try:
            answer = input('Do you want to HIT(H) or STAND(S)?: ')
            if not answer.upper() in hit_values and not answer.upper() in stand_values:
                raise 'Invalid input.'

            if answer.upper() == 'H' or 'HIT':
                hit(deck,hand)
            else:
                print("Player stands. Dealer's turn begins.")
                playing = False

            break
        except:
            print('Invalid answer. Please answer HIT or STAND.')

def show_some(player,dealer):
    "Show the cards on the board, hidding the first card on the dealer's hand"

    print("Dealer's hand:")
    print("\n<Covered Card>", str(dealer.cards[1]), sep = ' / ')
    print('\n')

    print("Player's hand:")
    print(*player.cards, sep = ' / ')

def show_all(player,dealer):
    "Show all the cards on the board"

    print("Dealer's hand:")
    print(*dealer.cards, sep = ' / ')
    print('\n')

    print("Player's hand:")
    print(*player.cards, sep = ' / ')

    





# deck = Deck()
# dealer = Hand()
# player = Hand()
#
# dealer.add_card(deck.deal())
# player.add_card(deck.deal())
#
# show_all(player,dealer)
