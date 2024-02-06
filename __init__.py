#!/usr/bin/python3

# standard python library imports
import sys, os
import random
import json

# third party imports
import pyautogui
import pygame
import pandas as pd

# custom imports
# from button import Button
import pygame

# Get path to folder containing running executable
program_folder = os.path.dirname(sys.argv[0])

class Button:
    def __init__(self, x, y, width, height, color, text=''):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.color = color
        self.text = text

    def draw(self, screen):
        # Draw the button rectangle
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.width, self.height))

        if self.text != '':
            font = pygame.font.SysFont('comicsans', 30)
            text_surface = font.render(self.text, True, (0, 0, 0))
            screen.blit(text_surface, (self.x + (self.width/2 - text_surface.get_width()/2), self.y + (self.height/2 - text_surface.get_height()/2)))

    def is_over(self, pos):
        # Pos is the mouse position or a tuple of (x,y) coordinates
        if self.x < pos[0] < self.x + self.width and self.y < pos[1] < self.y + self.height:
            return True
        return False

# pyautogui.alert(pd.read_csv(program_folder + "\\game_data.csv"))

pygame.init()

class Game:
    def __init__(self):
        # general settings
        self.window = "main_menu"

        # loaded game settings
        self.is_paused = False
        self.score = 0
        self.df = self.load_data(program_folder + "\\game_data.csv")
        self.columns = [100, 250, 400, 550, 700, 850]
        self.thumbs_up = pygame.image.load(program_folder + "\\thumbs-up-solid.png")
        self.font = pygame.font.SysFont(None, 50)
        print("running")
        self.thumbs_up_count = 3
        self.user_text = 'Your response: '
        self.speed_y = 1
        self.x = random.choice(self.columns)
        print(len(self.df))
        self.y = 20
        self.prompt, self.question_picked = self.pick_a_question(self.df)
        self.text_surface = self.render_text(self.prompt, self.font)
        

    def render_text(self, message, font, color=(255, 255, 255)):
        return font.render(message, True, color)

    def pick_a_question(self, df):
        df["skip_for_x_rounds"] = df["skip_for_x_rounds"].apply(lambda x: max(x - 1, 0))
        max_priority = max(df.loc[df["skip_for_x_rounds"] < 1, "priority"])
        prompts = df.loc[(df["skip_for_x_rounds"] < 1) & (df["priority"] == max_priority)].index
        chosen_prompt = random.choice(list(prompts))
        return chosen_prompt, df.loc[chosen_prompt]

    def load_data(self,file_path):
        try:
            return pd.read_csv(file_path,index_col=0,dtype={'answer': object})
        except:
            return None
        
    def display_message(self,font,screen,message):
        pygame.display.flip()

    def run_main_pygame_loop(self):
        pygame.display.set_caption("Flash Card App")
        screen = pygame.display.set_mode((1280, 800))
        font = pygame.font.SysFont(None, 50)

        GREEN = (0, 255, 0)
        RED = (255, 0, 0)

        pause_button = Button(200, 0, 150, 50, GREEN, 'Pause')
        load_button = Button(250, 200, 500, 50, GREEN, 'Load Facts (Under Construction)')
        start_button = Button(250, 250, 500, 50, GREEN, 'Start Game')
        high_scores_button = Button(250, 300, 500, 50, GREEN, 'High Scores (Under Construction)')
        game_over = Button(250, 350, 500, 50, GREEN, 'Game Over (Under Construction)')
        repair_button = Button(1050,700,250,50,GREEN,"Correct Answer")
        main_menu_button = Button(0,0,200,50,GREEN,"Main Menu")
        new_game_button = Button(250, 250, 500, 50, GREEN, 'Play Again')
    
        main_menu_buttons = [[load_button,"load"],[start_button,"main_game"],[high_scores_button,"high_scores"]]
        game_over_screen_buttons = [[new_game_button,"main_game"],[main_menu_button,"main_menu"]]

        running = True

        while running:
            if self.window == "main_menu":
                running = self.main_menu(main_menu_buttons,screen,RED,GREEN,running)
            elif self.window == "main_game":
                running = self.pausable_screen(repair_button,pause_button,screen,RED,GREEN,running,main_menu_button,self.run_game)
            elif self.window == "game_over":
                running = self.game_over(screen,RED,GREEN,running,game_over_screen_buttons)

        pygame.quit()

    def main_menu(self,main_menu_buttons,screen,RED,GREEN,running):
        """A main menu"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in main_menu_buttons:
                    if button[0].is_over(pygame.mouse.get_pos()):
                        self.window = button[1]

        screen.fill((0, 0, 0))

        for button in main_menu_buttons:
            button[0].draw(screen)
       
        pygame.display.flip()
        return running
    
    
    def game_over(self,screen,RED,GREEN,running,game_over_screen_buttons):
        """Game Over Screen"""
   
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                for button in game_over_screen_buttons:
                    if button[0].is_over(pygame.mouse.get_pos()):
                        self.window = button[1]
                        self.thumbs_up_count = 3

        screen.fill((0, 0, 0))

        for button in game_over_screen_buttons:
            button[0].draw(screen)

        pygame.display.flip()
        return running

    def pausable_screen(self,repair_button,pause_button,screen,RED,GREEN,running,main_menu_button,main_game_function):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pause_button.is_over(pygame.mouse.get_pos()):
                    self.is_paused = not self.is_paused
                    pause_button.text = 'Resume' if self.is_paused else 'Pause'
                    pause_button.color = RED if self.is_paused else GREEN
                    print("Game Paused!" if self.is_paused else "Game Resumed!")
                if main_menu_button.is_over(pygame.mouse.get_pos()):
                    self.window = "main_menu"
                else:
                    self.main_game_events(repair_button,event)
            
            else:
                self.main_game_events(repair_button,event)

        screen.fill((0, 0, 0))

        if not self.is_paused:
            main_game_function(screen,repair_button)

        for button in [main_menu_button, pause_button]:
            main_menu_button.draw(screen)
            pause_button.draw(screen)

        pygame.display.flip()
        return running
    def main_game_events(self,repair_button,event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if repair_button.is_over(pygame.mouse.get_pos()):
                self.is_paused = not self.is_paused
                import pyautogui
                new_answer = pyautogui.prompt(self.question_picked["answer"])
                self.df.at[self.prompt,"answer"] = new_answer

        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN:
                self.df.at[self.prompt,"attempts"] += 1
                self.df.at[self.prompt,"skip_for_x_rounds"] = 3
                if self.user_text[15:] == self.question_picked["answer"]:
                    # update table
                    self.df.at[self.prompt,"correct_attempts"] += 1
                    if self.df.at[self.prompt,"consecutive_weight"] < 0:
                        self.df.at[self.prompt,"consecutive_weight"] = 0
                    self.df.at[self.prompt,"consecutive_weight"] += 1

                    self.df.at[self.prompt,"priority"] -= self.df.at[self.prompt,"consecutive_weight"]

                    # pick next question for the game
                    self.y = 20  # Reset to the top of the screen
                    self.x = random.choice(self.columns)
                    self.prompt, self.question_picked = game.pick_a_question(self.df)
                    self.text_surface = game.render_text(self.prompt, self.font)
                    game.score += 1
                    self.user_text = 'Your response: '  # Clear the text when Enter is pressed
                else:
                    if self.df.at[self.prompt,"consecutive_weight"] > 0:
                        self.df.at[self.prompt,"consecutive_weight"] = -1
                    self.df.at[self.prompt,"consecutive_weight"] -= 1
                    # self.df.at[self.prompt,"priority"] -= self.df.at[self.prompt,"consecutive_weight"]
                    self.df.at[self.prompt,"priority"] += 2
                    self.thumbs_up_count -= 1
                    self.user_text = f'Your response: {self.question_picked["answer"]}'  # Clear the text when Enter is pressed
            elif event.key == pygame.K_BACKSPACE:
                self.user_text = self.user_text[:-1]  # Remove the last character
            else:
                self.user_text += event.unicode  # Add the character to the text
    def run_game(self,screen,repair_button):
        self.y += self.speed_y
        # Check if the text has reached the bottom of the screen
        if self.y + self.text_surface.get_height() > 800:
            self.thumbs_up_count -= 1
            self.y = 5  # Reset to the top of the screen
            self.x = random.choice(self.columns)
            self.prompt, self.question_picked = game.pick_a_question(self.df)
            self.text_surface = game.render_text(self.prompt, self.font)
            if self.thumbs_up_count < 0:
                self.window = "game_over"
        
        else:
            _ = screen.fill((0, 0, 0))
            _ = screen.blit(self.text_surface, (self.x, self.y))

            # Render and blit the user input text
            input_surface = game.render_text(self.user_text, self.font)
            _ = screen.blit(input_surface, (355, 5))

            score_surface = game.render_text(f"Score: {game.score}", self.font)
            _ = screen.blit(score_surface, (10, 750))
            repair_button.draw(screen)

            if self.thumbs_up_count > 0:
                _ = screen.blit(self.thumbs_up, (1280 - 50, 800-43))
                if self.thumbs_up_count > 1:
                    _ = screen.blit(self.thumbs_up, (1280 - 100, 800-43))
                    if self.thumbs_up_count > 2:
                        _ = screen.blit(self.thumbs_up, (1280 - 150, 800-43))
            elif self.thumbs_up_count < 0:
                self.window = "game_over"

            # Cap the frame rate
            _ = pygame.time.Clock().tick(6000)
        self.df.to_csv(program_folder + "\\game_data.csv")

if __name__ == "__main__":
    game = Game()
    game.run_main_pygame_loop()