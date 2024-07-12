import Player
import Bullet
import pygame
import Star
import Enemy
import Lives
import random
from pygame import mixer

#Initialize pygame
pygame.init()

#Starting the mixer
mixer.init()

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

while running:
    #Use Delta Time: Implement delta time for frame-independent movement.
    dt = clock.tick(60) / 1000.0

    time_since_last_shot += dt  # Update the cooldown timer
    time_since_last_spawn += dt #Update spawn timer

    #Clear Screen
    screen.fill((0,0,0))

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
    
    clock.tick(0)

pygame.quit()
