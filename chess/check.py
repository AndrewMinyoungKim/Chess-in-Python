import pygame

from .constants import *
from .board import Board
from .piece import Piece
from .debug import Debugger

#check for pins, no need to worry about skewers and forks, as it doesn't pin down another piece, just causes king to become protected

class Check:
    def __init__(self, state):
        self.check = None
        self.black_check, self.white_check = False, False
        self.__setup(state)
        
    def __setup(self, state):
        # black king then white king in array
        self.king = [state[7][4], state[0][4]]

        # in the pin, which direction takes you to your king!
        self.x_dir, self.y_dir = None, None # for dealing with leftover rook movements between current piece and king

        self.debug = Debugger()
        
    #return the tuple where the bishop or queen is, if there's no threat, return None
    def get_bishop_pin(self, state, row, col, turn, hue):
        # a diagonal relation to the king must require the same difference in rows and columns (diagonal relationship)
        if(abs(self.king[hue].row-row) != abs(self.king[hue].col-col)):
            return False

        # king is above 
        if(self.king[hue].row < row):
            # king is left of
            if(self.king[hue].col < col):
                # first check if there is another piece between currently chosen piece and their king
                dir_y, dir_x = -1, -1
                trav_row, trav_col = row+dir_y, col+dir_x

                while(trav_row >= 0 and trav_col >= 0 and not state[trav_row][trav_col]):
                    trav_row += dir_y
                    trav_col += dir_x

                if(trav_row >= 0 and trav_col >= 0):
                    if(trav_row != self.king[hue].row or trav_col != self.king[hue].col):
                        return False
                else:
                    return False

                # now check if it is pinned
                dir_y, dir_x = 1, 1
                trav_row, trav_col = row+dir_y, col+dir_x

                while(trav_row < 8 and trav_col < 8 and not state[trav_row][trav_col]):
                    trav_row += dir_y
                    trav_col += dir_x

                if(trav_row < 8 and trav_col < 8):
                    if(state[trav_row][trav_col].colour != turn):
                        if(state[trav_row][trav_col].name == 'Q' or state[trav_row][trav_col].name == 'B'):
                            self.y_dir, self.x_dir = -1, -1
                            return state[trav_row][trav_col]

                return False
                
            # king is right of
            elif(self.king[hue].col > col):
                # first check if there is another piece between currently chosen piece and their king
                dir_y, dir_x = -1, 1
                trav_row, trav_col = row+dir_y, col+dir_x

                while(trav_row >= 0 and trav_col < 8 and not state[trav_row][trav_col]):
                    trav_row += dir_y
                    trav_col += dir_x

                if(trav_row >= 0 and trav_col < 8):
                    if(trav_row != self.king[hue].row or trav_col != self.king[hue].col):
                        return False
                else:
                    return False

                # now check if it is pinned
                dir_y, dir_x = 1, -1
                trav_row, trav_col = row+dir_y, col+dir_x

                while(trav_row < 8 and trav_col >= 0 and not state[trav_row][trav_col]):
                    trav_row += dir_y
                    trav_col += dir_x

                if(trav_row < 8 and trav_col >= 0):
                    if(state[trav_row][trav_col].colour != turn):
                        if(state[trav_row][trav_col].name == 'Q' or state[trav_row][trav_col].name == 'B'):
                            self.y_dir, self.x_dir = -1, 1
                            return state[trav_row][trav_col]

                return False

        # king is below
        elif(self.king[hue].row > row):
            # king is left of
            if(self.king[hue].col < col):
                # first check if there is another piece between currently chosen piece and their king
                dir_y, dir_x = 1, -1
                trav_row, trav_col = row+dir_y, col+dir_x

                while(trav_row < 8 and trav_col >= 0 and not state[trav_row][trav_col]):
                    trav_row += dir_y
                    trav_col += dir_x

                if(trav_row < 8 and trav_col >= 0):
                    if(trav_row != self.king[hue].row or trav_col != self.king[hue].col):
                        return False
                else:
                    return False

                # now check if it is pinned
                dir_y, dir_x = -1, 1
                trav_row, trav_col = row+dir_y, col+dir_x

                while(trav_row >= 0 and trav_col < 8 and not state[trav_row][trav_col]):
                    trav_row += dir_y
                    trav_col += dir_x

                if(trav_row >= 0 and trav_col < 8):
                    if(state[trav_row][trav_col].colour != turn):
                        if(state[trav_row][trav_col].name == 'Q' or state[trav_row][trav_col].name == 'B'):
                            self.y_dir, self.x_dir = 1, -1
                            return state[trav_row][trav_col]

                return False

            # king is right of
            elif(self.king[hue].col > col):
                # first check if there is another piece between currently chosen piece and their king
                dir_y, dir_x = 1, 1
                trav_row, trav_col = row+dir_y, col+dir_x

                while(trav_row < 8 and trav_col < 8 and not state[trav_row][trav_col]):
                    trav_row += dir_y
                    trav_col += dir_x

                if(trav_row < 8 and trav_col < 8):
                    if(trav_row != self.king[hue].row or trav_col != self.king[hue].col):
                        return False
                else:
                    return False

                # now check if it is pinned
                dir_y, dir_x = -1, -1
                trav_row, trav_col = row+dir_y, col+dir_x

                while(trav_row >= 0 and trav_col >= 0 and not state[trav_row][trav_col]):
                    trav_row += dir_y
                    trav_col += dir_x

                if(trav_row >= 0 and trav_col >= 0):
                    if(state[trav_row][trav_col].colour != turn):
                        if(state[trav_row][trav_col].name == 'Q' or state[trav_row][trav_col].name == 'B'):
                            self.y_dir, self.x_dir = 1, 1
                            return state[trav_row][trav_col]

                return False

        return False

    #return the tuple where the rook or queen is, if there's no threat, return None
    def get_rook_pin(self, state, row, col, turn, hue):
        # for a straight queen or rook pin, the king needs to be in either the same column or row as the pinned piece
        if(self.king[hue].row != row and self.king[hue].col != col):
            return False

        # king in same column (file) as piece
        elif(self.king[hue].col == col):
            # check for pins with king below piece
            if(row < self.king[hue].row):
                # first check if there is another piece between currently chosen piece and their king
                direction = 1
                traverse_row = row + direction
                while(traverse_row < 8 and not state[traverse_row][col]):
                    traverse_row += direction

                if(traverse_row < 8):
                    if(traverse_row != self.king[hue].row):
                        return False
                else:
                    return False

                # now check if it is pinned
                direction = -1
                traverse_row = row + direction

                while(traverse_row >= 0 and not state[traverse_row][col]):
                    traverse_row += direction

                if(traverse_row >= 0):
                    if(state[traverse_row][col].colour != turn):
                        if(state[traverse_row][col].name == 'Q' or state[traverse_row][col].name == 'R'):
                            self.y_dir = 1
                            return state[traverse_row][col]

                return False

            # check for pins with king above piece
            elif(row > self.king[hue].row):
                # first check if there is another piece between currently chosen piece and their king
                direction = -1
                traverse_row = row + direction
                while(traverse_row >= 0 and not state[traverse_row][col]):
                    traverse_row += direction

                if(traverse_row >= 0):
                    if(traverse_row != self.king[hue].row):
                        return False
                else:
                    return False

                # now check if it is pinned
                direction = 1
                traverse_row = row + direction

                while(traverse_row < 8 and not state[traverse_row][col]):
                    traverse_row += direction

                if(traverse_row < 8):
                    if(state[traverse_row][col].colour != turn):
                        if(state[traverse_row][col].name == 'Q' or state[traverse_row][col].name == 'R'):
                            self.y_dir = -1
                            return state[traverse_row][col]

                return False

        # king in same row (rank) as piece
        elif(self.king[hue].row == row):
            # check for pins with king right of piece
            if(col < self.king[hue].col):
                # first check if there is another piece between currently chosen piece and their king
                direction = 1
                traverse_col = col + direction
                while(traverse_col < 8 and not state[row][traverse_col]):
                    traverse_col += direction

                if(traverse_col < 8):
                    if(traverse_col != self.king[hue].col):
                        return False
                else:
                    return False

                # now check if it is pinned
                direction = -1
                traverse_col = col + direction

                while(traverse_col >= 0 and not state[row][traverse_col]):
                    traverse_col += direction

                if(traverse_col >= 0):
                    if(state[row][traverse_col].colour != turn):
                        if(state[row][traverse_col].name == 'Q' or state[row][traverse_col].name == 'R'):
                            self.x_dir = 1
                            return state[row][traverse_col]

                return False
                
            # check for pins with king left of piece
            elif(col > self.king[hue].col):
                # first check if there is another piece between currently chosen piece and their king
                direction = -1
                traverse_col = col + direction
                while(traverse_col >= 0 and not state[row][traverse_col]):
                    traverse_col += direction

                if(traverse_col >= 0):
                    if(traverse_col != self.king[hue].col):
                        return False
                else:
                    return False

                # now check if it is pinned
                direction = 1
                traverse_col = col + direction

                while(traverse_col < 8 and not state[row][traverse_col]):
                    traverse_col += direction

                if(traverse_col < 8):
                    if(state[row][traverse_col].colour != turn):
                        if(state[row][traverse_col].name == 'Q' or state[row][traverse_col].name == 'R'):
                            self.x_dir = -1
                            return state[row][traverse_col]

                return False

        return False

    def get_diagonal_pin_movement(self, state, row, col, available_moves, threat):
        available_moves.clear()
        # squares between threat and piece
        trav_y = row - self.y_dir
        trav_x = col - self.x_dir
        while(not state[trav_y][trav_x]):
            available_moves.append((trav_y, trav_x))
            trav_y -= self.y_dir
            trav_x -= self.x_dir
        available_moves.append((trav_y, trav_x)) # add option to capture threat

        # squares between king and piece
        trav_y = row + self.y_dir
        trav_x = col + self.x_dir
        while(not state[trav_y][trav_x]):
            available_moves.append((trav_y, trav_x))
            trav_y += self.y_dir
            trav_x += self.x_dir

    def get_straight_pin_movement(self, state, row, col, available_moves, threat):
        # either of these variables should != None since this method is only called if there is a rook pin
        available_moves.clear()
        if(self.x_dir):
            # squares between threat and piece
            traverse_x = col - self.x_dir
            while(not state[row][traverse_x]):
                available_moves.append((row, traverse_x))
                traverse_x -= self.x_dir
            available_moves.append((row, traverse_x)) # add option to capture threat

            # squares between king and piece
            traverse_x = col + self.x_dir
            while(not state[row][traverse_x]):
                available_moves.append((row, traverse_x))
                traverse_x += self.x_dir

        elif(self.y_dir):
            # squares between threat and piece
            traverse_y = row - self.y_dir
            while(not state[traverse_y][col]):
                available_moves.append((traverse_y, col))
                traverse_y -= self.y_dir
            available_moves.append((traverse_y, col)) # add option to capture threat

            # squares between king and piece
            traverse_y = row + self.y_dir
            while(not state[traverse_y][col]):
                available_moves.append((traverse_y, col))
                traverse_y += self.y_dir

    # check for bishops coming diagonally, rooks coming straight, or queens from either way, no need to check knights and kings
    # NOTE: MUST CHECK FOR PAWNS, if horizontal, cannot move. If vertical/file pin, then can move upwards, but cannot capture anything. If diagonal pin, can only capture pin threat
    def check_pin(self, state, row, col, available_moves, turn):
        if(turn == self.king[1].colour): # WHITE
            hue = 1
            bishop_pin = self.get_bishop_pin(state, row, col, turn, hue)
            rook_pin = self.get_rook_pin(state, row, col, turn, hue)
        elif(turn == self.king[0].colour): # BLACK
            hue = 0
            bishop_pin = self.get_bishop_pin(state, row, col, turn, hue)
            rook_pin = self.get_rook_pin(state, row, col, turn, hue)

        # impossible to have two pins for one piece, either only straight or only diagonal for a pinned piece
        if(rook_pin):
            print(f"Pin: {FILE[rook_pin.col]}{rook_pin.row+1}")
            if(state[row][col].name == 'Q' or state[row][col].name == 'R'):
                self.get_straight_pin_movement(state, row, col, available_moves, rook_pin)
            elif(state[row][col].name == 'P'):
                if(self.y_dir):
                    for i in range(len(available_moves)):
                        if(available_moves[i][1] != self.king[hue].col):
                            available_moves.pop(i)
                else:
                    available_moves.clear()
            else:
                available_moves.clear()

        elif(bishop_pin):
            print(f"Pin: {FILE[bishop_pin.col]}{bishop_pin.row+1}")
            if(state[row][col].name == 'Q' or state[row][col].name == 'B'):
                self.get_diagonal_pin_movement(state, row, col, available_moves, bishop_pin)
            elif(state[row][col].name == 'P'):
                if((bishop_pin.row, bishop_pin.col) in available_moves):
                    available_moves.clear()
                    available_moves.append((bishop_pin.row, bishop_pin.col))
                else:
                    available_moves.clear()
            else:
                available_moves.clear()

        self.x_dir, self.y_dir = None, None

    # check if the move puts the king in check
    # returns the threat's position
    def _check_check(self, state, row, col, hue, runaway_king):
        # row and col are position of the opponent king

        # check for pawn attacks
        if(self.king[hue].colour != WHITE): # opponent king vs pawn
            pawn_dir = 1
        else:
            pawn_dir = -1

        if(row-pawn_dir >= 0 and row-pawn_dir < 8):
            if(col-pawn_dir >= 0 and col-pawn_dir < 8):
                if(state[row-pawn_dir][col-pawn_dir]):
                    if(state[row-pawn_dir][col-pawn_dir].name == 'P' and state[row-pawn_dir][col-pawn_dir].colour != self.king[hue].colour):
                        return (row-pawn_dir, col-pawn_dir)
            if(col+pawn_dir >= 0 and col+pawn_dir < 8):
                if(state[row-pawn_dir][col+pawn_dir]):
                    if(state[row-pawn_dir][col+pawn_dir].name == 'P' and state[row-pawn_dir][col+pawn_dir].colour != self.king[hue].colour):
                        return (row-pawn_dir, col+pawn_dir)
        
        # check vertical
        row_dir = -1
        trav_row = row+row_dir
        if(runaway_king and trav_row >= 0 and state[trav_row][col] == self.king[hue]):
            trav_row += row_dir # skip king's current spot
        while(trav_row >= 0 and not state[trav_row][col]):
            trav_row += row_dir
        if(trav_row >= 0):
            if(state[trav_row][col].colour != self.king[hue].colour and (state[trav_row][col].name == 'Q' or state[trav_row][col].name == 'R')):
                return (trav_row, col)
        row_dir = 1
        trav_row = row+row_dir
        if(runaway_king and trav_row < 8 and state[trav_row][col] == self.king[hue]):
            trav_row += row_dir # skip king's current spot
        while(trav_row < 8 and not state[trav_row][col]):
            trav_row += row_dir
        if(trav_row < 8):
            if(state[trav_row][col].colour != self.king[hue].colour and (state[trav_row][col].name == 'Q' or state[trav_row][col].name == 'R')):
                return (trav_row, col)

        # check horizontal
        col_dir = -1
        trav_col = col+col_dir
        if(runaway_king and trav_col >= 0 and state[row][trav_col] == self.king[hue]):
            trav_col += col_dir # skip king's current spot
        while(trav_col >= 0 and not state[row][trav_col]):
            trav_col += col_dir
        if(trav_col >= 0):
            if(state[row][trav_col].colour != self.king[hue].colour and (state[row][trav_col].name == 'Q' or state[row][trav_col].name == 'R')):
                return (row, trav_col)
        col_dir = 1
        trav_col = col+col_dir
        if(runaway_king and trav_col < 8 and state[row][trav_col] == self.king[hue]):
            trav_col += col_dir # skip king's current spot
        while(trav_col < 8 and not state[row][trav_col]):
            trav_col += col_dir
        if(trav_col < 8):
            if(state[row][trav_col].colour != self.king[hue].colour and (state[row][trav_col].name == 'Q' or state[row][trav_col].name == 'R')):
                return (row, trav_col)

        # check diagonals
        row_dir, col_dir = -1, -1
        trav_row, trav_col = row+row_dir, col+col_dir
        if(runaway_king and trav_row >= 0 and trav_col >= 0 and state[trav_row][trav_col] == self.king[hue]): # skip king's current spot
            trav_row += row_dir
            trav_col += col_dir
        while(trav_row >= 0 and trav_col >= 0 and not state[trav_row][trav_col]):
            trav_row += row_dir
            trav_col += col_dir
        if(trav_row >= 0 and trav_col >= 0):
            if(state[trav_row][trav_col].colour != self.king[hue].colour and (state[trav_row][trav_col].name == 'Q' or state[trav_row][trav_col].name == 'B')):
                return (trav_row, trav_col)
        row_dir, col_dir = 1, -1
        trav_row, trav_col = row+row_dir, col+col_dir
        if(runaway_king and trav_row < 8 and trav_col >= 0 and state[trav_row][trav_col] == self.king[hue]): # skip king's current spot
            trav_row += row_dir
            trav_col += col_dir
        while(trav_row < 8 and trav_col >= 0 and not state[trav_row][trav_col]):
            trav_row += row_dir
            trav_col += col_dir
        if(trav_row < 8 and trav_col >= 0):
            if(state[trav_row][trav_col].colour != self.king[hue].colour and (state[trav_row][trav_col].name == 'Q' or state[trav_row][trav_col].name == 'B')):
                return (trav_row, trav_col)
        row_dir, col_dir = -1, 1
        trav_row, trav_col = row+row_dir, col+col_dir
        if(runaway_king and trav_row >= 0 and trav_col < 8 and state[trav_row][trav_col] == self.king[hue]): # skip king's current spot
            trav_row += row_dir
            trav_col += col_dir
        while(trav_row >= 0 and trav_col < 8 and not state[trav_row][trav_col]):
            trav_row += row_dir
            trav_col += col_dir
        if(trav_row >= 0 and trav_col < 8):
            if(state[trav_row][trav_col].colour != self.king[hue].colour and (state[trav_row][trav_col].name == 'Q' or state[trav_row][trav_col].name == 'B')):
                return (trav_row, trav_col)
        row_dir, col_dir = 1, 1
        trav_row, trav_col = row+row_dir, col+col_dir
        if(runaway_king and trav_row < 8 and trav_col < 8 and state[trav_row][trav_col] == self.king[hue]): # skip king's current spot
            trav_row += row_dir
            trav_col += col_dir
        while(trav_row < 8 and trav_col < 8 and not state[trav_row][trav_col]):
            trav_row += row_dir
            trav_col += col_dir
        if(trav_row < 8 and trav_col < 8):
            if(state[trav_row][trav_col].colour != self.king[hue].colour and (state[trav_row][trav_col].name == 'Q' or state[trav_row][trav_col].name == 'B')):
                return (trav_row, trav_col)

        # check for knights
        x = row-2
        y = col-1
        if(x >= 0 and x < 8 and y >= 0 and y < 8 and state[x][y] and state[x][y].name == 'N' and state[x][y].colour != self.king[hue].colour):
            return (x, y)
        x = row-2
        y = col+1
        if(x >= 0 and x < 8 and y >= 0 and y < 8 and state[x][y] and state[x][y].name == 'N' and state[x][y].colour != self.king[hue].colour):
            return (x, y)
        x = row+2
        y = col-1
        if(x >= 0 and x < 8 and y >= 0 and y < 8 and state[x][y] and state[x][y].name == 'N' and state[x][y].colour != self.king[hue].colour):
            return (x, y)
        x = row+2
        y = col+1
        if(x >= 0 and x < 8 and y >= 0 and y < 8 and state[x][y] and state[x][y].name == 'N' and state[x][y].colour != self.king[hue].colour):
            return (x, y)
        x = row-1
        y = col-2
        if(x >= 0 and x < 8 and y >= 0 and y < 8 and state[x][y] and state[x][y].name == 'N' and state[x][y].colour != self.king[hue].colour):
            return (x, y)
        x = row-1
        y = col+2
        if(x >= 0 and x < 8 and y >= 0 and y < 8 and state[x][y] and state[x][y].name == 'N' and state[x][y].colour != self.king[hue].colour):
            return (x, y)
        x = row+1
        y = col-2
        if(x >= 0 and x < 8 and y >= 0 and y < 8 and state[x][y] and state[x][y].name == 'N' and state[x][y].colour != self.king[hue].colour):
            return (x, y)
        x = row+1
        y = col+2
        if(x >= 0 and x < 8 and y >= 0 and y < 8 and state[x][y] and state[x][y].name == 'N' and state[x][y].colour != self.king[hue].colour):
            return (x, y)

        return None

    # check for king's legal moves, remove any moves
    def check_legal_king(self, state, turn, available_moves):
        if(self.king[0].colour == turn):
            hue = 0
        else:
            hue = 1

        row, col = self.king[hue].row, self.king[hue].col
        colour = self.king[hue].colour

        runaway_king = True

        # remove any move that causes a check (checking the kings possibilities clockwise order)
        if(row-1 >= 0 and col-1 >= 0 and not (state[row-1][col-1] and state[row-1][col-1].colour == colour)): #NW
            if(self._check_check(state, row-1, col-1, hue, runaway_king) and (row-1, col-1) in available_moves):
                available_moves.remove((row-1, col-1))
        if(row-1 >= 0 and not (state[row-1][col] and state[row-1][col].colour == colour)): # N
            if(self._check_check(state, row-1, col, hue, runaway_king) and (row-1, col) in available_moves):
                available_moves.remove((row-1, col))
        if(row-1 >= 0 and col+1 < 8 and not (state[row-1][col+1] and state[row-1][col+1].colour == colour)): # NE
            if(self._check_check(state, row-1, col+1, hue, runaway_king) and (row-1, col+1) in available_moves):
                available_moves.remove((row-1, col+1))
        if(col+1 < 8 and not (state[row][col+1] and state[row][col+1].colour == colour)): # E
            if(self._check_check(state, row, col+1, hue, runaway_king) and (row, col+1) in available_moves):
                available_moves.remove((row, col+1))
        if(row+1 < 8 and col+1 < 8 and not (state[row+1][col+1] and state[row+1][col+1].colour == colour)): # SE
            if(self._check_check(state, row+1, col+1, hue, runaway_king) and (row+1, col+1) in available_moves):
                available_moves.remove((row+1, col+1))
        if(row+1 < 8 and not (state[row+1][col] and state[row+1][col].colour == colour)): # S
            if(self._check_check(state, row+1, col, hue, runaway_king) and (row+1, col) in available_moves):
                available_moves.remove((row+1, col))
        if(row+1 < 8 and col-1 >= 0 and not (state[row+1][col-1] and state[row+1][col-1].colour == colour)): # SW
            if(self._check_check(state, row+1, col-1, hue, runaway_king) and (row+1, col-1) in available_moves):
                available_moves.remove((row+1, col-1))
        if(col-1 >= 0 and not (state[row][col-1] and state[row][col-1].colour == colour)): # W
            if(self._check_check(state, row, col-1, hue, runaway_king) and (row, col-1) in available_moves):
                available_moves.remove((row, col-1))

        self.opponent_king_threat(state, available_moves)
        
    # neither king can come inside the other king's circle
    def opponent_king_threat(self, state, available_moves):
        white_king_circle = set()
        black_king_circle = set()
        self.get_opponent_king_circle(white_king_circle, 1)
        self.get_opponent_king_circle(black_king_circle, 0)
        shared_circle = white_king_circle.intersection(black_king_circle)
        common_squares = list(shared_circle)
        
        for i in range(len(common_squares)):
           if((common_squares[i][0], common_squares[i][1]) in available_moves):
               available_moves.remove((common_squares[i][0], common_squares[i][1]))

    def get_opponent_king_circle(self, circle, hue):
        row, col = self.king[hue].row, self.king[hue].col
        if(row-1 >= 0):
            circle.add((row-1, col))
            if(col-1 >= 0):
                circle.add((row-1, col-1))
            if(col+1 < 8):
                circle.add((row-1, col+1))
        if(row+1 < 8):
            circle.add((row+1, col))
            if(col-1 >= 0):
                circle.add((row+1, col-1))
            if(col+1 < 8):
                circle.add((row+1, col+1))
        if(col-1 >= 0):
            circle.add((row, col-1))
        if(col+1 < 8):
            circle.add((row, col+1))

    # need to check if your moved piece OR any other piece that was blocked by the moved piece is able to take the king
    def check_check(self, state, turn):
        if(turn == self.king[1].colour): # WHITE PIECE
            hue = 0 # BLACK KING
        else: # BLACK PIECE
            hue = 1 # WHITE KING
        
        self.check = self._check_check(state, self.king[hue].row, self.king[hue].col, hue, False)
        if(self.check):
            if(self.king[hue].colour == WHITE):
                self.white_check = True
            if(self.king[hue].colour == BLACK):
                self.black_check = True
        
    # need to check if the king can move elsewhere, if a piece can block, or if the opponent piece can be taken
    def save_king(self, state, row, col, available_moves, turn):
        if(turn == WHITE):
            hue = 1
        else:
            hue = 0

        # if you move the king elsewhere, out of check
        if(state[row][col].name == 'K'):
            self.check_legal_king(state, turn, available_moves)
        
        # block with piece or capture threat
        else:
            bishop_pin = self.get_bishop_pin(state, row, col, turn, hue)
            rook_pin = self.get_rook_pin(state, row, col, turn, hue)
            if(not (bishop_pin and rook_pin)):
                threat = self._check_check(state, self.king[hue].row, self.king[hue].col, hue, False) # this time, from king's perspective, see who's attacking you
                # only called if in check already, thus, threat will not equal None
                if(state[threat[0]][threat[1]].name != 'N' and state[threat[0]][threat[1]].name != 'P'): # cannot block if the threat is a knight, must capture it or move king. If it's a pawn, you can't really block
                    if(len(available_moves) > 0):
                        i = 0
                        fully_traversed = False
                        while(not fully_traversed):
                            diag_save = self.get_bishop_pin(state, available_moves[i][0], available_moves[i][1], turn, hue)
                            straight_save = self.get_rook_pin(state, available_moves[i][0], available_moves[i][1], turn, hue)
                            if((not (diag_save or straight_save)) and ((available_moves[i][0], available_moves[i][1]) != (threat[0], threat[1]))):
                                available_moves.pop(i)
                            else:
                                i += 1
                            
                            if(i == len(available_moves)):
                                fully_traversed = True
                else:
                    if((threat[0],threat[1]) in available_moves):
                        available_moves.clear()
                        available_moves.append((threat[0],threat[1]))
                    else:
                        available_moves.clear()
            
            else:
                available_moves.clear()

    def king_saved(self, turn):
        if(turn == WHITE):
            self.white_check = False
        else:
            self.black_check = False

    def check_checkmate(self, state, turn, pieces_left, board, win):
        piece_count = 0
        save_possible = False
        for i in range(ROW):
            for j in range(COL):
                if(state[i][j] and state[i][j].colour == turn):
                    piece_count += 1
                    available_moves = state[i][j].movement(False, board, state, win)
                    self.save_king(state, i, j, available_moves, turn)
                    if(len(available_moves) > 0):
                        save_possible = True
                        break
                    if(piece_count >= pieces_left):
                        break
        
        if(not save_possible):
            if(self.check):
                return "Checkmate"
            else:
                return "Stalemate"
        
        return None