
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

### FUNCTIONS ###
