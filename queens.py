# queens.py
#
# ICS 33 Winter 2026
# Project 0: History of Modern
#
# A module containing tools that could assist in solving variants of the
# well-known "n-queens" problem.  Note that we're only implementing one part
# of the problem: immutably managing the "state" of the board (i.e., which
# queens are arranged in which cells).  The rest of the problem -- determining
# a valid solution for it -- is not our focus here.
#
# Your goal is to complete the QueensState class described below, though
# you'll need to build it incrementally, as well as test it incrementally by
# writing unit tests in test_queens.py.  Make sure you've read the project
# write-up before you proceed, as it will explain the requirements around
# following (and documenting) an incremental process of solving this problem.
#
# DO NOT MODIFY THE Position NAMEDTUPLE OR THE PROVIDED EXCEPTION CLASSES.

from collections import namedtuple
from typing import Self



Position = namedtuple('Position', ['row', 'column'])

# Ordinarily, we would write docstrings within classes or their methods.
# Since a namedtuple builds those classes and methods for us, we instead
# add the documentation by hand afterward.
Position.__doc__ = 'A position on a chessboard, specified by zero-based row and column numbers.'
Position.row.__doc__ = 'A zero-based row number'
Position.column.__doc__ = 'A zero-based column number'



class DuplicateQueenError(Exception):
    """An exception indicating an attempt to add a queen where one is already present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where the duplicate queen exists."""
        self._position = position


    def __str__(self) -> str:
        return f'duplicate queen in row {self._position.row} column {self._position.column}'



class MissingQueenError(Exception):
    """An exception indicating an attempt to remove a queen where one is not present."""

    def __init__(self, position: Position):
        """Initializes the exception, given a position where a queen is missing."""
        self._position = position


    def __str__(self) -> str:
        return f'missing queen in row {self._position.row} column {self._position.column}'



class QueensState:
    """Immutably represents the state of a chessboard being used to assist in
    solving the n-queens problem."""

    def __init__(self, rows: int, columns: int):
        """Initializes the chessboard to have the given numbers of rows and columns,
        with no queens occupying any of its cells."""
        self.rows = rows
        self.columns = columns
        self._board: dict[Position, bool] = {}

        for row in range(rows):
            for column in range(columns):
                self._board[Position(row, column)] = False


    def queen_count(self) -> int:
        """Returns the number of queens on the chessboard."""
        count = 0

        for value in self._board.values():
            count += value

        return count


    def queens(self) -> list[Position]:
        """Returns a list of the positions in which queens appear on the chessboard,
        arranged in no particular order."""
        result = []
        for position in self._board:
            if self._board[position]:
                result.append(position)

        return result


    def has_queen(self, position: Position) -> bool:
        """Returns True if a queen occupies the given position on the chessboard, or
        False otherwise."""
        return self._board[position]


    def any_queens_unsafe(self) -> bool:
        """Returns True if any queens on the chessboard are unsafe (i.e., they can
        be captured by at least one other queen on the chessboard), or False otherwise."""
        for starting_row in range(self.rows):
            for starting_column in range(self.columns):
                starting_position = Position(starting_row, starting_column)

                if self.has_queen(starting_position):
                    # Checking for diagonal dangers
                    diagonal_offset = 1
                    while diagonal_offset+starting_row < self.rows and diagonal_offset+starting_column < self.columns:
                        if self.has_queen(Position(diagonal_offset+starting_row, diagonal_offset+starting_column)):
                            return True
                        diagonal_offset += 1

                    # Checking for horizontal dangers
                    horizontal_offset = 1
                    while horizontal_offset+starting_row < self.rows:
                        if self.has_queen(Position(horizontal_offset+starting_row, starting_column)):
                            return True
                        horizontal_offset += 1

                    # Checking for vertical dangers
                    vertical_offset = 1
                    while vertical_offset+starting_column < self.columns:
                        if self.has_queen(Position(starting_row, vertical_offset+starting_column)):
                            return True
                        vertical_offset += 1
        
        return False


    def with_queens_added(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens added in the given positions,
        without modifying 'self' in any way.  Raises a DuplicateQueenError when
        there is already a queen in at least one of the given positions."""
        result = QueensState(self.rows, self.columns)
        # Copying over self
        for row in range(result.rows):
            for column in range(result.columns):
                position = Position(row, column)
                result._board[position] = self._board[position]

        # Adding positions
        for position in positions:
            if result.has_queen(position):
                raise DuplicateQueenError(position)
            result._board[position] = True

        return result


    def with_queens_removed(self, positions: list[Position]) -> Self:
        """Builds a new QueensState with queens removed from the given positions,
        without modifying 'self' in any way.  Raises a MissingQueenError when there
        is no queen in at least one of the given positions."""
        result = QueensState(self.rows, self.columns)
        # Copying over self
        for row in range(result.rows):
            for column in range(result.columns):
                position = Position(row, column)
                result._board[position] = self._board[position]

        # Removing positions
        for position in positions:
            if not result.has_queen(position):
                raise MissingQueenError(position)
            result._board[position] = False

        return result
