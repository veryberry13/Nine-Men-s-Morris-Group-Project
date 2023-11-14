import atexit
import copy
import os
import pickle
import signal
import sys
import time


class Board:
    def __init__(self):
        self.__positions = [0] * 24
        self.__player_turn = 1
        self.__active_mills = []
        self.__remaining_turns = 18
        self.__permissible_moves = {
        0: [1, 3],
        1: [0, 2, 9],
        2: [1, 4],
        3: [0, 11, 5],
        4: [2, 12, 7],
        5: [3, 6],
        6: [5, 7, 14],
        7: [4, 6],
        8: [9, 11],
        9: [1, 8, 17, 10],
        10: [9, 12],
        11: [8, 3, 19, 13],
        12: [20, 10, 4, 15],
        13: [11, 14],
        14: [13, 22, 6, 15],
        15: [14, 12],
        16: [19, 17],
        17: [16, 18, 9],
        18: [17, 20],
        19: [16, 11, 21],
        20: [18, 12, 23],
        21: [19, 22],
        22: [14, 21, 23],
        23: [20, 22]
        }

    # Getter for positions
    def get_positions(self):
        return self.__positions

    # Setter for positions
    def set_positions(self, positions):
        self.__positions = positions

    # Getter for player_turn
    def get_player_turn(self):
        return self.__player_turn

    # Setter for player_turn
    def set_player_turn(self, player_turn):
        self.__player_turn = player_turn

    # Getter for active_mills
    def get_active_mills(self):
        return self.__active_mills

    # Setter for active_mills
    def set_active_mills(self, active_mills):
        self.__active_mills = active_mills

    # Getter for remaining_turns
    def get_remaining_turns(self):
        return self.__remaining_turns

    # Setter for remaining_turns
    def set_remaining_turns(self, remaining_turns):
        self.__remaining_turns = remaining_turns

    # Getter for permissible_moves
    def get_permissible_moves(self):
        return self.__permissible_moves
    
    def set_permissible_moves(self, permissible_moves):
        self.__permissible_moves = permissible_moves

class Game_Functions(Board):
    TEMP_LOG_PATH = "temp_log.pkl"
    SAVED_LOG_PATH = "board_log.pkl"  
    def __init__(self):
        super().__init__()
        # Add this new member for the in-memory log
        self.__temp_log = []

        # Handle exit events
        atexit.register(self.cleanup)
        signal.signal(signal.SIGINT, self.signal_handler)
        
        # check if log exists or create an empty one
        if not os.path.exists("board_log.pkl"):
            with open("board_log.pkl", "wb") as file:
                pickle.dump([], file)

    def printBoard(self):
        board = [' ' if piece == 0 else '1' if piece == 1 else '2' for piece in self.get_positions()]
        print(board[0] + "(00)----------------------" + board[1] +
            "(01)----------------------" + board[2] + "(02)")
        print("|                           |                           |")
        print("|                           |                           |")
        print("|                           |                           |")
        print("|       " + board[8] + "(08)--------------" +
            board[9] + "(09)--------------" + board[10] + "(10)     |")
        print("|       |                   |                    |      |")
        print("|       |                   |                    |      |")
        print("|       |                   |                    |      |")
        print("|       |        " + board[16] + "(16)-----" +
            board[17] + "(17)-----" + board[18] + "(18)       |      |")
        print("|       |         |                   |          |      |")
        print("|       |         |                   |          |      |")
        print("|       |         |                   |          |      |")
        print(board[3] + "(03)---" + board[11] + "(11)----" + board[19] + "(19)               " +
            board[20] + "(20)----" + board[12] + "(12)---" + board[4] + "(04)")
        print("|       |         |                   |          |      |")
        print("|       |         |                   |          |      |")
        print("|       |         |                   |          |      |")
        print("|       |        " + board[21] + "(21)-----" +
            board[22] + "(22)-----" + board[23] + "(23)       |      |")
        print("|       |                   |                    |      |")
        print("|       |                   |                    |      |")
        print("|       |                   |                    |      |")
        print("|       " + board[13] + "(13)--------------" +
            board[14] + "(14)--------------" + board[15] + "(15)     |")
        print("|                           |                           |")
        print("|                           |                           |")
        print("|                           |                           |")
        print(board[5] + "(05)----------------------" + board[6] +
            "(06)----------------------" + board[7] + "(07)")
        print("\n")
        print(f"Player {self.get_player_turn()}'s turn.")
        print(f"Player 1 pieces: {self.get_positions().count(1)}")
        print(f"Player 2 pieces: {self.get_positions().count(2)}")
        print(f"Remaining turns: {self.get_remaining_turns()}")
        print(f"Active mills: {self.get_active_mills()}")

    def is_occupied(self, position):
        return self.get_positions()[position] != 0

    def is_current_player(self, position):
        return self.get_positions()[position] == self.get_player_turn()

    def count_current_player_positions(self):
        return self.get_positions().count(self.get_player_turn())

    def place_piece(self, position):
        if 0 <= position <= 23:
            if not self.is_occupied(position):
                self.get_positions()[position] = self.get_player_turn()
                self.form_mill()
                self.check_remove_active_mill()
                self.set_player_turn(2 if self.get_player_turn() == 1 else 1)
                return True
        return False

    def move_piece(self, current_position, move_to):
        if 0 <= current_position <= 23 and 0 <= move_to <= 23:
            if self.is_occupied(current_position) and self.is_current_player(current_position) and move_to in self.get_permissible_moves()[current_position] and not self.is_occupied(move_to):
                self.get_positions()[move_to] = self.get_player_turn()
                self.get_positions()[current_position] = 0
                self.form_mill()
                self.check_remove_active_mill()
                self.set_player_turn(2 if self.get_player_turn() == 1 else 1)
                return True
        return False

    def is_permissible(self, current_position, move_to):
        return move_to in self.get_permissible_moves()[current_position]

    def remove_piece(self, position):
        if 0 <= position <= 23:
            if self.is_occupied(position) and not self.is_current_player(position):
                self.get_positions()[position] = 0
                return True
        return False

    def fly_piece(self, current_position, move_to):
        if 0 <= current_position <= 23 and 0 <= move_to <= 23:
            if self.is_occupied(current_position) and self.is_current_player(current_position) and not self.is_occupied(move_to):
                self.get_positions()[move_to] = self.get_player_turn()
                self.get_positions()[current_position] = 0
                self.form_mill()
                self.check_remove_active_mill()
                self.set_player_turn(2 if self.get_player_turn() == 1 else 1)
                return True
        return False

    def form_mill(self):
        mill_combinations = [
        [0, 1, 2], [2, 4, 7], [5, 6, 7],
        [0, 3, 5], [8, 9, 10], [10, 12, 15],
        [13, 14, 15], [8, 11, 13],
        [16, 17, 18], [18, 20, 23], [21, 22, 23],
        [16, 19, 21], [1, 9, 17], [20, 12, 4],
        [22, 14, 6], [3, 11, 19]
        ]
        newly_formed_mills = []

        for combo in mill_combinations:
            if self.get_positions()[combo[0]] == self.get_positions()[combo[1]] == self.get_positions()[combo[2]] == self.get_player_turn():
                if combo not in self.get_active_mills():
                    newly_formed_mills.append(combo)

        if newly_formed_mills:
            self.set_active_mills(self.get_active_mills() + newly_formed_mills)
            
            # Ask the player to remove a piece due to the formed mill
            while True:
                try:
                    position_to_remove = int(input("A mill was formed! Choose an opponent's piece to remove (0-23): "))
                    if self.remove_piece(position_to_remove):
                        break
                    else:
                        print("Invalid position. Try again.")
                except ValueError:
                    print("Invalid input. Try again.")

    def check_remove_active_mill(self):
        mills_to_remove = []

        for mill in self.get_active_mills():
            player_at_mill = self.get_positions()[mill[0]]
            if not (self.get_positions()[mill[0]] == self.get_positions()[mill[1]] == self.get_positions()[mill[2]] == player_at_mill):
                mills_to_remove.append(mill)

        for mill in mills_to_remove:
            self.get_active_mills().remove(mill)

    def is_game_over(self):
        current_player_pieces = self.get_positions().count(self.get_player_turn())
        return current_player_pieces <= 2

    def player_piece_count(self):
        return self.get_positions().count(self.get_player_turn())

    def is_gridlocked(self):
        opponent = 2 if self.get_player_turn() == 1 else 1
        for position, player in enumerate(self.get_positions()):
            if player == opponent:
                permissible = self.get_permissible_moves()[position]
                if any([self.get_positions()[move] == 0 for move in permissible]):
                    return False
        print(f"Player {opponent} is gridlocked and Player {self.get_player_turn()} wins!")
        exit()

    def start_menu(self):
        choice = input("Select: 1. New/Restart Game 2. Load Game 3. Game Type (default is 9): ")
        if choice == '1':
            self.new_restart_game()
        elif choice == '2':
            self.load()
        elif choice == '3':
            print("Currently, only Nine Men's Morris (9) is supported.")
            self.new_restart_game()
        else:
            print("Invalid choice.")
            self.start_menu()

    def save_current_state_to_log(self):
        state = {
            'positions': copy.deepcopy(self.get_positions()),
            'player_turn': self.get_player_turn(),
            'active_mills': copy.deepcopy(self.get_active_mills()),
            'remaining_turns': self.get_remaining_turns(),
            'permissible_moves': self.get_permissible_moves()
        }
        print("State before appending to temp_log:", state)  # Debug statement
        self.__temp_log.append(state)
        print("all states in temp_log:", self.__temp_log)  # Debug statement
        self.persist_log('temp')  # Persist to temporary log


    def persist_log(self, log_type):
        filepath = self.TEMP_LOG_PATH if log_type == 'temp' else self.SAVED_LOG_PATH
        with open(filepath, "wb") as file:
            pickle.dump(self.__temp_log, file)
        print(f"Saved {len(self.__temp_log)} logs to {filepath}")  # Debug statement


    def save(self):
        state = {
            'positions': self.get_positions(),
            'player_turn': self.get_player_turn(),
            'active_mills': self.get_active_mills(),
            'remaining_turns': self.get_remaining_turns(),
            'permissible_moves': self.get_permissible_moves()
        }
        
        # Print all states in the temp_log before saving
        print("States in log before saving:")
        for index, s in enumerate(self.__temp_log, 1):
            print(f"State {index}:")
            print(s)
            print("----------")
        
        # Clear the saved log and then save the current temporary log
        if os.path.exists(self.SAVED_LOG_PATH):
            os.remove(self.SAVED_LOG_PATH)
        self.persist_log('saved')
        print("Board state saved to saved log.")

    def load(self):
        if not os.path.exists(self.SAVED_LOG_PATH):
            print("No saved game state exists.")
            return

        with open(self.SAVED_LOG_PATH, "rb") as file:
            self.__temp_log = pickle.load(file)

        if not self.__temp_log:  # Check if the list is empty
            print("Saved log is empty.")
            return

        state = self.__temp_log[-1]  # Now it's safe to access the last element

        self.set_positions(state['positions'])
        self.set_player_turn(state['player_turn'])
        self.set_active_mills(state['active_mills'])
        self.set_remaining_turns(state['remaining_turns'])
        self.set_permissible_moves(state['permissible_moves'])

        self.printBoard()
        print("Board state loaded from log.")
        self.play_game()  # This will continue the game from the loaded state.

    def replay(self):
        if not os.path.exists(self.TEMP_LOG_PATH):
            print("No saved game states to replay.")
            return

        with open(self.TEMP_LOG_PATH, "rb") as file:
            log = pickle.load(file)

        if not log:
            print("Log is empty. Nothing to replay.")
            return

        # Save current state
        current_state = {
            'positions': self.get_positions(),
            'player_turn': self.get_player_turn(),
            'active_mills': self.get_active_mills(),
            'remaining_turns': self.get_remaining_turns(),
            'permissible_moves': self.get_permissible_moves()
        }

        index = 0
        while index < len(log):
            state = log[index]

            # Load state from log and display it
            self.set_positions(state['positions'])
            self.set_player_turn(state['player_turn'])
            self.set_active_mills(state['active_mills'])
            self.set_remaining_turns(state['remaining_turns'])
            self.set_permissible_moves(state['permissible_moves'])
            self.printBoard()

            choice = input("\n1. Next move\n2. Previous move\n3. Auto replay\n4. Exit replay\nChoose an option: ")

            if choice == '1':
                index += 1
            elif choice == '2':
                index -= 1
            elif choice == '3':
                delay = float(input("Enter the delay between moves in seconds: "))
                for remaining_index in range(index, len(log)):
                    state = log[remaining_index]
                    self.set_positions(state['positions'])
                    self.set_player_turn(state['player_turn'])
                    self.set_active_mills(state['active_mills'])
                    self.set_remaining_turns(state['remaining_turns'])
                    self.set_permissible_moves(state['permissible_moves'])
                    self.printBoard()
                    time.sleep(delay)
                break
            elif choice == '4':
                break

            # Bound the index to the available range
            index = max(0, min(index, len(log) - 1))

        # Restore the current state after exiting replay
        self.set_positions(current_state['positions'])
        self.set_player_turn(current_state['player_turn'])
        self.set_active_mills(current_state['active_mills'])
        self.set_remaining_turns(current_state['remaining_turns'])
        self.set_permissible_moves(current_state['permissible_moves'])


    def place_a_piece_phase(self):
        while self.get_remaining_turns() > 0:
            self.printBoard()
            try:
                position = int(input(f"Player {self.get_player_turn()}, enter a position (0-23), 24 to Load, 25 to Save, 26 to Restart, 27 to Replay or 28 to access main menu: "))
                
                if position == 24:
                    self.load()
                elif position == 25:
                    self.save()
                elif position == 26:
                    self.new_restart_game()
                elif position == 27:
                    self.replay()
                elif position == 28:
                    self.start_menu()
                elif self.place_piece(position):
                    self.set_remaining_turns(self.get_remaining_turns() - 1)
                    self.save_current_state_to_log()
                else:
                    print("Invalid move. Try again.")
            except ValueError:
                print("Invalid input. Try again.")

    def move_a_piece_phase(self):
        while not self.is_game_over():
            self.printBoard()
            try:
                if self.player_piece_count() == 3:
                    current_position = int(input(f"Player {self.get_player_turn()}, select a piece to fly (0-23), 24 to Load, 25 to Save, 26 to Restart, 27 to Replay or 28 to access main menu: "))
                else:
                    current_position = int(input(f"Player {self.get_player_turn()}, select a piece to move (0-23), 24 to Load, 25 to Save, 26 to Restart, 27 to Replay or 28 to access main menu: "))
                
                if current_position == 24:
                    self.load()
                elif current_position == 25:
                    self.save()
                elif current_position == 26:
                    self.new_restart_game()
                elif current_position == 27:
                    self.replay()
                elif current_position == 28:
                    self.start_menu()
                else:
                    if self.player_piece_count() == 3:
                        # if player is in fly phase then assign input to move_to
                        move_to = int(input(f"Select where to fly your piece: " ))
                    else:
                        move_to = int(input(f"Select where to move your piece {self.get_permissible_moves()[current_position]}: "))
                    
                    # Check if the player can fly their piece
                    # print the current player's piece count
                    print(f"Player {self.get_player_turn()} has {self.player_piece_count()} pieces left.")
                    if self.player_piece_count() == 3:
                        if not self.fly_piece(current_position, move_to):
                            print("Invalid move. Try again.")
                    else:
                        if not self.move_piece(current_position, move_to):
                            print("Invalid move. Try again.")
                            # Check game over condition after a move
                    self.save_current_state_to_log()
                if self.is_game_over():
                    print(f"Player {2 if self.get_player_turn() == 1 else 1} wins!")  # The opponent wins.
                    self.start_menu()
                    return
            except ValueError:
                print("Invalid input. Try again.")


    def new_restart_game(self):
        self.set_positions([0] * 24)
        self.set_player_turn(1)
        self.set_active_mills([])
        self.set_remaining_turns(18)
        if os.path.exists(self.TEMP_LOG_PATH):
            os.remove(self.TEMP_LOG_PATH)
        self.__temp_log = []  # clear the in-memory log
        self.printBoard()
        self.play_game()

    def play_game(self):
        self.place_a_piece_phase()
        self.move_a_piece_phase()
        print(f"Player {self.get_player_turn()} wins!")

    def cleanup(self):
        if os.path.exists(self.TEMP_LOG_PATH):
            os.remove(self.TEMP_LOG_PATH)

    def signal_handler(self, signal, frame):
        self.cleanup()
        print("\nGame exited, temporary log cleared.")
        sys.exit(0)

def main():
    game = Game_Functions()  # Create a Game_Functions object.
    game.start_menu()  # Start the game with the main menu.

if __name__ == "__main__":
    main()