import pygame
import random
import time

# Initialize Pygame
pygame.init()

# Define Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (5, 210, 80)
RED = (200, 0, 20)
BLUE = (80, 10, 250)
ORANGE = (255, 165, 0)
PINK = (255, 192, 203)

# Set dimensions
WIDTH = 600
HEIGHT = 600
BLOCK_SIZE = 20

# Set up display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Snake Game")

# Initialize clock for controlling the frame rate
clock = pygame.time.Clock()

# Fonts for displaying score and level
font_style = pygame.font.SysFont("bahnschrift", 25)
score_font = pygame.font.SysFont("comicsansms", 35)

def display_score(score, level):
    """Displays the current score and level on the screen."""
    value = score_font.render("Score: " + str(score), True, WHITE)
    level_text = score_font.render("Level: " + str(level), True, WHITE)
    screen.blit(value, [0, 0])
    screen.blit(level_text, [WIDTH - 120, 0])

def draw_snake(snake_block, snake_list):
    """Draws the snake on the screen."""
    for x in snake_list:
        pygame.draw.rect(screen, GREEN, [x[0], x[1], snake_block, snake_block])

def generate_food(snake_list):
    """Generates food with random weights and colors that do not overlap with the snake."""
    while True:
        food_x = random.randrange(1, (WIDTH - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        food_y = random.randrange(1, (HEIGHT - BLOCK_SIZE) // BLOCK_SIZE) * BLOCK_SIZE
        weight = random.choice([10, 30, 50])  # Food weights: 10, 30, 50
        if weight == 10:
            color = RED
            timer = 5
        elif weight == 30:
            color = ORANGE
            timer = 10
        else:
            color = PINK
            timer = 15
        if [food_x, food_y] not in snake_list:
            return [food_x, food_y, weight, color, timer]

def message(msg, color):
    """Displays a message on the screen."""
    mesg = font_style.render(msg, True, color)
    screen.blit(mesg, [WIDTH / 6, HEIGHT / 3])

def gameLoop():
    """Main game loop."""
    game_over = False
    game_close = False

    x1 = WIDTH // 2
    y1 = HEIGHT // 2

    x1_change = 0
    y1_change = 0

    snake_list = []
    length_of_snake = 1

    score = 0
    level = 1

    food = generate_food(snake_list)
    food_timer = time.time()  # Timer for food disappearance

    while not game_over:
        while game_close:
            screen.fill(BLUE)
            message("Game Over! Press Q-Quit or C-Play Again", RED)
            display_score(score, level)
            pygame.display.update()

            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_q:
                        game_over = True
                    if event.key == pygame.K_c:
                        gameLoop()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    x1_change = -BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_RIGHT:
                    x1_change = BLOCK_SIZE
                    y1_change = 0
                elif event.key == pygame.K_UP:
                    y1_change = -BLOCK_SIZE
                    x1_change = 0
                elif event.key == pygame.K_DOWN:
                    y1_change = BLOCK_SIZE
                    x1_change = 0

        if x1 >= WIDTH or x1 < 0 or y1 >= HEIGHT or y1 < 0:
            game_close = True

        x1 += x1_change
        y1 += y1_change
        screen.fill(BLUE)

        pygame.draw.rect(screen, food[3], [food[0], food[1], BLOCK_SIZE, BLOCK_SIZE])

        snake_head = [x1, y1]
        snake_list.append(snake_head)
        if len(snake_list) > length_of_snake:
            del snake_list[0]

        for x in snake_list[:-1]:
            if x == snake_head:
                game_close = True

        draw_snake(BLOCK_SIZE, snake_list)
        display_score(score, level)
        pygame.display.update()

        # Check if food should disappear based on its timer
        if time.time() - food_timer > food[4]:
            food = generate_food(snake_list)
            food_timer = time.time()

        if x1 == food[0] and y1 == food[1]:
            length_of_snake += food[2] // 10  # Increase length based on food weight
            score += food[2]  # Increase score based on food weight
            food = generate_food(snake_list)
            food_timer = time.time()  # Reset the food timer

            if score >= level * 30:
                level += 1
                clock.tick(10 + level)

        clock.tick(10 + level)

    pygame.quit()
    quit()

gameLoop()
