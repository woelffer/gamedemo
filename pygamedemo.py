import Player
import Bullet
import pygame
import Star
import Enemy
import Lives
import HUD
import random
import math
import Levels
import json
from pygame import mixer
import numpy as np

#Starting the mixer
pygame.mixer.pre_init(44100, -16, 2, 4096)
pygame.mixer.init()

#load music tracks 
music_tracks = {
    'theme': 'audio/retro_song.mp3',
    'song_2': 'audio/Game_Temp.wav'
    }

#Function to play a specific track
def play_music(track_name, loop = True):
    if pygame.mixer.music.get_busy():
        pygame.mixer.music.stop()
    
    pygame.mixer.music.load(music_tracks[track_name])
    loop_count = -1 if loop else 0
    pygame.mixer.music.play(loop_count)
    pygame.mixer.music.set_volume(0.1)  # Adjust volume if needed

current_track = 'theme'
play_music(current_track)



#Initialize pygame

pygame.init()

#LOad title screen image
title_screen_img = pygame.image.load('assets/Title_Screen_nobg.png')
 
clock = pygame.time.Clock()
#Screen Dimensions
screen_width, screen_height = 1280, 720
pygame.display.set_caption("Aerials")
screen = pygame.display.set_mode((screen_width, screen_height), pygame.DOUBLEBUF | pygame.HWSURFACE)

#Initialize HUD
HUD_model = HUD.HUD()

#Initialize Player, Lives, Enemy class objects
player_model = Player.Player()
enemies = [Enemy.Enemy(0, 0, False), Enemy.Enemy(400, 0, False), Enemy.Enemy(600, 0, False)]  # List of enemies
lives_model = Lives.Lives()



#Bullet initialize
bullet_speed = -500
bullets = []
enemy_bullets = []

#Can ADJUST THIS WHEN WE Introduce levels and powerups
BULLET_COOLDOWN = 0.05
ENEMY_BULLET_CD = 0.4

# Track the time since the last bullet was fired
time_since_last_shot = 0
time_enemy_last_shot = 0


running = True
game_over = False # Flag to track game over state

# Initialize stars
star_img = pygame.image.load("assets/Star.png").convert_alpha()  # Load the star image
num_stars = 100
stars = [Star.Star(star_img, screen_width, screen_height) for _ in range(num_stars)]

#Variables for spawning enemies
SPAWN_INTERVAL = 0.3 #Seconds between spawns
time_since_last_spawn = 0
#seed = random.seed(10)
#used for differeniating star images as they appear to share the same memory address so python can't interpret a new star image
# Requires numpy package to work properly 
def images_different(img1, img2):
    arr1 = pygame.surfarray.array3d(img1)
    arr2 = pygame.surfarray.array3d(img2)
    return not np.array_equal(arr1, arr2)



def spawn_enemy():
    x_pos = random.randint(0, screen_width - 64) #Enemy width 64 pixels 
    y_pos = -64 #start offscreen
    rand = random.randrange(0, 9)
    if rand >= 5:
        new_enemy = Enemy.Enemy(x_pos, y_pos, True)
        enemies.append(new_enemy)
    elif rand <= 4: 
        new_enemy = Enemy.Enemy(x_pos, y_pos, False)
        enemies.append(new_enemy)
   

# Initialize score thresholds
score_thresholds = {
    5000: 'theme',
    10000: 'song_2'
}

# Track the current song
def update_music(score):
    global current_track
    new_track = None

    if score >= 10000:
        new_track = 'song_2'
    elif score >= 5000:
        new_track = 'theme'

    if new_track and current_track != new_track:
        current_track = new_track
        play_music(current_track)


def reset_music():
    global current_track
    current_track = 'theme'
    play_music(current_track)

level = Levels.Levels(stars, screen, screen_width, screen_height, title_screen_img, clock, HUD_model)
level.TitleScreen()

current_level_name = 'The Starstruck Plains'





while running:
    ###
    ### Time settings and clock setup/ clear screen each frame
    ###
    #Use Delta Time: Implement delta time for frame-independent movement.
    dt = clock.tick(60) / 1000.0

    time_since_last_shot += dt  # Update the cooldown timer
    time_since_last_spawn += dt #Update spawn timer
    time_enemy_last_shot += dt # update the enemy bullet timer
    
    update_music(HUD_model.score)

    # Check score and update star image if necessary
    if HUD_model.score >= 10000:
        new_star_img = pygame.image.load("assets/Star_3.png").convert_alpha()
        new_level_name = 'Corrupted Spaceport'
    elif HUD_model.score >= 5000:
        new_star_img = pygame.image.load("assets/Star_2.png").convert_alpha()
        new_level_name = 'Spaces Between'
    else:
        new_star_img = pygame.image.load("assets/Star.png").convert_alpha()
        new_level_name = 'The Starstruck Plains'
    
    
    # Compare image content
    if images_different(star_img, new_star_img):
        star_img = new_star_img
        for star in stars:
            star.star_img = star_img  # Update the star image attribute

    # Update level name if it has changed
    if new_level_name != current_level_name:
        current_level_name = new_level_name
        HUD_model.draw_levelName(screen, current_level_name)  # Update the level name

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

        time_since_last_shot = 0
        new_bullets = Bullet.Bullet.create_bullets(player_model, bullet_speed)
        bullets.extend(new_bullets)

    #Spawn new enemies at intervals 
    if time_since_last_spawn >= SPAWN_INTERVAL:
         spawn_enemy()
         time_since_last_spawn = 0

    # List to keep track of enemies to be removed
    enemies_to_remove = set()
    bullets_to_remove = set()
    enemy_bullets_to_remove = set()
    

    speed_factor = 1 + (HUD_model.score // 5000) * 0.5  # Increase speed by 50% for every 5000 points
    
    # code for enemies to shoot - Uses the angle to determine firing position then shoots along that delta. 
    for enemy in enemies:
        if enemy.shooter_tag is True and time_enemy_last_shot >= ENEMY_BULLET_CD:              
            enemy_bullet = Bullet.Bullet((enemy.pos_x, enemy.pos_y), bullet_speed, player_model.pos_x, player_model.pos_y, bullet_type='enemy')
            enemy_bullets.extend(enemy_bullet.create_enemy_bullets(enemy, bullet_speed, player_model.pos_x, player_model.pos_y))    
            time_enemy_last_shot = 0
            


    for enemy in enemies:
        enemy.increase_speed(speed_factor)

    # Check for bullet collisions with enemies and bullet out of bounds
    for bullet in bullets:
        print("This is a player bullet address: ", bullet)
        if not bullet.rect() in screen.get_rect(): #remove bullet if bullet no longer on screen
            bullets_to_remove.add(bullet)
            #print(bullet)
        for enemy in enemies:
            if bullet.rect().colliderect(enemy.rect()):
                enemy.take_dmg()
                bullets_to_remove.add(bullet)  # Remove bullet after collision
                if not enemy.is_alive():
                    enemies_to_remove.add(enemy)  # Remove enemy if health is zero

                break  # Exit the inner loop to avoid modifying the list during iteration 
            
    # Check for enemy bullet out of bounds and enemy bullet collide with player model
    for enemy_bullet in enemy_bullets:
        print("This is a enemy bullet address:", enemy_bullet)
        if not enemy_bullet.rect().colliderect(screen.get_rect()):
            enemy_bullets_to_remove.add(enemy_bullet)
            print(enemy_bullets)
        
        if enemy_bullet.rect().colliderect(player_model.rect()):
            enemy_bullets_to_remove.add(enemy_bullet)
            player_model.take_dmg()
            print(enemy_bullets)
            break





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

    #update the player's state and animations

    player_model.update_position(dt)

    #Draw player and the line
    player_model.draw(screen)

    player_model.update_circle(dt)
    player_model.draw_circle(screen)

    #HUD update/ draw callsd
    HUD_model.draw_abilities(screen, player_model)
    HUD_model.draw_lives(screen, player_model.lives)

    # Remove marked enemies and bullets
    for enemy in enemies_to_remove:
        enemy.play_sound()
        enemy.sound_played = True #Set flag to indicat the sound has been playedS
        enemies.remove(enemy)
        HUD_model.update_score(200)
    
    #Update and draw stars
    for star in stars:
        star.move(dt)
        star.draw(screen)
  
    for bullet in bullets_to_remove: 
        if bullet in bullets:             
            bullets.remove(bullet)
    
    # Remove enemy bullets
    for enemy_bullet in enemy_bullets_to_remove:
        if enemy_bullet in enemy_bullets:
            enemy_bullets.remove(enemy_bullet)
 
    for bullet in bullets:
        bullet.move(dt)
        screen.blit(bullet.bullet_img, (bullet.pos_x, bullet.pos_y))
    
    for enemy_bullet in enemy_bullets:
        enemy_bullet.enemy_bullet_move(dt)
        screen.blit(enemy_bullet.bullet_img, (enemy_bullet.pos_x, enemy_bullet.pos_y))

    # Move and update enemies/lives/bullets/score
    for enemy in enemies:
        print(enemy.shooter_tag)
        if enemy.shooter_tag == True:
            enemy.move_to_shoot(player_model, dt)
        elif enemy.shooter_tag == False:
            enemy.move_towards_player(player_model, dt)
        enemy.update()
        enemy.draw(screen)
        #enemy.draw_collision_rect(screen)
          
    player_model.update(dt)
    

    #draw the score and level name from HUD class
    screen.blit(HUD_model.draw_score(screen), HUD_model.score_rect_pos)
    screen.blit(HUD_model.draw_levelName(screen, current_level_name), HUD_model.levelName_rect)
    
    
    if player_model.lives <= 0:
        level.EndScreen(player_model, lives_model, bullets, enemies, enemy_bullets, time_since_last_spawn, time_since_last_shot, HUD_model)
        reset_music() #Ensure music is reset on game restart
        # Optionally break out of the loop after game over handling
        #running = False

    pygame.display.flip()
    
    clock.tick(60)

pygame.quit()
