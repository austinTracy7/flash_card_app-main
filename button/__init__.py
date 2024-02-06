import pygame

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
