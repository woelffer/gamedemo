import pygame
import sys
import HUD  # Assuming you have an HUD module
import json
import random

class Levels:
    def __init__(self, stars, screen, screen_width, screen_height, title_screen_img, clock, hud):
        self.stars = stars
        self.screen = screen
        self.screen_width = screen_width
        self.screen_height = screen_height
        self.title_screen_img = title_screen_img
        self.clock = clock
        self.hud = hud
        # Load font for the title screen prompt
        self.prompt_font = pygame.font.Font('freesansbold.ttf', 28)

    def TitleScreen(self):
        prompt_text = self.prompt_font.render('Press [Enter] to Start', True, (255, 255, 255))
        prompt_rect = prompt_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 100))

        title_screen_active = True

        while title_screen_active:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:  # Enter to start
                        title_screen_active = False

            # Clear screen
            self.screen.fill((0, 0, 0))

            # Update and draw stars
            for star in self.stars:
                star.move(1 / 60.0)  # Use a fixed dt for consistent movement
                star.draw(self.screen)

            # Draw Title
            self.screen.blit(self.title_screen_img, (self.screen_width // 2 - self.title_screen_img.get_width() // 2,
                                                     self.screen_height // 2 - self.title_screen_img.get_height() // 2))

            # Draw the "Press [Enter] prompt"
            self.screen.blit(prompt_text, prompt_rect)

            # Update display
            pygame.display.flip()

            self.clock.tick(60)
        

    def EndScreen(self, player_model, lives_model, bullets, enemies,enemy_bullets, time_since_last_spawn, time_since_last_shot, hud, asteroids):

        #Load quotes from JSON file
        with open('assets/quotes.json') as f:
            quotes_data = json.load(f)

        #Extract quotes array
        quotes = quotes_data['quotes']

        #Select a random quote
        random_quote = random.choice(quotes)

        game_over = True
        while game_over:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        # Reset game state
                        player_model.reset()
                        lives_model.reset()
                        print(f"Hud reset Score before reset: {self.hud.score}")
                        self.hud.reset()
                        print(f"Hud reset Score after:  {self.hud.score}")
                        bullets.clear()
                        enemy_bullets.clear()
                        enemies.clear()
                        asteroids.clear()
                        game_over = False
                        # Reset time variables
                        self.time_since_last_spawn = 0
                        self.time_since_last_shot = 0
                        #reset_music()

                        break

            self.screen.fill((0, 0, 0))
            game_over_font = pygame.font.Font('freesansbold.ttf', 64)
            game_over_text = game_over_font.render('YOU DIED', True, (255, 0, 0))
            game_over_rect = game_over_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2))
            self.screen.blit(game_over_text, game_over_rect)
            self.screen.blit(self.hud.draw_score(self.screen), self.hud.score_rect_pos)

                # Draw "Press [Enter] to restart" prompt
            prompt_font = pygame.font.Font('freesansbold.ttf', 32)
            prompt_text = prompt_font.render('Press [Enter] to restart', True, (255, 255, 255))
            prompt_rect = prompt_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 50))
            self.screen.blit(prompt_text, prompt_rect)

            # Display random quote
            quote_font = pygame.font.Font('freesansbold.ttf', 24)
            quote_text = quote_font.render(random_quote, True, (255, 255, 255))
            quote_rect = quote_text.get_rect(center=(self.screen_width // 2, self.screen_height // 2 + 200))
            self.screen.blit(quote_text, quote_rect)

            #Update and draw stars
            for star in self.stars:
                star.move(1/60.0) #Use a fixed dt for consistent movement
                star.draw(self.screen)
        

            pygame.display.flip()

            self.clock.tick(60)
        

    def Stepper():
        pass

    def LevelOne():
        pass

