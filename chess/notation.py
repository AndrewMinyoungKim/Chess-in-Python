from .constants import *

class Notation:
    #display move that was made
    def display_move(self, state, row, col, colour):
        # IMPORTANT NOTE: When reading, the file letter comes first and THEN the rank number (e.g. d4), so it reads as Column THEN Row
        if(state[row][col].name == 'P'):
            print("{}: {}{}".format(colour, FILE[col], row+1))
        else:
            print("{}: {}{}{}".format(colour, state[row][col].name, FILE[col], row+1))

            #need to implement rest of notation for checks, checkmates, captures, castles, etc. (x, +, #, O-O, O-O-O)
            # move all sound effects to play in Notation once the notation portion is completed as you will need to determine all moves anyways, including regular captures, checks, etc.