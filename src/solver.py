from functools import wraps
import errno
import os
import signal

class TimeoutError(Exception):
    pass

def timeout(seconds=10, error_message=os.strerror(errno.ETIME)):
    def decorator(func):
        def _handle_timeout(signum, frame):
            raise TimeoutError(error_message)

        def wrapper(*args, **kwargs):
            signal.signal(signal.SIGALRM, _handle_timeout)
            signal.alarm(seconds)
            try:
                result = func(*args, **kwargs)
            finally:
                signal.alarm(0)
            return result

        return wraps(func)(wrapper)

    return decorator

@timeout(10, os.strerror(errno.ETIMEDOUT))
def solveSudoku(board):
    """
    Do not return anything, modify board in-place instead.
    """

    def checkrow(num, r, board):
        for i in range(9):
            if board[r][i] == num:
                return False
        return True

    def checkcolumn(num, c, board):
        for i in range(9):
            if board[i][c] == num:
                return False
        return True

    def checkbox(num, r, c, board):
        for i in range(r // 3 * 3, r // 3 * 3 + 3):
            for j in range(c // 3 * 3, c // 3 * 3 + 3):
                if board[i][j] == num:
                    return False
        return True

    def isValid(num, r, c, board):
        if checkrow(num, r, board) and checkcolumn(num, c, board) and checkbox(num, r, c, board):
            return True
        else:
            return False

    def getCandidate(board):
        for i in range(9):
            for j in range(9):
                if board[i][j] == '.':
                    return i, j
        return -1, -1

    def solve(board):
        r, c = getCandidate(board)
        if r == -1 and c == -1:
            return True
        for num in ['1', '2', '3', '4', '5', '6', '7', '8', '9']:
            if isValid(num, r, c, board):
                board[r][c] = num
                if solve(board):
                    return True
                board[r][c] = '.'

        return False

    solve(board)
    return board

board = [["5","5",".",".","7",".",".",".","."],
         ["6",".",".","1","9","5",".",".","."],
         [".","9","8",".",".",".",".","6","."],
         ["8",".",".",".","6",".",".",".","3"],
         ["4",".",".","8",".","3",".",".","1"],
         ["7",".",".",".","2",".",".",".","6"],
         [".","6",".",".",".",".","2","8","."],
         [".",".",".","4","1","9",".",".","5"],
         [".",".",".",".","8",".",".","7","9"]]

board = [["5","5",".",".",".",".",".",".","."],
         [".",".",".",".",".",".",".",".","."],
         [".",".",".",".",".",".",".",".","."],
         [".",".",".",".",".",".",".",".","."],
         [".",".",".",".",".",".",".",".","."],
         [".",".",".",".",".",".",".",".","."],
         [".",".",".",".",".",".",".",".","."],
         [".",".",".",".",".",".",".",".","."],
         [".",".",".",".",".",".",".",".","."]]

print(solveSudoku(board))
