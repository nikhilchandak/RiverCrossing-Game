import pygame
import sys
import os
import math
import numpy
from random import randrange, choice
from config import *

pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("River Crossing Competition")
clock = pygame.time.Clock()
background = pygame.Surface(screen.get_size())


def loadify(img):
    return pygame.image.load(img).convert_alpha()


BACKGROUND_IMAGE = loadify(BACKGROUND_IMAGE_PATH)
FIXED_OBSTACLE_IMAGE = loadify(FIXED_OBSTACLE_PATH)
MOVING_OBSTACLE_IMAGE = loadify(MOVING_OBSTACLE_PATH)
PLAYER_IMAGE = loadify(PLAYER_PATH)


class FixedObstacle(pygame.sprite.Sprite):
    def __init__(self, location):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(FIXED_OBSTACLE_PATH)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.width = self.image.get_width()
        self.crossed = False
        self.points = 5

    def draw(self, window):
        window.blit(self.image, self.rect)


class MovingObstacle(pygame.sprite.Sprite):
    def __init__(self, location, ship_speed=-1):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(MOVING_OBSTACLE_PATH)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location

        if ship_speed == -1:
            ship_speed = randrange(1, 12)

        self.speed = [ship_speed, 0]
        self.width = self.image.get_width()
        self.points = 10
        self.crossed = False

    def move(self):
        self.rect.move_ip(self.speed)
        self.rect.left %= SCREEN_WIDTH  # Wrap around screen

    def draw(self, window):
        window.blit(self.image, self.rect)


class River(object):
    def __init__(
            self,
            startingY,
            width,
            player_river=False,
            ship_speed=-1,
            level=1):
        self.y_start = startingY
        self.y_end = startingY + width
        self.bank_width = (int)(RIVER_BANK_RATIO * width)
        self.river_width = width - self.bank_width
        self.max_obstacles = max([2, round(SCREEN_WIDTH / 300.0)])

        if player_river:
            self.fixed_obstacles_count = randrange(1, self.max_obstacles + 1)
            self.moving_obstacles_count = 0
        else:
            self.fixed_obstacles_count = choice(
                [0, 0, 0, 1, 1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 3, 3, 3, 4])
            self.moving_obstacles_count = randrange(level, self.max_obstacles)

        self.fixed_obstacles, self.moving_obstacles = [], []
        self.platform = (0, self.y_start, SCREEN_WIDTH, self.bank_width)
        self.crossed = False

        def generateFixedObstacles():
            fixed_width = FIXED_OBSTACLE_IMAGE.get_width()
            fixed_height = FIXED_OBSTACLE_IMAGE.get_height()

            if self.fixed_obstacles_count == 0:
                return

            partitions = SCREEN_WIDTH // self.fixed_obstacles_count
            current_x = 0
            for count in range(self.fixed_obstacles_count):
                obstacle_x = randrange(
                    current_x, current_x + partitions - fixed_width * 2)
                obstacle_y = self.y_start + randrange(self.bank_width)
                current_x += partitions
                self.fixed_obstacles.append(FixedObstacle(
                    [obstacle_x, obstacle_y - fixed_height]))

        def generateMovingObstacles():
            fixed_width = MOVING_OBSTACLE_IMAGE.get_width()
            fixed_height = MOVING_OBSTACLE_IMAGE.get_height()

            if self.moving_obstacles_count == 0:
                return

            partitions = SCREEN_WIDTH // self.moving_obstacles_count
            current_x = 0
            for count in range(self.moving_obstacles_count):
                obstacle_x = randrange(
                    current_x, current_x + partitions - 2 * fixed_width)
                obstacle_y = self.y_start + self.bank_width + \
                    randrange(self.river_width - fixed_height)
                current_x += partitions
                self.moving_obstacles.append(MovingObstacle(
                    [obstacle_x, obstacle_y], ship_speed))

        generateFixedObstacles()
        generateMovingObstacles()

    def update(self):
        for ship in self.moving_obstacles:
            ship.move()

    def draw(self, window):
        pygame.draw.rect(window, BROWN, self.platform)
        for obj in self.moving_obstacles:
            obj.draw(window)
        for obj in self.fixed_obstacles:
            obj.draw(window)


class Player(pygame.sprite.Sprite):
    def __init__(self, location, score_position, keys, speed=PLAYER_SPEED):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load(PLAYER_PATH)
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect.left, self.rect.top = location
        self.width = self.image.get_width()
        self.height = self.image.get_height()
        self.time_points = 0
        self.obstacle_points = 0
        self.speed = speed
        self.alive = 0
        self.wins = 0
        self.score_position = score_position
        self.keys = keys

    def handle_keys(self):
        keys = pygame.key.get_pressed()
        if keys[self.keys[0]] and self.rect.left > self.speed[0]:
            self.rect.move_ip(-self.speed[0], 0)

        if keys[self.keys[1]] and self.rect.right < SCREEN_WIDTH - \
                self.speed[0]:
            self.rect.move_ip(self.speed[0], 0)

        if keys[self.keys[2]] and self.rect.top > self.speed[1]:
            self.rect.move_ip(0, -self.speed[1])

        if keys[self.keys[3]] and self.rect.bottom < SCREEN_HEIGHT - \
                self.speed[1]:
            self.rect.move_ip(0, self.speed[1])

    def draw(self, window):
        window.blit(self.image, self.rect)


class Player1(Player):
    def __init__(self, location, speed=PLAYER_SPEED):
        score_position = [
            SCREEN_WIDTH // 5,
            SCREEN_HEIGHT - SCREEN_HEIGHT // 30]
        keys = [pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN]
        Player.__init__(self, location, score_position, keys)


class Player2(Player):
    def __init__(self, location, speed=PLAYER_SPEED):
        score_position = [
            SCREEN_WIDTH - SCREEN_WIDTH // 5,
            SCREEN_HEIGHT - SCREEN_HEIGHT // 30]
        keys = [pygame.K_a, pygame.K_d, pygame.K_w, pygame.K_s]
        Player.__init__(self, location, score_position, keys)


current_player = 1
rivers = []
platform_width = 5
obstacles = [] # stores the list of all fixed/moving obstacles
player1 = Player1([0, 0])
player2 = Player2([0, 0])
round_start_timer = 0 
players = [player1, player2]
current_round = 0
round_over = False
ship_speeds = [SHIP_STARTING_SPEED, SHIP_STARTING_SPEED]


def draw_text(window, text, size, text_pos, color=WHITE, bold=False):
    """ Draws given text on the window """
    font = pygame.font.Font(FONT_PATH, size)
    if bold:
        font.set_bold(1)
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect()
    text_rect.midtop = text_pos
    window.blit(text_surface, text_rect)


def redraw_game_window(to_update=True):
    screen.blit(BACKGROUND_IMAGE, (0, 0))  # screen.fill(LIGHT_BLUE)

    for river in rivers:
        if to_update:
            river.update()
        river.draw(screen)

    player1_text = "Player1: Wins = " + \
        str(player1.wins) + " Score = " + \
        str(player1.time_points + player1.obstacle_points)
    draw_text(screen, player1_text, 15, player1.score_position, WHITE)

    player2_text = "Player2: Wins = " + \
        str(player2.wins) + " Score = " + \
        str(player2.obstacle_points + player2.time_points)
    draw_text(screen, player2_text, 15, player2.score_position, WHITE)

    draw_text(screen, "Round: " + str(current_round), 15,
              (SCREEN_WIDTH / 2.23, SCREEN_HEIGHT - platform_width), BLACK)
    current_time = (pygame.time.get_ticks() - round_start_timer) / 1000.0
    current_time = str(current_time)
    # print(current_time)
    current_time = current_time.split('.')
    current_time = current_time[0] + '.' + current_time[1][0]
    draw_text(
        screen,
        "Time: " +
        str(current_time),
        15,
        (SCREEN_WIDTH /
         1.78,
         SCREEN_HEIGHT -
         platform_width),
        BLACK)

    players[current_player].draw(screen)
    pygame.display.update()  # or pygame.display.flip()


def prepare_rivers(ship_speed=SHIP_STARTING_SPEED):
    global platform_width, obstacles, rivers
    obstacles = []
    rivers = []
    partition = float(SCREEN_HEIGHT) / (RIVERS + RIVER_BANK_RATIO)
    partition = math.ceil(partition)

    for river in range(RIVERS + 1):
        new_river = River(
            partition * river,
            partition,
            river == 0 or river == (
                RIVERS - 1),
            ship_speed)
        rivers.append(new_river)
        platform_width = new_river.bank_width

        obstacles.extend(new_river.moving_obstacles)
        obstacles.extend(new_river.fixed_obstacles)


def generate_player_positions():
    """ Generates both the player's position randomly such that 
            they are not in collision with the obstacle """
    global obstacles

    # Generate random position for player1 such that it is not in collision
    # with fixed obstacles
    y_pos = SCREEN_HEIGHT - PLAYER_IMAGE.get_height()
    x_pos = randrange(SCREEN_WIDTH - PLAYER_IMAGE.get_width())
    player1.rect.left, player1.rect.top = x_pos, y_pos
    while pygame.sprite.spritecollide(player1, obstacles, False):
        x_pos = randrange(SCREEN_WIDTH - PLAYER_IMAGE.get_width())
        player1.rect.left = x_pos

    # Generate random position for player2 such that it is not in collision
    # with fixed obstacles
    y_pos = 0
    x_pos = randrange(SCREEN_WIDTH - PLAYER_IMAGE.get_width())
    player2.rect.left, player2.rect.top = x_pos, y_pos
    while pygame.sprite.spritecollide(player2, obstacles, False):
        x_pos = randrange(SCREEN_WIDTH - PLAYER_IMAGE.get_width())
        player2.rect.left = x_pos
        player2.rect.top = randrange(10)


def reset_players():
    global round_start_timer, players, current_round, \
        current_player, round_over, ship_speeds
    players[current_player].alive = 0
    players[not current_player].alive = 1
    round_start_timer = pygame.time.get_ticks()

    if round_over:
        if player1.wins > player2.wins:
            ship_speeds = [SHIP_STARTING_SPEED *
                           (SPEED_DELTA) ** (player1.wins - player2.wins),
                           SHIP_STARTING_SPEED]
            player1.speed = [
                PLAYER_UPDATE_SPEED *
                speed for speed in player1.speed]
            player2.speed = PLAYER_SPEED
        elif player2.wins > player1.wins:
            ship_speeds = [SHIP_STARTING_SPEED, SHIP_STARTING_SPEED *
                           (SPEED_DELTA) ** (player2.wins - player1.wins)]
            player2.speed = [
                PLAYER_UPDATE_SPEED *
                speed for speed in player2.speed]
            player1.speed = PLAYER_SPEED
        else:
            player1.speed, player2.speed = PLAYER_SPEED, PLAYER_SPEED
            ship_speeds = [SHIP_STARTING_SPEED, SHIP_STARTING_SPEED]

    if current_player:
        current_round += 1

    current_player = not current_player
    round_over = False

    # print(ship_speeds, players[current_player].speed, current_player + 1)
    prepare_rivers(ship_speeds[current_player])
    generate_player_positions()


def collision_text():
    """ Displays animated text on colliding with obstacles """ 
    interval = 20
    font_size = 30
    for plus in range(50):
        redraw_game_window(False)
        draw_text(screen, COLLISION_MESSAGE, font_size + plus,
                  [SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2], RED)
        pygame.display.flip()
        pygame.time.delay(interval)


def check_collision():
    """ Function to check if any player is in collision with obstacle """
    global round_over

    if player1.alive:
        if pygame.sprite.spritecollide(
                player1,
                obstacles,
                False,
                pygame.sprite.collide_mask):
            collision_text()
            reset_players()
    else:
        if pygame.sprite.spritecollide(
                player2,
                obstacles,
                False,
                pygame.sprite.collide_mask):
            round_over = True
            collision_text()
            reset_players()


def add_time_points():
    global players
    time_taken = (pygame.time.get_ticks() - round_start_timer) / 1000
    delta = (int)(TIME_SCORE // (0.5 * ((time_taken) ** 2)))
    # print(time_taken, delta)
    x, y = players[current_player].score_position
    draw_text(screen, "Player" + str(current_player + 1) + " += " + str(delta),
              50, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + SCREEN_HEIGHT / 10),
              WHITE, True)
    pygame.display.flip()
    pygame.time.delay(2000)
    players[current_player].time_points += delta


def add_obstacle_points():
    player_y = players[current_player].rect.top + \
        players[current_player].image.get_height()
    for obstacle in obstacles:
        if not obstacle.crossed and obstacle.rect.top < SCREEN_HEIGHT and (
            (players[current_player].rect.top > obstacle.rect.top +
             obstacle.image.get_height() and current_player) or (
                not current_player and player_y < obstacle.rect.top)):
            obstacle.crossed = 1
            players[current_player].obstacle_points += obstacle.points


def check_player_reached():
    """ Checks if any player has reacher other end of the screen """
    global round_start_timer, round_over

    if player1.alive and player1.rect.top < (platform_width // 2):
        add_time_points()
        reset_players()
        player1.wins += 1
        return True

    elif player2.alive and (player2.rect.top + player2.image.get_height()) > \
            (SCREEN_HEIGHT - platform_width):
        player2.wins += 1
        round_over = True
        add_time_points()
        reset_players()
        return True


def check_quit():
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()  # running = False
            sys.exit()


def update_player_position():
    players[current_player].handle_keys()


def wait_for_key():
    """ Waits for player to press BACKSPACE key when in start/end screen """
    global current_round, current_player, player1, \
        player2, ship_speeds, round_over

    pygame.display.flip()
    waiting = True
    while waiting:
        check_quit()
        keys = pygame.key.get_pressed()
        if keys[pygame.K_BACKSPACE]:
            waiting = False

    current_round = -1
    current_player = 1
    player2.time_points, player2.obstacle_points, player1.obstacle_points, \
        player1.time_points = [0, 0, 0, 0]
    player1.speed, player2.speed = [PLAYER_SPEED, PLAYER_SPEED]
    ship_speeds = [SHIP_STARTING_SPEED, SHIP_STARTING_SPEED]
    round_over = False
    player1.wins, player2.wins = [0, 0]
    run_rounds()


def game_over():
    screen.blit(BACKGROUND_IMAGE, (0, 0))  # screen.fill(LIGHT_BLUE)
    draw_text(screen, "Game Over!", 60, (SCREEN_WIDTH / 2, SCREEN_HEIGHT / 5))

    player1_text = "Player1: Wins = " + \
        str(player1.wins) + ", Score = " + \
        str(player1.time_points + player1.obstacle_points)
    draw_text(screen, player1_text, 30,
              (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 5))

    player2_text = "Player2: Wins = " + \
        str(player2.wins) + ", Score = " + \
        str(player2.time_points + player2.obstacle_points)
    draw_text(screen, player2_text, 30,
              (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 5))

    draw_text(screen, BEGIN_AGAIN_INSTRUCTIONS, 25,
              (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 4 / 5), BLACK)
    wait_for_key()


def start_screen():
    screen.blit(BACKGROUND_IMAGE, (0, 0))  # screen.fill(LIGHT_BLUE)
    draw_text(screen, TITLE, 50, (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 0.2 / 7))
    draw_text(screen, PLAYER1_INSTRUCTIONS, 30,
              (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 1.5 / 7))
    draw_text(screen, PLAYER2_INSTRUCTIONS, 30,
              (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 2 / 7))
    draw_text(screen, BEGIN_INSTRUCTIONS, 25,
              (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 3 / 7), BLACK)
    draw_text(screen, TIME_SCORING, 25,
              (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 4 / 7))
    draw_text(screen, FIXED_OBSTACLE_SCORING, 25,
              (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 4.5 / 7))
    draw_text(screen, MOVING_OBSTACLE_SCORING, 25,
              (SCREEN_WIDTH / 2, SCREEN_HEIGHT * 5 / 7))
    draw_text(
        screen,
        GOAL,
        30,
        (SCREEN_WIDTH /
         2,
         SCREEN_HEIGHT *
         5.75 /
         7),
        GREEN_CYAN)
    draw_text(
        screen,
        THEME_CREDITS,
        18,
        (SCREEN_WIDTH /
         2,
         SCREEN_HEIGHT *
         6.5 /
         7),
        ORANGE)
    wait_for_key()


def run_rounds():
    reset_players()
    while current_round <= ROUNDS:
        check_quit()
        update_player_position()
        add_obstacle_points()
        redraw_game_window()
        check_player_reached()
        check_collision()
        clock.tick(FPS)
    game_over()


start_screen()
