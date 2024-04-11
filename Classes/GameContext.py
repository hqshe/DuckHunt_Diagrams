import os
import pygame


class GameContext:
    def __init__(self, settings):
        script_dir = os.path.dirname(os.path.abspath(__file__))
        font_path = os.path.join(script_dir, '..', 'assets', 'font', 'myFont.ttf')
        self.settings = settings
        self.timer = pygame.time.Clock()
        self.font = pygame.font.Font(font_path, 32)
        self.big_font = pygame.font.Font(os.path.join(script_dir, '..', 'assets', 'font', 'myFont.ttf'), 60)
        self.WIDTH = settings.width
        self.HEIGHT = settings.height
        self.screen = pygame.display.set_mode([self.WIDTH, self.HEIGHT])
        self.bgs = [pygame.image.load(os.path.join(script_dir, '..', 'assets', 'bgs', f'{i}.png')) for i in range(1, 4)]
        self.banners = [pygame.image.load(os.path.join(script_dir, '..', 'assets', 'banners', f'{i}.png')) for i in range(1, 4)]
        self.guns = [pygame.transform.scale(pygame.image.load(os.path.join(script_dir, '..', 'assets', 'guns', f'{i}.png')), (100, 100)) for i in range(1, 4)]
        self.target_images = [[pygame.transform.scale(pygame.image.load(os.path.join(script_dir, '..', 'assets', 'targets', f'{i}', f'{j}.png')), (120 - (j * 18), 80 - (j * 12))) for j in range(1, 5 if i == 3 else 4)] for i in range(1, 4)]

        self.targets = settings.targets
        self.level = 0
        self.points = 0
        self.total_shots = 0
        self.mode = 0  # 0 = freeplay, 1 - accuracy, 2 - timed
        self.ammo = 0
        self.time_passed = 0
        self.time_remaining = 0
        self.counter = 1

        self.file = open(os.path.join(script_dir, '..', 'high_scores.txt'), 'r')
        self.read_file = self.file.readlines()
        self.file.close()

        self.best_freeplay = int(self.read_file[0])
        self.best_ammo = int(self.read_file[1])
        self.best_timed = int(self.read_file[2])
        self.shot = False
        self.menu = True
        self.game_over = False
        self.pause = False
        self.clicked = False
        self.write_values = False
        self.new_coords = True
        self.one_coords = [[], [], []]
        self.two_coords = [[], [], []]
        self.three_coords = [[], [], [], []]
        self.menu_img = pygame.image.load(os.path.join(script_dir, '..', 'assets', 'menus', 'mainMenu.png'))
        self.game_over_img = pygame.image.load(os.path.join(script_dir, '..', 'assets', 'menus', 'gameOver.png'))
        self.pause_img = pygame.image.load(os.path.join(script_dir, '..', 'assets', 'menus', 'pause.png'))
        self.resume_level = 0
        self.plate_sound = pygame.mixer.Sound(os.path.join(script_dir, '..', 'assets', 'sounds', 'Broken plates.wav'))
        self.plate_sound.set_volume(0.2)
        self.bird_sound = pygame.mixer.Sound(os.path.join(script_dir, '..', 'assets', 'sounds', 'Drill Gear.mp3'))
        self.bird_sound.set_volume(0.2)
        self.laser_sound = pygame.mixer.Sound(os.path.join(script_dir, '..', 'assets', 'sounds', 'Laser Gun.wav'))
        self.laser_sound.set_volume(0.3)
        pygame.mixer.init()
        pygame.mixer.music.load(os.path.join(script_dir, '..', 'assets', 'sounds', 'bg_music.mp3'))

    def generate_enemy_coordinates(self):
        for i in range(3):
            my_list = self.targets[0]
            for j in range(my_list[i]):
                self.one_coords[i].append((self.WIDTH // (my_list[i]) * j, 300 - (i * 150) + 30 * (j % 2)))

        for i in range(3):
            my_list = self.targets[1]
            for j in range(my_list[i]):
                self.two_coords[i].append((self.WIDTH // (my_list[i]) * j, 300 - (i * 150) + 30 * (j % 2)))

        for i in range(4):
            my_list = self.targets[2]
            for j in range(my_list[i]):
                self.three_coords[i].append((self.WIDTH // (my_list[i]) * j, 300 - (i * 100) + 30 * (j % 2)))

    def draw_level(self, coords):
        if self.level == 1:
            target_rects = [[], [], []]
        elif self.level == 2:
            target_rects = [[], [], []]
        elif self.level == 3:
            target_rects = [[], [], [], []]

        for i in range(len(coords)):
            for j in range(len(coords[i])):
                target_rects[i].append(
                    pygame.rect.Rect((coords[i][j][0] + 20, coords[i][j][1]), (60 - i * 12, 60 - i * 12)))
                self.screen.blit(self.target_images[self.level - 1][i], coords[i][j])

        return target_rects

    def draw_score(self):
        points_text = self.font.render(f'Points: {self.points}', True, 'black')
        self.screen.blit(points_text, (320, 660))
        shots_text = self.font.render(f'Total Shots: {self.total_shots}', True, 'black')
        self.screen.blit(shots_text, (320, 687))
        time_text = self.font.render(f'Time Elapsed: {self.time_passed}', True, 'black')
        self.screen.blit(time_text, (320, 714))
        if self.mode == 0:
            mode_text = self.font.render('Freeplay!', True, 'black')
        if self.mode == 1:
            mode_text = self.font.render('Ammo Remaining: {self.ammo}', True, 'black')
        if self.mode == 2:
            mode_text = self.font.render('Time Remaining {self.time_remaining}', True, 'black')
        self.screen.blit(mode_text, (320, 741))

    def move_level(self):
        if self.level == 1 or self.level == 2:
            max_val = 3
        else:
            max_val = 4

        if self.level == 1:
            coords = self.one_coords
        elif self.level == 2:
            coords = self.two_coords
        elif self.level == 3:
            coords = self.three_coords

        for i in range(max_val):
            for j in range(len(coords[i])):
                my_coords = coords[i][j]
                if my_coords[0] < -150:
                    coords[i][j] = (self.WIDTH, my_coords[1])
                else:
                    coords[i][j] = (my_coords[0] - 2 ** i, my_coords[1])
        return coords
