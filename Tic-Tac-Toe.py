import random
import sys

def index(location):
    '''
                     7 | 8 | 9                  0 | 1 | 2
                     - - - - -                  - - - - -
    maps location :  4 | 5 | 6  onto indices :  3 | 4 | 5
                     - - - - -                  - - - - -
                     1 | 2 | 3                  6 | 7 | 8

    :param location: Location
    :return: index in array
    '''
    if location == 7 or location == 4 or location == 1:
        return 7 - location
    elif location == 8 or location == 5 or location == 2:
        return 9 - location
    elif location == 9 or location == 6 or location == 3:
        return 11 - location


def location(index):
    '''
                     7 | 8 | 9                  0 | 1 | 2
                     - - - - -                  - - - - -
    gets location :  4 | 5 | 6  from indices :  3 | 4 | 5
                     - - - - -                  - - - - -
                     1 | 2 | 3                  6 | 7 | 8

    :param index: index in array
    :return: location
    '''
    if index == 0 or index == 3 or index == 6:
        return 7 - index
    elif index == 1 or index == 4 or index == 7:
        return 9 - index
    elif index == 2 or index == 5 or index == 8:
        return 11 - index


def print_board(board):
    '''
    Prints the current board configuration
    :param board: Data structure representing the board
    :return: Nil
    '''
    print("Current board configuration : ")
    print(board[0] + "|" + board[1] + "|" + board[2])
    print(board[3] + "|" + board[4] + "|" + board[5])
    print(board[6] + "|" + board[7] + "|" + board[8])


def check_for_win(board, player, computer):
    '''
    Checks if there is a win/ loss/ draw
    :param board: board configuration
    :param player: player's character (X/O)
    :param computer: computer's character (O/X)
    :return: returns if the game is over or on
    '''
    # 'win_configs' list is used to the winning configurations - 8 of them
    win_configs = ([1, 5, 9], [3, 5, 7], [1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9])
    game_over = False
    for config in win_configs:
        a = board[index(config[0])]
        b = board[index(config[1])]
        c = board[index(config[2])]
        if a == b and b == c:
            if a == player:
                print ("You win! I accept defeat!")
                game_over = True
                break
            elif a == computer:
                print ("You lose!")
                game_over = True
                break
        else:
            empty_spaces = 9
            for i in range(9):
                if board[i] != " " and board[i] != "_":
                    empty_spaces -= 1
            if empty_spaces == 0:
                print ("A draw!")
                game_over = True
                break
    print_board(board)
    return game_over


def heuristic(board, player, computer):
    '''
    Computes heuristic value for the empty squares and selects the one with maximum value

    |-------------------------------------------------------------------------------------------------|
    |                                           HEURISTIC                                             |
    |-------------------------------------------------------------------------------------------------|
    | Value of each empty square equals sum of the points (mentioned below) for its win paths         |
    | 1. Empty: [ | | ] - 1 point                                                                     |
    | 2. One symbol: [X| | ] - 10 points // can be any symbol in any place                            |
    | 3. Two different symbols: [X|O| ] - 0 points // they can be arranged in any possible way        |
    | 4. Two identical player's symbols: say [X|X| ] - 100 points // arranged in any of three ways    |
    | 5. Two identical computer's symbols: say [O|O| ] - 1000 points // arranged in any of three ways |
    |-------------------------------------------------------------------------------------------------|

    :param board: board configuration
    :param player: player's character (X/O)
    :param computer: computer's character (O/X)
    :return: location corresponding to maximum heuristic value(for computer's next turn)
    '''
    win_configs = ([1, 5, 9], [3, 5, 7], [1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9])
    empty_squares = []
    for i in range(9):
        if board[i] == ' ' or board[i] == '_':
            empty_squares.append(i)

    max_h_value = 0
    max_h_location = 0
    for i in empty_squares:
        current = location(i)
        h = 0
        for x in win_configs:
            if x.count(current) == 1:
                if (board[index(x[0])] == ' ' or board[index(x[0])] == '_') and \
                        (board[index(x[1])] == ' ' or board[index(x[1])] == '_') and \
                        (board[index(x[2])] == ' ' or board[index(x[2])] == '_'):
                    h += 1
                elif (board[index(x[0])] == player and
                      (board[index(x[1])] == ' ' or board[index(x[1])] == '_') and
                      (board[index(x[2])] == ' ' or board[index(x[2])] == '_')) or \
                     (board[index(x[1])] == player and
                      (board[index(x[2])] == ' ' or board[index(x[2])] == '_') and
                      (board[index(x[0])] == ' ' or board[index(x[0])] == '_')) or \
                     (board[index(x[2])] == player and
                      (board[index(x[0])] == ' ' or board[index(x[0])] == '_') and
                      (board[index(x[1])] == ' ' or board[index(x[1])] == '_')) or \
                     (board[index(x[0])] == computer and
                      (board[index(x[1])] == ' ' or board[index(x[1])] == '_') and
                      (board[index(x[2])] == ' ' or board[index(x[2])] == '_')) or \
                     (board[index(x[1])] == computer and
                      (board[index(x[2])] == ' ' or board[index(x[2])] == '_') and
                      (board[index(x[0])] == ' ' or board[index(x[0])] == '_')) or \
                     (board[index(x[2])] == computer and
                      (board[index(x[0])] == ' ' or board[index(x[0])] == '_') and
                      (board[index(x[1])] == ' ' or board[index(x[1])] == '_')):
                    h += 10
                elif (board[index(x[0])] == player and board[index(x[1])] == computer and
                      (board[index(x[2])] == ' ' or board[index(x[2])] == '_')) or \
                        (board[index(x[0])] == computer and board[index(x[1])] == player and
                         (board[index(x[2])] == ' ' or board[index(x[2])] == '_')) or \
                        (board[index(x[1])] == player and board[index(x[2])] == computer and
                         (board[index(x[0])] == ' ' or board[index(x[0])] == '_')) or \
                        (board[index(x[1])] == computer and board[index(x[2])] == player and
                         (board[index(x[0])] == ' ' or board[index(x[0])] == '_')) or \
                        (board[index(x[2])] == player and board[index(x[0])] == computer and
                         (board[index(x[1])] == ' ' or board[index(x[1])] == '_')) or \
                        (board[index(x[2])] == computer and board[index(x[0])] == player and
                         (board[index(x[1])] == ' ' or board[index(x[1])] == '_')):
                    h += 0
                elif (board[index(x[0])] == player and board[index(x[1])] == player and
                      (board[index(x[2])] == ' ' or board[index(x[2])] == '_')) or \
                     (board[index(x[1])] == player and board[index(x[2])] == player and
                      (board[index(x[0])] == ' ' or board[index(x[0])] == '_')) or \
                    (board[index(x[2])] == player and board[index(x[0])] == player and
                     (board[index(x[1])] == ' ' or board[index(x[1])] == '_')):
                    h += 100
                elif (board[index(x[0])] == computer and board[index(x[1])] == computer and
                      (board[index(x[2])] == ' ' or board[index(x[2])] == '_')) or \
                     (board[index(x[1])] == computer and board[index(x[2])] == computer and
                      (board[index(x[0])] == ' ' or board[index(x[0])] == '_')) or \
                     (board[index(x[2])] == computer and board[index(x[0])] == computer and
                      (board[index(x[1])] == ' ' or board[index(x[1])] == '_')):
                    h += 1000
        if h > max_h_value:
            max_h_value = h
            max_h_location = current
    return max_h_location


def player_turn(board, player):
    '''
    Initiates a player's turn and updates the board configuration accordingly
    :param board: board configuration
    :param player: player's character (X/O)
    :return: Nil
    '''
    choice = input("Your move : ")
    if choice.isdigit() == False:
        print("Enter an integer. Try again!")
        player_turn(board, player)
    if int(choice) > 9 or int(choice) < 1:
        print("Enter a number from 1 to 9. Try again!")
        player_turn(board, player)
    if board[index(int(choice))] == 'X' or board[index(int(choice))] == 'O':
        print("That's already taken! Try again!")
        player_turn(board, player)
    else:
        board[index(int(choice))] = player


def computer_turn(board, player, computer):
    '''
    Initiates the computer's turn and updates the board configuration accordingly
    :param board: board configuration
    :param player: player's character (X/O)
    :param computer: computer's character (O/X)
    :return: Nil
    '''
    move = heuristic(board, player, computer)
    board[index(move)] = computer


def tic_tac_toe(board, player, computer):
    '''
    Alternates the turns b/w the player and the computer until the game is over
    :param board: board configuration
    :param player: player's character (X/O)
    :param computer: computer's character (O/X)
    :return: True if game is over
             False if game is still on
    '''
    game_over = False
    turn = 1
    while not game_over:
        if turn % 2:
            player_turn(board, player)
        else:
            computer_turn(board, player, computer)
        turn += 1
        game_over = check_for_win(board, player, computer)


def main():
    print("Welcome to Tic Tac Toe!")
    print("The board is set up like a numeric keypad :")
    print("7|8|9")
    print("4|5|6")
    print("1|2|3")

    player = ''
    computer = ''

    flag = False
    while(not flag):
        player = input("Which character do you want? X/O : ")
        if player == 'X' or player == 'x':
            player = 'X'
            computer = 'O'
            flag = True
        elif player == 'O' or player == 'o':
            player = 'O'
            computer = 'X'
            flag = True
        else:
            print("Invalid choice. Try again!")
            flag = False

    board = ["_", "_", "_", "_", "_", "_", " ", " ", " "]
    print_board(board)
    tic_tac_toe(board, player, computer)

if __name__ == '__main__':
    main()


# # Alternative AI turn algo. (without heuristics)
# # ----------------------------------------------
# moved = False
#
# # The first turn of the computer :
# #   If the player has chosen the centre square ==> Choose a random corner
# #   Otherwise, choose the centre square
# if turn == 2:
#     if board[4] != player:
#         board[4] = computer
#         moved = True
#     else:
#         moved = pick_corner(board, computer)
# else:
#     # Possibility of a win in the next step
#     win_configs = ([1, 5, 9], [3, 5, 7], [1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 4, 7], [2, 5, 8], [3, 6, 9])
#
#     # Computer has a chance of winning
#     for x in win_configs:
#         if board[index(x[1])] == computer and board[index(x[2])] == computer \
#                 and board[index(x[0])] != player:
#             board[index(x[0])] = computer
#             moved = True
#             break
#         if board[index(x[2])] == computer and board[index(x[0])] == computer \
#                 and board[index(x[1])] != player:
#             board[index(x[1])] = computer
#             moved = True
#             break
#         if board[index(x[0])] == computer and board[index(x[1])] == computer \
#                 and board[index(x[2])] != player:
#             board[index(x[2])] = computer
#             moved = True
#             break
#
#     # Player has a chance of winning ==> Thwart his plan
#     for x in win_configs:
#         if board[index(x[1])] == player and board[index(x[2])] == player \
#                 and board[index(x[0])] != computer:
#             board[index(x[0])] = computer
#             moved = True
#             break
#         if board[index(x[0])] == player and board[index(x[2])] == player \
#                 and board[index(x[1])] != computer:
#             board[index(x[1])] = computer
#             moved = True
#             break
#         if board[index(x[0])] == player and board[index(x[1])] == player \
#                 and board[index(x[2])] != computer:
#             board[index(x[2])] = computer
#             moved = True
#             break
# # else decide b/w sides and corners
