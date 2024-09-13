import pygame
from ob import Player, Road, Tree, Pr
import random

pygame.init()

# Set screen dimensions
SCREEN = WIDTH, HEIGHT = 288, 512
win = pygame.display.set_mode(SCREEN)

clock = pygame.time.Clock()
FPS = 10

# Define colors
BLUE = (30, 144, 255)
WHITE = (255, 255, 255)  # Color for blinking effect
RED = (255, 0, 0)        # Color for crash display

# Load images
home_img = pygame.image.load('home.png')
bg = pygame.image.load('bg.png')  # Background image
bg = pygame.transform.scale(bg, (WIDTH, HEIGHT))  # Resize to fit screen

p = Player(100, HEIGHT - 120, 0)
move_left = False
move_right = False

road = Road()
speed = 2
tree_group = pygame.sprite.Group()
Pr_group = pygame.sprite.Group()

# Page control variables
home_page = False
game_page = True
counter = 0

# Collision and blinking variables
collision_count = 0
blink_count = 0
blink_interval = 10  # Number of frames to blink
blink_timer = 0

# Font for displaying text
font = pygame.font.Font(None, 36)

# Set window title
pygame.display.set_caption("Pygame window")

# Game loop
running = True
while running:
    win.fill(BLUE)

    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE or event.key == pygame.K_q:
                running = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x < WIDTH // 2:
                move_left = True
            else:
                move_right = True

        if event.type == pygame.MOUSEBUTTONUP:
            move_left = False
            move_right = False

    # Display the appropriate page
    if home_page:
        win.blit(home_img, (0, 0))  # Draw home page image
    if game_page:
        win.blit(bg, (0, 0))  # Draw game background
        road.draw(win)  # Draw the road
        road.update(speed)  # Update road position
        
        counter += 1
        if counter % 60 == 0:
            tree = Tree(random.choice([-5, WIDTH-35]), -20)
            tree_group.add(tree)
        tree_group.draw(win)
        tree_group.update(speed)
        if counter % 90 == 0:
            obs = random.choices([1, 2, 3], weights=[6, 2, 2], k=1)[0]
            obee = Pr(obs)
            Pr_group.add(obee)
        
        Pr_group.draw(win)
        Pr_group.update(speed)

        # Check for collisions between player and obstacles
        if pygame.sprite.spritecollideany(p, Pr_group):
            collision_count += 1
            if collision_count == 1:
                blink_count = blink_interval
            elif collision_count == 2:
                blink_count = blink_interval
            elif collision_count >= 3:
                print("Game Over!")
                running = False
            # Remove collided obstacles
            collided_objects = pygame.sprite.spritecollide(p, Pr_group, True)
            for obj in collided_objects:
                obj.kill()

        # Handle blinking effect
        if blink_count > 0:
            blink_timer += 1
            if blink_timer % blink_interval < blink_interval // 2:
                p.draw(win)  # Draw player with normal image
            else:
                # Draw player with a solid color to simulate blinking
                pygame.draw.rect(win, WHITE, p.rect)
            if blink_timer >= blink_interval * 2:
                blink_count = 0
                blink_timer = 0
        else:
            p.draw(win)  # Draw player with normal image

        # Draw the number of crashes on the screen
        crash_text = font.render(f'Crashes: {collision_count}', True, RED)
        win.blit(crash_text, (10, 10))

        # Update player movement
        p.update(move_left, move_right)

        # Update the display AFTER drawing everything
        pygame.display.update()

# Quit pygame
pygame.quit()
