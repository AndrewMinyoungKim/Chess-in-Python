from unittest import result
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
        self.num_black_pieces, self.num_white_pieces = 16, 16

    def _init(self, win, state):
        self.turn = WHITE
        self.board = Board()
        self.board.new_board(win, state)

        self.selected = False
        self.selected_x, self.selected_y = None, None

        self.available_moves = []

        # check for legal castles, promotions, en passants
        self.special_moves = SpecialMoves()

        # check for legal moves, any checks, and checkmates
        self.check = Check(state)

        self.checkmate, self.stalemate = False, False

        self.debug = Debugger()

    def update(self):
        pygame.display.update()

    def check_promotion(self, row, col):
        if(self.state[row][col].name == 'P'):
            if(self.state[row][col].colour == BLACK and row == 0):
                self.special_moves.promotion(self.state, row, col)
            elif(self.state[row][col].colour == WHITE and row == 7):
                self.special_moves.promotion(self.state, row, col)

    def colour_king_in_check(self, colour):
        if(self.check.black_check):
            hue = 0
        else:
            hue = 1
        self.board.draw_selected_piece(self.check.king[hue].row, self.check.king[hue].col, self.win, colour, self.state)

    def erase_coloured_boxes(self):
        #erase previously coloured boxes
        self.board.draw_selected_piece(self.selected_x, self.selected_y, self.win, GREY if (self.selected_x + self.selected_y) % 2 == 0 else GREEN, self.state)
        erase = True
        self.state[self.selected_x][self.selected_y].movement(erase, self.board, self.state, self.win) # erase := True requires Python 3.8 or newer
        if(self.check.check):
            self.colour_king_in_check(RED)

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
        self.available_moves = self.state[row][col].movement(erase, self.board, self.state, self.win) # erase := False requires Python 3.8 or newer

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
        self.selected = False
        self.selected_x, self.selected_y = None, None
        self.available_moves.clear()

    def move_select(self, row, col):
        self.select_piece(row, col)
        #check for castle if king (and unmoved rook in clear rank) or check for en passant for pawn (need to memorize previous move, maybe use a variable to signify a pawn moved two squares)
        if(self.state[row][col].name != 'K'):
            self.check.check_pin(self.state, row, col, self.available_moves, self.turn)
        elif(not self.check.check):
            self.check.check_legal_king(self.state, self.turn, self.available_moves)
        
        if(self.check.check):
            self.check.save_king(self.state, row, col, self.available_moves, self.turn)

        self.display_available_moves()

    def perform_move_select(self, row, col, attack):
        self.erase_coloured_boxes()
        successful_turn = self.perform_move(row, col, attack)
        self.check_promotion(row, col)

        # recover from being in check
        if((self.turn == WHITE and self.check.white_check) or (self.turn == BLACK and self.check.black_check)):
            self.recover_from_check()

        # check for checks
        self.check.check_check(self.state, self.turn)
        if(self.check.check):
            print("CHECK!")
            self.colour_king_in_check(RED)

        self.reset_selected_moves()
        return successful_turn

    def mouseclick(self, row, col):
        successful_turn = False

        # selecting a piece when one is not selected yet
        if(not self.selected and self.state[row][col]):

            # selecting a piece when it's your turn
            if(self.state[row][col].colour == self.turn):
                self.move_select(row, col)
            
        # actions when a piece is already selected
        elif(self.selected):

            # moving to an empty space
            if(not self.state[row][col] and (row, col) in self.available_moves):
                successful_turn = self.perform_move_select(row, col, False) # attack := False

            # capturing another piece
            elif(self.state[row][col] and (row, col) in self.available_moves):
                successful_turn = self.perform_move_select(row, col, True) # attack := True
                
                if(self.turn == WHITE):
                    self.num_black_pieces -= 1
                elif(self.turn == BLACK):
                    self.num_white_pieces -= 1
                
                if(self.num_black_pieces == 1 and self.num_white_pieces == 1):
                    self.stalemate = True
                    self.__game_over()

            # selecting another piece when one was already selected/clicking on another ally piece
            elif(self.state[row][col]):
                if(self.state[row][col].colour == self.turn):
                    self.erase_coloured_boxes()
                    self.move_select(row, col)

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
                    #print("Black's Turn")

                    # if no moves available for player, check if any move available anywhere
                    if(self.check.check):
                        self._detect_checkmate()

                else:
                    self.turn = WHITE
                    self.display_move(row, col)
                    #print("White's Turn")

                    # if no moves available for player, check if any move available anywhere, if not, checkmate or stalemate
                    if(self.check.check):
                        self._detect_checkmate()

        return (self.checkmate or self.stalemate)
    
    #display move that was made
    def display_move(self, row, col):
        # IMPORTANT NOTE: When reading, the file letter comes first and THEN the rank number (e.g. d4), so it reads as Column THEN Row
        if(self.state[row][col].name == 'P'):
            print("{}{}".format(FILE[col], row+1))
        else:
            print("{}{}{}".format(self.state[row][col].name, FILE[col], row+1))

            #need to implement rest of notation for checks, checkmates, captures, castles, etc.
            
            #need to check for if check occurs due to move

    def recover_from_check(self):
        if(self.check.white_check): hue = 1
        else: hue = 0
        self.colour_king_in_check(GREY if (self.check.king[hue].row + self.check.king[hue].col) % 2 == 0 else GREEN)
        self.check.king_saved(self.turn)

    def _detect_checkmate(self):
        result = self.check.check_checkmate(self.state, self.turn, self.num_black_pieces, self.board, self.win)
        if(result):
            if(result == "Checkmate"):
                self.checkmate = True
                self.__game_over()
            elif(result == "Stalemate"):
                self.stalemate = True
                self.__game_over()

    def __game_over(self):
        if(self.checkmate):
            self.colour_king_in_check(BROWN)
            print("CHECKMATE")
            if(self.turn != WHITE): # the turn was switched before calling function, used for finding any possible moves
                winner = "White"
                hue = 1
            else:
                winner = "Black"
                hue = 0
            self.board.draw_selected_piece(self.check.king[hue].row, self.check.king[hue].col, self.win, GOLD, self.state)
            print(f"Winner!: {winner}")
        
        elif(self.stalemate):
            print("STALEMATE")
            print("You're all losers!")

        else:
            print("Shrek Error")

        game_over = True