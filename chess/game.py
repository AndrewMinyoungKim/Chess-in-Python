import pygame
import gc

from .constants import *
from .board import Board
from .piece import Piece
from .special_moves import SpecialMoves
from .check import Check
from .debug import Debugger

class Game:
    def __init__(self, win):
        self.win = win
        self.state = []
        self._init(self.win, self.state)
        #stalemate if all pieces are gone except the two kings
        #all_pieces = dict(w_num_P = 8, w_num_N = 2, w_num_B = 2, w_num_R = 2, w_num_Q = 1, b_num_P = 8, b_num_N = 2, b_num_B = 2, b_num_R = 2, b_num_Q = 1)

    def _init(self, win, state):
        self.turn = WHITE
        self.board = Board()
        self.board.new_board(win, state)

        self.selected = False
        self.selected_x, self.selected_y = None, None

        self.available_moves = []

        # check for legal castles, promotions, en passants
        self.special_moves = SpecialMoves()

        self.white_castle = True
        self.black_castle = True
        self.white_kingside_castle = True
        self.white_queenside_castle = True
        self.black_kingside_castle = True
        self.black_queenside_castle = True

        # check for legal moves, any checks, and checkmates
        self.check = Check(state)

        self.debug = Debugger()

    def update(self):
        pygame.display.update()

    def check_promotion(self, row, col):
        if(self.state[row][col].name == 'P'):
            if(self.state[row][col].colour == BLACK and row == 0):
                self.special_moves.promotion(self.state, row, col)
            elif(self.state[row][col].colour == WHITE and row == 7):
                self.special_moves.promotion(self.state, row, col)

    def erase_coloured_boxes(self):
        #erase previously coloured boxes
        self.board.draw_selected_piece(self.selected_x, self.selected_y, self.win, GREY if (self.selected_x + self.selected_y) % 2 == 0 else GREEN, self.state)
        erase = True
        self.state[self.selected_x][self.selected_y].movement(erase, self.board, self.state, self.win)

    def display_available_moves(self):
        for i in range(len(self.available_moves)):
            if(self.state[self.available_moves[i][0]][self.available_moves[i][1]]):
                self.board.draw_selected_piece(self.available_moves[i][0], self.available_moves[i][1], self.win, ORANGE, self.state)
            else:
                self.board.draw_square(self.available_moves[i][0], self.available_moves[i][1], self.win, ORANGE)

    def select_piece(self, row, col):
        self.selected = True
        self.selected_x, self.selected_y = row, col
        self.board.draw_selected_piece(row, col, self.win, PURPLE, self.state)

        erase = False
        del(self.available_moves)
        self.available_moves = self.state[row][col].movement(erase, self.board, self.state, self.win)

    def perform_move(self, row, col, attack):
        #make the switch, delete the opponent piece in square if(attack == True)
        if(attack):
            taken_piece = self.state[row][col]
            self.state[row][col] = 0
            del(taken_piece)
            gc.collect()

        self.state[self.selected_x][self.selected_y], self.state[row][col] = self.state[row][col], self.state[self.selected_x][self.selected_y]
        self.state[row][col].row = row
        self.state[row][col].col = col
        self.state[row][col].calc_pos()
        self.board.draw_square(self.selected_x, self.selected_y, self.win, GREY if (self.selected_x + self.selected_y) % 2 == 0 else GREEN)
        self.board.draw_selected_piece(row, col, self.win, GREY if (row + col) % 2 == 0 else GREEN, self.state)
        return True

    def reset_selected_moves(self):
        #reset
        self.selected = False
        self.selected_x, self.selected_y = None, None
        self.available_moves.clear()

    def mouseclick(self, row, col):
        successful_turn = False

        # selecting a piece when one is not selected yet
        if(not self.selected and self.state[row][col]):

            # selecting a piece when it's your turn
            if(self.state[row][col].colour == self.turn):
                self.select_piece(row, col)
                #check for castle if king (and unmoved rook in clear rank) or check for en passant for pawn (need to memorize previous move, maybe use a variable to signify a pawn moved two squares)
                check_pin = self.check.check_pin(self.state, row, col, self.available_moves, self.turn)
                self.display_available_moves()
            
        # actions when a piece is already selected
        elif(self.selected):

            # moving to an empty space
            if(not self.state[row][col] and (row, col) in self.available_moves):
                self.erase_coloured_boxes()
                successful_turn = self.perform_move(row, col, False)
                self.check_promotion(row, col)
                check = self.check.check_check(self.state, self.turn)
                self.reset_selected_moves()

            # capturing another piece
            elif(self.state[row][col] and (row, col) in self.available_moves):
                self.erase_coloured_boxes()
                successful_turn = self.perform_move(row, col, True)
                self.check_promotion(row, col)
                check = self.check.check_check(self.state, self.turn)
                self.reset_selected_moves()

            # selecting another piece when one was already selected/clicking on another ally piece
            elif(self.state[row][col]):
                if(self.state[row][col].colour == self.turn):
                    self.erase_coloured_boxes()
                    self.select_piece(row, col)
                    check_pin = self.check.check_pin(self.state, row, col, self.available_moves, self.turn)
                    self.display_available_moves()

                else:
                    self.erase_coloured_boxes()
                    self.reset_selected_moves()

            else:
                self.erase_coloured_boxes()
                self.reset_selected_moves()

            if(successful_turn):
                if(self.turn == WHITE):
                    self.turn = BLACK
                    self.display_move(row, col)
                    print("Black's Turn")
                else:
                    self.turn = WHITE
                    self.display_move(row, col)
                    print("White's Turn")
    
    #display move that was made
    def display_move(self, row, col):
        # IMPORTANT NOTE: When reading, the file letter comes first and THEN the rank number (e.g. d4), so it reads as Column THEN Row
        if(self.state[row][col].name == 'P'):
            print("{}{}".format(FILE[col], row+1))
        else:
            print("{}{}{}".format(self.state[row][col].name, FILE[col], row+1))

            #need to implement rest of notation for checks, checkmates, captures, castles, etc.
            
            #need to check for if check occurs due to move