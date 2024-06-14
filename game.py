import matplotlib.pyplot as plt
import numpy as np
from matplotlib.patches import Rectangle
from enum import Enum


class PieceType(Enum):
    Pawn = 1
    Knight = 2
    Bishop = 3
    Rook = 4
    Queen = 5
    King = 6

class TeamColor(Enum):
    White = 0
    Black = 1

class Piece:
    def __init__(self, type: PieceType, color: TeamColor, value, location):
        self.type = type
        self.color = color
        self.value = value
        self.location = location
        self.hasMoved = False


class Team:
    def __init__(self, color: TeamColor):
        self.color = color
        self.bottomRow = 0 if color == TeamColor.White else 7
        self.pieces = []

        self.populate()


    def populate(self):
        # Pawns
        pawn_row = (self.bottomRow + 1) if self.color == TeamColor.White else (self.bottomRow - 1)
        for i in range(8):
            self.pieces.append(Piece(type=PieceType.Pawn, color=self.color, value=1, location=(pawn_row, i)))
        # Rooks
        for i in [0,7]:
            self.pieces.append(Piece(type=PieceType.Rook, color=self.color, value=5, location=(self.bottomRow, i)))
        # Knights
        for i in [1, 6]:
            self.pieces.append(Piece(type=PieceType.Knight, color=self.color, value=3, location=(self.bottomRow, i)))
        # Bishop
        for i in [2, 5]:
            self.pieces.append(Piece(type=PieceType.Bishop, color=self.color, value=3, location=(self.bottomRow, i)))
        # King & Queen
        self.pieces.append(Piece(type=PieceType.Queen, color=self.color, value=9, location=(self.bottomRow, 3)))
        self.pieces.append(Piece(type=PieceType.King, color=self.color, value=9999, location=(self.bottomRow, 4)))


class Game:
    def __init__(self):
        self.white = Team(TeamColor.White)
        self.black = Team(TeamColor.Black)

        self.team_to_move = TeamColor.White
        self.board = [[None for _ in range(8)] for _ in range(8)]

        self.fill_board(self.white.pieces)
        self.fill_board(self.black.pieces)


    def fill_board(self, team_pieces: [Piece]):
        for piece in team_pieces:
            row, col = piece.location
            self.board[row][col] = piece


    def move_piece(self, piece: Piece, to_location: (int, int)):
        valid_move = self.verify_move(piece, to_location)
        assert valid_move

        piece.hasMoved = True
        self.board[piece.location[0]][piece.location[1]] = None
        self.board[to_location[0]][to_location[1]] = piece
        piece.location = to_location

        pass

    def verify_move(self, piece: Piece, to_location: (int, int)):
        assert piece.color == self.team_to_move

        # Check if there is no piece on the to_location of the same team
        trow, tcol = to_location
        occupier = self.board[trow][tcol]

        if occupier is not None:
            assert occupier.color == piece.color
        # Bounds check

        # check if the position is out of bounds
        if piece.type == PieceType.Pawn:
            return self.verify_pawn_move(piece.location, to_location, piece.color)
        elif piece.type == PieceType.Knight:
            return self.verify_night_move(piece.location, to_location, piece.color)

        return False

    def verify_night_move(self, from_location: (int, int), to_location: (int, int), team_color: TeamColor):
        # Moves in an L shape
        frow, fcol = from_location
        trow, tcol = to_location
        if (abs(frow - trow) == 1 and abs(frow - fcol) == 2) or (abs(frow - trow) == 2 and abs(fcol - tcol) == 1):
            return True
        return False

    def verify_pawn_move(self, from_location: (int, int), to_location: (int, int), teamColor: TeamColor):
        has_moved = (from_location == 1 and teamColor == TeamColor.White) or (from_location == 6 and teamColor == TeamColor.Black)

        frow, fcol = from_location
        trow, tcol = to_location

        occupier = self.board[trow][tcol]
        is_capture = (occupier is not None and occupier is not teamColor)

        # No pieces of myself
        if occupier is not None and occupier.color == teamColor:
            return False

        # Check if the move is in the correct direction
        if teamColor == TeamColor.White and frow > trow or teamColor == TeamColor.Black and frow < trow:
            return False
        # Check if the capture is valid
        if is_capture and abs(frow - trow) == 1 and abs(fcol - tcol) == 1:
            return True
        elif fcol != tcol:
            return False

        # is first move
        if not has_moved and abs(frow - trow) <= 2:
            return True
        elif abs(frow - trow) == 1:
            return True

        return False


def display_board(board):
    symbols = {
        PieceType.Pawn: ('♙\t', '♟\t'),
        PieceType.Knight: ('♘\t', '♞\t'),
        PieceType.Bishop: ('♗\t', '♝\t'),
        PieceType.Rook: ('♖\t', '♜\t'),
        PieceType.Queen: ('♕\t', '♛\t'),
        PieceType.King: ('♔\t', '♚\t')
    }
    column_labels = "  \t a\t b\t c\t d\t e\t f\t g\t h"
    print(column_labels)
    for row in reversed(range(8)):
        row_display = [str(1 + row) + '\t']  # Row numbers on the left
        for col in range(8):
            piece = board[row][col]
            if piece:
                symbol = symbols[piece.type][piece.color.value]
            else:
                symbol = '⬜\t' if (row + col) % 2 == 0 else '⬛\t'
            row_display.append(symbol)
        row_display.append('\t' + str(1 + row))
        print(' '.join(row_display))



    print(column_labels)

if __name__ == '__main__':
    game = Game()
    p = game.white.pieces[10]
    game.move_piece(p, (2, 2))
    display_board(game.board)