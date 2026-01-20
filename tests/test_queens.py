# test_queens.py
#
# ICS 33 Winter 2026
# Project 0: History of Modern
#
# Unit tests for the QueensState class in "queens.py".
#
# Docstrings are not required in your unit tests, though each test does need to have
# a name that clearly indicates its purpose.  Notice, for example, that the provided
# test method is named "test_queen_count_is_zero_initially" instead of something generic
# like "test_queen_count", since it doesn't entirely test the "queen_count" method,
# but instead focuses on just one aspect of how it behaves.  You'll want to do likewise.

from queens import *
import unittest



class TestQueensState(unittest.TestCase):
    # NOTE: queen_count tests
    def test_queen_count_is_zero_initially(self):
        state = QueensState(8, 8)
        self.assertEqual(state.queen_count(), 0)

    def test_queen_count_increases(self):
        state = QueensState(8, 8).with_queens_added([Position(0, 0)])
        self.assertEqual(state.queen_count(), 1)

    # NOTE: Initialization tests
    def test_queenState_has_proper_rows_and_columns(self):
        state = QueensState(8, 8)
        self.assertEqual(state.rows, 8)
        self.assertEqual(state.columns, 8)

    def test_does_not_have_queen_in_any_position_initially(self):
        state = QueensState(8, 8)
        for i in range(8):
            for j in range(8):
                self.assertFalse(state.has_queen(Position(i, j)))

    # NOTE: with_queens_added tests
    def test_has_queen_after_adding(self):
        state = QueensState(8, 8)
        self.assertFalse(state.has_queen(Position(0, 0)))
        state = state.with_queens_added([Position(0, 0)])
        self.assertTrue(state.has_queen(Position(0, 0)))

    def test_has_queen_after_adding_multiple_simultaneously(self):
        state = QueensState(8, 8)
        self.assertFalse(state.has_queen(Position(0, 0)))
        self.assertFalse(state.has_queen(Position(1, 1)))
        state = state.with_queens_added([Position(0, 0), Position(1, 1)])
        self.assertTrue(state.has_queen(Position(0, 0)))
        self.assertTrue(state.has_queen(Position(1, 1)))

    def test_cannot_add_queens_to_filled_position(self):
        state = QueensState(8, 8).with_queens_added([Position(0, 0)])
        with self.assertRaises(DuplicateQueenError):
            state.with_queens_added([Position(0, 0)])

    # NOTE: with_queens_removed tests
    def test_has_queen_after_removing(self):
        state = QueensState(8, 8).with_queens_added([Position(0, 0)])
        self.assertTrue(state.has_queen(Position(0, 0)))
        state = state.with_queens_removed([Position(0, 0)])
        self.assertFalse(state.has_queen(Position(0, 0)))

    def test_has_queen_after_removing_multiple_simultaneously(self):
        state = QueensState(8, 8).with_queens_added([Position(0, 0), Position(1, 1)])
        self.assertTrue(state.has_queen(Position(0, 0)))
        self.assertTrue(state.has_queen(Position(1, 1)))
        state = state.with_queens_removed([Position(0, 0), Position(1, 1)])
        self.assertFalse(state.has_queen(Position(0, 0)))
        self.assertFalse(state.has_queen(Position(1, 1)))

    def test_cannot_remove_queens_from_empty_positions(self):
        state = QueensState(8, 8)
        with self.assertRaises(MissingQueenError):
            state.with_queens_removed([Position(0, 0)])

    # NOTE: queens tests
    def test_queens_empty(self):
        state = QueensState(8, 8)
        self.assertEqual(state.queens(), [])

    def test_queens_normal(self):
        state = QueensState(8, 8).with_queens_added([Position(0, 0)])
        self.assertEqual(state.queens(), [Position(0, 0)])

    def test_queens_multiple(self):
        state = QueensState(8, 8).with_queens_added([Position(0, 0), Position(1, 1)])
        self.assertEqual(set(state.queens()), {Position(0, 0), Position(1, 1)})

    # NOTE: any_queens_unsafe tests
    def test_empty_board_is_safe(self):
        state = QueensState(8, 8)
        self.assertFalse(state.any_queens_unsafe())

    def test_normal_board_is_safe(self):
        state = QueensState(8, 8).with_queens_added([Position(0, 0), Position(4, 3), Position(6, 2)])
        self.assertFalse(state.any_queens_unsafe())

    def test_diagonal_queens_unsafe(self):
        state = QueensState(8, 8).with_queens_added([Position(0, 0), Position(1, 1)])
        self.assertTrue(state.any_queens_unsafe())

    def test_diagonal_queens_unsafe_edge(self):
        state = QueensState(8, 8).with_queens_added([Position(2, 2), Position(4, 4)])
        self.assertTrue(state.any_queens_unsafe())

    def test_horizontal_queens_unsafe(self):
        state = QueensState(8, 8).with_queens_added([Position(0, 0), Position(0, 7)])
        self.assertTrue(state.any_queens_unsafe())

    def test_horizontal_queens_unsafe_edge(self):
        state = QueensState(8, 8).with_queens_added([Position(5, 5), Position(5, 6)])
        self.assertTrue(state.any_queens_unsafe())

    def test_vertical_queens_unsafe(self):
        state = QueensState(8, 8).with_queens_added([Position(0, 0), Position(7, 0)])
        self.assertTrue(state.any_queens_unsafe())

    def test_vertical_queens_unsafe_edge(self):
        state = QueensState(8, 8).with_queens_added([Position(3, 3), Position(4, 3)])
        self.assertTrue(state.any_queens_unsafe())

    def test_only_two_queens_unsafe(self):
        state = QueensState(8, 8).with_queens_added([Position(0, 0), Position(0, 7), Position(1, 2), Position(2, 4)])
        self.assertTrue(state.any_queens_unsafe())

    def test_four_queens_unsafe(self):
        state = QueensState(8, 8).with_queens_added([Position(0, 0), Position(0, 7), Position(7, 0), Position(7, 7)])
        self.assertTrue(state.any_queens_unsafe())

    # NOTE: Exception tests
    def test_duplicate_queen_error_str(self):
        err = DuplicateQueenError(Position(1, 1))
        try:
            raise err
        except DuplicateQueenError:
            self.assertEqual(str(err), 'duplicate queen in row 1 column 1')

    def test_missing_queen_error_str(self):
        err = MissingQueenError(Position(1, 1))
        try:
            raise err
        except MissingQueenError:
            self.assertEqual(str(err), 'missing queen in row 1 column 1')


if __name__ == '__main__':
    unittest.main()
