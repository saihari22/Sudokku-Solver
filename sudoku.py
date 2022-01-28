#!/usr/bin/env python
#coding:utf-8

"""
Each sudoku board is represented as a dictionary with string keys and
int values.
e.g. my_board['A1'] = 8
"""
import sys
import math
import time
import statistics

ROW = "ABCDEFGHI"
COL = "123456789"

def print_board(board):
    """Helper function to print board in a square."""
    print("-----------------")
    for i in ROW:
        row = ''
        for j in COL:
            row += (str(board[i + j]) + " ")
        print(row)


def board_to_string(board):
    """Helper function to convert board dictionary to string for writing."""
    ordered_vals = []
    for r in ROW:
        for c in COL:
            ordered_vals.append(str(board[r + c]))
    return ''.join(ordered_vals)


def backtracking(board):
    solved_board = board
    pending_values = []
    for i, j in board.items():
        if j == 0:
            pending_values.append(i)

    if len(pending_values) == 0:
        solved_board = board_to_string(board)
        return solved_board

    possible_values = {}
    for r in ROW:
        for c in COL:
            possible_values[r + c] = [i for i in range(1, 10)]
    for r in ROW:
        for c in COL:
            if board[r + c] == 0:
                pass
            else:
                item = board[r + c]
                possible_values = reducePossibleValues(possible_values,item,r, c )

    min_remain_value = {}
    for i in pending_values:
        min_remain_value[i] = len(possible_values[i])
    mrv_key = min(min_remain_value, key=min_remain_value.get)
    valueSet = possible_values[mrv_key]

    while len(valueSet) != 0:
        item = valueSet[0]
        valueSet.remove(item)
        if forwardCheck(possible_values, item, mrv_key):
            board[mrv_key] = item
            if backtracking(board) == False:
                board[mrv_key] = 0
            else:
                solved_board = board_to_string(board)
                return solved_board
    return False

def forwardCheck(possible_values, item, index):

    row,col = index[0],index[1]
    rowint = ROW.find(row)
    colint=int(col)
    for i in COL:
        if i != col:
            tempPossibleValue = possible_values[row + i]
            if len(tempPossibleValue) == 1:
                if tempPossibleValue[0] == item:
                    return False
        else:
            pass
    for i in ROW:
        if i != row:
            tempPossibleValue = possible_values[i + col]
            if len(tempPossibleValue) == 1:
                if tempPossibleValue[0] == item:
                    return False
        else:
            pass
    gridRow = math.floor(rowint / 3)
    gridCol = math.floor((colint - 1) / 3)
    for i in range(0,3):
        for j in range(0,3):
            rowindex, colindex = ROW[gridRow * 3 + i], COL[gridCol * 3 + j]
            if (rowindex != row or colindex != col):
                tempPossibleValue = possible_values[rowindex + colindex]
                if len(tempPossibleValue) == 1:
                    if tempPossibleValue[0] == item:
                        return False
            else:
                pass
    return True

def reducePossibleValues(possible_values, item, r, c):
    colint=int(c)
    for i in COL:
        valueSet = possible_values[r + i]
        if item in valueSet:
            valueSet.remove(item)
    for i in ROW:
        valueSet = possible_values[i + c]
        if item in valueSet:
            valueSet.remove(item)

    gridRow = math.floor(ROW.find(r)/ 3)
    gridCol = math.floor((colint - 1)/ 3)
    for i in range(0,3):
        for j in range(0,3):
            rowindex,colindex = ROW[gridRow * 3 + i], COL[gridCol * 3 + j]
            valueSet = possible_values[rowindex + colindex]
            if item in valueSet:
                valueSet.remove(item)
    possible_values[r + c] = [-1]
    return possible_values

if __name__ == '__main__':
    if len(sys.argv) > 1:

        # Running sudoku solver with one board $python3 sudoku.py <input_string>.
        print(sys.argv[1])
        # Parse boards to dict representation, scanning board L to R, Up to Down
        board = { ROW[r] + COL[c]: int(sys.argv[1][9*r+c])
                 for r in range(9) for c in range(9)}

        solved_board = backtracking(board)
        # Write board to file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")
        outfile.write(solved_board)
        outfile.write('\n')

    else:
        # Running sudoku solver for boards in sudokus_start.txt $python3 sudoku.py

        #  Read boards from source.
        src_filename = 'sudokus_start.txt'
        try:
            srcfile = open(src_filename, "r")
            sudoku_list = srcfile.read()
        except:
            print("Error reading the sudoku file %s" % src_filename)
            exit()

        # Setup output file
        out_filename = 'output.txt'
        outfile = open(out_filename, "w")

        # Solve each board using backtracking
        number_solved=0
        time_taken=[]

        for line in sudoku_list.split("\n"):
            start_time=time.time()
            if len(line) < 9:
                continue

            # Parse boards to dict representation, scanning board L to R, Up to Down
            board = { ROW[r] + COL[c]: int(line[9*r+c])
                     for r in range(9) for c in range(9)}

            # Print starting board.
            #print_board(board)

            # Solve with backtracking
            solved_board = backtracking(board)
            outfile.write(solved_board)
            outfile.write('\n')
            number_solved+=1
            end_time = time.time()
            time_taken.append(end_time-start_time)
            #print_board(board)
        '''print("Running Time Statistics")
        print("Number of boards: ",number_solved)
        print("Min Time: ", min(time_taken))
        print("Max Time: ", max(time_taken))
        print("Mean: ", statistics.mean(time_taken))
        print("Standard Deviation: ", statistics.stdev(time_taken))'''
        print("Finishing all boards in file.")