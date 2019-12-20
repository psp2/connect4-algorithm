import sys
import random
import signal
from random import randint

def sigint_handler(signum, frame):
    sys.exit(0)


def necessary_move(board: list, board_size: int, cur_player: int) -> int:
    for col in range(board_size):
        if board[0][col] != 0:
            continue
        row = 1
        while row < board_size:
            if row == board_size-1 and board[row][col] == 0:
                break
            elif board[row][col] != 0:
                row -= 1
                break
            row += 1
        board[row][col] = cur_player
        win = validate_win(cur_player, board, board_size, row, col)
        board[row][col] = 0
        if win:
            return col
    return -1


def minimax(board: list, board_size: int) -> int:
    return 0


def order_cols_by_height(board: list, board_size: int) -> int:
    col_heights = [0] * board_size
    for col in range(board_size):
        height = board_size
        for row in range(board_size):
            if board[row][col] != 0:
                break
            height -= 1
        col_heights[col] = height
    return col_heights


def pick_col_by_height(board: list, board_size: int) -> int:
    ordered_cols = order_cols_by_height(board, board_size)
    while True:
        if len(ordered_cols) == 1:
            return ordered_cols[0]
        # min_option = ordered_cols.index(min(ordered_cols))
        # max_option = ordered_cols.index(max(ordered_cols))
        # selected_col = random.choice([min_option, min_option, max_option])
        # if selected_col > 0 and selected_col < board_size-1:
        #     selected_col = randint(selected_col-1, selected_col+1)
        min_height = min(ordered_cols)
        max_height = max(ordered_cols)
        options = [col for col, height in enumerate(ordered_cols) if (height == min_height or height == max_height)]
        selected_col = random.choice(options)
        # if selected_col > 0 and selected_col < board_size-1:
        #     selected_col = randint(selected_col-1, selected_col+1)

        if board[0][selected_col] != 0:
            ordered_cols.pop(selected_col)
            continue

        #Verify that the semi-randomized selections won't cause a loss
        row = 1
        while row < board_size:
            if row == board_size-1 and board[row][selected_col] == 0:
                break
            elif board[row][selected_col] != 0:
                row -= 1
                break
            row += 1
        board[row][selected_col] = 2
        win = False
        if row != 0:
            row -= 1
            board[row][selected_col] = 1
            win = validate_win(1, board, board_size, row, selected_col)
            board[row][selected_col] = 0
            board[row+1][selected_col] = 0
        else:
            board[row][selected_col] = 0
        if win:
            continue
        # if board[0][selected_col] != 0:
        #     continue
        else:
            return selected_col


def choose_column(board: list, board_size: int) -> int:
    """
    Selects column for AI Player.

    First checks for immediate opportunities (wins) or vulnerabilities (losses).
    If neither of the above are present, uses the minimax algorithm.
    """
    # First check for immediate opportunities or vulnerabilities for AI
    opportunity = necessary_move(board, board_size, 2)
    if opportunity != -1:
        return opportunity
    # Note that opportunities are 1st priority.
    # This is because you could stop 1 vulnerability but still have more undetected. But if you win first via 'opportunity,' this is irrelevant.
    vulnerability = necessary_move(board, board_size, 1)
    if vulnerability != -1:
        return vulnerability

    # If neither of the above are present, use minimax algorithm
    # return minimax(board, board_size)

    # Temporary Selection Process; Remove Later
    return pick_col_by_height(board, board_size)



def validate_win(player: int, board: list, board_size: int, row: int, col: int) -> bool:
    """
    Validate whether the current player has "connected 4" after his or her latest move.

    Check 4 directions total, relative to the latest piece.
    1) Vertical (up-down)
    2) Horizontal (left-right)
    3) Diagonal 1 (Top Left to Bottom Right)
    4) Diagonal 2 (Top Right to Bottom Left)
    """
    # Vertical
    count = 0
    cur_row = row
    while cur_row >= 0:
        if board[cur_row][col] != player:
            break
        count += 1
        cur_row -= 1
    cur_row = row+1
    while cur_row < board_size:
        if board[cur_row][col] != player:
            break
        count += 1
        cur_row += 1
    if count > 3:
        return True

    # Horizontal
    count = 0
    cur_col = col
    while cur_col >= 0:
        if board[row][cur_col] != player:
            break
        count += 1
        cur_col -= 1
    cur_col = col+1
    while cur_col < board_size:
        if board[row][cur_col] != player:
            break
        count += 1
        cur_col += 1
    if count > 3:
        return True

    # Diagonal 1
    count = 0
    cur_row = row
    cur_col = col
    while cur_col >= 0 and cur_row >= 0:
        if board[cur_row][cur_col] != player:
            break
        count += 1
        cur_row -= 1
        cur_col -= 1
    cur_row = row+1
    cur_col = col+1
    while cur_col < board_size and cur_row < board_size:
        if board[cur_row][cur_col] != player:
            break
        count += 1
        cur_row += 1
        cur_col += 1
    if count > 3:
        return True

    # Diagonal 2
    count = 0
    cur_row = row
    cur_col = col
    while cur_col < board_size and cur_row >= 0:
        if board[cur_row][cur_col] != player:
            break
        count += 1
        cur_row -= 1
        cur_col += 1
    cur_row = row+1
    cur_col = col-1
    while cur_col >= 0 and cur_row < board_size:
        if board[cur_row][cur_col] != player:
            break
        count += 1
        cur_row += 1
        cur_col -= 1
    if count > 3:
        return True

    # If no winning sequence found, return False
    return False


def play_game(board_size: int, num_players: int) -> int:
    if num_players == 1:
        print('You are Player 1. The CPU is Player 2.')
    cur_player = 1
    board = [[0]*board_size for row in range(board_size)]
    while True:
        print(*board, sep='\n')
        if cur_player == 2 and num_players == 1:
            print('CPU')
            selected_col = choose_column(board, board_size)
            print('CPU selects column: ' + str(selected_col+1))
        else:
            print('Player ' + str(cur_player))
            while True:
                try:
                    selected_col = int(input('Select a column from 1 to ' + str(board_size) + ': ')) - 1
                except ValueError:
                    print('Invalid Input')
                    continue
                if selected_col < 0 or selected_col >= board_size:
                    print('Invalid Column Selection')
                    continue
                elif board[0][selected_col] != 0:
                    print('Selected Column is Full. Choose a different one.')
                    continue
                else:
                    break
        # Iterate through a column, replace the lowest possible 0 (default) with the Player's token
        row = 1
        while row < board_size:
            if row == board_size-1 and board[row][selected_col] == 0:
                board[row][selected_col] = cur_player
                break
            elif board[row][selected_col] != 0:
                row -= 1
                board[row][selected_col] = cur_player
                break
            row += 1
        # Validate whether the current player has won
        if validate_win(cur_player, board, board_size, row, selected_col):
            print(*board, sep='\n')
            return cur_player
        # Validate whether the game can continue (if all are non-zero in the top row, the game ends in a tie)
        if all(board[0]):
            print(*board, sep='\n')
            return 0
        # Switch players
        cur_player = 2 if cur_player == 1 else 1


def run_game():
    signal.signal(signal.SIGINT, sigint_handler)
    # Decide if you want to play against an AI or another human
    print('Select Number of Players\nChoose 1 to play an AI, and choose 2 to play a friend.')
    while True:
        try:
            num_players = int(input('Number of Players (1 or 2): '))
        except ValueError:
            print('Invalid Input')
            continue
        if num_players is 1 or num_players is 2:
            break
        else:
            print('Invalid Number of Players')
    # Select board size
    while True:
        try:
            board_size = int(input('Select a board length from 6 to 10: '))
        except ValueError:
            print('Invalid Input')
            continue
        if board_size > 5 and board_size < 11:
            break
        else:
            print('Invalid Board Size')
    # Play Game with 1 or 2 players
    winner = play_game(board_size, num_players)
    # Results
    if winner == 1:
        print('Player 1 has Won.')
    elif winner == 2 and num_players == 1:
        print('The Computer has Won.')
    elif winner == 2 and num_players == 2:
        print('Player 2 has Won.')
    else:
        print('Game ends in Tie.')


if __name__ == '__main__':
    while True:
        run_game()
        while True:
            try:
                play_again = input('Play Again? Type Y for Yes, N for No. ')
            except ValueError:
                print('Invalid Input.')
                continue
            if play_again == 'Y':
                break
            elif play_again == 'N':
                sys.exit(0)
            else:
                print('Please enter Y or N.')
