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

    def draw_game_over(self):
        self.context.level = 0
        display_score = self.context.time_passed if self.context.mode == 0 else self.context.points
        self.context.screen.blit(self.context.game_over_img, (0, 0))
        mouse_pos = pygame.mouse.get_pos()
        clicks = pygame.mouse.get_pressed()
        exit_button = pygame.rect.Rect((170, 661), (260, 100))
        menu_button = pygame.rect.Rect((475, 661), (260, 100))
        self.context.screen.blit(self.context.big_font.render(f'{display_score}', True, 'black'), (650, 570))
        if menu_button.collidepoint(mouse_pos) and clicks[0] and not self.context.clicked:
            self.context.clicked = True
            self.context.level = 0
            self.context.pause = False
            self.context.game_over = False
            self.context.menu = True
            self.context.points = 0
            self.context.total_shots = 0
            self.context.time_passed = 0
            self.context.time_remaining = 0

        if exit_button.collidepoint(mouse_pos) and clicks[0] and not self.context.clicked:
            self.context.run = False
