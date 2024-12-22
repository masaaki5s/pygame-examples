"""
三目並べ: 基本ロジック
"""
import random

EMPTY, X, O = 0, -1, 1
TIE = 2

def initial_board():
    board = [[EMPTY]*3 for _ in range(3)]
    return board

def print_board(board):
    symbol = {EMPTY:'.', X:'x', O:'o'}
    for row in board:
        for s in row:
            print(symbol[s], end=' ')
        print()
    print('--')

def empty_cells(board):
    ret = []
    for i in range(3):
        for j in range(3):
            if board[i][j] == EMPTY:
                ret.append((i, j))
    return ret

def check_bingo(board):
    for p in [O, X]:
        for i in range(3):
            if sum(board[i]) == p * 3:
                return p
        
        for j in range(3):
            col = [board[i][j] for i in range(3)]
            if sum(col) == p * 3:
                return p
        
        diag = [board[i][i] for i in range(3)]
        if sum(diag) == p * 3:
            return p
        
        diag = [board[i][2-i] for i in range(3)]
        if sum(diag) == p * 3:
            return p
    return 0

def check_winner(board):
    winner = check_bingo(board)
    if winner != 0:
        return winner
    if empty_cells(board) == []:
        return TIE
    return 0

def computer_move(board, player):
    for p in [player, -player]:
        for i in range(3):
            if sum(board[i]) == p * 2:
                j = board[i].index(0)
                return (i, j)            

        for j in range(3):
            s = [board[i][j] for i in range(3)]
            if sum(s) == p * 2:
                i = s.index(0)
                return (i, j)

        s = [board[i][i] for i in range(3)]
        if sum(s) == p * 2:
            i = s.index(0)
            return (i, i)

        s = [board[i][2-i] for i in range(3)]
        if sum(s) == p * 2:
            i = s.index(0)
            return (i, 2-i)

    moves = empty_cells(board)
    return random.choice(moves)

def human_move(board, player):
    while True:
        move = input('次の一手を入力してください: ')
        if len(move) == 2:
            i, j = int(move[0]) - 1, int(move[1]) - 1
            if board[i][j] == EMPTY:
                return (i, j)
            print('そこには打てません')
        else:
            print('11や32のように1から3の数字2つで入力してください')
            
def main():
    board = initial_board()
    computer = X
    human_player = O
    player = human_player

    while check_winner(board) == 0:
        print_board(board)

        if player == human_player:
            i, j = human_move(board, player)
        else:
            i, j = computer_move(board, player)

        board[i][j] = player

        if player == human_player:
            player = computer
        else:
            player = human_player

    print_board(board)
    winner = check_winner(board)
    if winner == human_player:
        print("あなたの勝ちです！")
    elif winner == computer:
        print("コンピューターの勝ちです！")
    else:
        print("引き分けです")

if __name__ == "__main__":
    main()