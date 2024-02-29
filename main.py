import pygame
from Classes.Settings import Settings
from Classes.Gun import Gun
from Classes.Menu import Menu
from Classes.GameContext import GameContext

def main():
    pygame.init()
    settings = Settings()
    context = GameContext(settings)
    gun = Gun(context)
    menu = Menu(context)
    pygame.mixer.music.play()
    run = True
    context.level = 0
    context.generate_enemy_coordinates()
    while run:
        context.timer.tick(settings.fps)

        if context.level != 0:
            if context.counter < 60:
                context.counter += 1
            else:
                context.counter = 1
                context.time_passed += 1
                if context.mode == 2:
                    context.time_remaining -= 1

        context.screen.fill('black')
        context.screen.blit(context.bgs[context.level - 1], (0, 0))
        context.screen.blit(context.banners[context.level - 1], (0, context.HEIGHT - 200))
        menu.draw()

        if context.level == 1:
            context.target_boxes = context.draw_level(context.one_coords)
            context.one_coords = context.move_level()
            if context.shot:
                context.one_coords = gun.check_shot(context.target_boxes, context.one_coords)
                context.shot = False

        elif context.level == 2:
            context.target_boxes = context.draw_level(context.two_coords)
            context.two_coords = context.move_level()
            if context.shot:
                context.two_coords = gun.check_shot(context.target_boxes, context.two_coords)
                context.shot = False

        elif context.level == 3:
            context.target_boxes = context.draw_level(context.three_coords)
            context.three_coords = context.move_level()
            if context.shot:
                context.three_coords = gun.check_shot(context.target_boxes, context.three_coords)
                context.shot = False