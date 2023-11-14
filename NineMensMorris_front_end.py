import sys

import pygame

from NineMensMorris_version7 import Game_Functions as Game_Functions

DEBUG = True
# Global Variables
board = Game_Functions()
pygame.font.init()  # you have to call this at the start, 
                    # if you want to use this module.
myfont = pygame.font.SysFont('Arial', 18)
# Print the positions, player turn, active mills, remaining turns, and permissible moves
print("Positions:", board.get_positions())
print("Player Turn:", board.get_player_turn())
print("Active Mills:", board.get_active_mills())
print("Remaining Turns:", board.get_remaining_turns())
print("Permissible Moves:", board.get_permissible_moves())

# Initialize pygame
print(" calling pygame.init()")
pygame.init()
print("pygame initialized")
# Set the size of the screen
screen = pygame.display.set_mode((600, 750))

pygame.display.set_caption("Nine Men Morris")
print("game window initialized")
# nine mens morris board image 
boardImg = pygame.image.load('morrisbig.png') 
# avatar images
leafImg = pygame.image.load('player1_30x30.png')
fireImg = pygame.image.load('player2_30x30.png')
highImg = pygame.image.load('high.png')
roboImg = pygame.image.load('robo1.png')
# coordinates of each board position in Board and corresponding position in the nine mens morris board image
print("images loaded")
coords = {
    0: (22, 22, 120, 770),
    1: (230, 22, 820, 770),
    2: (450, 22, 230, 660),
    3: (22, 240, 710, 660),
    4: (450, 240, 350, 540),
    5: (22, 450, 590, 540),
    6: (230, 450, 120, 425),
    7: (450, 450, 230, 425),
    8: (95, 95, 350, 425),
    9: (230, 95, 590, 425),
    10: (380, 95, 710, 425),
    11: (95, 240, 820, 425),
    12: (380, 240, 350, 310),
    13: (95, 378, 470, 310),
    14: (230, 378, 590, 310),
    15: (380, 378, 230, 190),
    16: (162, 169, 470, 190),
    17: (230, 169, 710, 190),
    18: (308, 169, 120, 80),
    19: (162, 240, 470, 80),
    20: (308, 240, 820, 80),
    21: (162, 308, 415, 790),
    22: (230, 308, 430, 680),
    23: (308, 308, 430, 575)
}
# coordinates of each clickable position
# mul = 500 / 843
# clickables = [pygame.Rect(mul * c[0], mul * c[1], 35, 35) for c in coords.values()]
clickables = [pygame.Rect(c[0], c[1], 30, 30) for c in coords.values()]
# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)


# Functions to draw the game state
def draw_board(screen, board_img, positions, coords):
    try:
        # Draw the background board
        screen.blit(board_img.convert(), (0, 0))
        # Draw boarders around the clickable areas
        if DEBUG:
            for rect in clickables:
                pygame.draw.rect(screen, BLACK, rect, 1)
            
        # Draw the pieces on the board
        for pos, value in enumerate(positions):
            x, y, _, _ = coords[pos]
            if value == 1:
                screen.blit(leafImg.convert_alpha(), (x, y))
            elif value == 2:
                screen.blit(fireImg.convert_alpha(), (x, y))
    except Exception as e:
        print(f"Error drawing the board: {e}")

def draw_game_info(screen, game_functions, gameover):
    # Display the variables from the Board class
    if gameover == True:
        texts = [
        f"Game Over! Player {2 if game_functions.get_player_turn() == 1 else 1} wins!"
    ]
    if gameover == False:    
        texts = [
            f"Positions: {game_functions.get_positions()}",
            f"Player Turn: {game_functions.get_player_turn()}",
            f"Active Mills: {game_functions.get_active_mills()}",
            f"Remaining Turns: {game_functions.get_remaining_turns()}",
        ]

    for i, text in enumerate(texts):
        textsurface = myfont.render(text, False, (0, 0, 0))
        screen.blit(textsurface, (10, 600 + i*30))

def game_loop():

    print("Initializing game window...")
    screen.fill(WHITE)
    clock = pygame.time.Clock()

    print("Entering main game loop...")
    running = True
    startpos = None
    endpos = None
    removepos = False
    gameover = False
    while running:
        try:
            # Event handling
            
            for event in pygame.event.get():
                print(" The board positions(A): ", board.get_positions())
                board_positions_now = board.get_positions()
                print(" The board positions(B): ", board_positions_now)

                print(f"Event: {event}")  # This will print out each event captured
                if event.type == pygame.QUIT:
                    print("Quit event detected. Closing game window...")
                    board.cleanup()
                    running = False
                    break
                    
                print("event.type: ", event.type)
                print("pygame.MOUSEBUTTONUP: ", pygame.MOUSEBUTTONUP)
                if event.type == pygame.MOUSEBUTTONUP:
                    # Check if a clickable area was clicked
                    print("here")
                    for idx, rect in enumerate(clickables):
                        print("the clickables are: ", enumerate(clickables))
                        print("The idx is: ", idx)
                        print("The rect is: ", rect)
                        print("here1")
                        print("event.pos: ", event.pos)
                        if rect.collidepoint(event.pos):
                            print("here1.5")
                            if removepos == True:
                                        board_positions_now = board.get_positions()
                                        if board.form_mill(idx):
                                            board.check_remove_active_mill()
                                            removepos = False
                                            board.save_current_state_to_log()
                                            break
                                        break
                            if board.get_remaining_turns() != 0:
                                print("here2")
                                print(f"Clicked on position: {idx}")
                                if board.place_piece(idx):  
                                    board.check_remove_active_mill()
                                    if board.form_mill_GUI():
                                        removepos = True
                                        break
                                    board.save_current_state_to_log()
                                    break
                            if board.get_remaining_turns() == 0:
                                    if board.is_game_over():
                                        print("Game over!")
                                        print(f"Player {2 if board.get_player_turn() == 1 else 1} wins!") 
                                        gameover = True 
                                        break
                                    if startpos == None: 
                                        startpos = idx 
                                        print("startpos: ", startpos)
                                        break
                                    else:
                                        if startpos == idx:
                                            break
                                        endpos = idx
                                        print("endpos: ", endpos)
                                        if board.player_piece_count() == 3:
                                            if board.fly_piece(startpos, endpos):
                                                board.check_remove_active_mill()
                                                if board.form_mill_GUI():
                                                    removepos = True
                                                    startpos = None
                                                    endpos = None
                                                    break
                                                board.save_current_state_to_log()
                                                startpos = None
                                                endpos = None
                                                break
                                            else:
                                                startpos = None
                                                endpos = None
                                        else:
                                            if board.move_piece(startpos, endpos):
                                                board.check_remove_active_mill()
                                                if board.form_mill_GUI():
                                                    removepos = True
                                                    startpos = None
                                                    endpos = None
                                                    break
                                                board.save_current_state_to_log()
                                                startpos = None
                                                endpos = None
                                                break 
                                            else:
                                                startpos = None
                                                endpos = None

            #print("startpos: ", startpos)
            #print("endpos: ", endpos)
            print("removepos: ", removepos)
            print("board positions: ", board.get_positions())
            print("board player turn: ", board.get_player_turn())
                # Add more event handling logic here for other phases
            print("remaining turns: ", board.get_remaining_turns())
            # Drawing the game state
            #print("Calling draw_board()...")
            screen.fill(WHITE)
            draw_board(screen, boardImg, board.get_positions(), coords)
            
            #print("Calling draw_game_info()...")
            draw_game_info(screen, board, gameover)

            # Updating the display
            #print("Updating display...")
            pygame.display.flip()

            # Frame rate
            clock.tick(60)
        except Exception as e:
            print(f"Error in game loop: {e}")
            running = False

    print("Exiting game...")
    # remove temp file
    board.cleanup()

    pygame.quit()
    sys.exit()

# #set positions in board to 1 or 2
# board.set_positions([1, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2,
#                      2, 2, 2, 2, 2, 2, 0, 0, 0, 0, 0, 0])
# # Call the main game loop
#game_functions.new_restart_game()
game_loop()