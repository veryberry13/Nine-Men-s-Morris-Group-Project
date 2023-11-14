import unittest

from NineMensMorris_version6 import Board, Game_Functions


class TestPlacePiece(unittest.TestCase):
    def setUp(self):
        self.game = Game_Functions()

    def test_successfully_placing_a_piece(self):
        """
        Test placing a piece on an empty slot successfully.
        """
        # Given the game has started and it's player 1's turn
        initial_positions = self.game.get_positions()
        self.assertEqual(self.game.get_player_turn(), 1)
        self.assertEqual(initial_positions[0], 0)

        # When I click on an empty slot
        self.game.place_piece(0)

        # Then a piece should be placed in that slot
        self.assertEqual(self.game.get_positions()[0], 1)

        # And the turn should switch to the other player
        self.assertEqual(self.game.get_player_turn(), 2)

    def test_unsuccessful_placing_on_occupied_slot(self):
        """
        Test placing a piece on an occupied slot unsuccessfully.
        """
        # Given the game has started and it's player 1's turn
        self.game.place_piece(0)
        self.assertEqual(self.game.get_positions()[0], 1)
        self.assertEqual(self.game.get_player_turn(), 2)

        # When I click on an already occupied slot
        success = self.game.place_piece(0)

        # Then a piece should not be placed in that slot
        self.assertEqual(self.game.get_positions()[0], 1)

        # And a warning should be displayed indicating the slot is occupied
        # In this case, we use the returned value as a proxy for the warning
        self.assertFalse(success)

if __name__ == '__main__':
    unittest.main()