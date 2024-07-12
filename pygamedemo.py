import Player
import Bullet
import pygame
import Star
import Enemy
import Lives
import random
import math
from pygame import mixer

#Initialize pygame
pygame.init()

#Starting the mixer
mixer.init()
theme = mixer.Sound('audio/retro_song.mp3')
channel = mixer.Channel(3)
channel.play(theme)

#Load ability icon 
circle_ability_icon = pygame.image.load("assets/circle.png")
circle_ability_icon = pygame.transform.scale(circle_ability_icon, (64, 64))

#Load font for text 
ability_font = pygame.font.Font('freesansbold.ttf', 24)

def draw_abilities(screen):
    screen_width, screen_height = screen.get_size()
    padding = 10
    icon_size = 64
    
    # Calculate positions
    circle_icon_pos = (screen_width - icon_size - padding, screen_height - icon_size - padding)

    # Draw ability icons
    screen.blit(circle_ability_icon, circle_icon_pos) 

    #Draw test next to ability
    text_surface = ability_font.render("Press 'E'", True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.right = circle_icon_pos[0] - padding
    text_rect.centery = circle_icon_pos[1] + icon_size // 2
    screen.blit(text_surface, text_rect)   
 
# Colors
white = (255, 255, 255)
black = (0, 0, 0)
score = 0

font = pygame.font.Font('freesansbold.ttf', 32)

def update_score_text():
    return font.render('SCORE: ' + str(score), True, white, black)

text = update_score_text()
textRect = text.get_rect()

#Initialize Player 
player_model = Player.Player()
enemies = [Enemy.Enemy(0, 0), Enemy.Enemy(400, 0), Enemy.Enemy(600, 0)]  # List of enemies
lives_model = Lives.Lives()

#Bullet initialize
bullet_speed = -500
bullets = []

#Can ADJUST THIS WHEN WE Introduce levels and powerups
BULLET_COOLDOWN = 0.05


# Track the time since the last bullet was fired
time_since_last_shot = 0

#Screen Dimensions
screen_width, screen_height = 1280, 720
pygame.display.set_caption("Galaga Clone")



screen = pygame.display.set_mode((screen_width, screen_height))
clock = pygame.time.Clock()
running = True

# Initialize stars
star_img = pygame.image.load("assets/Star.png")  # Load the star image
num_stars = 50
stars = [Star.Star(star_img, screen_width, screen_height) for _ in range(num_stars)]

#Variables for spawning enemies
SPAWN_INTERVAL = 0.3 #Seconds between spawns
time_since_last_spawn = 0

def spawn_enemy():
     x_pos = random.randint(0, screen_width - 64) #Enemy width 64 pixels 
     y_pos = -64 #start offscreen
     new_enemy = Enemy.Enemy(x_pos, y_pos)
     enemies.append(new_enemy)


# Function to draw abilities in the bottom right corner
def draw_abilities(screen, player):
    screen_width, screen_height = screen.get_size()
    padding = 10  # Padding from the edges
    icon_size = 64  # Size of the ability icon

    # Calculate positions
    circle_icon_pos = (screen_width - icon_size - padding, screen_height - icon_size - padding)

    # Draw ability icon
    screen.blit(circle_ability_icon, circle_icon_pos)

    # Draw text next to the ability icon
    current_time = pygame.time.get_ticks() / 1000  # Convert to seconds
    cooldown_remaining = max(0, player.ability_cooldown - (current_time - player.last_ability_use_time))
    if cooldown_remaining > 0:
        text_surface = ability_font.render(f"Cooldown: {cooldown_remaining:.1f}s", True, (255, 255, 255))
    else:
        text_surface = ability_font.render("Press 'E'", True, (255, 255, 255))
    text_rect = text_surface.get_rect()
    text_rect.right = circle_icon_pos[0] - padding
    text_rect.centery = circle_icon_pos[1] + icon_size // 2
    screen.blit(text_surface, text_rect)

while running:
    #Use Delta Time: Implement delta time for frame-independent movement.
    dt = clock.tick(60) / 1000.0

    time_since_last_shot += dt  # Update the cooldown timer
    time_since_last_spawn += dt #Update spawn timer

    #Clear Screen
    screen.fill((0,0,0))
    #aaaaaaaaadraw_abilities(screen)

    #Update and draw the player's circle
    player_model.update_circle(dt)
    player_model.draw_circle(screen)

    # Update and draw stars
    for star in stars:
        star.move(dt)
        star.draw(screen)

    #Draw Players
    screen.blit(player_model.player_img, (player_model.pos_x, player_model.pos_y))


    #screen.blit(enemy_model.enemy_img, (enemy_model.pos_x, enemy_model.pos_y))

    #Draw Player lives
    lives_model.draw(screen)


    #Update and draw bullets
    for bullet in bullets:
        bullet.move(dt)
        screen.blit(bullet.bullet_img, (bullet.pos_x, bullet.pos_y))            

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    key = pygame.key.get_pressed()
    moved = False

    player_model.handle_keys(dt, screen_width, screen_height)


    if key[pygame.K_SPACE] and time_since_last_shot >= BULLET_COOLDOWN:

        # Reset the cooldown timer
        time_since_last_shot = 0

        # Calculate the bullet positions relative to the player
        bullet_offset_1 = (54, 6)
        bullet_offset_2 = (4, 6)
        bullet_position_1 = [player_model.pos_x + bullet_offset_1[0], player_model.pos_y + bullet_offset_1[1]]
        bullet_position_2 = [player_model.pos_x + bullet_offset_2[0], player_model.pos_y + bullet_offset_2[1]]
        # Create new bullets and add them to the list
        new_bullet_1 = Bullet.Bullet(bullet_position_1, bullet_speed)
        new_bullet_2 = Bullet.Bullet(bullet_position_2, bullet_speed)
        new_bullet_1.play_sound()
        new_bullet_2.play_sound()
        bullets.append(new_bullet_1)
        bullets.append(new_bullet_2)
        if event.type == pygame.QUIT:
            running = False

    #Spawn new enemies at intervals 
    if time_since_last_spawn >= SPAWN_INTERVAL:
         spawn_enemy()
         time_since_last_spawn = 0

    #Draw stars
    for star in stars:
       star.draw(screen) 

    # Move bullets
    for bullet in bullets:
        bullet.move(dt)

    # List to keep track of enemies to be removed
    enemies_to_remove = set()
    bullets_to_remove = set()
    
    #Draw abilities in the bottom right corner
    draw_abilities(screen, player_model)

    # Check for bullet collisions with enemies
    for bullet in bullets:
        for enemy in enemies:
            if bullet.rect().colliderect(enemy.rect()):
                enemy.take_dmg()
                bullets_to_remove.add(bullet)  # Remove bullet after collision
                if not enemy.is_alive():

                    enemies_to_remove.add(enemy)  # Remove enemy if health is zero
                    
                break  # Exit the inner loop to avoid modifying the list during iteration           
   

    # Check for collisions between player and enemies
    for enemy in enemies:
        if player_model.rect().colliderect(enemy.rect()):
            player_model.take_dmg()
            enemies_to_remove.add(enemy)
            lives_model.remove_life()
            break
    
    #Check for circle collisions with enemies
    if player_model.circle_active:
        circle_center = (player_model.pos_x + player_model.player_img.get_width() // 2, player_model.pos_y + player_model.player_img.get_height() // 2)
        for enemy in enemies:
            enemy_center = (enemy.pos_x + enemy.enemy_img.get_width() // 2, enemy.pos_y + enemy.enemy_img.get_height() // 2)
            distance = math.sqrt((circle_center[0] - enemy_center[0]) ** 2 + (circle_center[1] - enemy_center[1]) ** 2)
            if distance < player_model.circle_radius + enemy.enemy_img.get_width() // 2: #Assume enemy is a cirle for simplicity
                enemy.health = 0
                if not enemy.is_alive():
                    enemies_to_remove.add(enemy)

    # Remove marked enemies and bullets
    for enemy in enemies_to_remove:
        enemy.play_sound()
        enemy.sound_played = True #Set flag to indicat the sound has been playedS
        enemies.remove(enemy)
        score += 200
        text = update_score_text()
    for bullet in bullets_to_remove:
        bullets.remove(bullet)


    # Move and update enemies
    for enemy in enemies:
        enemy.move_towards_player(player_model, dt)
        enemy.update()
        enemy.draw(screen)
          

    screen.blit(player_model.player_img, (player_model.pos_x, player_model.pos_y))
    
    lives_model.draw(screen)
    
    for bullet in bullets:
        screen.blit(bullet.bullet_img, (bullet.pos_x, bullet.pos_y))             


    screen.blit(text, textRect)

    pygame.display.flip()
    
    clock.tick(60)

pygame.quit()
