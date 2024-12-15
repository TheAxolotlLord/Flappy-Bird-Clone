import pygame
import random
import os

# Initialize Pygame
pygame.init()

# Constants
SCREEN_WIDTH = 400 * 2
SCREEN_HEIGHT = 600 * 2
BIRD_WIDTH = 17 * 3
BIRD_HEIGHT = 18 * 3
PIPE_WIDTH = 80
PIPE_GAP =  200
PIPE_VELOCITY = 5
GRAVITY = 0.5
JUMP_STRENGTH = -10

# Set up the screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird')

# Colors 
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (135, 206, 235)

# Load bird image
current_dir = os.path.dirname(__file__)  # Gets the directory of the script
image_folder = os.path.join(current_dir, 'images')  # Joins with the 'images' folder
bird_img = pygame.image.load(os.path.join(image_folder, 'bird.png'))
bird_img = pygame.transform.scale(bird_img, (BIRD_WIDTH, BIRD_HEIGHT))

# Bird class
class Bird:
    def __init__(self):
        self.x = 50
        self.y = SCREEN_HEIGHT // 2
        self.velocity = 0
    
    def move(self):
        self.velocity += GRAVITY 
        self.y += self.velocity 

    def jump(self):
        self.velocity = JUMP_STRENGTH

    def draw(self): 
        screen.blit(bird_img, (self.x, self.y))  # Draw bird image

# Pipe class
class Pipe:
    def __init__(self):
        self.x = SCREEN_WIDTH
        self.height = random.randint(100, SCREEN_HEIGHT - PIPE_GAP - 100)  # Random height for the top pipe
        self.top_rect = pygame.Rect(self.x, 0, PIPE_WIDTH, self.height)  # Top pipe position and size
        self.bottom_rect = pygame.Rect(self.x, self.height + PIPE_GAP, PIPE_WIDTH, SCREEN_HEIGHT - self.height - PIPE_GAP)  # Bottom pipe position and size

    def move(self):
        self.x -= PIPE_VELOCITY
        self.top_rect.x = self.x
        self.bottom_rect.x = self.x

    def draw(self):
        # Draw the top pipe (green color)
        pygame.draw.rect(screen, GREEN, self.top_rect)
        # Draw the bottom pipe (green color)
        pygame.draw.rect(screen, GREEN, self.bottom_rect)

# Game loop
def game():
    bird = Bird()
    pipes = []
    clock = pygame.time.Clock()
    score = 0
    game_over = False

    while not game_over:
        screen.fill((135, 206, 235))  # Background color (light blue)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_over = True
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                bird.jump()

        bird.move()

        # Create pipes
        if len(pipes) == 0 or pipes[-1].x < SCREEN_WIDTH - 400:
            pipes.append(Pipe())

        # Move and draw pipes
        for pipe in pipes[:]:
            pipe.move()
            pipe.draw()
            if pipe.x + PIPE_WIDTH < 0:
                pipes.remove(pipe)
                score += 1  # Increase score when pipe moves out of screen

        # Check for collisions
        for pipe in pipes:
            if bird.y < 0 or bird.y + BIRD_HEIGHT > SCREEN_HEIGHT:
                game_over = True
            if pipe.top_rect.colliderect(pygame.Rect(bird.x, bird.y, BIRD_WIDTH, BIRD_HEIGHT)) or \
               pipe.bottom_rect.colliderect(pygame.Rect(bird.x, bird.y, BIRD_WIDTH, BIRD_HEIGHT)):
                game_over = True

        bird.draw()

        # Display score
        font = pygame.font.SysFont("Arial", 32)
        score_text = font.render(f"Score: {score}", True, (255, 255, 255))
        screen.blit(score_text, (10, 10))

        pygame.display.update()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    game()
