import pygame

class Menu:
    def __init__(self, context):
        self.context = context

    def draw(self):
        if self.context.menu:
            self.context.level = 0
            self.draw_menu()
        if self.context.game_over:
            self.context.level = 0
            self.draw_game_over()
        if self.context.pause:
            self.context.level = 0
            self.draw_pause()