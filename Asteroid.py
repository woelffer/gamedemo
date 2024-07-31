import pygame
import json
import random

FRAME_WIDTH = 192
FRAME_HEIGHT = 192
ANIMATION_SPEED = 0.1

class Asteroid:
    def __init__(self, position, json_path, sprite_sheet):
        self.pos_x, self.pos_y = position
        self.sprite_sheet = pygame.image.load(sprite_sheet).convert_alpha()
        self.roll_frames = [self.sprite_sheet.subsurface(pygame.Rect(i * FRAME_WIDTH, 0, FRAME_WIDTH, FRAME_HEIGHT)) for i in range(5)]
        self.speed = random.randint(100, 300) #Random between 5 and 15
        self.direction = random.choice(["south", "southwest", "southeast"])
        self.frame_index = 0
        self.frame_counter = 0

        # Initialize rect to match the visible portion of the sprite
        self.rect = self.roll_frames[0].get_bounding_rect()

    def load_frames(self, json_path):
        with open(json_path) as f:
            data = json.load(f)
        frames = []
        for frame_name in data['frames']:
            frame_info = data['frames'][frame_name]['frame']
            x, y, w, h = frame_info['x'], frame_info['y'], frame_info['w'], frame_info['h']
            frame_surface = self.sprite_sheet.subsurface(pygame.Rect(x, y, w, h))
            self.roll_frames.append(frame_surface)
        # Update rect size to match the first frame
        self.rect = self.roll_frames[0].get_bounding_rect()

    def update(self, dt):
        #Update animation
        self.frame_counter += ANIMATION_SPEED
        if self.frame_counter >= 1:
            self.frame_counter = 0
            self.frame_index = (self.frame_index + 1) % len(self.roll_frames)
        
        # Update position based on direction
        if self.direction == "south":
            self.pos_y += self.speed * dt
        elif self.direction == "southwest":
            self.pos_x -= self.speed * dt
            self.pos_y += self.speed * dt
        elif self.direction == "southeast":
            self.pos_x += self.speed * dt
            self.pos_y += self.speed * dt
        
    # Get the current frame's bounding rectangle
        current_frame = self.roll_frames[self.frame_index]
        bounding_rect = current_frame.get_bounding_rect()

        # Calculate the offset caused by the bounding rectangle not starting at (0, 0)
        offset_x = bounding_rect.x
        offset_y = bounding_rect.y

        # Update the position of the rect to match the sprite's position plus offset
        self.rect = pygame.Rect(
            self.pos_x + offset_x, 
            self.pos_y + offset_y, 
            bounding_rect.width, 
            bounding_rect.height)


    def draw(self, screen):
        screen.blit(self.roll_frames[self.frame_index], (self.pos_x, self.pos_y))

        pygame.draw.rect(screen, (255, 0, 0, 127), self.rect, 2)