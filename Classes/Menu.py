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

    def draw_menu(self):
        self.context.level = 0
        self.context.game_modes = ["Freeplay!", "Ammo Remaining:", "Time Remaining:"]
        mouse_pos = pygame.mouse.get_pos()
        clicks = pygame.mouse.get_pressed()
        self.context.screen.blit(self.context.menu_img, (0, 0))
        freeplay_button = pygame.rect.Rect((170, 524), (260, 100))
        self.context.screen.blit(self.context.font.render(f'{self.context.best_freeplay}', True, 'black'), (340, 580))
        ammo_button = pygame.rect.Rect((475, 524), (260, 100))
        self.context.screen.blit(self.context.font.render(f'{self.context.best_ammo}', True, 'black'), (650, 580))
        timed_button = pygame.rect.Rect((170, 661), (260, 100))
        self.context.screen.blit(self.context.font.render(f'{self.context.best_timed}', True, 'black'), (350, 710))
        reset_button = pygame.rect.Rect((475, 661), (260, 100))

        if freeplay_button.collidepoint(mouse_pos) and clicks[0] and not self.context.clicked:
            self.context.mode = 0
            self.context.level = 1
            self.context.menu = False
            self.context.time_passed = 0
            self.context.total_shots = 0
            self.context.points = 0
            self.context.clicked = True
            self.context.new_coords = True

        if ammo_button.collidepoint(mouse_pos) and clicks[0] and not self.context.clicked:
            self.context.mode = 1
            self.context.level = 2
            self.context.menu = False
            self.context.time_passed = 0
            self.context.ammo = 81
            self.context.total_shots = 0
            self.context.points = 0
            self.context.clicked = True
            self.context.new_coords = True

        if timed_button.collidepoint(mouse_pos) and clicks[0] and not self.context.clicked:
            self.context.mode = 2
            self.context.level = 3
            self.context.menu = False
            self.context.time_remaining = 30
            self.context.time_passed = 0
            self.context.total_shots = 0
            self.context.points = 0
            self.context.clicked = True
            self.context.new_coords = True

        if reset_button.collidepoint(mouse_pos) and clicks[0] and not self.context.clicked:
            self.context.best_freeplay = 0
            self.context.best_ammo = 0
            self.context.best_timed = 0
            self.context.clicked = True
            self.context.write_values = True

    def draw_pause(self):
        self.context.level = 0
        mouse_pos = pygame.mouse.get_pos()
        clicks = pygame.mouse.get_pressed()
        resume_button = pygame.rect.Rect((170, 661), (260, 100))
        menu_button = pygame.rect.Rect((475, 661), (260, 100))
        self.context.screen.blit(self.context.pause_img, (0, 0))
        if resume_button.collidepoint(mouse_pos) and clicks[0] and not self.context.clicked:
            self.context.level = self.context.resume_level
            self.context.pause = False
            self.context.clicked = True

        if menu_button.collidepoint(mouse_pos) and clicks[0] and not self.context.clicked:
            pygame.mixer.music.play()
            self.context.level = 0
            self.context.pause = False
            self.context.menu = True
            self.context.points = 0
            self.context.total_shots = 0
            self.context.time_passed = 0
            self.context.time_remaining = 0
            self.context.clicked = True
            self.context.new_coords = True

