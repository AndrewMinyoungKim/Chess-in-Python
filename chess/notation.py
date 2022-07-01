import pygame
from .constants import *

class Notation:
    def __init__(self):
        # dict of move types
        self.moves = {"move": False, "capture": False, "queenside-castle": False,"kingside-castle": False, "check": False, "stalemate": False, "checkmate": False}
        
        # sound effect: new game
        pygame.mixer.init()
        pygame.mixer.Channel(1).play(pygame.mixer.Sound('assets/new game.wav'))

        # other variables
        self.old_row, self.old_col = None, None
        self.en_passant = False
        self.pawn_promotion = None
        self.winner = None

        # maybe in the future, take account for disambiguating moves? e.g. both rooks on same rank. one moves to a square on same rank?

    #display move that was made
    def display_move(self, state, row, col, colour):
        # IMPORTANT NOTE: When reading, the file letter comes first and THEN the rank number (e.g. d4), so it reads as Column THEN Row
        if(self.moves["checkmate"]):
            if(self.moves["move"]):
                if(state[row][col].name == 'P'):
                    print(f"{colour}: {FILE[col]}{row+1}#")
                else:
                    if(self.pawn_promotion):
                        print(f"{colour}: {FILE[col]}{row+1}={self.pawn_promotion}#")
                    else:
                        print(f"{colour}: {state[row][col].name}{FILE[col]}{row+1}#")
            elif(self.moves["capture"]):
                if(state[row][col].name == 'P'):
                    if(self.en_passant):
                        print(f"{colour}: {FILE[self.old_col]}x{FILE[col]}{row+1}# e.p.")
                    else:
                        print(f"{colour}: {FILE[self.old_col]}x{FILE[col]}{row+1}#")
                else:
                    if(self.pawn_promotion):
                        print(f"{colour}: {FILE[self.old_col]}x{FILE[col]}{row+1}={self.pawn_promotion}#")
                    else:
                        print(f"{colour}: {state[row][col].name}x{FILE[col]}{row+1}#")
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/checkmate.wav'))
            self.end()
        
        elif(self.moves["stalemate"]):
            if(self.moves["move"]):
                if(state[row][col].name == 'P'):
                    print(f"{colour}: {FILE[col]}{row+1}=")
                else:
                    if(self.pawn_promotion):
                        print(f"{colour}: {FILE[col]}{row+1}={self.pawn_promotion}=")
                    else:
                        print(f"{colour}: {state[row][col].name}{FILE[col]}{row+1}=")
            elif(self.moves["capture"]):
                if(state[row][col].name == 'P'):
                    if(self.en_passant):
                        print(f"{colour}: {FILE[self.old_col]}x{FILE[col]}{row+1}= e.p.")
                    else:
                        print(f"{colour}: {FILE[self.old_col]}x{FILE[col]}{row+1}=")
                else:
                    if(self.pawn_promotion):
                        print(f"{colour}: {FILE[self.old_col]}x{FILE[col]}{row+1}={self.pawn_promotion}=")
                    else:
                        print(f"{colour}: {state[row][col].name}x{FILE[col]}{row+1}=")
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/stalemate.wav'))
            self.end()
        
        elif(self.moves["check"]):
            if(self.moves["move"]):
                if(state[row][col].name == 'P'):
                    print(f"{colour}: {FILE[col]}{row+1}+")
                else:
                    if(self.pawn_promotion):
                        print(f"{colour}: {FILE[col]}{row+1}={self.pawn_promotion}+")
                    else:
                        print(f"{colour}: {state[row][col].name}{FILE[col]}{row+1}+")
            elif(self.moves["capture"]):
                if(state[row][col].name == 'P'):
                    if(self.en_passant):
                        print(f"{colour}: {FILE[self.old_col]}x{FILE[col]}{row+1}+ e.p.")
                    else:
                        print(f"{colour}: {FILE[self.old_col]}x{FILE[col]}{row+1}+")
                else:
                    if(self.pawn_promotion):
                        print(f"{colour}: {FILE[self.old_col]}x{FILE[col]}{row+1}={self.pawn_promotion}+")
                    else:
                        print(f"{colour}: {state[row][col].name}x{FILE[col]}{row+1}+")
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/check.wav'))
        
        elif(self.moves["queenside-castle"] or self.moves["kingside-castle"]):
            if(self.moves["queenside-castle"]):
                print(f"{colour}: O-O-O")
            else:
                print(f"{colour}: O-O")
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/castle.wav'))
        
        elif(self.moves["capture"]):
            if(state[row][col].name == 'P'):
                if(self.en_passant):
                    print(f"{colour}: {FILE[self.old_col]}x{FILE[col]}{row+1} e.p.")
                else:
                    print(f"{colour}: {FILE[self.old_col]}x{FILE[col]}{row+1}")
            else:
                if(self.pawn_promotion):
                    print(f"{colour}: {FILE[self.old_col]}x{FILE[col]}{row+1}={self.pawn_promotion}")
                else:
                    print(f"{colour}: {state[row][col].name}x{FILE[col]}{row+1}")
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/capture.wav'))
        
        elif(self.moves["move"]):
            if(state[row][col].name == 'P'):
                print(f"{colour}: {FILE[col]}{row+1}")
                # different ways to print with variables. Here, for a normal pawn move: "Colour: file rank" e.g.: White: e4
                # print("{0}: {1}{2}".format(colour, FILE[col], row+1))
                # print("{}: {}{}".format(colour, FILE[col], row+1))
                # print("{piece_colour}: {file}{rank}".format(piece_colour = colour, file = FILE[col], rank = row+1))
                # print(f"{colour}: {FILE[col]}{row+1}") # most convenient way imo, f-strings
            else:
                if(self.pawn_promotion):
                    print(f"{colour}: {FILE[col]}{row+1}={self.pawn_promotion}")
                else:
                    print(f"{colour}: {state[row][col].name}{FILE[col]}{row+1}")
            pygame.mixer.Channel(0).play(pygame.mixer.Sound('assets/move.wav'))
        else:
            print("SHREK ERROR")

        self.reset()
            
    def reset(self):
        self.moves["move"] = False
        self.moves["capture"] = False
        self.moves["queenside-castle"] = False
        self.moves["kingside-castle"] = False
        self.moves["check"] = False
        self.moves["stalemate"] = False
        self.moves["checkmate"] = False
        self.old_row, self.old_col = None, None
        self.en_passant = False
        self.pawn_promotion = None

    def end(self):
        if(self.winner):
            print(f"Winner: {self.winner}")
        else:
            print("Stalemate. You're all losers!")

        print("-- Game Over --")