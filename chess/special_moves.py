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

    def check_castle(self, state, colour):
        if(colour == BLACK and not self.black_castle):
            return self.black_castle
        elif(colour == WHITE and not self.white_castle):
            return self.white_castle

    def promotion(self, state, row, col):
        valid_promotion = False
        promotion_options = ['Q', 'R', 'B', 'N']
        promotion_input = input(f"Enter what piece you'd like your pawn on {FILE[col]}{row+1} to promote to: Queen (Q), Rook (R), Bishop (B) or Knight (N)?")
        while(not valid_promotion):
            if(promotion_input not in promotion_options):
                promotion_input = input("Please enter a letter in the parantheses: Queen (Q), Rook (R), Bishop (B) or Knight (N)")
            else:
                valid_promotion = True

    def enpassant_chance(self, state, row, col):
        self.en_passant = True
        self.en_passant_piece = state[row][col]

    def remove_enpassant(self):
        self.en_passant = False
        self.en_passant_piece = None