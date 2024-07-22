import pygame
from pygame import mixer 

class Bullet: 
    def __init__(self, position, speed):
        self.bullet_img = pygame.image.load("assets/Bullet.png").convert_alpha()
        self.bullet_sound = mixer.Sound("audio/8-bit-machine-gun.aiff")
        self.bullet_sound.set_volume(0.1)
        self.pos_x, self.pos_y = position
        self.speed = speed
    
    def move(self, dt):
        self.pos_y += self.speed * dt
    
    def rect(self):
        return self.bullet_img.get_rect(topleft =(self.pos_x, self.pos_y))

    def play_sound(self):
        channel = pygame.mixer.Channel(2)
        channel.play(self.bullet_sound)

    @staticmethod
    def create_bullets(player_model, bullet_speed):
        bullet_offset_1 = (54, 6)
        bullet_offset_2 = (4, 6)
        bullet_position_1 = [player_model.pos_x + bullet_offset_1[0], player_model.pos_y + bullet_offset_1[1]]
        bullet_position_2 = [player_model.pos_x + bullet_offset_2[0], player_model.pos_y + bullet_offset_2[1]]
        new_bullet_1 = Bullet(bullet_position_1, bullet_speed)
        new_bullet_2 = Bullet(bullet_position_2, bullet_speed)
        new_bullet_1.play_sound()
        new_bullet_2.play_sound()
        return [new_bullet_1, new_bullet_2]
    