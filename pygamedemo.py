import Player
import Bullet
import pygame
import Star
import Enemy
import Lives
import HUD
import random
import math
import json
from pygame import mixer

#Starting the mixer
pygame.mixer.pre_init(44100, 16, 2, 4096)
mixer.init()
theme = mixer.Sound('audio/retro_song.mp3')
channel = mixer.Channel(3)
channel.play(theme, loops=-1) #Loop the music indefinitely
channel.set_volume(0.1)

#Initialize pygame

pygame.init()

#Load quotes from JSON file
with open('assets/quotes.json') as f:
    quotes_data = json.load(f)

#Extract quotes array
quotes = quotes_data['quotes']

#Select a random quote
random_quote = random.choice(quotes)


#LOad title screen image
title_screen_img = pygame.image.load('assets/Title_Screen_nobg.png')
 

#Screen Dimensions
screen_width, screen_height = 1280, 720
pygame.display.set_caption("Aerials")
screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF | pygame.HWSURFACE)

#Initialize HUD
HUD_model = HUD.HUD()

#Initialize Player, Lives, Enemy class objects
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


clock = pygame.time.Clock()
running = True
game_over = False # Flag to track game over state

# Initialize stars
star_img = pygame.image.load("assets/Star.png").convert_alpha()  # Load the star image
num_stars = 100
stars = [Star.Star(star_img, screen_width, screen_height) for _ in range(num_stars)]

#Variables for spawning enemies
SPAWN_INTERVAL = 0.3 #Seconds between spawns
time_since_last_spawn = 0

def spawn_enemy():
     x_pos = random.randint(0, screen_width - 64) #Enemy width 64 pixels 
     y_pos = -64 #start offscreen
     new_enemy = Enemy.Enemy(x_pos, y_pos)
     enemies.append(new_enemy)

# Load font for the title screen prompt
prompt_font = pygame.font.Font('freesansbold.ttf', 28)
prompt_text = prompt_font.render('Press [Enter] to Start', True, HUD_model.WHITE)
prompt_rect = prompt_text.get_rect(center=(screen_width // 2, screen_height // 2 + 100))

#Title Screen Loop

title_screen_active = True

while title_screen_active:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN: #Enter to start 
                title_screen_active = False

    #Clear screen
    screen.fill((0,0,0))

    #Update and draw stars
    for star in stars:
        star.move(1/60.0) #Use a fixed dt for consistent movement
        star.draw(screen)
    
    #Draw Title
    screen.blit(title_screen_img, (screen_width // 2 - title_screen_img.get_width() // 2,
                                   screen_height // 2 - title_screen_img.get_height() // 2))
    
    #Draw the "Press [Enter] prompt"
    screen.blit(prompt_text, prompt_rect)
    
    #Update display
    pygame.display.flip()

    clock.tick(60)




while running:
    ###
    ### Time settings and clock setup/ clear screen each frame
    ###
    #Use Delta Time: Implement delta time for frame-independent movement.
    dt = clock.tick(60) / 1000.0

    time_since_last_shot += dt  # Update the cooldown timer
    time_since_last_spawn += dt #Update spawn timer

    #Clear Screen
    screen.fill((0,0,0))


    ###
    ### Event handling and what have you
    ###

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

    # List to keep track of enemies to be removed
    enemies_to_remove = set()
    bullets_to_remove = set()
    

   
    speed_factor = 1 + (HUD_model.score // 5000) * 0.5  # Increase speed by 50% for every 5000 points
    for enemy in enemies:
        enemy.increase_speed(speed_factor)

    # Check for bullet collisions with enemies
    
    for bullet in bullets:
        #print(bullet)
        for enemy in enemies:
            if bullet.rect().colliderect(enemy.rect()):
                enemy.take_dmg()
                bullets.remove(bullet)  # Remove bullet after collision
                if not enemy.is_alive():
                    enemies_to_remove.add(enemy)  # Remove enemy if health is zero
            if not bullet.rect() in screen.get_rect():
                bullets.remove(bullet)
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
    
                    
    #####
    ##### Update/Draw calls each frame below
    #####
    
    #Player update/draw calls
    screen.blit(player_model.player_img, (player_model.pos_x, player_model.pos_y))
    player_model.update_circle(dt)
    player_model.draw_circle(screen)

    #HUD update/ draw calls
    HUD_model.draw_abilities(screen, player_model)
    HUD_model.draw_lives(screen, player_model.lives)

    # Remove marked enemies and bullets
    for enemy in enemies_to_remove:
        enemy.play_sound()
        enemy.sound_played = True #Set flag to indicat the sound has been playedS
        enemies.remove(enemy)
        HUD_model.update_score()
    
    #Update and draw stars
    for star in stars:
        star.move(dt)
        star.draw(screen)
  
    for bullet in bullets_to_remove:
        bullets.remove(bullet)
 
    for bullet in bullets:
        bullet.move(dt)
        screen.blit(bullet.bullet_img, (bullet.pos_x, bullet.pos_y)) 

    # Move and update enemies/lives/bullets/score
    for enemy in enemies:
        enemy.move_towards_player(player_model, dt)
        enemy.update()
        enemy.draw(screen)
        #enemy.draw_collision_rect(screen)
          
    player_model.update(dt)
    

    #draw the score and level name from HUD class
    screen.blit(HUD_model.draw_score(screen), HUD_model.score_rect_pos)
    screen.blit(HUD_model.draw_levelName(screen, 'The Starstruck Plains'), HUD_model.levelName_rect)
    
    
    if player_model.lives <= 0:
        game_over = True

    pygame.display.flip()
    
    clock.tick(60)
    print(clock.get_fps())
    #Game over screen

    while game_over:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                game_over = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    # Reset game state
                    player_model.reset()
                    lives_model.reset()
                    HUD_model.reset()
                    bullets.clear()
                    enemies.clear()
                    game_over = False
                    # Reset time variables
                    time_since_last_spawn = 0
                    time_since_last_shot = 0

                    random_quote = random.choice(quotes)

        screen.fill((0, 0, 0))
        game_over_font = pygame.font.Font('freesansbold.ttf', 64)
        game_over_text = game_over_font.render('YOU DIED', True, (255, 0, 0))
        game_over_rect = game_over_text.get_rect(center=(screen_width // 2, screen_height // 2))
        screen.blit(game_over_text, game_over_rect)
        screen.blit(HUD_model.draw_score(screen), HUD_model.score_rect_pos)

            # Draw "Press [Enter] to restart" prompt
        prompt_font = pygame.font.Font('freesansbold.ttf', 32)
        prompt_text = prompt_font.render('Press [Enter] to restart', True, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(center=(screen_width // 2, screen_height // 2 + 50))
        screen.blit(prompt_text, prompt_rect)

        # Display random quote
        quote_font = pygame.font.Font('freesansbold.ttf', 24)
        quote_text = quote_font.render(random_quote, True, (255, 255, 255))
        quote_rect = quote_text.get_rect(center=(screen_width // 2, screen_height // 2 + 200))
        screen.blit(quote_text, quote_rect)

         #Update and draw stars
        for star in stars:
            star.move(1/60.0) #Use a fixed dt for consistent movement
            star.draw(screen)
    

        pygame.display.flip()

        clock.tick(60)


pygame.quit()
