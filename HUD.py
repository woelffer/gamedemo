import pygame

class HUD:
    def __init__(self):
        #set some basic colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        #set Score, score rect, levelname display rect:
        self.score_rect_pos = []
        self.score_rect = []
        self.levelName = ''
        self.levelName_rect = []
        self.score = 0
        self.remaining_lives = 3
        self.lives_rect_pos = []
        #Load ability icon 
        self.circle_ability_icon = pygame.image.load("assets/circle.png").convert_alpha()
        self.circle_ability_icon = pygame.transform.scale(self.circle_ability_icon, (64, 64))
        #load lives icon
        self.lives_img = pygame.image.load("assets/Spaceship.png").convert_alpha()
        self.lives_img = pygame.transform.scale(self.lives_img, (50, 50))
        #Load fonts for texts 
        self.ability_font = pygame.font.Font('freesansbold.ttf', 24)
        self.score_font = pygame.font.Font('freesansbold.ttf', 24)
        self.levelName_font = pygame.font.Font('freesansbold.ttf', 12)

    def reset(self):
        # Reset all attributes to their initial values
        self.score_rect_pos = []
        self.score_rect = []
        self.levelName = ''
        self.levelName_rect = []
        self.score = 0
        self.remaining_lives = 3
        self.lives_rect_pos = []
        
    def draw_abilities(self, screen, player):
        screen_width, screen_height = screen.get_size()
        padding = 10  # Padding from the edges
        icon_size = 64  # Size of the ability icon

        # Calculate positions
        circle_icon_pos = (screen_width - icon_size - padding, screen_height - icon_size - padding)

        # Draw ability icon
        screen.blit(self.circle_ability_icon, circle_icon_pos)

        # Draw text next to the ability icon
        current_time = pygame.time.get_ticks() / 1000  # Convert to seconds
        cooldown_remaining = max(0, player.ability_cooldown - (current_time - player.last_ability_use_time))
        if cooldown_remaining > 0:
            text_surface = self.ability_font.render(f"Cooldown: {cooldown_remaining:.1f}s", True, (255, 255, 255))
        else:
            text_surface = self.ability_font.render("Press 'E'", True, (255, 255, 255))
        text_rect = text_surface.get_rect()
        text_rect.right = circle_icon_pos[0] - padding
        text_rect.centery = circle_icon_pos[1] + icon_size // 2
        screen.blit(text_surface, text_rect)
        
         # Draw text next to the shift ability icon
        shift_cooldown_remaining = max(0, player.shift_ability_cooldown - (current_time - player.last_shift_ability_time))
        if shift_cooldown_remaining > 0:
            shift_text_surface = self.ability_font.render(f"Shift CD: {shift_cooldown_remaining:.1f}s", True, (255, 255, 255))
        else:
            shift_text_surface = self.ability_font.render("Press 'Shift'", True, (255, 255, 255))
        shift_text_rect = shift_text_surface.get_rect()
        shift_text_rect.right = circle_icon_pos[0] - padding
        shift_text_rect.centery = circle_icon_pos[1] + icon_size // 2 + text_rect.height + padding
        screen.blit(shift_text_surface, shift_text_rect)
        
    def update_score(self, amount):
        self.score += amount
        
    def draw_score(self, screen):
        screen_width, screen_height = screen.get_size()
        padding = 10

        #calculate positions
        self.score_rect_pos = screen_width - screen_width + padding, screen_height - screen_height + padding 
        #return the render
        return self.score_font.render('SCORE: ' + str(self.score), True, self.WHITE, self.BLACK)


    #idea to have level names instead of numbers can also be used later to make sure we are "stepping into the right levels" by passing thru HUD class
    def draw_levelName(self, screen, level_name):
        screen_width, screen_height = screen.get_size()
        pad_x = 10
        pad_y = 40

        #calculate postions
        self.levelName_rect = screen_width - screen_width + pad_x, screen_height - screen_height + pad_y
        #return the render
        return self.levelName_font.render('Area: ' + str(level_name), True, self.WHITE, self.BLACK)


    def draw_lives(self, screen, lives):
        screen_width, screen_height = screen.get_size()
        pad_x = 10
        pad_y = 50
        counter = 0
        ##print(lives, end = '\n')

        #calc positions for lives placement
        for live in range(lives):
            counter = live
            self.lives_rect_pos.append(((screen_width - screen_width) + pad_x, screen_height - pad_y - (pad_y * counter)))
            
            
        #draw lives in rect positions

        for rect in self.lives_rect_pos:
            rect_pos_x, rect_pos_y = rect
            #print(rect_pos_x, end = '\n')
            #print(rect_pos_y, end = '\n')
           
            screen.blit(self.lives_img, (rect_pos_x, rect_pos_y))   
              
        self.lives_rect_pos.clear()
        
     
    
