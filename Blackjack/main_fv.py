####################################
# author: Gonzalo Salazar
# course: 2020 Complete Python Bootcamps: From Zero to Hero in Python
# purpose: milestone project 2 - create a Blackjack game (w/o splitting and
#          doubling down)
# description: Main script + Funtions + Classess
# name: Blackjack 101 (Final Version 2.0)
####################################

#recall: to set working directory
#cd ..
#cd Coding-Projects/Blackjack

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
            chips.bet = int(input('\nHow many chips would you like to bet?: '))

            if chips.total < chips.bet:
                raise BalanceError('Bet amount is larger than the available balance.')

            break
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
            answer = input('\nDo you want to (H)IT or (S)TAND?: ')

            if answer.upper() in hit_values:
                hit(deck,hand)

            elif answer.upper() in stand_values:
                print("Player stands. Dealer's turn begins.")
                playing = False

            elif not answer.upper() in hit_values and not answer.upper() in stand_values:
                raise 'Invalid input.'

            break

        except:
            print('Invalid answer. Please answer (H)IT or (S)TAND.')

def show_some(player,dealer):
    "Show the cards on the board, hidding the first card on the dealer's hand"

    print("Dealer's hand:")
    print("<Covered Card>", str(dealer.cards[1]), sep = ' / ')
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

def player_busts(player,dealer,chips):
    print('\nPlayer busts, dealer collects ' + str(chips.bet))
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print('\nPlayer wins! ' + str(chips.bet))
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print('\nDealer busts, player wins! ' + str(chips.bet))
    chips.win_bet()

def dealer_wins(player,dealer,chips):
    print('\nDealer wins ' + str(chips.bet))
    chips.lose_bet()

def push(player,dealer):
    print('\nThere is a Push (Tie). Nobody wins.')

### GAME SETTING ###
def main():
    global playing

    while True:

        # Opening statement
        print('Welcome to Blackjack 101. These are the rules:')
        print("-> The goal of blackjack is to beat the dealer's hand without going over 21.",
                 "-> Face cards are worth 10. Aces are worth 1 or 11, whichever makes a better hand.",
                 "-> Each player starts with two cards, one of the dealer's cards is hidden until the end.",
                 "-> To 'HIT' is to ask for another card. To 'STAND' is to hold your total and end your turn.",
                 "-> If you go over 21 you bust, and the dealer wins regardless of the dealer's hand.",
                 "-> If you are dealt 21 from the start (Ace & 10), you got a blackjack.",
                 "-> Blackjack usually means you win 1.5 the amount of your bet. Depends on the casino.",
                 "   In this case, if you win, you will win exactly what you have bet.",
                 "-> Dealer will hit until his/her cards total 17 or higher.",
                 "-> Doubling and splitting are not allowed in this version.",
                 sep = '\n')
        print("\nPlease enjoy the game. Let's start!")

        # Create & shuffle the deck, deal two cards to each player
        deck = Deck()
        deck.shuffle()

        dealer_hand = Hand()
        hit(deck,dealer_hand)
        hit(deck,dealer_hand)

        player_hand = Hand()
        hit(deck,player_hand)
        hit(deck,player_hand)

        # Set up the Player's chips
        chips = Chips()

        # Prompt the Player for their bet
        take_bet(chips)

        # Show cards (but keep one dealer card hidden)
        print('\n---------------------------------------')
        print('(1) The current board is: \n')
        show_some(player_hand,dealer_hand)
        print('---------------------------------------')

        while playing:
            # Prompt for Player to Hit or Stand
            hit_or_stand(deck,player_hand)

            # Show cards (but keep one dealer card hidden)
            print('\n---------------------------------------')
            print('(2) The current board now is: \n')
            show_some(player_hand,dealer_hand)
            print('---------------------------------------')

            if player_hand.value > 21:
                player_busts(player_hand,dealer_hand,chips)
                break

        if player_hand.value <= 21:

            while dealer_hand.value < 17:
                hit(deck,dealer_hand)

            # Show ALL cards
            print('\n---------------------------------------')
            print('(3) The final board is: \n')
            show_all(player_hand,dealer_hand)
            print('---------------------------------------')

            # Winning scenarios where player wins
            if dealer_hand.value > 21:
                dealer_busts(player_hand,dealer_hand,chips)
            elif player_hand.value < dealer_hand.value:
                dealer_wins(player_hand,dealer_hand,chips)
            elif player_hand.value > dealer_hand.value:
                player_wins(player_hand,dealer_hand,chips)
            else:
                push(player_hand,dealer_hand)

        # Inform Player of their chips total
        print('\nYour current chips balance is: ' + str(chips.total))

        # Ask to play again
        while True:
            answer = input('Would you like to continue playing (Y or N)?: ')

            if answer.upper() in ('Y','N'):
               break
            else:
               print('Invalid answer. Please say (Y)es or (N)o.')
               continue

        if answer.upper() == 'Y':
            playing = True
            continue
        else:
            return print('\nHope you had enjoyed the game. See you next time!')

### LET'S PLAY! ###
main()
