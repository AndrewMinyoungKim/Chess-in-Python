import pygame

from .constants import *
from .board import Board
from .piece import Piece

class SpecialMoves:
    def __init__(self):
        self.black_castle = True
        self.white_castle = True
        self.white_kingside_castle = True
        self.white_queenside_castle = True
        self.black_kingside_castle = True
        self.black_queenside_castle = True

        self.en_passant = False
        self.row_en_passant, self.col_en_passant = None, None
        self.en_passant_piece = None

        self.repetition = False

    def check_castle(self, state, colour, check, available_moves):
        if(colour == BLACK and not self.black_castle):
            return self.black_castle
        elif(colour == WHITE and not self.white_castle):
            return self.white_castle

        if(colour == BLACK):
            hue = 0
            if(self.black_kingside_castle):
                if(not state[7][5] and not state[7][6]):
                    square_1, square_2 = check.check_for_check(state, 7, 5, hue, False), check.check_for_check(state, 7, 6, hue, False)
                    if(not square_1 and not square_2):
                        available_moves.append((7, 6))
            if(self.black_queenside_castle):
                if(not state[7][1] and not state[7][2] and not state[7][3]):
                    square_1, square_2 = check.check_for_check(state, 7, 2, hue, False), check.check_for_check(state, 7, 3, hue, False)
                    if(not square_1 and not square_2):
                        available_moves.append((7, 2))
        elif(colour == WHITE):
            hue = 1
            if(self.white_kingside_castle):
                if(not state[0][5] and not state[0][6]):
                    square_1, square_2 = check.check_for_check(state, 0, 5, hue, False), check.check_for_check(state, 0, 6, hue, False)
                    if(not square_1 and not square_2):
                        available_moves.append((0, 6))
            if(self.white_queenside_castle):
                if(not state[0][1] and not state[0][2] and not state[0][3]):
                    square_1, square_2 = check.check_for_check(state, 0, 2, hue, False), check.check_for_check(state, 0, 3, hue, False)
                    if(not square_1 and not square_2):
                        available_moves.append((0, 2))

    def promotion(self, row, col):
        valid_promotion = False
        promotion_options = ['Q', 'R', 'B', 'N']
        promotion_input = input(f"Enter what piece you'd like your pawn on {FILE[col]}{row+1} to promote to: Queen (Q), Rook (R), Bishop (B) or Knight (N)?: ")
        while(not valid_promotion):
            if(promotion_input.upper() in promotion_options):
                valid_promotion = True
                return promotion_input.upper()
            else:
                promotion_input = input("Please enter a letter in the parantheses: Queen (Q), Rook (R), Bishop (B) or Knight (N): ")

    def enpassant_chance(self, state, row, col):
        self.en_passant = True
        self.en_passant_piece = state[row][col]

    def remove_enpassant(self):
        self.en_passant = False
        self.en_passant_piece = None