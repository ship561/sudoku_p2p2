from flask import Flask, render_template, url_for, request, redirect, flash, session
import numpy as np

app = Flask(__name__)

@app.route("/")
@app.route("/sudoku")
def sudoku():
    return render_template("sudoku.html")

@app.route('/sudoku_solve', methods=['POST'])
@app.route('/solve', methods=['POST'])
def sudoku_solve():
    data = request.form
    board = transform_data(data)
    if isValidSudoku(board):
        solved_board = solveSudoku(board)
        return render_template('sudoku_solve.html', solved_board=solved_board)
    else:
        # flash('Invalid Sudoku')
        return redirect(url_for('sudoku'))

def transform_data(data):
    output = ''
    for val in data.values():
        if val == '':
            output += '.'
        elif int(val) in range(1, 10):
            output += val
    output = list(output)
    result = np.reshape(output,(9, 9))
    return result

def solveSudoku(board):
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

def isValidSudoku(board):
    def is_valid_row(board):
        for row in board:
            if not is_valid(row):
                return False
        return True

    def is_valid_column(board):
        for col in zip(*board):
            if not is_valid(col):
                return False
        return True

    def is_valid_square(board):
        for i in (0,3,6):
            for j in (0,3,6):
                square = [board[x][y] for x in range(i,i+3)
                                        for y in range(j,j+3)]
                if not is_valid(square):
                    return False
        return True

    def is_valid(value):
        res = [i for i in value if i != '.']
        return len(res) == len(set(res))

    return is_valid_row(board) and is_valid_column(board) and is_valid_square(board)
if __name__ == "__main__":
    app.run(debug=True)