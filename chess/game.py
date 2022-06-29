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
                self.state[row][col].name = self.special_moves.promotion(row, col)
                self.board.draw_selected_piece(row, col, self.win, GREY if (row + col) % 2 == 0 else GREEN, self.state)
            elif(self.state[row][col].colour == WHITE and row == 7):
                self.state[row][col].name = self.special_moves.promotion(row, col)
                self.board.draw_selected_piece(row, col, self.win, GREY if (row + col) % 2 == 0 else GREEN, self.state)

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
        if(self.special_moves.white_castle and self.turn == WHITE and self.state[self.selected_x][self.selected_y].name == 'K'):
            if((0, 6) in self.available_moves):
                self.board.draw_square(0, 6, self.win, GREY if 6 % 2 == 0 else GREEN)
            if((0, 2) in self.available_moves):
                self.board.draw_square(0, 2, self.win, GREY if 2 % 2 == 0 else GREEN)
        if(self.special_moves.black_castle and self.turn == BLACK and self.state[self.selected_x][self.selected_y].name == 'K'):
            if((7, 6) in self.available_moves):
                self.board.draw_square(7, 6, self.win, GREY if (7+6) % 2 == 0 else GREEN)
            if((7, 2) in self.available_moves):
                self.board.draw_square(7, 2, self.win, GREY if (7+2) % 2 == 0 else GREEN)

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

    def switch_places(self, old_row, old_col, new_row, new_col):
        self.state[old_row][old_col], self.state[new_row][new_col] = self.state[new_row][new_col], self.state[old_row][old_col]
        self.state[new_row][new_col].row = new_row
        self.state[new_row][new_col].col = new_col
        self.state[new_row][new_col].calc_pos()
        self.board.draw_square(old_row, old_col, self.win, GREY if (old_row + old_col) % 2 == 0 else GREEN)
        self.board.draw_selected_piece(new_row, new_col, self.win, GREY if (new_row + new_col) % 2 == 0 else GREEN, self.state)

    def take_piece(self, row, col):
        taken_piece = self.state[row][col]
        self.state[row][col] = 0
        del(taken_piece)
        gc.collect()

    def perform_move(self, row, col, attack):
        #make the switch, delete the opponent piece in square if(attack == True)
        if(attack):
            self.take_piece(row, col)
        
        # disables en_passant next turn after en passant is enabled
        if(self.special_moves.en_passant):
            if((row, col) == (self.special_moves.row_en_passant, self.special_moves.col_en_passant) and self.state[self.selected_x][self.selected_y].name == 'P' and self.state[self.selected_x][self.selected_y].colour == self.turn):
                if(self.turn == WHITE):
                    en_passant_victim_row = self.special_moves.row_en_passant - 1 # == 4
                else:
                    en_passant_victim_row = self.special_moves.row_en_passant + 1 # == 3
                self.take_piece(en_passant_victim_row, col)
                self.board.draw_square(en_passant_victim_row, col, self.win, GREY if (en_passant_victim_row + col) % 2 == 0 else GREEN)
                    
            self.special_moves.en_passant = False
            self.special_moves.row_en_passant, self.special_moves.col_en_passant = None, None

        # enables en passant chance if pawn moves up two squares
        if(self.state[self.selected_x][self.selected_y].name == 'P' and abs(row-self.selected_x) == 2):
            self.special_moves.en_passant = True
            self.special_moves.col_en_passant = col
            if(self.turn == WHITE):
                self.special_moves.row_en_passant = row - 1 # == 2
            else:
                self.special_moves.row_en_passant = row + 1 # == 5

        # castle
        if(self.state[self.selected_x][self.selected_y].name == 'K' and abs(self.selected_y-col) > 1):
            # all row values will be the same in a castle
            if(col == 2):
                rook_start_col = 0
                rook_new_col = 3
            elif(col == 6):
                rook_start_col = 7
                rook_new_col = 5

            self.switch_places(row, rook_start_col, row, rook_new_col)

        self.switch_places(self.selected_x, self.selected_y, row, col)
        return True

    def reset_selected_moves(self):
        self.selected = False
        self.selected_x, self.selected_y = None, None
        self.available_moves.clear()

    def move_select(self, row, col):
        self.select_piece(row, col)

        if(self.special_moves.en_passant and self.state[row][col].name == 'P'):
            if(self.turn == WHITE):
                en_passant_row = self.special_moves.row_en_passant - 1 # == 4
            else:
                en_passant_row = self.special_moves.row_en_passant + 1 # == 3
            if(row == en_passant_row and abs(col-self.special_moves.col_en_passant) == 1):
                self.available_moves.append((self.special_moves.row_en_passant,self.special_moves.col_en_passant))
        
        if(self.state[row][col].name != 'K'):
            self.check.check_pin(self.state, row, col, self.available_moves, self.turn)
        elif(not self.check.check):
            self.check.check_legal_king(self.state, self.turn, self.available_moves)
            self.special_moves.check_castle(self.state, self.turn, self.check, self.available_moves)
        
        if(self.check.check):
            self.check.save_king(self.state, row, col, self.available_moves, self.turn)

        self.display_available_moves()

    def process_move(self, row, col, attack):
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

        # check for lost ability to castle
        # black castles
        if(self.special_moves.black_castle and self.turn == BLACK and (self.state[row][col].name == 'K' or self.state[row][col].name == 'R')):
            if(self.state[row][col].name == 'K'):
                self.special_moves.black_castle = False
                self.special_moves.black_kingside_castle, self.special_moves.black_queenside_castle = False, False
            else:
                if(self.selected_y == 0):
                    self.special_moves.black_queenside_castle = False
                else:
                    self.special_moves.black_kingside_castle = False

                if(not (self.special_moves.black_queenside_castle and self.special_moves.black_kingside_castle)):
                    self.special_moves.black_castle = False
        # white castles
        elif(self.special_moves.white_castle and self.turn == WHITE and (self.state[row][col].name == 'K' or self.state[row][col].name == 'R')):
            if(self.state[row][col].name == 'K'):
                self.special_moves.white_castle = False
                self.special_moves.white_kingside_castle, self.special_moves.white_queenside_castle = False, False
            else:
                if(self.selected_y == 0):
                    self.special_moves.white_queenside_castle = False
                else:
                    self.special_moves.white_kingside_castle = False

                if(not (self.special_moves.white_queenside_castle and self.special_moves.white_kingside_castle)):
                    self.special_moves.white_castle = False

        # lost castle ability due to rook taken
        if(self.special_moves.black_castle and row == 7 and (col == 0 or col == 7) and self.state[row][col].colour != BLACK):
            if(col == 0):
                self.special_moves.black_queenside_castle = False
            else:
                self.special_moves.black_kingside_castle = False
            
            if(not self.special_moves.black_queenside_castle and not self.special_moves.black_kingside_castle):
                self.special_moves.black_castle = False

        if(self.special_moves.white_castle and row == 0 and (col == 0 or col == 7) and self.state[row][col].colour != WHITE):
            if(col == 0):
                self.special_moves.white_queenside_castle = False
            else:
                self.special_moves.white_kingside_castle = False
            
            if(not self.special_moves.white_queenside_castle and not self.special_moves.white_kingside_castle):
                self.special_moves.white_castle = False
        
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
                successful_turn = self.process_move(row, col, False) # attack := False

            # capturing another piece
            elif(self.state[row][col] and (row, col) in self.available_moves):
                successful_turn = self.process_move(row, col, True) # attack := True
                
                # decrement number of pieces on the board for captured side
                if(self.turn == WHITE):
                    self.num_black_pieces -= 1
                elif(self.turn == BLACK):
                    self.num_white_pieces -= 1
                
                # stalemate from only 2 kings on the board
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

                    # if no moves available for player, check if any move available anywhere, if not, checkmate or stalemate
                    self._detect_checkmate()

                else:
                    self.turn = WHITE
                    self.display_move(row, col)
                    #print("White's Turn")

                    # if no moves available for player, check if any move available anywhere, if not, checkmate or stalemate
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
        if(self.turn == WHITE):
            result = self.check.check_checkmate(self.state, self.turn, self.num_white_pieces, self.board, self.win)
        else:
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
            self.board.draw_selected_piece(self.check.king[0].row, self.check.king[0].col, self.win, BROWN, self.state)
            self.board.draw_selected_piece(self.check.king[1].row, self.check.king[1].col, self.win, BROWN, self.state)
            print("You're all losers!")

        else:
            print("Shrek Error")

        game_over = True