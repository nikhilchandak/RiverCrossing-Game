# Technical Details
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 700
ROUNDS = 3
RIVERS = 6
RIVER_BANK_RATIO = 0.2
FPS = 60

# Colors
BROWN = (165, 42, 42)
LIGHT_BLUE = (173, 216, 230)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
ORANGE = (247, 103, 8)
GREEN_CYAN = (6, 78, 64)

# Messages
COLLISION_MESSAGE = "YOU DIED"
TITLE = "Welcome to CrossTheRiver!"
PLAYER1_INSTRUCTIONS = "UP DOWN LEFT RIGHT keys for Player 1"
PLAYER2_INSTRUCTIONS = "W S A D keys for Player 2"
GOAL = "Goal: Reach the other end of the screen"
BEGIN_INSTRUCTIONS = "Press BACKSPACE key to begin (Note: Player 1 starts);"
NOTES = "Other player automatically starts if one player dies or reachers the other end"
THEME_CREDITS = "Theme Credits: Raj Singh Parihar, His Challenge: Cross 2000 points! :)"
TIME_SCORING = "Scoring is inversely proportional to the time taken."
FIXED_OBSTACLE_SCORING = "Crossing fixed obstacles gains 5points"
MOVING_OBSTACLE_SCORING = "Crossing moving obstacles gains 10points"
BEGIN_AGAIN_INSTRUCTIONS = "Press BackSpace key to start again"

# Image/Font Paths
BACKGROUND_IMAGE_PATH = "water_surface_low.jpg"  # "water_surface.png"
FIXED_OBSTACLE_PATH = "south_park_satan.png"
MOVING_OBSTACLE_PATH = "devil_image.png"
PLAYER_PATH = "jesus_50.png"
FONT_PATH = "Supercell-magic-webfont.ttf"
DIED_SOUND_FILE = "died_sound.mp3"

# Scoring/Speed details
TIME_SCORE = 4000
SPEED_DELTA = 1.4
SHIP_STARTING_SPEED = 6.0
PLAYER_UPDATE_SPEED = 1.4
PLAYER_SPEED = [3, 3]
