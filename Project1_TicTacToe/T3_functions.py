####################################
# author: Gonzalo Salazar
# course: 2020 Complete Python Bootcamps: From Zero to Hero in Python
# purpose: milestone project 1 - create a Tic-Tac-Toe game
# description: set of functions necessary to run this code, as well as the
#              main body of the TIC TAC TOE game, called game()
# other: N/A
####################################

import os
def clear():
    os.system('clear')

def player_selection():
    print('\nWelcome to this Tic-Tac-Toe game.' +
          '\nThe rules are already known to everyone.' +
          '\nYou must be two people and each one must play their corresponding turn.' +
          '\nPlease choose who is going to be the first player' +
          '\n(the person who will start playing).')

    p1 = ''

    while p1 not in ['X','O','x','o']:
            p1 = input('Player 1, please select your preferred marker, X or O: ').upper()

            if p1 not in ['X','O','x','o']:
                print('The value is not valid. Please choose X or O.')

    if p1 == 'X':
        p2 = 'O'
    else:
        p2 = 'X'

    return [p1, p2]

def board_display(board = ['1','2','3','4','5','6','7','8','9']):
    print('\n'+board[0] + '|' + board[1] + '|' + board[2] +
          '\n'+board[3] + '|' + board[4] + '|' + board[5] +
          '\n'+board[6] + '|' + board[7] + '|' + board[8] )

def position_selection(board):
    pos = 0
    default_board = ['1','2','3','4','5','6','7','8','9']

    while pos not in range(1,10) or board[pos-1] not in default_board:
        try:
            pos = int(input('Please, select the cell you want to select (from 1 to 9): '))
            if pos not in range(1,10):
                print('The value is not valid. Please select an interger number between 1 and 9 (inclusive).')
                continue
            if board[pos-1] not in default_board:
                print('Cell {num} is already filled. Please select among the remaining cells.'.format(num = pos))
        except ValueError:
            print('The value is not valid. Please select a interger number between 1 and 9 (inclusive).')

    return (pos-1)

def is_winner(board,marker):
    # rows
    r1 = (board[0] == board[1] == board[2] == marker)
    r2 = (board[3] == board[4] == board[5] == marker)
    r3 = (board[6] == board[7] == board[8] == marker)

    # columns
    c1 = (board[0] == board[3] == board[6] == marker)
    c2 = (board[1] == board[4] == board[7] == marker)
    c3 = (board[2] == board[5] == board[8] == marker)

    # diagonals
    d1 = (board[0] == board[4] == board[8] == marker)
    d2 = (board[2] == board[4] == board[6] == marker)

    isTRUE = [r1,r2,r3,c1,c2,c3,d1,d2]

    for value in isTRUE:
        if value == True:
            return True
        else:
            pass
    return False

def is_board_full(board):
    i = 0
    for cell in board:
        if cell == 'X' or cell == 'O':
            i += 1

    if i == 9:
        return True

    return False

def is_tie(board,marker):
    if is_winner(board,marker) == False and is_board_full(board) == True:
        return True

    return False

def replay():
    answer = ''

    while answer not in ['Y','N','y','n']:
        answer = input('\nWould you like to play again? Please answer (Y)es or (N)o: ')

        if answer not in ['Y','N','y','n']:
            print('The value is not valid. Please choose Y or N.')

    return answer

def game():
    marker = player_selection()
    board = ['1','2','3','4','5','6','7','8','9']
    player = [1,2]
    i = 0

    print('\nThis is the board you are supposed to fill in with your preferences.')
    board_display()

    while not is_board_full(board):

        print('\nPlayer {p} has to choose one cell from the previous board.'.format(p = player[i]))
        pos = position_selection(board)

        board[pos] = marker[i]
        clear()
        board_display(board)


        if is_winner(board,marker[i]) == True:
            print('Player {p} wins.'.format(p = player[i]))
            return True

        elif is_tie(board,marker[i]) == True:
            print('There is a tie, nobody wins.')
            return True

        if i == 0:
            i = 1
        else:
            i = 0
