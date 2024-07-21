import pygame 
import math 
from pygame import mixer

class Enemy:
    def __init__(self, posx, posy):
        try:
            self.enemy_img = pygame.image.load("assets/Enemy_Spaceship.png").convert_alpha()
            self.dmg_img = pygame.image.load("assets/Inv_Spaceship.png").convert_alpha()
        except pygame.error as e:
            print(f"Error loading image: {e}")
            return
        self.pos_x, self.pos_y = posx, posy
        self.base_speed = 200
        self.speed = self.base_speed
        self.health = 5
        #self.enemy_img = pygame.transform.rotate(self.enemy_img, 180)
        self.dmg_img = pygame.transform.rotate(self.dmg_img, 180)
        self.original_enemy_img = self.enemy_img #keep copy of the orginal image
        self.original_dmg_img = self.dmg_img #keep copy of the original dmg image
        self.damaged = False
        self.damaged_time = 0 # Time when the enemy was last damaged
        try:
            self.death_sound = mixer.Sound("audio/retro-explosion-2.wav")
            self.death_sound.set_volume(0.1)
        except pygame.error as e:
            print(f"Error loading sound: {e}")
            self.death_sound = None

        self.sound_played = False #Flag to track if the sound has been played
        self.angle = 0 #Initial angle
 

    def move_towards_player(self, player, dt):
        #Find direction vector (dx, dy) between enemy and player
        dx = player.pos_x - self.pos_x
        dy = player.pos_y - self.pos_y

        #Calculate distance
        distance = math.sqrt(dx ** 2 + dy ** 2)

        if distance != 0:
            #Normalize the direction vector
            dx /= distance
            dy /= distance
        
        self.angle = math.degrees(math.atan2(dy, dx)) +90
        
        #Update the enemy position
        self.pos_x += dx * self.speed * dt
        self.pos_y += dy * self.speed * dt
    
    def draw(self, screen):
        #Rotate the enmey image based on the angle
        rotated_enemy_img = pygame.transform.rotate(self.original_enemy_img, -self.angle)
        rotated_dmg_img = pygame.transform.rotate(self.original_dmg_img, -self.angle)
        rotated_rect = rotated_enemy_img.get_rect(center=(self.pos_x, self.pos_y))
        if self.damaged:
            screen.blit(rotated_dmg_img, rotated_rect.topleft)
        else:
            screen.blit(rotated_enemy_img, rotated_rect.topleft)
    
    def draw_collision_rect(self, screen):
        # Get the rotated image and its rectangle centered at the enemy's position
        rotated_img = pygame.transform.rotate(self.enemy_img, -self.angle)
        rotated_rect = rotated_img.get_rect(center=(self.pos_x, self.pos_y))
        # Draw the collision rectangle around the enemy
        rect = self.rect()
        pygame.draw.rect(screen, (255, 0, 0), rotated_rect, 2)  # Red color, 2 pixels thick
    
    def draw_dmg(self, screen):
    # Temporarily set the damaged flag and draw the damaged image
        self.damaged = True
        self.draw(screen)
        self.damaged = False

    def take_dmg(self):
        self.health -= 1
        self.damaged = True
        # Optionally, set a timer to switch back to normal image after some time
        self.damaged_time = pygame.time.get_ticks() # Get current time

    def update(self):
        #Check if the damged stae should be reset
        if self.damaged and pygame.time.get_ticks() - self.damaged_time > 300: #500 ms
            self.damaged = False
    
    def is_alive(self):
        return self.health > 0
    
    def play_sound(self):
        try:
            channel = mixer.Channel(1)
            if channel: 
                channel.play(self.death_sound)
            else:
                print("No Available Channels to play")
        except pygame.error as e:
            print(f"Pygame error occurred: {e}")

    def rect(self):
        rotated_img = pygame.transform.rotate(self.enemy_img, -self.angle)
        rotated_rect = rotated_img.get_rect(center=(self.pos_x, self.pos_y))
        return self.enemy_img.get_rect(topleft = (self.pos_x, self.pos_y))
    
    def increase_speed(self, factor):
        self.speed = self.base_speed * factor