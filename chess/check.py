import pygame

from .constants import *
from .board import Board
from .piece import Piece
from .debug import Debugger

#check for pins, no need to worry about skewers and forks, as it doesn't pin down another piece, just causes king to become protected

class Check:
    def __init__(self, state):
        self.checkmate = False
        self.check = False
        self.winner = None
        self.__setup(state)
        
    def __setup(self, state):
        #self.white_king, self.black_king = state[0][4], state[7][4]
        # black king then white king in array
        self.king = [state[7][4], state[0][4]]

        # in the pin, which direction takes you to your king!
        self.x_dir, self.y_dir = None, None # for dealing with leftover rook movements between current piece and king

        self.debug = Debugger()
        
    #return the tuple where the bishop or queen is, if there's no threat, return None
    def get_bishop_pin(self, state, row, col, available_moves, turn, hue):
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
    def get_rook_pin(self, state, row, col, available_moves, turn, hue):
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
        # # attempt to use sets and intersections to calculate moves in between threat and piece
        # # problem: two queens beside each other share many other moves that don't block their kings
        # threat_moves_line = threat.rook_movement(False, board, state, win)
        # threat_set = set(threat_moves_line)
        # avail_set = set(available_moves)
        # # get intersection of both sets of moves and convert back to list (giving you what's available to move for pinned piece)
        # move_set = avail_set.intersection(threat_set)
        # available_moves = list(move_set)
        # # add additional moves outside intersection between current piece and king

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
            bishop_pin = self.get_bishop_pin(state, row, col, available_moves, turn, hue)
            rook_pin = self.get_rook_pin(state, row, col, available_moves, turn, hue)
        elif(turn == self.king[0].colour): # BLACK
            hue = 0
            bishop_pin = self.get_bishop_pin(state, row, col, available_moves, turn, hue)
            rook_pin = self.get_rook_pin(state, row, col, available_moves, turn, hue)

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

    # check if the move puts the king in check (what about somewhere the king cannot go???)
    def check_legal(self, state, turn, hue):
        # check for pawn attacks
        row, col = self.king[hue].row, self.king[hue].col # opponent king
        if(turn == WHITE):
            pawn_dir = 1
        else:
            pawn_dir = -1

        if(row-pawn_dir >= 0 and row-pawn_dir < 8):
            if(col-pawn_dir >= 0 and row-pawn_dir < 8):
                if(state[row-pawn_dir][col-pawn_dir]):
                    if(state[row-pawn_dir][col-pawn_dir].name == 'P' and state[row-pawn_dir][col-pawn_dir].colour != self.king[hue].colour):
                        return True
            if(col+pawn_dir >= 0 and row-pawn_dir < 8):
                if(state[row-pawn_dir][col+pawn_dir]):
                    if(state[row-pawn_dir][col+pawn_dir].name == 'P' and state[row-pawn_dir][col+pawn_dir].colour != self.king[hue].colour):
                        return True
        
        # check horizontal
        row_dir = -1
        trav_row = row+row_dir
        while(trav_row >= 0 and not state[trav_row][col]):
            trav_row += row_dir
        if(trav_row >= 0):
            if(state[trav_row][col].colour != self.king[hue].colour and (state[trav_row][col].name == 'Q' or state[trav_row][col].name == 'R')):
                return True
        row_dir = 1
        trav_row = row+row_dir
        while(trav_row < 8 and not state[trav_row][col]):
            trav_row += row_dir
        if(trav_row < 8):
            if(state[trav_row][col].colour != self.king[hue].colour and (state[trav_row][col].name == 'Q' or state[trav_row][col].name == 'R')):
                return True

        # check vertical
        col_dir = -1
        trav_col = col+col_dir
        while(trav_col >= 0 and not state[row][trav_col]):
            trav_col += col_dir
        if(trav_col >= 0):
            if(state[row][trav_col].colour != self.king[hue].colour and (state[row][trav_col].name == 'Q' or state[row][trav_col].name == 'R')):
                return True
        col_dir = 1
        trav_col = col+col_dir
        while(trav_col < 8 and not state[row][trav_col]):
            trav_col += col_dir
        if(trav_col < 8):
            if(state[row][trav_col].colour != self.king[hue].colour and (state[row][trav_col].name == 'Q' or state[row][trav_col].name == 'R')):
                return True

        # check diagonals
        row_dir, col_dir = -1, -1
        trav_row, trav_col = row+row_dir, col+col_dir
        while(trav_row >= 0 and trav_col >= 0 and not state[trav_row][trav_col]):
            trav_row += row_dir
            trav_col += col_dir
        if(trav_row >= 0 and trav_col >= 0):
            if(state[trav_row][trav_col].colour != self.king[hue].colour and (state[trav_row][trav_col].name == 'Q' or state[trav_row][trav_col].name == 'B')):
                return True
        row_dir, col_dir = 1, -1
        trav_row, trav_col = row+row_dir, col+col_dir
        while(trav_row < 8 and trav_col >= 0 and not state[trav_row][trav_col]):
            trav_row += row_dir
            trav_col += col_dir
        if(trav_row < 8 and trav_col >= 0):
            if(state[trav_row][trav_col].colour != self.king[hue].colour and (state[trav_row][trav_col].name == 'Q' or state[trav_row][trav_col].name == 'B')):
                return True
        row_dir, col_dir = -1, 1
        trav_row, trav_col = row+row_dir, col+col_dir
        while(trav_row >= 0 and trav_col < 8 and not state[trav_row][trav_col]):
            trav_row += row_dir
            trav_col += col_dir
        if(trav_row >= 0 and trav_col < 8):
            if(state[trav_row][trav_col].colour != self.king[hue].colour and (state[trav_row][trav_col].name == 'Q' or state[trav_row][trav_col].name == 'B')):
                return True
        row_dir, col_dir = 1, 1
        trav_row, trav_col = row+row_dir, col+col_dir
        while(trav_row < 8 and trav_col < 8 and not state[trav_row][trav_col]):
            trav_row += row_dir
            trav_col += col_dir
        if(trav_row < 8 and trav_col < 8):
            if(state[trav_row][trav_col].colour != self.king[hue].colour and (state[trav_row][trav_col].name == 'Q' or state[trav_row][trav_col].name == 'B')):
                return True

        # check for knights
        x = row-2
        y = col-1
        if(x >= 0 and x < 8 and y >= 0 and y < 8 and state[x][y] and state[x][y].name == 'N' and state[x][y].colour != self.king[hue].colour):
            return True
        x = row-2
        y = col+1
        if(x >= 0 and x < 8 and y >= 0 and y < 8 and state[x][y] and state[x][y].name == 'N' and state[x][y].colour != self.king[hue].colour):
            return True
        x = row+2
        y = col-1
        if(x >= 0 and x < 8 and y >= 0 and y < 8 and state[x][y] and state[x][y].name == 'N' and state[x][y].colour != self.king[hue].colour):
            return True
        x = row+2
        y = col+1
        if(x >= 0 and x < 8 and y >= 0 and y < 8 and state[x][y] and state[x][y].name == 'N' and state[x][y].colour != self.king[hue].colour):
            return True
        x = row-1
        y = col-2
        if(x >= 0 and x < 8 and y >= 0 and y < 8 and state[x][y] and state[x][y].name == 'N' and state[x][y].colour != self.king[hue].colour):
            return True
        x = row-1
        y = col+2
        if(x >= 0 and x < 8 and y >= 0 and y < 8 and state[x][y] and state[x][y].name == 'N' and state[x][y].colour != self.king[hue].colour):
            return True
        x = row+1
        y = col-2
        if(x >= 0 and x < 8 and y >= 0 and y < 8 and state[x][y] and state[x][y].name == 'N' and state[x][y].colour != self.king[hue].colour):
            return True
        x = row+1
        y = col+2
        if(x >= 0 and x < 8 and y >= 0 and y < 8 and state[x][y] and state[x][y].name == 'N' and state[x][y].colour != self.king[hue].colour):
            return True

        return False

    def check_check(self, state, turn):
        if(turn == self.king[1].colour): # WHITE PIECE
            hue = 0 # BLACK KING
        else: # BLACK PIECE
            hue = 1 # WHITE KING
        
        self.check = self.check_legal(state, turn, hue)
        if(self.check):
            print("CHECK!")
        # call this function in Game when a piece is moved (successful_turn)
        # the move puts the opponent's king in check, this should be called after playing
        # need to check if your moved piece OR any other piece that was blocked by the moved piece is able to take the king (must check every piece on the board)
        # need to check if the king can move elsewhere, if a piece can block, or if the opponent piece can be taken

    def check_checkmate(self, state):
        pass #call from check_check to check if there is a checkmate, if the king can move elsewhere, if a piece can block, or if the opponent piece can be taken
        
    def check_stalemate(self, state):
        pass # need to check for stalemates