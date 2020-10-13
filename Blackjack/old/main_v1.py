####################################
# author: Gonzalo Salazar
# course: 2020 Complete Python Bootcamps: From Zero to Hero in Python
# purpose: milestone project 2 - create a Blackjack game (w/o splitting and
#          doubling down)
# description: Main script
# comment: It runs on a Jupyter Notebook, but does not run on Python IDLE.
#          PENDING TO CHECK FOR THE REASON!
####################################

#recall: to set working directory
#cd ..
#cd Coding-Projects/Blackjack

bj_modules import *

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

main()
