import pygame, sys
from pygame.locals import *
import random

# Initialize Pygame
pygame.init()

FPS = 60
FramePerSec = pygame.time.Clock()

# Colors
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

SCREEN_WIDTH = 400
SCREEN_HEIGHT = 600

DISPLAYSURF = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Racing Game")

# Load images
player_image = pygame.image.load("Player.png")
enemy_image = pygame.image.load("Enemy.png")
coin_images = [pygame.image.load("Coin.png"), pygame.image.load("Coin1.png"), pygame.image.load("Coin2.png")]
road_image = pygame.image.load("Road.jpg")

# Scale images
player_image = pygame.transform.scale(player_image, (50, 70))
enemy_image = pygame.transform.scale(enemy_image, (50, 70))
coin_images = [pygame.transform.scale(coin, (30, 30)) for coin in coin_images]
road_image = pygame.transform.scale(road_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

score = 0
font = pygame.font.SysFont('Arial', 36)

# Function to display the game over screen
def game_over_screen():
    game_over_text = font.render("Game Over", True, RED)
    final_score_text = font.render(f"Your Score: {score}", True, GREEN)
    exit_text = font.render("Press Q to Exit", True, BLUE)

    DISPLAYSURF.fill(WHITE)
    DISPLAYSURF.blit(game_over_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 3 - 50))
    DISPLAYSURF.blit(final_score_text, (SCREEN_WIDTH // 3, SCREEN_HEIGHT // 2))
    DISPLAYSURF.blit(exit_text, (SCREEN_WIDTH // 4, SCREEN_HEIGHT // 2 + 50))

    pygame.display.update()

# Function to reset the game
def reset_game():
    global player, enemy, background_y, score, coins, enemy_speed
    player = Player()
    enemy = Enemy()
    coins = pygame.sprite.Group()
    background_y = 0
    score = 0
    enemy_speed = 10  # Initial speed of the enemy
    for _ in range(5):
        coins.add(Coin())

# Define the Enemy class
class Enemy(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = enemy_image
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    # Move the enemy
    def move(self):
        self.rect.move_ip(0, enemy_speed)
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.top = 0
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)

    # Draw the enemy on the screen
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Define the Player class
class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = player_image
        self.rect = self.image.get_rect()
        self.rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT - 100)
        self.last_position_y = self.rect.y

    # Update the player's position
    def update(self):
        pressed_keys = pygame.key.get_pressed()

        if self.rect.left > 0:
            if pressed_keys[K_LEFT]:
                self.rect.move_ip(-5, 0)
        if self.rect.right < SCREEN_WIDTH:
            if pressed_keys[K_RIGHT]:
                self.rect.move_ip(5, 0)

        if self.rect.y < self.last_position_y - 15:
            global score
            score += 10
            self.last_position_y = self.rect.y

    # Draw the player on the screen
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Define the Coin class
class Coin(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = random.choice(coin_images)  # Randomly select one of the three coin images
        self.rect = self.image.get_rect()
        self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        self.weight = self.assign_weight()  # Assign a weight based on the coin image

    # Assign weight based on the coin image
    def assign_weight(self):
        if self.image == coin_images[0]:
            return 1  # Coin.png
        elif self.image == coin_images[1]:
            return 3  # Coin1.png
        elif self.image == coin_images[2]:
            return 5  # Coin2.png

    # Update the coin's position
    def update(self):
        if self.rect.top > SCREEN_HEIGHT:
            self.rect.center = (random.randint(40, SCREEN_WIDTH - 40), 0)
        else:
            self.rect.move_ip(0, 5)

    # Draw the coin on the screen
    def draw(self, surface):
        surface.blit(self.image, self.rect)

# Function to save the high score
def save_high_score(score):
    with open("high_score.txt", "w") as f:
        f.write(str(score))

# Function to load the high score
def load_high_score():
    try:
        with open("high_score.txt", "r") as f:
            return int(f.read())
    except FileNotFoundError:
        return 0

# Initialize game elements
all_sprites = pygame.sprite.Group()
enemies = pygame.sprite.Group()
coins = pygame.sprite.Group()

player = Player()
enemy = Enemy()

all_sprites.add(player)
all_sprites.add(enemy)
enemies.add(enemy)

for _ in range(5):
    coin = Coin()
    all_sprites.add(coin)
    coins.add(coin)

background_y = 0
enemy_speed = 10  # Initial speed of the enemy
coins_collected = 0  # Initialize the counter for collected coins

load_high_score()

coin_spawn_timer = pygame.time.get_ticks()
coin_spawn_delay = 2000

game_running = True
while game_running:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()

    if pygame.time.get_ticks() - coin_spawn_timer > coin_spawn_delay:
        coin_spawn_timer = pygame.time.get_ticks()
        new_coin = Coin()
        all_sprites.add(new_coin)
        coins.add(new_coin)

    if pygame.sprite.spritecollide(player, enemies, False):
        game_over_screen()

        waiting_for_input = True
        while waiting_for_input:
            for event in pygame.event.get():
                if event.type == KEYDOWN:
                    if event.key == K_q:
                        save_high_score(score)
                        pygame.quit()
                        sys.exit()
                if event.type == QUIT:
                    save_high_score(score)
                    pygame.quit()
                    sys.exit()

    if game_running:
        player.update()
        for e in enemies:
            e.move()
        for c in coins:
            c.update()

        collected_coins = pygame.sprite.spritecollide(player, coins, True)
        for coin in collected_coins:
            score += coin.weight * 10  # Increase score based on coin weight
            coins_collected += 1

            # Increase enemy speed after collecting N coins
            if coins_collected % 5 == 0:
                enemy_speed += 2

        background_y += 5
        if background_y >= SCREEN_HEIGHT:
            background_y = 0

        DISPLAYSURF.fill(WHITE)
        DISPLAYSURF.blit(road_image, (0, background_y - SCREEN_HEIGHT))
        DISPLAYSURF.blit(road_image, (0, background_y))

        all_sprites.draw(DISPLAYSURF)

        score_text = font.render(f"Score: {score}", True, BLUE)
        DISPLAYSURF.blit(score_text, (SCREEN_WIDTH - score_text.get_width() - 20, 20))

        pygame.display.update()

    FramePerSec.tick(FPS)
